{
    'name': 'Library',  # nama modul yg dibaca user di UI
    'version': '1.0',
    'author': 'Yulia',
    'summary': 'Modul Library',  # deskripsi singkat dari modul
    'description': 'Library Module',  # bisa nampilkan gambar/ deskripsi dalam bentuk html. html diletakkan
    # di idea/static/description, bisa kasi icon modul juga.
    'category': 'Latihan',
    'website': 'http://sib.petra.ac.id',
    'depends': ['base'],  # list of dependencies, conditioning startup order
    'data': [
        'security/ir.model.access.csv',
        'views/book_views.xml',
        'views/publisher_views.xml',
        'views/bookrent_views.xml',
        # 'views/nilai_mhs_views.xml',
    ],
    'qweb': [],  # untuk memberi tahu static file, misal CSS
    'demo': [],  # demo data (for unit tests)
    'installable': True,
    'auto_install': False,  # indikasi install, saat buat database baru
}
