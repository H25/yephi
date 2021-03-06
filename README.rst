Social media for movie lovers
-----------------------------

Introduction
++++++++++++

This project was started as my bachelor thesis project. The idea was to create a basic social media using `Django <https://www.djangoproject.com/>`_ and since I'm addicted to movies, I have created this project for movie lovers.
Although in the project there are several apps which focus on movies, it can be customized easily to be a fully working social media for any other needs.


Installation
++++++++++++

Setup virtualenv::

    sudo easy_install pip
    sudo pip install virtualenv
    virtualenv env_django143 --no-site-packages

Install dependencies::

    pip install -r requirements.txt

Create the database and change the settings accordingly::

    cp yephi/local_settings.sample.py yephi/local_settings.py    

Sync database::

    python manage.py syncdb

Load fixtures::

    python manage.py loaddata deployment/initial_data.xml

Reindex for search::

    python manage.py rebuild_index

Run with gunicorn::

    python manage.py run_gunicorn -D --bind=127.0.0.1:8000


License
+++++++

This project is licensed under `GPLv3 <http://www.gnu.org/licenses/gpl-3.0.html>`_.