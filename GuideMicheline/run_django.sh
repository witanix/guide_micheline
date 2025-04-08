#/bin/sh

python3 manage.py makemigrations  && \
python3 manage.py migrate  --noinput && \
 python3 manage.py collectstatic --noinput && \
 python3 manage.py migrate && python3 manage.py runserver 5000