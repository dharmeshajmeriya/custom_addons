{
    'name': 'Real Estate ',
    'summary': 'Real Estate site',
    'sequence':10,
    'version': '14.0.1.0.0',
    'description': '---Real Estate Software---',

    'website': 'https://www.cybrosys.com',
    'category': 'Productivity',
    'depends': ['base','mail','sale'],
    'license': 'AGPL-3',
    'data': [
    'security/ir.model.access.csv',
        'views/building.xml'
    ],
    'demo': [],
    'installable': True,
    'application':True,
    'auto_install': False,
}