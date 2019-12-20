# -*- coding: utf-8 -*-
{
    'name': "Agenda Esi",

    'summary': """
        Organize Events, trainings, schedule, specials event and more
        """,

    'description': """
        Agenda ESI allows you to
        manage events in the agenda.
        These events include courses taken, questions, project submissions, meetings and other activities organized
        """,

    'author': "HE2B-ESI",
    'website': "http://esi-bru.be",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Events',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/resources.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/myagenda.xml',
        'views/partner.xml',
        'reports/reports.xml',
        'wizards/reports.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

}
