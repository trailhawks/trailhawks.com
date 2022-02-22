<h1 align="center">Welcome to Lawrence Trail Hawks website 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-2022.2.1-blue.svg?cacheSeconds=2592000" />
  <a href="#" target="_blank">
    <img alt="License: LIMITED" src="https://img.shields.io/badge/License-LIMITED-yellow.svg" />
  </a>
  <a href="https://twitter.com/webology" target="_blank">
    <img alt="Twitter: webology" src="https://img.shields.io/twitter/follow/webology.svg?style=social" />
  </a>
</p>

> The [trailhawks.com](https://trailhawks.com) and [hawkhundred.com](https://hawkhundred.com) websites have been running on Django and Postgres going on ten years. 

### 🏠 [Homepage](https://github.com/trailhawks/trailhawks.com)

### ✨ [Demo](https://trailhawks.com/)

## Install

```sh
docker-compose build
```

## Usage

```shell
# Clone our repo from GitHub
git clone git@github.com:trailhawks/trailhawks.com.git
cd trailhawks.com

# copy our sample env and edit it
cp .env-sample .env

# build our primary Docker image
docker-compose build

# Some house cleaning
docker-compose run --rm web python manage.py collectstatic --noinput
docker-compose run --rm web python manage.py migrate
docker-compose run --rm web python manage.py createsuperuser

# Run our dev server
docker-compose up

# Open the Admin and add some races and weekly runs
open http://localhost:8000/admin/
```
## Run tests

```sh
# TDB
# docker-compose run --rm web pytest
```

## Author

👤 **Jeff Triplett**

* Website: https://jefftriplett.com
* Twitter: [@webology](https://twitter.com/webology)
* Github: [@jefftriplett](https://github.com/jefftriplett)

## Show your support

Give a ⭐️ if this project helped you!

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
