# GPTChatMate v1.7.2b13
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

## Usage
Install via pip, and run via the package name.
```
gpt-chat-mate
```

### Commands

`chat optional[<ID>]` - Start a new chat or continue an existing one by providing the ID.

`delete <ID>` - Delete an existing chat.

`list`,`ls` - List existing chats stored in the database.

`help` - List available commands.

`exit` - Exit the program.

### Special Prompt Keywords

`paste` - You can use the paste command as a prompt to enter paste mode. Paste mode allows you to freely type or paste
many lines of text as a prompt. You then use `EOF` to indicate that you want to submit the prompt.
