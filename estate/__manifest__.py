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
        'views/estate_property_type_view.xml',
        'views/estate_search.xml',
        'views/estate_menus.xml',
    ],
    'application': True,
    'installable': True,
}
