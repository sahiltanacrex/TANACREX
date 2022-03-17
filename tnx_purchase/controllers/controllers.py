# -*- coding: utf-8 -*-
# from odoo import http


# class TnxPurchase(http.Controller):
#     @http.route('/tnx_purchase/tnx_purchase/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tnx_purchase/tnx_purchase/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tnx_purchase.listing', {
#             'root': '/tnx_purchase/tnx_purchase',
#             'objects': http.request.env['tnx_purchase.tnx_purchase'].search([]),
#         })

#     @http.route('/tnx_purchase/tnx_purchase/objects/<model("tnx_purchase.tnx_purchase"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tnx_purchase.object', {
#             'object': obj
#         })
