# -*- coding: utf-8 -*-

{
    'name': 'Mora cliente',
    'version': '1.0',
    'category': 'Hidden',
    'sequence': 6,
    'summary': 'Cálculo de mora por cliente',
    'description': """

""",
    'author': "STechnologies",
    'depends': ['base','account','account_followup'],
    'data': [
        'views/account_followup_views.xml',
        'views/mora_cliente_views.xml',
        'views/res_partner_views.xml',
    ],
    'assets':{},
    'installable': True,
    'auto_install': False,
}
