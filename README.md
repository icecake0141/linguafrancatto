# Linguafrancatto

This project is a language translation bot for Slack using DeepL as a backend.  


## About The Project

This bot the ability to automatically post translated messages between channels with a specific basename or to post translated messages triggered by a specific keyword.  It uses Slack's Event API as a monitoring mechanism for messages, so it works as an endpoint web server, and is designed to run on the Google App Engine, but it can also run on an on-premise environment.  This project was created using the Slack Bolt SDK for Python.

What you need:
* DeepL API authentication key = Valid subscription of DeepL API plan
* Slack Bot Token and Slack signing secret = Admin access to a slack workspace


### Built With

* [Slack Bolt for Python](https://github.com/slackapi/bolt-python)
* [Flask](https://flask.palletsprojects.com/)


## Getting Started

TBD
### Slack
### DeepL
### Google App Engine
### On-Premise

### Prerequisites

TBD
* Python
  ```sh
  pip install -r requirements.txt
  ```


### Installation

TBD
1. Get a API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
3. Enter your API in `config.js`
   ```JS
   const API_KEY = 'ENTER YOUR API';
   ```


## Resources

* [Deepl API](https://www.deepl.com/docs-api/introduction/)
* [Slack API](https://api.slack.com/)
* [Slack Bolt for Python](https://slack.dev/bolt-python/tutorial/getting-started)
* [slack Bolt with GaE and Flask](https://github.com/slackapi/bolt-python/blob/main/examples/google_app_engine/flask/main.py)
* [Google App Engine](https://cloud.google.com/appengine/docs/standard/python3/runtime)


## License

Distributed under the MIT License. See `LICENSE` for more information.


## Contact

Project Link: [https://github.com/icecake0141/linguafrancatto](https://github.com/icecake0141/linguafrancatto)


## Acknowledgements
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template/)
