from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        
        # Check if order contains hosting product
        hosting_product = self.env['product.product'].search([
            ('is_hosting_product', '=', True)
        ], limit=1)
        
        if hosting_product and hosting_product.id in self.order_line.mapped('product_id').ids:
            # Create hosting instance
            self.env['hosting.instance'].create({
                'name': f'instance-{self.name}',
                'partner_id': self.partner_id.id,
                'state': 'draft'
            }).action_deploy()
        
        return res