#Integration test 1/2
waitress-serve --host=127.0.0.1 --port=8080 wsgi:app &
result_integration=$(python integration.py)
pkill -f waitress-serve
if [ $result_integration = 0]; then
    echo PASS:Integration Test;exit 0
else
    echo $result_integration;exit 1
