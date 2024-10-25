from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_hosting_product = fields.Boolean(
        string='Is Hosting Product',
        help='Check if this product should trigger Odoo hosting deployment'
    )