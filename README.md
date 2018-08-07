# lynlab

[![Build Status](https://travis-ci.org/lynlab/lynlab.svg?branch=master)](https://travis-ci.org/lynlab/lynlab)

## Prerequisites
  - python 3.6 (or later)
  - docker

## Development
```
# Install required libraries.
pip install -r requirements.txt

# Migrate database schema.
python manage.py migrate

# Run server.
python manange.py runserver localhost:8080
```

You can use [direnv](https://direnv.net/) to set environment variables easily.

```
cp .envrc.template .envrc
vim .envrc
```

## Deployment
```
docker build -t lynlab/lynlab .
docker run -e 'NAME=VALUE' ... lynlab/lynlab
```

## Environment variables
  - `DJANGO_ENV` : application profile (`dev` | `prod`)
  - `DJANGO_SECRET_KEY`
  - `DB_HOST`
  - `DB_USERNAME`
  - `DB_PASSWORD`
  - `DB_NAME`
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_STORAGE_BUCKET_NAME`
  - `AWS_X_API_KEY`
  - `EMAIL_HOST_PASSWORD`

## Services
  - public
    - Blog (`/blog`)
    - Wiki (`/wiki`)
    - Storage (formal: media, `/storage`)
  - private
    - Moneybook
