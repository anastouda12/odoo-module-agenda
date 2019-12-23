from odoo.tests import common


class TestAgendaStudent(common.TransactionCase):
    def test_some_action(self):
        record = self.env['myagenda.agenda.student'].create(
            {'name': 'Student agenda'})

        # Todo for each model
