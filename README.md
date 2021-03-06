gitality
========

Django Dash participation, http://gitality.com/


## Idea

Gitality is supposed to serve as achievement engine for open source developers.
Developers unlock achievements by contributing to their GitHub projects.

## Usage

Login via Github. Add your Github project at the 'Create' page.
Every 25 minutes status of your project will be updated (webhooks support is not available yet) and you'll get
new achievements and see stats.


## Installation

#### Getting project source code:

```bash
$ git clone https://github.com/dmrz/gitality.git gitality_project
```

#### Installing using virtualenvwrapper

If you use [virtualenv](https://pypi.python.org/pypi/virtualenv) with [virtualenvwrapper](https://pypi.python.org/pypi/virtualenvwrapper), installation is straightforward:

```bash
$ cd gitality_project
$ make
```

This will create virtualenv `gitality`, prepare local settings module at `gitality/gitality/local_settings.py`, install requirements, sync database (sqlite), run migrations and seed with development fixtures.

You can now run project using `make run`.

In a case you want to use postgresql, instead of sqlite, run `make settings_postgres`, edit `gitality/gitality/local_settings.py` to provide your settings, create postgres database or just run `make postgres` (assuming your current system user has permissions to create databases and your db name is `gitality`), then run `make db` to sync, migrate and seed it.

#### Step by step installation

Once you've managed and activated your virtual (or not :|) environment:

```bash
$ cd gitality_project
```

* Prepare local settings (skip this step if you want to create your own):

```bash
$ make settings # if you want to use sqlite
$ make settings_postgres # if you want to use postgresql
```

* Edit your local settings at `gitality/gitality/local_settings.py` or create your own if you skipped previous step (local settings module requires to have DATABASES setting).

* Install project requirements:

```bash
$ pip install -r requirements.txt
```

* Sync, migrate and seed database:

```bash
$ python gitality/manage.py syncdb --noinput
$ python gitality/manage.py migrate --noinput
$ python gitality/manage.py loaddata fixtures/dev/*
$ python gitality/manage.py loaddata fixtures/common/*
```

* Run project:

```bash
$ python gitality/manage.py runserver
```

**NOTE:** You can login to admin using the following credentials: `username = admin`, `password = admin`.


## Important

Certain additional settings are required for a project to operate properly, you can provide all in `gitality/gitality/local_settings.py`:

```python
# Used for GitHub sign in support, you can get these
# by creating an application in your GitHub settings.
GITHUB_APP_ID = '...'
GITHUB_API_SECRET = '...'

# GitHub account credentials that
# will be used to consume GitHub's API.
GITHUB_BOT_NAME = '...'
GITHUB_BOT_PASSWORD = '...'
```

Gitality uses background and periodic tasks for it's functionality by utilizing amazing [Celery](http://www.celeryproject.org/) project. Celery worker uses [redis](http://redis.io/) as broker and result backend, so it has to be installed (otherwise you can override celery settings).

Running celery (in separte terminal window):

```bash
$ python gitality/manage.py celery worker -B
```
