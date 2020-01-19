from datetime import datetime
from getpass import getpass
import functools
import xmlrpc.client
HOST = 'localhost'
PORT = 8069
DB = 'agenda06'  # Here the name of the DB
USER = input("Username :")
PASS = getpass("Password :")
ROOT = 'http://%s:%d/xmlrpc/' % (HOST, PORT)

# 1. Login
uid = xmlrpc.client.ServerProxy(ROOT + 'common').login(DB, USER, PASS)
if(uid > 0):
    print("Logged in as %s (uid:%d)" % (USER, uid))
    date = datetime.now()
    today = date.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    print(today)


    call = functools.partial(
    xmlrpc.client.ServerProxy(ROOT + 'object').execute,
    DB, uid, PASS)

    # Get the user partner_id logged
    user_id = call('res.users', 'search_read', [
               ('email', 'ilike', USER)])[0]
    partner_id = (user_id['partner_id'][0])
    print(' ')
    print("# Events registered")
    print(' ')
    # 3. Read the events student
    events_student = call('myagenda.event.student', 'search_read',
                      [], ['name', 'typeEvent', 'attendees_ids', 'agenda_id', 'location', 'duration', 'start_date', 'organizer_id'])
    for event in events_student:
        if partner_id in event['attendees_ids']:
            if(event['start_date'] >= today):
                print("Event : %s | Agenda : %s | Type : %s | Organizer : %s | Date : %s | Duration : %s | Location : %s " %
                      (event['name'], event['agenda_id'][1], event['typeEvent'], event['organizer_id'][1], event['start_date'], event['duration'], event['location']))

    # 4. Read the events pedagogic

    events_pedagogic = call('myagenda.event.pedagogic', 'search_read',
                        [], ['name', 'typeEvent', 'attendees_ids', 'agenda_id', 'location', 'duration', 'start_date', 'organizer_id'])
    for event in events_pedagogic:
        if partner_id in event['attendees_ids']:
            if(event['start_date'] >= today):
                print("Event : %s | Agenda : %s | Type : %s | Organizer : %s | Date : %s | Duration : %s | Location : %s " %
                      (event['name'], event['agenda_id'][1], event['typeEvent'], event['organizer_id'][1], event['start_date'], event['duration'], event['location']))

    # 5. Read the events administrative

    events_administrative = call('myagenda.event.administrative', 'search_read',
                             [], ['name', 'typeEvent', 'attendees_ids', 'agenda_id', 'location', 'duration', 'start_date', 'organizer_id'])
    for event in events_administrative:
        if partner_id in event['attendees_ids']:
            if(event['start_date'] >= today):
                print("Event : %s | Agenda : %s | Type : %s | Organizer : %s | Date : %s | Duration : %s | Location : %s " %
                      (event['name'], event['agenda_id'][1], event['typeEvent'], event['organizer_id'][1], event['start_date'], event['duration'], event['location']))
    print(' ')
else:
    print("Login failed bad credentials !")
