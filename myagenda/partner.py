from odoo import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    role = fields.Selection(string='Role', selection=[(
        'staff', 'staff'), ('attendee', 'attendee')],
        default='attendee'
    )

    idnumber = fields.Char(string='ID',
                           required=True, default=lambda self: self.env['ir.sequence'].next_by_code('increment_idnumber')
                           )
    events_ids = fields.Many2many('myagenda.event',
                                  string="Events", readonly=True)
    agenda_ids = fields.Many2many(
        'myagenda.agenda',
        string='Agenda',
        readonly=True
    )

    _sql_constraints = [
        ('idnumber_unique',
         'UNIQUE(idnumber)',
         "The ID-number must be unique"),
    ]
