# Unlock Auto(AUTO)
Home space (Admin) for developing a marketplace for selling cars from Kazakhstan to Russia

## Table of contents

<!-- TOC -->
* [Unlock Auto(AUTO)](#unlock-autoauto)
  * [Table of contents](#table-of-contents)
  * [Information of stands](#information-of-stands)
  * [Dev stand <a id="maintainer-anchor"></a>](#dev-stand-a-idmaintainer-anchora)
  * [How to up this project](#how-to-up-this-project)
  * [Code style verifications](#code-style-verifications)
  * [How to run tests](#how-to-run-tests)
  * [How to prepare your code to push](#how-to-prepare-your-code-to-push)
    * [Branch](#branch)
    * [Commits](#commits)
    * [Merge requests](#merge-requests)
<!-- TOC -->

## Information of stands

## Dev stand <a id="maintainer-anchor"></a>
| Name        | Value                                                                           |
|-------------|---------------------------------------------------------------------------------|
| Domain      | https://content.unlock-auto.akhter.dev/admin                                    |
| OpenAPI Doc | https://content.unlock-auto.akhter.dev/docs                                     |
| Login/Pass  | `username`/`password`                                                           |
| Maintainer  | [@azizminov](https://t.me/azizminov)                                            |
| Jira        | [Unlock Auto](https://akhter.atlassian.net/jira/software/projects/UA/boards/37) |


## How to up this project
1. Need to create .env for docker-compose in this case for local development do next:

```shell
$ cp .env.ci .env
```

2. You need to have Docker and Docker Compose installed. If not, here is the link to the Docker [documentation](https://docs.docker.com/engine/install/) with installation instructions.If Docker is already installed, here is the command you need to execute:
```shell
$ docker-compose up -d # or docker compose up -d
```
3. To check if containers with application is up use:
```shell
$ docker-compose ps
```
There should be output like this
```shell
NAME                IMAGE                  COMMAND                  SERVICE             CREATED             STATUS                   PORTS
ums-app-1           ums-app                "entrypoint.sh start…"   app                 2 minutes ago       Up 14 seconds            0.0.0.0:8000->8000/tcp
ums-db-1            postgres:14.1-alpine   "docker-entrypoint.s…"   db                  2 minutes ago       Up 2 minutes (healthy)   0.0.0.0:5453->5432/tcp
ums-redis-1         redis:6.2.6-alpine     "docker-entrypoint.s…"   redis               2 minutes ago       Up 2 minutes (healthy)   0.0.0.0:6379->6379/tcp
```

4. Check http://localhost:8000/ there should be an application and root endpoint returns
```json
{"detail": "Not Found"}
```

## Code style verifications
1. Install pre-commit locally:
```shell
$ pip install pre-commit
```
2. In the root of repository install pre-commit hooks using:
```shell
$ pre-commit install
```
3. For the first run use:
```shell
$ pre-commit run --all
```

## How to run tests
To run tests use docker container and from the inside use pytest with flags
```shell
$ pytest -v . --cov=./ --cov-report term-missing --cov-report xml --cov-fail-under=50 --color=yes
```

## How to prepare your code to push
### Branch
For this project you should use formalized names for the branches eg. **_`UNLOCK-123/add_reports`_**, where **_`UNLOCK`_** is the project prefix, **_`123`_** identification number of you tasks and **_`add_reports`_** short name of feature you need to create.
### Commits
Commits should start from the main action like `[ADD] [REFACTOR] [FIX] [REMOVE]` after this title and in imperative way with list `If applied, this commit will` fix/add/remove something, example:
```shell
[ADD]
- Add adapter for ones in /path/to/file.py
- Add middleware for authchecking in /path/to/file.py
[REMOVE]
- Remove static files from app/static
```
### Merge requests
1. Always do **squash commits**;
2. Rename title from commit message to number_of_task/action, like: `UNLOCK-123/add_reports`;
3. Write main actions which will do your MR.
