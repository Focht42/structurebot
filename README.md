# EVE Online Structure Checker

Structure bot will check your EVE Online POS and Citadels for fuel, mining silos, offline services, reinforcement, 
etc. and push a notification to Slack.

It uses the ESI proxy from [Neucore](https://github.com/tkhamez/neucore).

## Configuration

**Prerequisites**

* Configure Neucore with an EVE Login with the following scopes and roles:
    ```
    esi-calendar.read_calendar_events.v1
    esi-universe.read_structures.v1
    esi-corporations.read_structures.v1
    esi-assets.read_corporation_assets.v1
    esi-corporations.read_starbases.v1
    esi-industry.read_corporation_mining.v1
   
    Station_Manager
    Director
    Accountant
    ```
* Add a Neucore app with the `app-esi` role and access to the EVE login from step 1.

### Environment Variables

The following config items need to be defined in the environment:

**Neucore Configuration**

* NEUCORE_HOST  
  The Neucore domain, e.g. `account.bravecollective.com`.
* NEUCORE_APP_TOKEN  
  The base64 encoded "Id:Secret" of the app.
* NEUCORE_DATASOURCE  
  The datasource parameter for Neucore ESI requests, e.g. `96061222:structures` (character ID:Login name), see also 
https://account.bravecollective.com/api.html#/Application%20-%20ESI/esiV2.

**Slack Configuration**

* OUTBOUND_WEBHOOK  
  Your Slack administrator will need to create an [Incoming Webhook for an application](https://api.slack.com/apps)
  with the bot token scope `chat:write` for you to use to send messages to Slack.

**EVE Configuration**

* CORPORATION_NAME  
  The name of the corp which owns the structures. Must match the character used in NEUCORE_DATASOURCE.
* TOO_SOON  
  How many days in advance you'd like to receive fuel or silo warnings
* STRONT_HOURS  
  The minimum number of hours worth of stront you'd like your POS to have
* DETONATION_WARNING  
  How many days in advance to notify about scheduled detonations
* JUMPGATE_FUEL_WARN  
  The minimum amount of liquid ozone in Ansiblex before a notification
* IGNORE_POS  
  Set to True to ignore POSes. 

**Other Configuration**

* ESI_CACHE  
  Can be used for EsiPY, e.g. diskcache:/path/to/cache
* DEBUG
  Print debug information.
* USER_AGENT
  Change the user agent used for ESI requests.

## Run

Runs with Python 3.8 and 3.9

### Dev Env

```sh
# Install Python versions if necessary
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt-get update
$ sudo apt-get install python3.8 python3.8-venv python3.9 python3.9-venv

# Init, for 3.8
$ python3.8 -m venv .venv8
$ source .venv8/bin/activate
$ pip install pipenv
$ pipenv install --dev
$ deactivate

# Run
$ source .venv8/bin/activate
$ source ./.env
$ pytest
$ python structurebot.py [-d]
$ python structure-audit.py [-d] [--csv]
$ deactivate
```
