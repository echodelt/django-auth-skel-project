django-auth-skel-project
==================

Yet another Django skeleton project.

This one is for **Django 1.10** and requires either Python 2.7 or 3.4+.

---

Based on the Django’s default authentification system, it includes :

* user registration, login, password change & reset pages
* a minimal user's profile editor (intended to be extended or redisigned as needed)
* unit tests related to the corresponding forms and views
* Bootstrap themed page

This skeleton assumes that the backend database is a MySQL server : this can
however be easily changed by editing the provided settings file in the "core" package.

---

Quick start
------------

First create the MySQL database and it's user with the appropriate privileges :

    $ mysql -uroot -p

    mysql> CREATE DATABASE django_skel_project DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;

    mysql> GRANT ALL PRIVILEGES ON django_skel_project.* TO 'dev_user'@'localhost' IDENTIFIED BY 'dev_pwd';

    mysql> FLUSH PRIVILEGES;

    mysql> quit


Next, create a virtualenv dedicated to this project :

    $ mkvirtualenv django-skel-project -p /usr/bin/python3.4

    $ deactivate


The "sensitive" configuration parameters related to the project (secret key,
MySQL and mail host/user/name...) won't be stored in the settings files located
in the source tree but rather registered as **environment variables**.

The project's settings module to load will also be registered as an environment
variable in order to ease later configuration tweaks if needed.

These environment variables will here be stored in the **bin/postactivate**
script of the previously created virtualenv, which is sourced just after the
environment activation.

So edit the  ~/.virtualenvs/django-skel-project/bin/postactivate file and copy
the following content in it :

    #!/bin/bash
    # This hook is sourced after this virtualenv is activated.

    export DJANGO_SETTINGS_MODULE=core.settings.dev

    export SECRET_KEY="your_secret_key"

    export ALLOWED_HOSTS="localhost,testserver"

    export MYSQL_DB_NAME="django_skel_project"
    export MYSQL_DB_USER="dev_user"
    export MYSQL_DB_PASSWORD="dev_pwd"
    export MYSQL_DB_HOST="localhost"
    export MYSQL_DB_PORT="3306"

    # Don't forget to uncomment and set the following parameters
    # (required, among others, for the processing of password reset requests)

    # export EMAIL_HOST=YOUR_EMAIL_HOST
    # export EMAIL_PORT=YOUR_EMAIL_PORT
    # export EMAIL_HOST_USER=YOUR_EMAIL_HOST_USER
    # export EMAIL_HOST_PASSWORD=YOUR_EMAIL_HOST_PASSWORD
    # export EMAIL_USE_TLS=True|False
    # export DEFAULT_FROM_EMAIL=YOUR_DEFAULT_FROM_EMAIL

Next activate the virtualenv, install the dependencies and run the migrations :

    $ workon django-skel-project

    $ pip install -r requirements/requirements.txt

    $ python manage.py migrate


Run the test server with :

    $ python manage.py runserver

and navigate to localhost:8000.
