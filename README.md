# whereami

## Possible architecture changes!
At the moment we have 2 different architectures in mind. 
First, using users to track everything is way more difficult but may seem interesting for employers.
Second, use links to join private games without having users to sign in.


### To create a virtual environment
``` sh
cd whereami
python3 -m venv env
```

To activate the virtual environment in linux
``` sh
source env/bin/activate
```
To quit the virtual environment
``` sh
deactivate
```
### To run the app using docker-compose

``` sh
docker-compose up --build -d
```

### To test

First access docker-compose web service

``` sh
docker-compose run web bash
```

And then:

``` sh
python manage.py test --keepdb
```

#### WARNING: make sure you have hstore extension created in the test db. If you don't have it do it like how it's said below. And use --keepdb to prevent the extension from being removed (because django creates a new DB everytime)

``` sh
docker-compose run db bash
psql --host=[your host name] --dbname=[your test db name] --username=[your username]
create extension hstore;
```