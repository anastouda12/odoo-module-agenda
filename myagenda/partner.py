from odoo import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    role = fields.Selection(string='Role', selection=[(
        'staff', 'staff'), ('attendee', 'attendee')],
        default='attendee'
    )

    events_student_ids = fields.Many2many('myagenda.event.student',
                                          string="Events student", readonly=True)

    events_pedagogic_ids = fields.Many2many('myagenda.event.pedagogic',
                                            string="Events pedagogic", readonly=True)

    events_administrative_ids = fields.Many2many('myagenda.event.administrative',
                                                 string="Events administrative", readonly=True)

    agenda_student_ids = fields.Many2many(
        'myagenda.agenda.student',
        string='Agenda student',
        readonly=True
    )

    agenda_pedagogic_ids = fields.Many2many(
        'myagenda.agenda.pedagogic',
        string='Agenda pedagogic',
        readonly=True
    )

    agenda_administrative_ids = fields.Many2many(
        'myagenda.agenda.administrative',
        string='Agenda administrative',
        readonly=True
    )
