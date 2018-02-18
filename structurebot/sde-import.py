#!/usr/bin/env python
#
# Convert SDE invControlTowerResources into python python dict

import sqlite3
import pprint

pprinter = pprint.PrettyPrinter()

conn = sqlite3.connect('sqlite-latest.sqlite')
c = conn.cursor()


pos_fuel = {}
fuel_types = {}

pos_query = """select t.controlTowerTypeID, p.purposeText, t.resourceTypeID, \
i.typeName, i.volume, t.quantity \
from invControlTowerResources as t \
join invControlTowerResourcePurposes as p on t.purpose = p.purpose \
join invTypes as i on t.resourceTypeID = i.typeID
"""

# invControlTowerResources
for row in conn.execute(pos_query):
    (controlTowerTypeID, purpose, resourceTypeID, resourceTypeName, volume, quantity) = row
    tower_dict = pos_fuel.setdefault(controlTowerTypeID, {})
    if resourceTypeID not in fuel_types:
        fuel_types[resourceTypeID] = {'typeName': resourceTypeName, 'volume': volume}
    tower_dict[resourceTypeID] = quantity

moon_goo = {}

goo_query = 'select typeID, typeName, volume from invTypes where groupID = 427'

# invTypes
for row in conn.execute(goo_query):
    (typeID, typeName, volume) = row
    moon_goo[typeID] = {'typeName': typeName, 'volume': volume}


pos_mods = {}

mods_query = """select i.typeID, i.typeName, i.capacity, r.raceName, g.groupName \
                from invTypes as i \
                left join chrRaces as r on i.raceID=r.raceID \
                join invGroups as g on i.groupID=g.groupID \
                join invCategories as c on g.categoryID=c.categoryID \
                where c.categoryID = 23 and i.published=1"""

# invTypes
for row in conn.execute(mods_query):
    (typeID, typeName, capacity, raceName, groupName) = row
    pos_mods[typeID] = {'typeName': typeName,
                        'capacity': capacity,
                        'raceName': raceName,
                        'groupName': groupName}


with open('pos_resources.py', 'w') as resources:
    resources.write('pos_fuel = ' + pprinter.pformat(pos_fuel))
    resources.write('\n\n')
    resources.write('fuel_types = ' + pprinter.pformat(fuel_types))
    resources.write('\n\n')
    resources.write('moon_goo = ' + pprinter.pformat(moon_goo))
    resources.write('\n\n')
    resources.write('pos_mods = ' + pprint.pformat(pos_mods))
    resources.write('\n')
