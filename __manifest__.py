{
    'name': 'GesMin',
    'version': '1.0',
    'summary': 'Gestión Minera con Inteligencia Artificial',
    'description': """
        Módulo para cargar archivos PDF y convertirlos a formato JSON
        utilizando un script Python externo.
    """,
    'author': 'GreenFields',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/pdf_views.xml',
        'views/wizard_views.xml',
        'views/menu.xml',
        'views/folder_views.xml',
        'controllers/main.xml',
    ],
    'external_dependencies': {
    'python': ['pymongo', 'pdf2image', 'pytesseract']
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}