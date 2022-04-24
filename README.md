# Coupon

Python Django Rest Framework and SQLite database

## Technologies
- Python 3.9
- Django Rest Framework - Framework
- SQLite - Develop Database
- Docker - Project Structure
- Docker-compose - Development Environment


## How to use?

### Docker

1. Clone this repository

2. To copy `.env.example` to `.env`, run: `make copy-envs`

3. Build docker image and run migrates: `make build`

4. Run api: `make run`

5. In your browser call: [Swagger Localhost](http://localhost:8000/api/docs)

### Locally

1. Clone this repository.
2. Create a virtualenv
3. To initialize and install dependencies, run: `make init`
4. To apply the migrations, run: `make migrate` 
5. Run: `make run-local`
6. In your browser call: [Swagger Localhost](http://0.0.0.0:8000/swagger/)


#### Testing

To test, just run `make test`.

To see the test coverage, run `make test-coverage`

To run a specifc test, run `make test-matching k=<test-name>`
