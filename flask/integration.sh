#Integration test
waitress-serve --host=127.0.0.1 --port=8080 wsgi:app &
python integration.py | cat
pkill -f waitress-serve
exit 4
