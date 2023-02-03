# -*- coding: utf-8 -*-
# from odoo import http


# class TnxProduction(http.Controller):
#     @http.route('/tnx_production/tnx_production/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tnx_production/tnx_production/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tnx_production.listing', {
#             'root': '/tnx_production/tnx_production',
#             'objects': http.request.env['tnx_production.tnx_production'].search([]),
#         })

#     @http.route('/tnx_production/tnx_production/objects/<model("tnx_production.tnx_production"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tnx_production.object', {
#             'object': obj
#         })
