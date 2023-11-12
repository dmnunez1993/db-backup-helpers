# DB Backup Helpers

App for automating Database backups and uploading to the cloud

### Dependencies

- [docker](https://www.docker.com/) - Used for the dev environment and for deployment

### Set up the dev environment

Make sure Docker is installed. The dev environment should work with Linux, macOS and Windows (through WSL2)

To build the dev environment:

    cd dev_environment
    ./build

To run the dev environment:

    cd dev_environment
    ./run

### Start developing

In order to start developing, you need to run the following in the root of the repository:

    cp .env.example .env

Open this file and complete each parameter.

### Currently supported databases

- mysql
