<!--
SPDX-License-Identifier: MIT
Copyright (c) 2020 icecake0141
-->

<!--
This file was created or modified with the assistance of an AI (Large Language Model). Review for correctness and security.
-->

# Linguafrancatto

A language translation bot for Slack using DeepL as a backend.

## About

This bot has the ability to automatically post translated messages between channels with a specific basename or to post translated messages triggered by a specific keyword. It uses Slack's Event API as a monitoring mechanism for messages, so it works as an endpoint web server, and is designed to run on Google App Engine, but it can also run in an on-premise environment. This project was created using the Slack Bolt SDK for Python.

## Requirements

* DeepL API Key (Valid subscription to DeepL API plan)
* Slack Bot Token and Slack Signing Secret (Admin access to a Slack workspace)
* Python 3.8 or higher

### Built With

* [Slack Bolt for Python](https://github.com/slackapi/bolt-python)
* [Flask](https://flask.palletsprojects.com/)
* [DeepL API](https://www.deepl.com/docs-api/introduction/)

## Environment Variables

The following environment variables must be set (as `env_variables.yaml` file or system environment variables):

| Environment Variable | Description | Required |
|---------------------|-------------|----------|
| `DEEPL_TOKEN` | DeepL API authentication token | Yes |
| `SLACK_SIGNING_SECRET` | Slack App signing secret | Yes |
| `SLACK_BOT_TOKEN` | Slack Bot token | Yes |
| `MULTI_CHANNEL` | Comma-separated list of Slack channel basenames that need continuous translation | Yes |
| `DEBUG_MODE` | Debug mode (`True` or `False`) | No (Default: False) |
| `PORT` | Server port number | No (Default: 3000) |
| `GUARDIAN_UID` | Slack UID of bot administrator | No |
| `PROJECT_ID` | Google Secret Manager project ID | No |
| `SECRET_NAME` | Google Secret Manager secret name | No |
| `SECRET_VERSION` | Google Secret Manager secret version | No |

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/icecake0141/linguafrancatto.git
   cd linguafrancatto
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Create `env_variables.yaml` based on `env_variables.yaml.sample` and set the required environment variables.

## Running Locally

1. Set environment variables (as `.env` file or system environment variables).

2. Start the application:
   ```sh
   python main.py
   ```

3. By default, the server starts on port 3000. This can be changed with the `PORT` environment variable.

4. Slack Event API endpoint: `http://your-server:3000/slack/events`

## Slack and DeepL Setup

### Slack App Configuration

1. Create a new app at [Slack API](https://api.slack.com/apps).
2. Under **OAuth & Permissions**, add the following Bot Token Scopes:
   - `channels:history` - Read channel messages
   - `channels:read` - Read channel information
   - `chat:write` - Send messages
   - `users:read` - Read user information
3. Enable **Event Subscriptions** and set the Request URL: `https://your-server/slack/events`
4. Under **Subscribe to bot events**, add `message.channels`.
5. Install the app to your workspace and obtain the Bot User OAuth Token.

### DeepL API Configuration

1. Create an account at [DeepL API](https://www.deepl.com/pro-api).
2. Obtain your API key and set it as the `DEEPL_TOKEN` environment variable.

## Usage

### Keyword-Triggered Translation

Include the following keywords in your message to translate it to the specified language:

- **Nyan** - Translate to Japanese
- **Meow** - Translate to English
- **Miaou** - Translate to French
- **Мяу** - Translate to Russian

Example:
```
Hello, how are you? Nyan
```
This message will be translated to Japanese.

### Multi-Channel Automatic Translation

Channels with basenames set in the `MULTI_CHANNEL` environment variable will have messages automatically translated.

Example: If `MULTI_CHANNEL=general`:
- `general` (or `general-ja`) - Japanese channel
- `general-en` - English channel
- `general-fr` - French channel

Messages posted in any of these channels will be automatically translated and posted to the other language channels.

### Usage Statistics

Post `Meousage` in a channel to display DeepL API usage statistics.

## Deploying to Google App Engine

1. Review the `app.yaml` file and adjust settings as needed.

2. Set environment variables in `env_variables.yaml` (refer to `env_variables.yaml.sample`).

3. Ensure Google Cloud SDK is installed.

4. Deploy:
   ```sh
   gcloud app deploy
   ```

5. View logs:
   ```sh
   gcloud app logs tail -s default
   ```

## Development & Testing

### Debug Mode

Set `DEBUG_MODE=True` to enable detailed log output.

### Code Formatting

```sh
black .
```

### Linting

```sh
ruff check .
```

### Testing

This project currently has no automated tests. For manual testing, send actual messages in a Slack workspace to verify functionality.

## Security

- **Environment Variables**: Manage API tokens and secrets as environment variables, and do not hardcode them in source code.
- **HTTPS**: Always use HTTPS in production. The Slack Event API requires an HTTPS endpoint.
- **Authentication**: Use Slack Signing Secret to verify request authenticity (automatically handled by Slack Bolt SDK).
- **Google Secret Manager**: We recommend using Google Secret Manager for managing sensitive information.

## License

This project is distributed under the MIT License. See the `LICENSE` file for details.

## Links

* Project Link: [https://github.com/icecake0141/linguafrancatto](https://github.com/icecake0141/linguafrancatto)

## References

* [DeepL API Documentation](https://www.deepl.com/docs-api/introduction/)
* [Slack API](https://api.slack.com/)
* [Slack Bolt for Python - Getting Started](https://slack.dev/bolt-python/tutorial/getting-started)
* [Slack Bolt with Google App Engine and Flask](https://github.com/slackapi/bolt-python/blob/main/examples/google_app_engine/flask/main.py)
* [Google App Engine Python 3 Runtime](https://cloud.google.com/appengine/docs/standard/python3/runtime)

## Acknowledgements

* [Best-README-Template](https://github.com/othneildrew/Best-README-Template/)
