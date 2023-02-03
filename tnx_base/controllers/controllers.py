# -*- coding: utf-8 -*-
# from odoo import http


# class TnxBase(http.Controller):
#     @http.route('/tnx_base/tnx_base/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tnx_base/tnx_base/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tnx_base.listing', {
#             'root': '/tnx_base/tnx_base',
#             'objects': http.request.env['tnx_base.tnx_base'].search([]),
#         })

#     @http.route('/tnx_base/tnx_base/objects/<model("tnx_base.tnx_base"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tnx_base.object', {
#             'object': obj
#         })
