#Integration test
waitress-serve --host=127.0.0.1 --port=8080 wsgi:app &
python integration.py > result_integration
pkill -f waitress-serve
exit $result_integration
