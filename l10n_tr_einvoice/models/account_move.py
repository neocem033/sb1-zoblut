from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'

    l10n_tr_einvoice_status = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('error', 'Error')
    ], string='E-Invoice Status', default='draft', copy=False)
    
    l10n_tr_einvoice_type = fields.Selection([
        ('einvoice', 'E-Invoice'),
        ('earchive', 'E-Archive')
    ], string='Electronic Invoice Type', copy=False)
    
    l10n_tr_einvoice_number = fields.Char(
        string='Electronic Invoice Number',
        copy=False,
        readonly=True
    )

    def action_post(self):
        res = super().action_post()
        for move in self:
            if move.move_type in ('out_invoice', 'out_refund'):
                move._check_tr_einvoice_requirements()
        return res

    def _check_tr_einvoice_requirements(self):
        self.ensure_one()
        if not self.partner_id.vat:
            raise UserError(_('Partner VAT is required for e-Invoice/e-Archive.'))
        # Determine invoice type based on partner
        if self.partner_id.l10n_tr_einvoice_registered:
            self.l10n_tr_einvoice_type = 'einvoice'
        else:
            self.l10n_tr_einvoice_type = 'earchive'

    def action_send_einvoice(self):
        self.ensure_one()
        if self.l10n_tr_einvoice_status != 'draft':
            raise UserError(_('Invoice has already been processed.'))
        
        try:
            # Implementation for sending to GIB will go here
            self.l10n_tr_einvoice_status = 'sent'
        except Exception as e:
            self.l10n_tr_einvoice_status = 'error'
            _logger.error('Error sending e-invoice: %s', str(e))
            raise UserError(_('Failed to send electronic invoice: %s') % str(e))