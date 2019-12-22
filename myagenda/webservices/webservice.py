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

# 2. Read the sessions
events = call('myagenda.event.student', 'search_read',
              [], ['name', 'typeEvent'])
for event in events:
    print("Event %s (%s type)" % (event['name'], event['typeEvent']))
