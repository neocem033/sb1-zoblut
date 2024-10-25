from odoo import models, fields, api, _
from odoo.exceptions import UserError
import docker
import logging
import random
import string

_logger = logging.getLogger(__name__)

class HostingInstance(models.Model):
    _name = 'hosting.instance'
    _description = 'Odoo Hosting Instance'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Instance Name', required=True, copy=False)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('stopped', 'Stopped'),
        ('error', 'Error')
    ], default='draft', string='Status', tracking=True)
    
    container_id = fields.Char(string='Docker Container ID', readonly=True)
    port = fields.Integer(string='Port', readonly=True)
    url = fields.Char(string='Instance URL', compute='_compute_url')
    db_name = fields.Char(string='Database Name', readonly=True)
    admin_password = fields.Char(string='Admin Password', readonly=True)
    
    @api.model
    def _get_available_port(self):
        """Get an available port between 8069 and 8099"""
        used_ports = self.search([]).mapped('port')
        for port in range(8069, 8100):
            if port not in used_ports:
                return port
        raise UserError(_('No available ports found'))

    def _generate_random_string(self, length=12):
        """Generate a random string for passwords and database names"""
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    @api.depends('port')
    def _compute_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for instance in self:
            if instance.port:
                instance.url = f"http://{base_url}:{instance.port}"
            else:
                instance.url = False

    def action_deploy(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Instance can only be deployed from draft state'))

        try:
            client = docker.from_env()
            
            # Generate unique names and passwords
            self.db_name = f"db_{self._generate_random_string(8)}"
            self.admin_password = self._generate_random_string()
            self.port = self._get_available_port()

            # Create and start the container
            container = client.containers.run(
                'odoo:18',
                detach=True,
                environment={
                    'HOST': 'db',
                    'PORT': '5432',
                    'USER': 'odoo',
                    'PASSWORD': self.admin_password,
                },
                ports={f'8069/tcp': self.port},
                name=f"odoo_{self.name}_{self.id}"
            )
            
            self.container_id = container.id
            self.state = 'running'
            
            # Send email to customer
            template = self.env.ref('l10n_tr_hosting.email_template_instance_ready')
            template.send_mail(self.id, force_send=True)
            
        except Exception as e:
            self.state = 'error'
            _logger.error('Error deploying Odoo instance: %s', str(e))
            raise UserError(_('Failed to deploy Odoo instance: %s') % str(e))

    def action_stop(self):
        self.ensure_one()
        if self.state != 'running':
            raise UserError(_('Can only stop running instances'))

        try:
            client = docker.from_env()
            container = client.containers.get(self.container_id)
            container.stop()
            self.state = 'stopped'
        except Exception as e:
            _logger.error('Error stopping container: %s', str(e))
            raise UserError(_('Failed to stop container: %s') % str(e))

    def action_start(self):
        self.ensure_one()
        if self.state != 'stopped':
            raise UserError(_('Can only start stopped instances'))

        try:
            client = docker.from_env()
            container = client.containers.get(self.container_id)
            container.start()
            self.state = 'running'
        except Exception as e:
            _logger.error('Error starting container: %s', str(e))
            raise UserError(_('Failed to start container: %s') % str(e))