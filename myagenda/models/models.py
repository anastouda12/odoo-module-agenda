# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from odoo import modules
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import base64


def get_default_img(cat):
    if cat == "agenda_student":
        img = 'icon-agenda_student.jpg'
    elif cat == "agenda_pedagogic":
        img = 'icon-agenda_pedagogic.jpg'
    elif cat == "agenda_administrative":
        img = 'icon-agenda_administrative.jpg'
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
                          default=get_default_img("agenda_student"))

    color = fields.Integer()

    type_agenda = fields.Char(
        string='Type',
        default="Agenda default",
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
    _name = 'myagenda.agenda.student'
    _inherit = 'myagenda.agenda'

    type_agenda = fields.Char(
        string='Type',
        default="Agenda student",
        readonly=True
    )
    events_ids = fields.One2many(
        'myagenda.event.student', 'agenda_id', string='Events', ondelete='cascade',
        store=True
    )
    image = fields.Binary("Image", attachment=True,
                          default=get_default_img("agenda_student"))


class AgendaPedagogic(models.Model):
    _name = 'myagenda.agenda.pedagogic'
    _inherit = 'myagenda.agenda'

    type_agenda = fields.Char(
        string='Type',
        default="Agenda pedagogic",
        readonly=True
    )
    events_ids = fields.One2many(
        'myagenda.event.pedagogic', 'agenda_id', string='Events', ondelete='cascade',
        store=True
    )
    image = fields.Binary("Image", attachment=True,
                          default=get_default_img("agenda_pedagogic"))


class AgendaAdministrative(models.Model):
    _name = 'myagenda.agenda.administrative'
    _inherit = 'myagenda.agenda'

    type_agenda = fields.Char(
        string='Type',
        default="Agenda administrative",
        readonly=True
    )
    events_ids = fields.One2many(
        'myagenda.event.administrative', 'agenda_id', string='Events', ondelete='cascade',
        store=True
    )
    image = fields.Binary("Image", attachment=True,
                          default=get_default_img("agenda_administrative"))


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

    type_agenda = fields.Char(string="Agenda default",
                              readonly=True, store=True)

    attachement = fields.Many2many(
        'ir.attachment',
        string='Attachment'
    )

    start_date = fields.Datetime(
        string='Date',
        required=True
    )

    end_date = fields.Datetime(string="End date")

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

    @api.onchange('attendees_ids')
    def _verify_valid_attendees(self):
        for record in self:
            for r in record.attendees_ids:
                if r and r not in record.agenda_id.attendees_ids:
                    raise exceptions.ValidationError(
                        _("Attendee not registered in the corresponding agenda"))

    @api.constrains('organizer_id')
    def _verify_valid_organizer(self):
        for r in self:
            if r.organizer_id and r.organizer_id not in r.agenda_id.attendees_ids:
                raise exceptions.ValidationError(
                    _("Organizer not registered in the corresponding agenda"))

    @api.constrains('end_date', 'periodicity')
    def _check_good_state(self):
        for r in self:
            if r.end_date and not r.periodicity or not r.end_date and r.periodicity:
                raise exceptions.ValidationError(
                    _("End date and periodicity work together"))

    @api.model
    def create(self, vals):
        new_record = super(Event, self).create(vals)
        if vals['periodicity']:
            DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
            date = datetime.strptime(vals['start_date'], DATETIME_FORMAT)
            end_date = datetime.strptime(vals['end_date'], DATETIME_FORMAT)
            vals['start_date'] = date
            vals['end_date'] = end_date
            if vals['periodicity'] == 'Weekly':
                while vals['start_date'] < vals['end_date']:
                    vals['start_date'] += relativedelta(days=+7)
                    record2 = super(Event, self).create(vals)
            if vals['periodicity'] == 'Monthly':
                while vals['start_date'] < vals['end_date']:
                    vals['start_date'] += relativedelta(months=+1)
                    record2 = super(Event, self).create(vals)
            if vals['periodicity'] == 'Daily':
                while vals['start_date'] < vals['end_date']:
                    vals['start_date'] += relativedelta(days=+1)
                    record2 = super(Event, self).create(vals)
        return new_record

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the event should not be the description"),
    ]


class eventStudent(models.Model):
    _name = 'myagenda.event.student'

    _inherit = 'myagenda.event'
    type_agenda = fields.Char(string="Agenda student",
                              readonly=True, store=True)
    agenda_id = fields.Many2one(
        'myagenda.agenda.student', String='Agenda', ondelete='cascade',
        required=True,
        store=True,
    )
    organizer_id = fields.Many2one(
        'res.partner', String='Organizer', ondelete='cascade', domain=[('role', '=', "attendee")], default=lambda self: self.env.user.partner_id,
        required=True,
        readonly=True,
        store=True
    )


class eventPedagogic(models.Model):
    _name = 'myagenda.event.pedagogic'

    _inherit = 'myagenda.event'
    type_agenda = fields.Char(
        string="Agenda pedagogic", readonly=True, store=True)
    agenda_id = fields.Many2one(
        'myagenda.agenda.pedagogic', String='Agenda', ondelete='cascade',
        required=True,
        store=True,
    )


class eventAdministrative(models.Model):
    _name = 'myagenda.event.administrative'

    _inherit = 'myagenda.event'
    type_agenda = fields.Char(
        string="Agenda administrative", readonly=True, store=True)
    agenda_id = fields.Many2one(
        'myagenda.agenda.administrative', String='Agenda', ondelete='cascade',
        required=True,
        store=True,
    )
