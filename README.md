# Geospatial data app API

APi project for working with geospatial data. Interacts with a database table
of places with id, name, description and coordinates fields.

## Features

* documentation at /api/doc/swagger/
* getting a list of places
* creating a place
* retrieving a place by its ID
* updating (and partial updating) a place
* deleting a place
* getting a place that is the nearest to provided coordinates as a query parameter


Technologies used:
* Django REST Framework
* PostgreSQL and PostGIS

## Run with docker

Docker should be installed.

1. Clone project 

```shell
git clone https://github.com/yuliia-stopkyna/geo-app.git
cd geo-app
```

2. Create ```.env``` file with your environment 
variables (look at ```.env.sample``` example file) in the project directory.


3. Run docker

```shell
docker-compose build
docker-compose up
```

## Run without docker

Install PostgreSQL with PostGIS extension and create database.

1. Clone project and create virtual environment

```shell
git clone https://github.com/yuliia-stopkyna/geo-app.git
cd geo-app
python -m venv venv
source venv/bin/activate # on MacOS
venv\Scripts\activate # on Windows
pip install -r requirements.txt
```

2. Install Geospatial libraries (GDALL, GEOS, PROJ): more information
about it [here](https://docs.djangoproject.com/en/4.2/ref/contrib/gis/install/geolibs/).

* On **Debian/Ubuntu**
```shell
sudo apt-get install binutils libproj-dev gdal-bin
```

* **macOS** instruction is [here](https://docs.djangoproject.com/en/4.2/ref/contrib/gis/install/#macos).

* If you run on **Windows**, you can use [OSGeo4W installer](https://trac.osgeo.org/osgeo4w/) for geospatial libraries.
Make sure to pick GDAL package. Then, in the `geo_app/settings.py` uncomment `GDAL_LIBRARY_PATH`, `GEOS_LIBRARY_PATH`,
`PROJ_LIB` and specify the path to the corresponding files on your computer (must be in `OSGeo4W` directory).


3. Set environment variables

```shell
set POSTGRES_HOST=<your db host>
set POSTGRES_DB=<your db name>
set POSTGRES_USER=<your db user>
set POSTGRES_PASSWORD=<your db password>
set DJANGO_SECRET_KEY=<your Django secret key>
```
4. Make migrations and run server

```shell
python manage.py migrate
python manage.py runserver
```