from datetime import datetime, timedelta

from odoo import models, fields, api
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
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_start': self.date_start,
                'date_end': self.date_end,
            },
        }

        # use `module_name.report_id` as reference.
        # `report_action()` will call `get_report_values()` and pass `data` automatically.
        return self.env.ref('myagenda.event_report').report_action(self, data=data)


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
        events = self.env['myagenda.event'].search([])
        for event in events:
            if(event.start_date >= date_start and event.start_date <= date_end):

                docs.append({
                    'name': event.name,
                    'type': event.typeEvent,
                    'start_date': event.start_date,
                    'organizer': event.organizer_id.idnumber,
                    'agenda': event.agenda_id.name,
                    'location': event.location,





                })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': date_start,
            'date_end': date_end,
            'docs': docs,
        }


class AttendeesEventReportWizard(models.TransientModel):
    _name = 'myagenda.attendees_event.report.wizard'

    events_ids = fields.Many2one('myagenda.event',
                                 string='Event',
                                 required=True,
                                 )

    @api.multi
    def get_report(self):
        """Call when button 'Get Report' clicked.
        """
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'events_ids': self.events_ids.name,
            },
        }

        # use `module_name.report_id` as reference.
        # `report_action()` will call `get_report_values()` and pass `data` automatically.
        return self.env.ref('myagenda.attendees_event_report').report_action(self, data=data)


class ReportAgendaEvent(models.AbstractModel):
    """Abstract Model for report template.
    for `_name` model, please use `report.` as prefix then add `module_name.report_name`.
    """

    _name = 'report.myagenda.attendees_event_report_view'

    @api.model
    def get_report_values(self, docids, data=None):
        events_ids = data['form']['events_ids']

        docs = []
        events = self.env['myagenda.event'].search([])
        for event in events:
            if(event.name == events_ids):
                for attendee in event.attendees_ids:
                    docs.append({
                        'name': attendee.name,
                        'idnumber': attendee.idnumber,
                        'role': attendee.role,
                        'img': event.image,
                    })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'events_ids': events_ids,
            'docs': docs,
        }
