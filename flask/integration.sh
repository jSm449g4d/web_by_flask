#Integration test
waitress-serve --host=127.0.0.1 --port=8080 wsgi:app &
result_integration=$(python integration.py)
pkill -f waitress-serve
echo $result_integration
if [ $result_integration = 0]; then
    echo ok;exit 0
else
    echo $result_integration;exit 1
