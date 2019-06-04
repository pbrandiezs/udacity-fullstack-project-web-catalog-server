# Program: application.py 
* Author: Perry Brandiezs
* Date: May 1, 2019
* Last Updated: June 4, 2019


This program demonstrates CRUD operations using an Item Catalog.

*   Create: Ability to create an airplane item
*   Read:   Ability to read an inventory list showing category name, item name, item description.  Ability to show item detail, login required.
*   Update: Ability to edit item detail, login required.
*   Delete: Ability to delete an item, login required and must be item creator.

This program demonstrates OAuth2 authentication and authorization using a third party provider.
*   Login / Logout using Facebook is provided, link can be found at the top-right of the main screen.
*   Login required to display item detail, update an item, or delete an item.
*   Must also be the item creator to delete.

This program demonstrates API endpoints.
*   Display all items
*   Display specific item detail
*   Display all users

This program is used to demonstrate a Linux Web Server configuration using:
*   AWS Lightsail
*   Apache2
*   PostgreSQL

## Notes to Udacity grader
* The IP address is 34.210.153.255, ssh port 2000
* You may login with ssh grader@34.210.153.255 -p 2200 -i privatekeyfile, using the privatekeyfile provided with project submission
* The URL is https://34.210.153.255.xip.io
* Note https is required to support oauth2 login with facebook, connecting with http will redirect to https.
### Summary of software installed
```
Server level software:
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi-py3
sudo apt-get install postgresql
sudo apt-get install libpq-dev postgresql-client postgresql-client-common
sudo apt-get install python3-dev
sudo apt-get install python3-pip

Python packages (requirements.txt):
blinker==1.3
chardet==2.3.0
Click==7.0
cloud-init==18.5
command-not-found==0.3
configobj==5.0.6
cryptography==1.2.3
Flask==1.0.3
hibagent==1.0.1
httplib2==0.12.3
idna==2.0
itsdangerous==1.1.0
Jinja2==2.10.1
jsonpatch==1.10
jsonpointer==1.9
language-selector==0.1
MarkupSafe==1.1.1
oauth2client==4.1.3
oauthlib==1.0.3
passlib==1.7.1
prettytable==0.7.2
psycopg2==2.8.2
pyasn1==0.4.5
pyasn1-modules==0.2.5
pycurl==7.43.0
pygobject==3.20.0
PyJWT==1.3.0
pyserial==3.0.1
python-apt==1.1.0b1+ubuntu0.16.4.4
python-debian==0.1.27
python-systemd==231
PyYAML==3.11
requests==2.9.1
rsa==4.0
six==1.12.0
SQLAlchemy==1.3.4
ssh-import-id==5.5
ufw==0.35
unattended-upgrades==0.1
urllib3==1.13.1
Werkzeug==0.15.4

```
### Summary of additional configuration changes made:
* Modified code to use python 3
```
1. xrange statements replaced with range
2. shebang changed to python 3
3. modified to use bytes instead of strings to work with python 3
```
* Modified code to use PostgreSQL, instead of SQLite
```
1. Modifications to create_planes.py to not assign id, but instead increment automatically
```
* Modified application.py to work with Apache / wsgi
```
1. Remove the flask web server from the bottom of the code
```
### Summary of third-party resources used:
Reference sites:

https://www.fullstackpython.com/blog/postgresql-python-3-psycopg2-ubuntu-1604.html
https://www.learndatasci.com/tutorials/using-databases-python-postgres-sqlalchemy-and-alembic/
https://www.compose.com/articles/using-postgresql-through-sqlalchemy/
https://github.com/httplib2/httplib2/wiki/Examples-Python3
https://stackoverflow.com/questions/7585435/best-way-to-convert-string-to-bytes-in-python-3
https://stackoverflow.com/questions/37063685/facebook-oauth-the-domain-of-this-url-isnt-included-in-the-apps-domain

Reference step 13 for guidance on the wsgi script
https://github.com/iliketomatoes/linux_server_configuration

For guidance on disabling the flask server in __init_.py
https://github.com/kcalata/Linux-Server-Configuration/blob/master/README.md

Defining Apache virtual hosts, and redirecting to https:
https://groups.google.com/forum/#!topic/django-users/3fx4HuGXQ4U
https://www.tecmint.com/redirect-http-to-https-on-apache/

wsgi references:
http://flask.pocoo.org/docs/1.0/deploying/mod_wsgi/
https://wsgi.readthedocs.io/en/latest/

xip.io reference:
http://xip.io/

import not at top of file reference:
https://stackoverflow.com/questions/36827962/pep8-import-not-at-top-of-file-with-sys-path



## Installation for reference only needed if deploying a new server
* Deploy an AWS LightSail server, and log in to ubuntu per AWS procedures.
### Update the server
```
sudo apt-get update
sudo apt-get upgrade
sudo reboot
```
### Enforce key based login
```
sudo vi /etc/ssh/sshd_config
-make sure PasswordAuthentication no
```
### Configure Lightsail firewall rules
```
On AWS console, navigate to the Networking tab.
Add Custom port 2200,
add port HTTPS 443.

If not already defined:
add port HTTP 80, 
add port SSH 22,
add port custom 123 (ntp).
```
### Configure ssh to use port 2200
```
sudo vi /etc/ssh/sshd_config
Change line Port 22 to Port 2200
sudo service ssh restart

ssh in again using port 2200
```
### Configure ubuntu firewall
```
sudo ufw status
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 2200/tcp
sudo ufw allow 443/tcp
sudo ufw allow www
sudo ufw allow ntp
sudo ufw enable
sudo ufw status
```
### Add user grader and catalog
```
sudo adduser grader
```
### Generate key pair on local machine, not on the server:
```
ssh-keygen
place the .pub file on the server
	login as grader, or do sudo su - grader
	mkdir .ssh
	touch .ssh/authorized_keys
	paste the public key into the authorized_keys file
	chmod 700 .ssh
	chmod 644 .ssh/authorized_keys
	
ssh grader@ip -p 2200 -i privatekeyfile   #to login
```
### Add to sudoers:
```
sudo cp /etc/sudoers.d/90-cloud-init-users /etc/sudoers.d/grader
sudo vi /etc/sudoers.d/grader   
	Change ubuntu to grader
```
### Install Apache
```
sudo apt-get install apache2
```
### Configure to use wsgi
```
sudo apt-get install libapache2-mod-wsgi-py3
sudo vi /etc/apache2/sites-enabled/000-default.conf to look similar to:

<VirtualHost *:80>
        # The ServerName directive sets the request scheme, hostname and port that
        # the server uses to identify itself. This is used when creating
        # redirection URLs. In the context of virtual hosts, the ServerName
        # specifies what hostname must appear in the request's Host: header to
        # match this virtual host. For the default virtual host (this file) this
        # value is not decisive as it is used as a last resort host regardless.
        # However, you must set it for any further virtual host explicitly.
        #ServerName www.example.com

        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/html

        # Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
        # error, crit, alert, emerg.
        # It is also possible to configure the loglevel for particular
        # modules, e.g.
        #LogLevel info ssl:warn

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        # For most configuration files from conf-available/, which are
        # enabled or disabled at a global level, it is possible to
        # include a line for only one particular virtual host. For example the
        # following line enables the CGI configuration for this host only
        # after it has been globally disabled with "a2disconf".
        #Include conf-available/serve-cgi-bin.conf
        # WSGIDaemonProcess myapp user=catalog group=catalog threads=5
        # WSGIScriptAlias / /var/www/html/myapp.wsgi
        Redirect / https://34.210.153.255
</VirtualHost>

<VirtualHost *:443>
    ServerAdmin webmaster@localhost
    DocumentRoot /var/www/html
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
    SSLEngine on
    SSLCertificateFile /etc/apache2/ssl/ca.crt
    SSLCertificateKeyFile /etc/apache2/ssl/ca.key
    WSGIDaemonProcess myapp user=catalog group=catalog threads=5
    WSGIScriptAlias / /var/www/html/myapp.wsgi
</VirtualHost>

# vim: syntax=apache ts=4 sw=4 sts=4 sr noet
```
### Install PostgreSQL
```
sudo apt-get install postgresql
sudo adduser catalog
sudo -u postgres createuser catalog             
```
### Install additional packages
```
sudo apt-get install libpq-dev postgresql-client postgresql-client-common
sudo apt-get install python3-dev
sudo apt-get install python3-pip
sudo pip3 install psycopg2
```
### Modify apache user to catalog
```
sudo vi /etc/apache2/envvars
Change APACHE_RUN_USER and APACHE_RUN_GROUP to catalog, instead of www-data
```
### Connect to the github repo
```
Login as ubuntu
ssh-keygen
Add the id_rsa.pub key to github ssh keys
git clone git@github.com:pbrandiezs/udacity-fullstack-project-web-catalog-server.git udacity-project
```
### Enable ssl for the webserver
```
sudo a2enmod ssl
```
### Generate and install certificates
```
sudo openssl genrsa -out ca.key 2048
sudo openssl req -nodes -new -key ca.key -out ca.csr
sudo openssl x509 -req -days 365 -in ca.csr -signkey ca.key -out ca.crt
sudo mkdir /etc/apache2/ssl
sudo cp ca.* /etc/apache2/ssl/
```
### Install additional packages
```
sudo pip3 install sqlalchemy
sudo pip3 install passlib
sudo pip3 install itsdangerous
sudo pip3 install flask
sudo pip3 install oauth2client
sudo pip3 install werkzeug
sudo pip3 install click
sudo pip3 install httplib2
```
### Install application
```
cd ~/udacity-project
sudo mkdir /var/www/html/catalog
sudo cp models.py /var/www/html/catalog/models.py
sudo cp create_planes.py /var/www/html/catalog/create_planes.py
sudo cp application.py /var/www/html/catalog/__init__.py
sudo cp myapp.wsgi /var/www/html/myapp.wsgi
sudo chown catalog.catalog /var/www/html/myapp.wsgi
sudo chown -R catalog.catalog /var/www/html/catalog

# cp in the templates, static files, and fb_client_secrets
sudo cp -r templates /var/www/html/catalog/
sudo cp -r static /var/www/html/catalog/
sudo cp fb_client_secrets.json /var/www/html/catalog/fb_client_secrets.json
sudo chmod 640 /var/www/html/catalog/fb_client_secrets.json
sudo chown -R catalog.catalog /var/www/html/catalog
```
### Add to facebook developers console
```
Add the new domain to the facebook developer console for the application
Site URL:   https://(public_ip).xip.io/
Add additional domains to Domain Manager, under advanced settings, for example
with a public IP of 34.210.153.255
https://34.210.153.255.xip.io/login
https://34.210.153.255/
http://34.210.153.255/
https://34.210.153.255.xip.io/
http://34.210.153.255.xip.io/
```
### Rebuild and populate the database
```
sudo service apache2 stop
sudo -u postgres dropdb ItemCatalog
sudo -u postgres createdb -O catalog ItemCatalog
sudo -u catalog python3 models.py
sudo -u catalog python3 create_planes.py
sudo service apache2 start
```
### Connect to the website
```
https://34.210.153.255.xip.io/

* Note must use https.
```
### Accept the certicate when first connecting
* Note if a timeout error occurs, please try clearing cache and attempt again.  It will be necessary to Click Advanced / Proceed.
* Click Advanced
* Click Proceed
### API endpoints
Reach the API endpoints at:
```
https://34.210.153.255.xip.io/items/JSON
https://34.210.153.255.xip.io/item/<int:item_id>/JSON
https://34.210.153.255.xip.io/users/JSON
https://34.210.153.255.xip.io/categories/JSON
```
### Expected Output
* See the file Expected_Output.docx for screenshots
### Test Users
The application is live with Facebook, use any Facebook id to test.
