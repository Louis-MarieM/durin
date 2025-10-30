# Durin
Durin is a batch ETL for collecting financial, economic and text data.

## Installation and run
### Prerequisites to installation
- Windows or Linux distribution.
- [Docker](https://docs.docker.com/get-started/get-docker/) installed (version 26.1.1 worked).

### Installation of Durin
- Clone the project.
    ```sh
    git clone https://github.com/Louis-MarieM/durin.git
    ```
- (Optionnal) Configure a file [`.env`](/config/.env.example) (cf. [Durin configuration](#durin-configuration)).
We use `.env.dev` for development.

### Build and run Durin
- Open a shell into parent directory `/durin`, where there is the docker-compose file.
- Run this command to **build and run** Durin's development version :
    ```sh
    docker-compose -f docker-compose.dev.yml --env-file config/.env.dev up --build
    ```

### Run tests
- Open a shell into parent directory `/durin`, where there is the docker-compose file.
- Run this command to **run** Durin's **tests** :
    ```sh
    docker-compose -f docker-compose.dev.yml --env-file config/.env.dev run --rm etl-pipeline pytest -q
    ```
N.B. : Logs are disable by default, we can unable their adding these pytest options : `-o log_cli=true -o log_cli_level=DEBUG` 

### Run Durin (debug mode)
- Open a shell into parent directory `/durin`, where there is the docker-compose file.
- Run this command to **run** Durin's in **debug mode**:
    ```sh
    docker-compose -f docker-compose.dev.yml --env-file config/.env.dev run --rm --service-ports etl-pipeline python -Xfrozen_modules=off -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m durin
    ```
- Attach a client to localhost:5678. (cf. [VSCode](#vscode))

### Run tests (debug mode)
- Open a shell into parent directory `/durin`, where there is the docker-compose file.
- Run this command to **run** Durin's **tests in debug mode**:
    ```sh
    docker-compose -f docker-compose.dev.yml --env-file config/.env.dev run --rm --service-ports etl-pipeline python -Xfrozen_modules=off -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m pytest -o log_cli=true -o log_cli_level=DEBUG -q
    ```
- Attach a client to localhost:5678. (cf. [VSCode](#vscode))

### VSCode
If you are using VSCode as IDE :
- Create the folder `.vscode` into parent directory.
- Create the file `launch.json` into the folder `.vscode`.
- Add this content into `launch.json` :
    ```
    {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Attach to Existing ETL Container",
                "type": "debugpy",
                "request": "attach",
                "connect": {
                    "host": "localhost",
                    "port": 5678
                },
                "pathMappings": [
                    {
                        "localRoot": "${workspaceFolder}",  // local path (Windows)
                        "remoteRoot": "/durin"              // path in container
                    }
                ]
            }
        ]
    }
    ```
When you runned Durin or tests in debug mode, then run this configuration in `RUN AND DEBUG` section of VSCode to attach a client to container and trigger breakpoints.

## Logs
Durin's logs are configured in [`logger.py`](/src/durin/config/logger.py)

Tests's logs are locked by default. There are configured with theses options :
```
-o log_cli=true -o log_cli_level=DEBUG
```

## Durin configuration
#### .env
- `VERSION` : to update at each merge.
- `LOG_LEVEL` : log level of every module.