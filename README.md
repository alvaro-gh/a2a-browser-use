# Proof of Concept for browser-use

This code is a bare-bones A2A implementation of browser-use as I'm learning about A2A while doing browser-use.

## What this does

The client asks ChatGPT to open linkedin and log in if it is necessary.

## Requirements

This requires the following:

* You must have an OpenAI account, some money in it and an API key set as an environment variable (`OPENAI_API_KEY`).
* You must set your linkedin user and password as environment variables, `LINKEDIN_USER` and `LINKEDIN_PASSWORD`.

## How to run this

**Clone the repository**

```
$ git clone https://github.com/alvaro-gh/a2a-browser-use.git
$ cd a2a-browser-use
```

**Create virtual environment**
You need to have Python 3.12 installed using `uv` (see guide [here](https://docs.astral.sh/uv/guides/install-python/))

```
$ uv venv -p 3.12
$ source .venv/bin/activate
```

**Install dependencies**

```
$ uv sync
```

**Install Playwright**

```
$ playwright install chromium --with-deps --no-shell
```

**Create a cookies file**

```
$ mkdir data
$ touch data/state.json
$ echo '{"cookies": []}' > data/state.json
```

**Run the server**

```
$ uv run .
```

**Run the client**
In another terminal, activate the virtual environment and run:

```
$ uv run client.py
```

## My playwright Installation

After setting up things with UV I installed playwright, consider this section just an annotation for me.

```
$ playwright install chromium --with-deps --no-shell
Downloading Chromium 136.0.7103.25 (playwright build v1169) from https://cdn.playwright.dev/dbazure/download/playwright/builds/chromium/1169/chromium-mac-arm64.zip
125.8 MiB [====================] 100% 0.0s
Chromium 136.0.7103.25 (playwright build v1169) downloaded to /Users/XXXX/Library/Caches/ms-playwright/chromium-1169
Downloading FFMPEG playwright build v1011 from https://cdn.playwright.dev/dbazure/download/playwright/builds/ffmpeg/1011/ffmpeg-mac-arm64.zip
1 MiB [====================] 100% 0.0s
FFMPEG playwright build v1011 downloaded to /Users/XXXX/Library/Caches/ms-playwright/ffmpeg-1011
```