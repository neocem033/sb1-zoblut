{
    'name': 'Odoo Hosting Automation',
    'version': '18.0.1.0.0',
    'category': 'Website',
    'summary': 'Automatic Odoo hosting deployment with Docker',
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'depends': [
        'website_sale',
        'base',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hosting_instance_views.xml',
        'views/res_config_settings_views.xml',
        'views/sale_order_views.xml',
        'data/hosting_cron.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}