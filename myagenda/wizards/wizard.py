from odoo import models, fields, api, exceptions, _


class Wizard(models.TransientModel):
    _name = 'myagenda.wizard'

    def _get_partner(self):
        return self.env.user.partner_id

    user_id = fields.Many2one('res.partner', default=_get_partner,
                              readonly=True,
                              string='User'
                              )

    @api.multi
    def subscribe(self):
        if self.env.user.partner_id in self.event_id.agenda_id.attendees_ids:
            self.event_id.attendees_ids |= self.env.user.partner_id
            return {}
        else:
            raise exceptions.ValidationError(
                _("You are not registered in the corresponding agenda !)"))
            return {}

    @api.multi
    def unsubscribe(self):
        partner = self.env.user.partner_id
        self.event_id.attendees_ids = [(2, partner.id)]
        return {}


class WizardEventStudent(models.TransientModel):
    _name = 'myagenda.event.student.wizard'
    _inherit = "myagenda.wizard"

    def _default_event(self):
        return self.env['myagenda.event.student'].browse(self._context.get('active_id'))

    event_id = fields.Many2one('myagenda.event.student',
                               string="Event", required=True, default=_default_event,
                               readonly=True
                               )


class WizardEventPedagogic(models.TransientModel):
    _name = 'myagenda.event.pedagogic.wizard'
    _inherit = "myagenda.wizard"

    def _default_event(self):
        return self.env['myagenda.event.pedagogic'].browse(self._context.get('active_id'))

    event_id = fields.Many2one('myagenda.event.pedagogic',
                               string="Event", required=True, default=_default_event,
                               readonly=True
                               )


class WizardEventAdministrative(models.TransientModel):
    _name = 'myagenda.event.administrative.wizard'
    _inherit = "myagenda.wizard"

    def _default_event(self):
        return self.env['myagenda.event.administrative'].browse(self._context.get('active_id'))

    event_id = fields.Many2one('myagenda.event.administrative',
                               string="Event", required=True, default=_default_event,
                               readonly=True
                               )


class WizardAgendaStudent(models.TransientModel):
    _name = 'myagenda.agenda.student.wizard'
    _inherit = "myagenda.wizard"

    def _default_event(self):
        return self.env['myagenda.agenda.student'].browse(self._context.get('active_id'))

    agenda_id = fields.Many2one('myagenda.agenda.student',
                                string="Agenda", required=True, default=_default_event,
                                readonly=True
                                )

    @api.multi
    def subscribe(self):
        self.agenda_id.attendees_ids |= self.env.user.partner_id
        return {}

    @api.multi
    def unsubscribe(self):
        partner = self.env.user.partner_id
        self.agenda_id.attendees_ids = [(2, partner.id)]
        return {}


class WizardAgendaPedagogic(models.TransientModel):
    _name = 'myagenda.agenda.pedagogic.wizard'
    _inherit = "myagenda.wizard"

    def _default_event(self):
        return self.env['myagenda.agenda.pedagogic'].browse(self._context.get('active_id'))

    agenda_id = fields.Many2one('myagenda.agenda.pedagogic',
                                string="Agenda", required=True, default=_default_event,
                                readonly=True
                                )

    @api.multi
    def subscribe(self):
        self.agenda_id.attendees_ids |= self.env.user.partner_id
        return {}

    @api.multi
    def unsubscribe(self):
        partner = self.env.user.partner_id
        self.agenda_id.attendees_ids = [(2, partner.id)]
        return {}


class WizardAgendaPedagogic(models.TransientModel):
    _name = 'myagenda.agenda.administrative.wizard'
    _inherit = "myagenda.wizard"

    def _default_event(self):
        return self.env['myagenda.agenda.administrative'].browse(self._context.get('active_id'))

    agenda_id = fields.Many2one('myagenda.agenda.administrative',
                                string="Agenda", required=True, default=_default_event,
                                readonly=True
                                )

    @api.multi
    def subscribe(self):
        self.agenda_id.attendees_ids |= self.env.user.partner_id
        return {}

    @api.multi
    def unsubscribe(self):
        partner = self.env.user.partner_id
        self.agenda_id.attendees_ids = [(2, partner.id)]
        return {}
