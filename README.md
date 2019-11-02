# web_by_flask
For studying the web framework
## how to use
plz install requirements
`$ sudo apt install python3-pip apache2-dev libapache2-mod-wsgi-py3
$ pip3 install mod_wsgi flask` 

plz setting apache2.conf
`$ sudo vim /etc/apache2/apache2.conf`
plz add below
`WSGIScriptAlias (root path) (path to /flask/wsgi.py)`
