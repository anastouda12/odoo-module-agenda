# -*- coding: utf-8 -*-
from odoo import http

# class Myagenda(http.Controller):
#     @http.route('/myagenda/myagenda/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/myagenda/myagenda/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('myagenda.listing', {
#             'root': '/myagenda/myagenda',
#             'objects': http.request.env['myagenda.myagenda'].search([]),
#         })

#     @http.route('/myagenda/myagenda/objects/<model("myagenda.myagenda"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('myagenda.object', {
#             'object': obj
#         })