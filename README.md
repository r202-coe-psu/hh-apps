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
* Run inventory api module

~~~~
$ source hh-env
(hh-env)$ cd hh-apps
(hh-env)$ HHAPPS_INVENTORY_API_SETTINGS=$(pwd)/api-inventory-development.cfg hhapps-inventory-api -d
~~~~

* Note
 * `HHSERVICE_INVENTORY_API_SETTINGS` = an API setting file environent
 * `api-inventory-development.cfg` = an API setting file contains configurating variables.
 * `hhapps-inventory-api` = an API executable file

