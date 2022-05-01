# Lagos

## Development

```shell
pdm install
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