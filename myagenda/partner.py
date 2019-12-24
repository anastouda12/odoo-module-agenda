from odoo import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    role = fields.Selection(string='Role', selection=[(
        'staff', 'staff'), ('attendee', 'attendee')],
        default='attendee'
    )

    events_ids = fields.Many2many('myagenda.event',
                                  string="Events", readonly=True)
    agenda_ids = fields.Many2many(
        'myagenda.agenda',
        string='Agenda',
        readonly=True
    )
