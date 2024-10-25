{
    'name': 'Turkey - E-Invoice and E-Archive',
    'version': '18.0.1.0.0',
    'category': 'Localization',
    'summary': 'Turkey E-Invoice and E-Archive Integration',
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'depends': [
        'account',
        'l10n_tr',
        'base_vat',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_company_views.xml',
        'views/res_config_settings_views.xml',
        'views/account_move_views.xml',
        'data/einvoice_types.xml',
    ],
    'installable': True,
    'auto_install': False,
}