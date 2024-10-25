from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    l10n_tr_einvoice_registered = fields.Boolean(
        string='E-Invoice Registered',
        help='Check if the partner is registered in the e-Invoice system'
    )
    l10n_tr_einvoice_alias = fields.Char(
        string='E-Invoice Alias',
        help='E-Invoice alias/identifier for the partner'
    )