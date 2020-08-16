# Lawrence Trail Hawks website

The [trailhawks.com](https://trailhawks.com) and [hawkhundred.com](https://hawkhundred.com) websites have been running on Django and Postgres going on ten years. 

## Install instructions

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

## License

The website code is released for learning purposes and to help other non-profits. For non-commercial usage, please contact @jefftriplett for licensing information.
