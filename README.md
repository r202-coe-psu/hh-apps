# HHApps

HHApps is a part of Home Hero projects. HHApps provides applications for smart living.

# Development

## HHApps Repository

 * Clone repository

~~~~
$ git clone git@138.47.200.245:HomeHero-Projects/hh-apps.git
~~~~

* Create Python virtual environment

~~~~
$ pyvenv hh-env
$ source hh-env
(hh-env)$ cd hh-apps
(hh-env)$ python setup.py develop
~~~~

* Install `hhclient` for web module
 * Clone repository
~~~~
git clone git@138.47.200.245:HomeHero-Projects/python-hhclient.git
~~~~
 * install `hhclient` in testing environment
~~~~
$ source hh-env
(hh-env)$ cd python-hhclient
(hh-env)$ python setup.py develop
~~~~

### API app module
* Create stock api configuration file name `api-stock-development.cfg`
~~~~
# secret_key same value as HHService API
SECRET_KEY = '722661a83fab23164071e17a888de24c25db80b42fde'

# Database
MONGODB_DB = 'homehero-stock'
~~~~

* Run inventory api module

~~~~
$ source hh-env
(hh-env)$ cd hh-apps
(hh-env)$ HHAPPS_STOCK_API_SETTINGS=$(pwd)/api-stock-development.cfg hhapps-stock-api -d
~~~~

* Note
 * `HHAPPS_STOCK_API_SETTINGS` = an API setting file environent
 * `api-stock-development.cfg` = an API setting file contains configurating variables.
 * `hhapps-stock-api` = an API executable file

