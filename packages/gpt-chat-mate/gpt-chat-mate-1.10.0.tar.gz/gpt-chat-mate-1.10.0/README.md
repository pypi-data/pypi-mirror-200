# GPTChatMate v1.10.0
A python cli front-end for the chatGPT API.

## Installation
Note: This app requires `sqlite3` version `>3.35.0`.
```
pip install gpt-chat-mate
```

## Configuration
Running the app for the first time will produce a `.config.json` file locally with default config options.

`db_filename` - the filename to use for the sqlite database.

`gpt_model` - which GPT model to use for the chat.

`print_style` - the pygments style to use for the GPT output.

`token_limit` - the limit on the number of [tokens](https://platform.openai.com/docs/introduction/tokens)
that the app will send in a single API call.
Note: the user will still be shown the full conversation history even if the token limits the conversation sent
to the API.

`openai_req_timeout` - The OpenAI API request can sometimes hang for an insane amount of time, so this sets a timeout.
The default is 60.

`default_editor` - The editor to use for things like editing an existing system prompt. The default is `vim`.

`editor_on_paste` - Edit all multiline prompts using an editor instead of the command line. Defaults to `false`
because it may not work on all systems.

## Usage
Install via pip, and run via the package name.
```
gpt-chat-mate
```

### Commands

`chat optional[<ID>]` - Start a new chat or continue an existing one by providing the ID.

`delete <ID>` - Delete an existing chat.

`list`,`ls` - List existing chats stored in the database.

`duplicate <ID>` - duplicates a chat with just the system prompt. (Does not duplicate the whole chat)

`rename <ID> optional[<name>]` - rename a chat. If `<name>` is not given, chatGPT is used to rename it.

`esp <ID>` - (e)dit (s)ystem (p)rompt allows you to edit the system prompt of a chat. (This has only been tested on a unix system).

`help` - List available commands.

`exit` - Exit the program.

### Special Prompt Keywords

`paste` - You can use the paste command as a prompt to enter paste mode. Paste mode allows you to freely type or paste
many lines of text as a prompt. You then use `EOF` to indicate that you want to submit the prompt.
