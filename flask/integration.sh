#Integration test
waitress-serve --host=127.0.0.1 --port=8080 wsgi:app &
python integration.py | exit
pkill -f waitress-serve
echo STR
exit 1
