# LLM Chat Service

This is an LLM Chat for corporate users.
The purpose is to act as a proxy for different LMM model APIs like OpenAI's GPT, Llama2, Claude etc. 
Providing a unified experience for the organization users, and also home grown features like monitoring, load-balancing, authorization and more.

The core of this project is a web service using FastAPI and later we will provide a chat UI for the user.

Note that we are service the APIs over:
`http://<hostname>:<port>/api/v1/....`


### Getting started:
* Enable virtual environment using poetry: `poetry shell`
* Install packages: `poetry install`
* If you want to install 3rd party libraries, run: `poetry add <pacakge>` (e.g. `poetry add openai`)
* To use openai api, add api key enviromental veriable: OPENAI_API_KEY
* Create a `.env` file in the root folder and set `OPENAI_API_KEY` env var with the key value.

### Running Tests
* Run ut: `pytest tests/unit`
* Run e2e: `pytest tests/e2e`

### Running tools:
* Run pylint: `./run_pylint.sh`

### Running the service

In your console - export the `OPENAI_API_KEY` env var with the key value.

### Running the demo
* Run the service in one terminal: `uvicorn app.main:app --reload`
* Run the demo in another terminal: `streamlit run demo/demo.py`

#### Dev mode:
* Run this: `uvicorn app.main:app --reload`

* Access the /simple api: http://127.0.0.1:8000/api/v1/simple

#### "Prod" mode (no reload):
`uvicorn app.main:app`

### Debugging the service
Run `main.py` and add breakpoints

### Adding logs to the files
Add this import code line at the beginning of the file:
`from app.internal import infra_logger`

#### Methods to use the loggers:
Info logger:
`infra_logger.log_info("Insert your text here")`

Error logger:
`infra_logger.log_error("Insert your text here")`

Warning logger:
`infra_logger.log_warning("Insert your text here")`

Debug logger:
`infra_logger.log_debug("Insert your text here")`

### Project structure
To understand the diff when structuring a "big" application, read the following:
https://fastapi.tiangolo.com/tutorial/bigger-applications/

