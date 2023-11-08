# -*- coding: utf-8 -*-
# from odoo import http


# class TnxContact(http.Controller):
#     @http.route('/tnx_contact/tnx_contact/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tnx_contact/tnx_contact/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tnx_contact.listing', {
#             'root': '/tnx_contact/tnx_contact',
#             'objects': http.request.env['tnx_contact.tnx_contact'].search([]),
#         })

#     @http.route('/tnx_contact/tnx_contact/objects/<model("tnx_contact.tnx_contact"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tnx_contact.object', {
#             'object': obj
#         })
