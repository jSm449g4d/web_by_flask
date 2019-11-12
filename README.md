# web_by_flask
For studying the web framework

The images are in development
![1](https://github.com/jSm449g4d/web_by_flask/blob/master/assets/image-4.png)

## how to use
plz install requirements<br>
`$ sudo apt install python3-pip apache2-dev libapache2-mod-wsgi-py3`<br>
`$ pip3 install mod_wsgi flask` 

plz clone `flask/` folder 

plz setting apache2.conf<br>
`$ sudo vim /etc/apache2/apache2.conf`

plz add below<br>
`WSGIScriptAlias (root path) (path to flask/wsgi.py)`

### Some features are restricted by permissions.
`$ sudo chmod -R 777 (path to flask/)`
