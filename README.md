# Lagos

This was inspired by _The Librarian_ program built by the character _Lagos_ in the novel __Snow Crash__.

- [Lagos](#lagos)
  - [Usage](#usage)
    - [Start the websocket and client](#start-the-websocket-and-client)
    - [(Recommended) Run the websocket and client from Docker](#recommended-run-the-websocket-and-client-from-docker)
  - [Chatting](#chatting)
  - [Development Setup](#development-setup)
    - [Visual Studio Code Integration](#visual-studio-code-integration)
  - [Troubleshooting](#troubleshooting)
    - [Cannot find libhdf5 on macOS when running `pdm install`](#cannot-find-libhdf5-on-macos-when-running-pdm-install)

## Usage

### Start the websocket and client

```
# Start a websocket server
pdm run lagos serve
```

Then, load the chatbot client with the specified model:

```
pdm run lagos start -m "models/mybot-output"
```

The model here is whatever transformers dialogpt model you've fine-tuned. So in my case, I previously did fine-tuning on `dialogpt-small` using chat logs from a Discord channel...

### (Recommended) Run the websocket and client from Docker

To use the docker setup, you need to have a `.env` setup with the `MODELS_DIR` set to the location of the models and `MODEL_NAME` to the name of the pre-trained model you want to use.

Example:

```
MODELS_DIR=/Users/bitjockey/Projects/SolipsisAI/research/models
MODEL_NAME=mybot-medium
```

Then build and run:

```
docker-compose build
docker-compose up
```

You can point to a different env file with `--env-file`:

```
docker-compose --env-file .env.development up
```

To bring containers down:

```
docker-compose down
```

## Chatting

After starting up the websocket and client(s), you can then chat with the bot from a websocket client like `wscat`:

```shell
# Install the wscat websocket client
npm install -g wscat

# Connect to the websocket
wscat -c 'ws://localhost:8001/'
```

Replace `localhost` with whatever the hostname or IP address is.

Then, from within `wscat`, you can send an event containing the `user_id` and `text` of the message.
```shell
# Initial input 
> {"user_id": "bitjockey", "text": "Hello"}
```

This will output something like:
```shell
< {"user_id": "bitjockey", "text": "Hello"}
< {"user_id": "ba46f082-8acc-448c-bf56-03ce0993a88a", "is_typing": true}
< {"conversation_id": "1f65bbe2-9e98-417b-95a7-6533b2e2c114", "user_id": "ba46f082-8acc-448c-bf56-03ce0993a88a", "text": "Hi", "is_typing": false}
```

**NOTE**: it may take a bit of time to load the model's response as there is intentionally a random delay between responses; this is to mimic how chats between humans aren't necessarily instantaneous.


## Development Setup
```shell
pdm install
pdm install -G pytorch
pdm install -G nlp
pdm install -G dev

# Install dependencies for macos
pdm install -G macos
```

### Visual Studio Code Integration

Put this in `.vscode/settings.json`:

```json
{
    "python.analysis.extraPaths": [
        "./__pypackages__/3.9/lib"
    ]
}
```

Then run: `pdm run code .` to launch VS Code with the venv loaded.

## Troubleshooting

### Cannot find libhdf5 on macOS when running `pdm install`

First make sure to install it with `brew install hdf5`.

Then set the environment variable: `export HDF5_DIR="$(brew --prefix hdf5)"`.

This will force `pdm install` to look at that directory for the lib files.