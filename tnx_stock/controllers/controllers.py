# -*- coding: utf-8 -*-
# from odoo import http


# class TnxStock(http.Controller):
#     @http.route('/tnx_stock/tnx_stock/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tnx_stock/tnx_stock/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tnx_stock.listing', {
#             'root': '/tnx_stock/tnx_stock',
#             'objects': http.request.env['tnx_stock.tnx_stock'].search([]),
#         })

#     @http.route('/tnx_stock/tnx_stock/objects/<model("tnx_stock.tnx_stock"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tnx_stock.object', {
#             'object': obj
#         })
