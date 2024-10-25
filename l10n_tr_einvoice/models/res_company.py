from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    l10n_tr_einvoice_username = fields.Char(
        string='E-Invoice Username',
        help='Username for e-Invoice integration'
    )
    l10n_tr_einvoice_password = fields.Char(
        string='E-Invoice Password',
        help='Password for e-Invoice integration'
    )
    l10n_tr_einvoice_test_mode = fields.Boolean(
        string='Test Mode',
        default=True,
        help='Enable test mode for e-Invoice integration'
    )
    l10n_tr_einvoice_alias = fields.Char(
        string='Company E-Invoice Alias',
        help='Company e-Invoice alias/identifier'
    )