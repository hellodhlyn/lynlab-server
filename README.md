# lynlab

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
# (TBD)
```




## Deployment
```
docker build -t lynlab/lynlab .
docker push lynlab/lynlab
```
