#Integration test 1/2
waitress-serve --host=127.0.0.1 --port=8080 wsgi:app &
result_integration=$(python integration.py)
pkill -f waitress-serve
if [ $result_integration = "ok" ]; then
    echo PASS:Integration Test;exit 0
else
    echo REJECT:$result_integration;exit 1
fi
