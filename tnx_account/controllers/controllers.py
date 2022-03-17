# -*- coding: utf-8 -*-
# from odoo import http


# class TnxAccount(http.Controller):
#     @http.route('/tnx_account/tnx_account/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tnx_account/tnx_account/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tnx_account.listing', {
#             'root': '/tnx_account/tnx_account',
#             'objects': http.request.env['tnx_account.tnx_account'].search([]),
#         })

#     @http.route('/tnx_account/tnx_account/objects/<model("tnx_account.tnx_account"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tnx_account.object', {
#             'object': obj
#         })
