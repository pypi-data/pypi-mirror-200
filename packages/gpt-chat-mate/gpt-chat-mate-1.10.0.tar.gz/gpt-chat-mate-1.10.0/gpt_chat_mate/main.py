import cmd
import json
import os
import readline
import sqlite3
import subprocess
import tempfile
from dataclasses import asdict, dataclass

import openai
import tiktoken
from func_timeout import FunctionTimedOut, func_timeout
from pyfiglet import Figlet
from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import get_lexer_by_name

from . import __version__


@dataclass
class Config:
    db_filename: str
    gpt_model: str
    print_style: str
    token_limit: int
    openai_req_timeout: int = 60
    default_editor: str = "vim"
    editor_on_paste: bool = False


class ColorPalette:
    CYAN = "\033[96m"
    ENDC = "\033[0m"


def num_tokens_from_messages(messages: list, model: str = "gpt-3.5-turbo-0301") -> int:
    """Returns the number of tokens used by a list of messages.
    This was copied straight from openai docs.
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")

    if model == "gpt-3.5-turbo":
        # Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        # Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.
        return num_tokens_from_messages(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = (
            4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        )
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not presently implemented for model {model}.
            See https://github.com/openai/openai-python/blob/main/chatml.md
            for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += (
                    tokens_per_name  # role is always required and always 1 token
                )
    num_tokens += 3  # every reply is primed with <im_start>assistant
    return num_tokens


def color_print(color, text):
    print(f"{color}{text}{ColorPalette.ENDC}")


class QueryShell(cmd.Cmd):
    def db_query(self, query: str, params=()):
        with sqlite3.connect(self.config.db_filename) as con:
            cur = con.cursor()
            cur.execute(query, params)
            result = cur.fetchall()
            cur.close()
            con.commit()

        return result

    def prompt_with_editor(self, in_text: str) -> str:
        # using .md so that an editor like vim will highlight the text
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".md") as tmp_file:
            tmp_file.write(in_text)
            tmp_file.flush()

            subprocess.call([self.config.default_editor, tmp_file.name])

            tmp_file.seek(0)
            return tmp_file.read().strip()

    def paste_mode(self, prompt) -> str:
        """Shared function for multiline prompts"""
        if self.config.editor_on_paste:
            result = self.prompt_with_editor("")
            readline.add_history(result)
            color_print(ColorPalette.CYAN, "user")
            print(
                highlight(
                    result,
                    get_lexer_by_name("markdown"),
                    Terminal256Formatter(style=self.config.print_style),
                )
            )
            return result

        print('Paste mode activated. "EOF" indicates the end of the prompt.')
        lines = []
        while True:
            line = input(f"(paste){prompt}")
            if line == "EOF":
                con_line = "\n".join(lines)
                readline.add_history(con_line)
                return con_line
            lines.append(line)


class ChatShell(QueryShell):
    prompt = "prompt>"

    def __init__(self, chat_id, messages, config: Config):
        super().__init__()
        self.chat_id = chat_id
        self.messages = messages
        self.config = config

    @staticmethod
    def do_exit(_):
        return True

    def do_paste(self, _):
        return self.default(self.paste_mode(self.prompt))

    def get_output_messages(self):
        """Once the chat exceeds the model's token limit, we can't send the
        whole chat back to the API. We have to start cutting it off so that
        we can stay within the limit.
        """
        token_limit = self.config.token_limit
        # 0 is always the system prompt, and we always want that in the output
        token_count = num_tokens_from_messages(
            [self.messages[0]], model=self.config.gpt_model
        )
        system_idx = int(len(self.messages) / -1)
        i = -1
        while token_count <= token_limit:
            if i == system_idx:
                # this means that we hit the system prompt before hitting the token limit.
                #  meaning that we can just send everything
                return self.messages
            token_count += num_tokens_from_messages(
                [self.messages[i]], model=self.config.gpt_model
            )
            i -= 1

        i += 1
        if token_count > token_limit:
            i += 1
        return [self.messages[0]] + self.messages[i:]

    def default(self, line):
        if line == "":
            return

        self.messages.append({"role": "user", "content": line})
        try:
            resp = func_timeout(
                self.config.openai_req_timeout,
                openai.ChatCompletion.create,
                kwargs=dict(
                    model=self.config.gpt_model, messages=self.get_output_messages()
                ),
            )
            resp_msg = resp["choices"][0]["message"]
            color_print(ColorPalette.CYAN, "assistant")
            print(
                highlight(
                    resp_msg["content"],
                    get_lexer_by_name("markdown"),
                    Terminal256Formatter(style=self.config.print_style),
                )
            )
            self.messages.append(resp_msg)
            self.db_query(
                "INSERT INTO message (chat_id, role, content) VALUES (?, ?, ?), (?, ?, ?);",
                (
                    self.chat_id,
                    "user",
                    line,
                    self.chat_id,
                    resp_msg["role"],
                    resp_msg["content"],
                ),
            )
        except (Exception, FunctionTimedOut) as e:
            print("Something went wrong while executing the query to openai")
            print(e)


class GPTChatMate(QueryShell):
    prompt = "GPTChatMate>"

    @staticmethod
    def do_exit(_):
        """exit the program"""
        return True

    def generate_chat_name(self, system_prompt: str) -> str:
        print("Using chatGPT to generate chat name...")
        messages = [
            {
                "role": "system",
                "content": "You are a professional name creator for chatGPT chats. You are given a chatGPT system"
                "prompt and you generate 2 to 3 word names that describe the chat",
            },
            {
                "role": "user",
                "content": f"Name this system prompt: {system_prompt}\nPrint just the name and no other text",
            },
        ]
        resp = func_timeout(
            self.config.openai_req_timeout,
            openai.ChatCompletion.create,
            kwargs=dict(model=self.config.gpt_model, messages=messages),
        )
        return resp["choices"][0]["message"]["content"]

    def pretty_print_messages(self, messages):
        for message in messages:
            color_print(ColorPalette.CYAN, message["role"])
            print(
                highlight(
                    message["content"],
                    get_lexer_by_name("markdown"),
                    Terminal256Formatter(style=self.config.print_style),
                )
            )

    def valid_id(self, _id) -> bool:
        if _id == "":
            print("You must provide an ID.")
            return False
        if not _id.isnumeric():
            print("Given ID must be a number.")
            return False
        existing_chats = [
            item[0] for item in self.db_query("SELECT chat_id FROM chat;")
        ]
        if int(_id) not in existing_chats:
            print(f"No chat exists for ID {_id}")
            return False
        return True

    def do_delete(self, _id):
        """
        delete <ID>

            where <ID> is the ID of the chat you want to delete.
        """
        if not self.valid_id(_id):
            return
        chat_id = int(_id)
        self.db_query("DELETE FROM message where chat_id = ?", (chat_id,))
        self.db_query("DELETE FROM chat where chat_id = ?", (chat_id,))
        print(f"Chat {_id} deleted.")

    def do_chat(self, _id):
        """
        chat optional[<ID>]

            where <ID> is the ID of a previous chat. A new chat will be created automatically if
            no ID is given.
        """
        if _id == "":
            name = input(
                "Please name the chat (leave blank to let chatGPT name it for you):\nname>"
            )
            system_prompt = input("Please provide a system prompt:\nsystem prompt>")

            if system_prompt == "paste":
                system_prompt = self.paste_mode("system prompt>")

            if name == "":
                try:
                    name = self.generate_chat_name(system_prompt)
                except (Exception, FunctionTimedOut) as e:
                    print(
                        "An attempt was made to generate a name, but something went wrong:"
                    )
                    print(e)
                    return

            messages = [{"role": "system", "content": system_prompt}]
            chat_id = self.db_query(
                "INSERT INTO chat (name) VALUES (?) RETURNING chat_id;",
                (name,),
            )[0][0]
            self.db_query(
                "INSERT INTO message (chat_id, role, content) VALUES (?, ?, ?)",
                (chat_id, "system", system_prompt),
            )
        elif not self.valid_id(_id):
            return
        else:
            chat_id = int(_id)
            messages = [
                {"role": role, "content": content}
                for role, content in self.db_query(
                    "SELECT role, content FROM message WHERE chat_id = ?", (chat_id,)
                )
            ]
            print("Current chat history:")
            self.pretty_print_messages(messages)
        ChatShell(chat_id, messages, self.config).cmdloop()

    def do_list(self, _):
        """
        list

            list the names of the chats that already exist.
        """
        existing_chats = self.db_query("SELECT chat_id, name FROM chat;")
        if len(existing_chats) > 0:
            print("Existing chats:")
            print(
                highlight(
                    "\n".join(f"{chat_id}. {name}" for chat_id, name in existing_chats),
                    get_lexer_by_name("markdown"),
                    Terminal256Formatter(style=self.config.print_style),
                )
            )
            return

        print('No chats exist yet. Run the "chat" command to start one.')

    def do_ls(self, line):
        """Alias of list command"""
        return self.do_list(line)

    def do_duplicate(self, line):
        """
        duplicate <ID>
            Duplicates a chat's system prompt into a new chat so that this
            doesn't have to be done manually by the user.
        """
        if not self.valid_id(line):
            return

        chat_id = self.db_query(
            """
            INSERT INTO chat (name)
            SELECT name FROM chat WHERE chat_id = ?
            RETURNING chat_id;
            """,
            (line,),
        )[0][0]
        self.db_query(
            """
            INSERT INTO message (chat_id, role, content)
            SELECT ?, role, content FROM message WHERE role = 'system' AND chat_id = ?;
        """,
            (chat_id, line),
        )

    def do_rename(self, line):
        """
        rename <ID> optional[<name>]
            Allows user to rename a chat.
        """
        args = line.split(" ")
        if not self.valid_id(args[0]):
            return

        chat_id = args[0]
        if len(args) > 1:
            new_name = " ".join(args[1:])
        else:
            system_prompt = self.db_query(
                "SELECT content FROM message WHERE role = 'system' AND chat_id = ?",
                (chat_id,),
            )[0][0]
            new_name = self.generate_chat_name(system_prompt)

        self.db_query(
            "UPDATE chat SET name = ? WHERE chat_id = ?;", (new_name, chat_id)
        )

    def do_esp(self, line):
        """
        esp <ID>
            (e)dit (s)ystem (p)rompt allows user to edit the system prompt of a chat
        """
        if not self.valid_id(line):
            return

        system_prompt = self.db_query(
            "SELECT content FROM message WHERE chat_id = ? AND role = 'system'",
            (line,),
        )[0][0]
        system_prompt = self.prompt_with_editor(system_prompt)

        self.db_query(
            "UPDATE message SET content = ? WHERE role = 'system' AND chat_id = ?",
            (system_prompt, line),
        )
        print(f"System prompt for chat {line} now set to:\n\n{system_prompt}")

    def set_config(self):
        if os.path.exists(".config.json"):
            with open(".config.json") as f:
                self.config = Config(**json.load(f))
            return

        print("No config found. Generating one.")
        self.config = Config(
            db_filename="chat.db",
            gpt_model="gpt-3.5-turbo",
            print_style="monokai",
            token_limit=4097,
        )
        with open(".config.json", "w") as f:
            f.write(json.dumps(asdict(self.config), indent=4))

    def preloop(self):
        print(Figlet().renderText(f"GPTChatMate {__version__}"))

        if os.path.exists(".key"):
            with open(".key") as f:
                openai.api_key = f.read().strip()
        else:
            print("No .key file found.")
            key = input("Please enter your OpenAI API key:")
            with open(".key", "w") as f:
                f.write(key)
            openai.api_key = key

        if sqlite3.sqlite_version_info[1] < 35:
            print(
                "ERROR: Bad sqlite3 version.\n"
                f"Your version: {sqlite3.sqlite_version}\n"
                "Required version: >3.35.0"
            )
        self.set_config()
        if not os.path.exists(self.config.db_filename):
            print("no DB found. Creating one.")
            self.db_query(
                """
                CREATE TABLE chat(
                    chat_id integer primary key,
                    name text
                );
            """,
            )
            self.db_query(
                """
                CREATE TABLE message(
                    message_id integer primary key,
                    chat_id integer,
                    role text,
                    content text,
                    FOREIGN KEY(chat_id) REFERENCES chat(chat_id)
                );
            """,
            )

        self.do_list("")


def main():
    GPTChatMate().cmdloop()


if __name__ == "__main__":
    main()
