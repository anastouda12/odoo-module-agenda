from odoo.tests import common

class TestEventStudent(common.TransactionCase):
    def test_event_student(self):
        record = self.env['myagenda.event.student'].create({'name': 'Student event'})
        #record.some_action()
        self.assertEqual(record.name, "Student event")