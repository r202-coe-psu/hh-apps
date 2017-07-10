# HHService

HHApps is a part of Home Hero projects. HHApps provides applications for smart living.

# Development

## HHService Repository

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
(hh-env)$ cd hh-service
(hh-env)$ HHAPPS_INVENTORY_SETTINGS=$(pwd)/inventory-development.cfg hhaoos-inventory -d
~~~~

* Note
 * `HHSERVICE_INVENTORY_SETTINGS` = an API setting file environent
 * `inventory-development.cfg` = an API setting file contains configurating variables.
 * `hhapps-inventory` = an API executable file

