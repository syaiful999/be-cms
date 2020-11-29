rm -rf appenv/
python3 -m venv appenv
. appenv/bin/activate
pip3 install -r requirements.txt
uwsgi --socket 0.0.0.0:8080 --protocol=http -w wsgi:app