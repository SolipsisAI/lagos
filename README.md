# Lagos

- [Lagos](#lagos)
  - [Usage](#usage)
  - [(Recommended) Docker](#recommended-docker)
  - [Development Setup](#development-setup)
    - [Visual Studio Code Integration](#visual-studio-code-integration)
  - [Troubleshooting](#troubleshooting)
    - [Cannot find libhdf5 on macOS when running `pdm install`](#cannot-find-libhdf5-on-macos-when-running-pdm-install)

## Usage

Start the websocket:

```
# Start a websocket server
pdm run lagos serve
```

Then, load the chatbot client with the specified model:

```
pdm run lagos start -m "models/mybot-output"
```

The model here is whatever transformers dialogpt model you've fine-tuned. So in my case, I previously did fine-tuning on `dialogpt-small` using chat logs from a Discord channel...

## (Recommended) Docker

To use the docker setup, you need to have a `.env` setup with the `MODELS_DIR` set to the location of the models.

Example:

```
MODELS_DIR=~/Projects/SolipsisAI/research/models
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

## Troubleshooting

### Cannot find libhdf5 on macOS when running `pdm install`

First make sure to install it with `brew install hdf5`.

Then set the environment variable: `export HDF5_DIR="$(brew --prefix hdf5)"`.

This will force `pdm install` to look at that directory for the lib files.