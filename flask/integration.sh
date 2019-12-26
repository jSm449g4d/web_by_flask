#Integration test
waitress-serve --host=127.0.0.1 --port=8080 wsgi:app &
result_integration=$(python integration.py)
pkill -f waitress-serve
echo $result_integration
exit $result_integration
