# Lagos

## Development

```shell
pdm install
pdm install -G dev

# Install dependencies for macos
pdm install -G macos
```

### Visual Studio Code

Put this in `.vscode/settings.json`:

```json
{
    "python.analysis.extraPaths": [
        "./__pypackages__/3.9/lib"
    ]
}
```