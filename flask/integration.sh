#Integration test
waitress-serve --host=127.0.0.1 --port=8080 wsgi:app &
result_integration=bash -c "python integration.py"
pkill -f waitress-serve
exit $result_integration
