from odoo import models, fields, api, exceptions, _


class Wizard(models.TransientModel):
    _name = 'myagenda.wizard'

    def _get_partner(self):
        return self.env.user.partner_id

    user_id = fields.Many2one('res.partner', default=_get_partner,
                              readonly=True,
                              string='You'
                              )

    @api.multi
    def subscribe(self):
        model = self.env.context.get('active_model')
        model_id = self.env[model].browse(self._context.get('active_id'))
        if model == 'myagenda.event.student' or model == 'myagenda.event.pedagogic' or model == 'myagenda.event.administrative':
            if self.env.user.partner_id not in model_id.agenda_id.attendees_ids:
                raise exceptions.ValidationError(
                    _("You are not registered in the corresponding agenda !"))
                return {}
            elif self.env.user.partner_id in model_id.agenda_id.attendees_ids:
                model_id.attendees_ids |= self.env.user.partner_id
                return {}
        else:
            model_id.attendees_ids |= self.env.user.partner_id
            return {}

    @api.multi
    def unsubscribe(self):
        model = self.env.context.get('active_model')
        model_id = self.env[model].browse(self._context.get('active_id'))
        partner = self.env.user.partner_id
        model_id.attendees_ids = [(2, partner.id)]
        return {}
