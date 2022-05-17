from odoo import models, fields, api, _

class bookrent_detil(models.Model):  # inherit dari Model
    _name = 'library.bookrent_detil'  # attribut dari class Model (lihat dokumen odoo)
    _description = 'class for the detail book rent'

    bookrent_id = fields.Many2one('library.bookrent', string='Book Rent', ondelete="cascade")
    book_id = fields.Many2one('library.book', string='Book', ondelete="cascade")
    bookrent_price = fields.Integer("Rent Price", store=1, related='book_id.rentprice', default=0)

    _sql_constraints = [('bookrent_detil_unik', 'unique(book_id, bookrent_id)', _('The rent for the book already exist!'))]

