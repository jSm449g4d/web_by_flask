# web_by_flask
For studying **web framework** <br>
This app is deployed on Cloud_Run(GCP) by CI/CD <br>
Cloud_Run(GCP): https://flask-uvutu72eta-uc.a.run.app/
## Images (in development)

![3](https://github.com/jSm449g4d/web_by_flask/blob/master/assets/nicoapi.png)

![4](https://github.com/jSm449g4d/web_by_flask/blob/master/assets/janomedoe.png)

![1](https://github.com/jSm449g4d/web_by_flask/blob/master/assets/aa.png)
_____
![2](https://github.com/jSm449g4d/web_by_flask/blob/master/assets/chat.png)
 
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
