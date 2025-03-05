{
    'name': 'Real Estate',
    'version': '1.0',
    'summary': 'Manage Real Estate Properties',
    'description': 'Module to manage real estate properties including details like pricing, availability, and features.',
    'author': 'Your Name',
    'website': 'https://www.example.com',
    'category': 'Real Estate',
    'sequence': -100,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
    ],
    'application': True,
    'installable': True,
}
