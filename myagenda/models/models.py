# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from odoo import modules
import base64


def get_default_img(cat):
    if cat == "agenda":
        img = 'icon-agenda.jpg'
    else:
        img = 'icon-event.png'
    with open(modules.get_module_resource('myagenda', 'static/img', img),
              'rb') as f:
        return base64.b64encode(f.read())


class Agenda(models.Model):
    _name = 'myagenda.agenda'
    name = fields.Char(String="Name", required=True, size=30)
    description = fields.Char(String="Description")
    events_ids = fields.One2many(
        'myagenda.event', 'agenda_id', string='Events', ondelete='cascade',
        store=True
    )
    events_count = fields.Integer(String="Events on agenda",
                                  compute='_compute_event',
                                  store=True
                                  )
    attendees_ids = fields.Many2many(
        'res.partner',
        string='Attendees', ondelete='cascade',
        domain=['|', ('role', '=', "staff"),
                ('role', '=', "attendee")],
        store=True

    )

    attendees_count = fields.Integer(String="Number attendees",
                                     compute='_compute_attendees',
                                     store=True
                                     )

    image = fields.Binary("Image", attachment=True,
                          default=get_default_img("agenda"))

    color = fields.Integer()

    type_agenda = fields.Selection(string='Type', selection=[],
                                   required=True,
                                   readonly=True
                                   )

    @api.depends('events_ids')
    def _compute_event(self):
        for record in self:
            record.events_count = len(record.events_ids)

    @api.depends('attendees_ids')
    def _compute_attendees(self):
        for record in self:
            record.attendees_count = len(record.attendees_ids)

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', _(u"Copy of {}%").format(self.name))])
        if not copied_count:
            new_name = _(u"Copy of {}").format(self.name)
        else:
            new_name = _(u"Copy of {} ({})").format(self.name, copied_count)

        default['name'] = new_name
        return super(Agenda, self).copy(default)

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the agenda should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The agenda title must be unique"),
    ]


class AgendaStudent(models.Model):
    _inherit = 'myagenda.agenda'

    type_agenda = fields.Selection(
        selection_add=[('Agenda student', 'Agenda student')])


class AgendaPedagogic(models.Model):
    _inherit = 'myagenda.agenda'

    type_agenda = fields.Selection(
        selection_add=[('Agenda pedagogic', 'Agenda pedagogic')])


class AgendaAdministrative(models.Model):
    _inherit = 'myagenda.agenda'

    type_agenda = fields.Selection(
        selection_add=[('Agenda administrative', 'Agenda administrative')])


class Event(models.Model):
    _name = 'myagenda.event'

    name = fields.Char(String="Name", required=True, size=30)
    description = fields.Char(String="Description")
    agenda_id = fields.Many2one(
        'myagenda.agenda', String='Agenda', ondelete='cascade',
        required=True,
        store=True,
    )
    organizer_id = fields.Many2one(
        'res.partner', String='Organizer', ondelete='cascade', domain=[('role', '=', "staff")],
        required=True,
        store=True
    )
    typeEvent = fields.Selection(string='Type', selection=[(
        'Course', 'Course'), ('Interrogation', 'Interrogation'), ('Exam', 'Exam'), ('Sport event', 'Sport event'),
        ('Awards', 'Awards'), ('Competition',
                               'Competition'), ('Conference', 'Conference'),
        ('Meeting', 'Meeting'), ('Special', 'Special'), ('Presentation', 'Presentation'), ('Trip', 'Trip'), ('Party', 'Party'), ('Other', 'Other')],
        required=False
    )

    type_agenda = fields.Selection(
        [('Agenda administrative', 'Agenda administrative'), ('Agenda pedagogic', 'Agenda pedagogic'), ('Agenda student', 'Agenda student')], readonly=True, store=True)

    start_date = fields.Datetime(
        string='Date',
        required=True
    )

    duration = fields.Float(
        help="Duration of the event")

    location = fields.Char(
        string='Location',
        help='Location where the event takes place',
        required=True
    )

    periodicity = fields.Selection(string='Periodicity', selection=[(
        'Daily', 'Daily'), ('Weekly', 'Weekly'), ('Monthly', 'Monthly')],
        required=False
    )

    max_registration = fields.Integer(
        string='Max registration',
        help='Maximum registration for the event',
        required=False
    )

    attendees_ids = fields.Many2many(
        'res.partner',
        string='Attendees', ondelete='cascade',
        domain=['|', ('role', '=', "staff"),
                ('role', '=', "attendee")],
        store=True

    )

    attendees_count = fields.Integer(String="Number attendees",
                                     compute='_compute_attendees',
                                     store=True
                                     )

    taken_registration = fields.Float(
        string="Registration", compute='_taken_registration',
        store=True
    )

    image = fields.Binary("Image", attachment=True,
                          default=get_default_img("event"))

    color = fields.Integer()

    @api.depends('attendees_ids')
    def _compute_attendees(self):
        for record in self:
            record.attendees_count = len(record.attendees_ids)

    @api.depends('max_registration', 'attendees_ids')
    def _taken_registration(self):
        for record in self:
            if not record.max_registration:
                record.taken_registration = 0.0
            else:
                record.taken_registration = 100.0 * \
                    len(record.attendees_ids) / record.max_registration

    @api.onchange('max_registration', 'attendees_ids')
    def _verify_valid_register(self):
        if self.max_registration < 0:
            raise exceptions.ValidationError(
                _("Incorrect 'max registration' value. The number of available registration may not be negative"))
        if self.max_registration < len(self.attendees_ids):
            raise exceptions.ValidationError(
                _("Too many attendees. Increase max of registration or remove excess attendees"))

    @api.onchange('max_registration', 'attendees_ids')
    def _check_organizer_not_in_attendees(self):
        for r in self:
            if r.organizer_id and r.organizer_id in r.attendees_ids:
                raise exceptions.ValidationError(
                    _("A event's organizer can't be an attendee"))

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', _(u"Copy of {}%").format(self.name))])
        if not copied_count:
            new_name = _(u"Copy of {}").format(self.name)
        else:
            new_name = _(u"Copy of {} ({})").format(self.name, copied_count)

        default['name'] = new_name
        return super(Event, self).copy(default)

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the event should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The event title must be unique"),
    ]
