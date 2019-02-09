# lynlab

[![](https://img.shields.io/circleci/project/github/lynlab/lynlab.svg?style=for-the-badge&logo=circleci&maxAge=3600)](https://circleci.com/gh/lynlab/lynlab)
[![](https://img.shields.io/codecov/c/github/lynlab/lynlab.svg?style=for-the-badge&maxAge=3600)](https://codecov.io/gh/lynlab/lynlab)
[![](https://img.shields.io/github/languages/top/lynlab/lynlab.svg?style=for-the-badge&colorB=375eab&maxAge=3600)](#)

## Prerequisites

- Golang (recommends 1.11 or later)
- PostgreSQL

## Development

### Environment Variables

- `DB_HOST`
- `DB_USERNAME`
- `DB_PASSWORD`
- `DB_NAME`

You can use [direnv](https://direnv.net/) to set environment variables easily.

```sh
cp .envrc.template .envrc
vim .envrc
```

### Run

```sh
# Run tests
make test

# Download dependencies
go mod download

# Run server
go run .
```

## Deployment
```
docker build -t lynlab/lynlab .
docker push lynlab/lynlab
```
