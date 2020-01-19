from odoo.tests import common

class TestAgendaStudent(common.TransactionCase):
    def test_agenda_student_without_event_and_attendee(self):
        record = self.env['myagenda.agenda.student'].create({'name': 'Student agenda',
        'description' : 'This is a student agenda', 'event_ids' : null, 'events_count' : 0,
        'attendees_ids' : null, 'attendees_count' : 0, 'color' : null,
        'type_agenda' : 'Agenda default', 'organizer_id' : null})
        record.get_default_img("agenda_student")
        record.compute_rules_edit()
        self.assertEqual(record.name, "Student agenda")
        self.assertEqual(record.description, "This is a student agenda")
        self.assertEqual(record.event_ids, null)
        self.assertEqual(record.events_count, 0)