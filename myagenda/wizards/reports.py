from datetime import datetime, timedelta

from odoo import models, fields, api, exceptions, _

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class AgendaEventReportWizard(models.TransientModel):
    _name = 'myagenda.event.report.wizard'

    date_start = fields.Date(
        string="Start Date", required=True, default=fields.Date.today)
    date_end = fields.Date(
        string="End Date", required=True, default=fields.Date.today)

    @api.multi
    def get_report(self):
        """Call when button 'Get Report' clicked.
        """
        model = self.env.context.get('active_model')
        model_id = self.env[model].browse(self._context.get('active_id'))
        if self.env.user.partner_id == model_id.organizer_id:
            data = {
                'ids': self.ids,
                'model': self._name,
                'form': {
                    'date_start': self.date_start,
                    'date_end': self.date_end,
                },
            }
            return self.env.ref('myagenda.event_report').report_action(self, data=data)
        else:
            raise exceptions.ValidationError(
                _("Action limited to the organizer : %s") % model_id.organizer_id.name)


class ReportAgendaEvent(models.AbstractModel):
    """Abstract Model for report template.
    for `_name` model, please use `report.` as prefix then add `module_name.report_name`.
    """

    _name = 'report.myagenda.event_report_view'

    @api.model
    def get_report_values(self, docids, data=None):
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        date_start_obj = datetime.strptime(date_start, DATE_FORMAT)
        date_end_obj = datetime.strptime(date_end, DATE_FORMAT)

        docs = []

        model = self.env.context.get('active_model')
        agenda = self.env[model].browse(self._context.get('active_id'))
        events = agenda.events_ids

        for event in events:
            if(event.start_date >= date_start and event.start_date <= date_end):

                docs.append({
                    'name': event.name,
                    'type': event.typeEvent,
                    'start_date': event.start_date,
                    'location': event.location,
                })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': date_start,
            'date_end': date_end,
            'agenda': agenda.name,
            'docs': docs,
        }
