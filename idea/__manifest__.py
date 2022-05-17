{
    'name': 'Idea',  # nama modul yg dibaca user di UI
    'version': '1.0',
    'author': 'Yulia',
    'summary': 'Modul Idea SIB UK Petra',  # deskripsi singkat dari modul
    'description': 'Ideas management module',  # bisa nampilkan gambar/ deskripsi dalam bentuk html. html diletakkan
    # di idea/static/description, bisa kasi icon modul juga.
    'category': 'Latihan',
    'website': 'http://sib.petra.ac.id',
<<<<<<< HEAD
    'depends': ['base', 'sales_team'],  # list test of dependencies, conditioning startup order
=======
    'depends': ['base', 'sales_team'],  # list of dependencies, conditioning startup order
>>>>>>> b56841da477bc65957393939451ab777d44a1643
    'data': [
        'security/ir.model.access.csv',
        'views/idea_views.xml',
        'views/voting_views.xml',
        'data/ir_sequence_data.xml',

    ],
    'qweb': [],  # untuk memberi tahu static file, misal CSS
    'demo': [],  # demo data (for unit tests)
    'installable': True,
    'auto_install': False,  # indikasi install, saat buat database baru
}
