release: pip install GDAL==3.2.1
web: gunicorn TPL.wsgi:application --log-file - --log-level debug
python manage.py collectstatic --noinput
manage.py migrate
