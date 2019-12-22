import functools
import xmlrpc.client
HOST = 'localhost'
PORT = 8069
DB = 'agenda06'
USER = 'admin'
PASS = 'admin'
ROOT = 'http://%s:%d/xmlrpc/' % (HOST, PORT)

# 1. Login
uid = xmlrpc.client.ServerProxy(ROOT + 'common').login(DB, USER, PASS)
print("Logged in as %s (uid:%d)" % (USER, uid))

call = functools.partial(
    xmlrpc.client.ServerProxy(ROOT + 'object').execute,
    DB, uid, PASS)

# Get the user partner_id logged
user_id = call('res.users', 'search_read', [
               ('email', 'ilike', USER)])[0]
partner_id = (user_id['partner_id'][0])

# 3. Read the events student
events_student = call('myagenda.event.student', 'search_read',
                      [], ['name', 'typeEvent', 'attendees_ids'])
for event in events_student:
    if partner_id in event['attendees_ids']:
        print("Event %s (%s)" % (event['name'], event['typeEvent']))

# 4. Read the events pedagogic

events_pedagogic = call('myagenda.event.pedagogic', 'search_read',
                        [], ['name', 'typeEvent', 'attendees_ids'])
for event in events_pedagogic:
    if partner_id in event['attendees_ids']:
        print("Event %s (%s type)" % (event['name'], event['typeEvent']))

# 5. Read the events administrative

events_administrative = call('myagenda.event.administrative', 'search_read',
                             [], ['name', 'typeEvent', 'attendees_ids'])
for event in events_administrative:
    if partner_id in event['attendees_ids']:
        print("Event %s (%s type)" % (event['name'], event['typeEvent']))
