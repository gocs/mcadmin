# McAdmin

## requirements

install npm
install docker (docker compose is included)

## todo

- [x] user management
- [x] user role
- [x] minecraft whitelist
- [x] minecraft server status
- [x] payment rest api

## commands

- copy the `.env.example` to `.env` and fill in the values
- `make setup` start the docker containers (initial build)
- `make twi` build the tailwind (initial build)
- `make up` restart the docker containers (succeeding builds)

the setup may pause to allow you to make a username, password, and email for the superuser

see the `Makefile` for more commands

- go to `http://localhost`
