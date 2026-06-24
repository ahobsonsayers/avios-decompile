# Avios Android App Decompile

A repo to decompile the Avios Android APK and reverse engineer the API it uses.

The reverse-engineered API is documented in ./docs, and proof-of-concept scripts for using the API unofficially can be found in ./scripts.

All use of the API requires you to first obtain the Auth0 client ID so you can authenticate. The client ID is not provided due to liability concerns, but it’s made easy (and automated) to obtain using this repo - so read on!

## Prerequisites

- **go-task** — task runner for running commands
- **jadx** — decompiles Android APKs to readable Java source code
- **uv** — Python package manager, used to install required dependencies to run proof-of-concept scripts

Install with:

```bash
brew install go-task jadx uv
```

Once the tools are installed, install the Python dependencies with:

```bash
uv sync
```

## Obtaining the Auth0 Client ID

To obtain the client ID you must personally download and decompile the Android APK, and then extract the client ID.

Thankfully this is very easy to do.

Once you have satisfied the prerequisites, run:

```bash
task download
task decompile
task extract
```

> [!NOTE]
> `decompile` may finish with errors—this is normal for obfuscated Android APKs and the decompiled output is still usable.

If successful, the Auth0 client ID will be printed. You can now set this in your `.env` (copy `.env.example`) and use the proof-of-concept scripts to show unofficial API usage.