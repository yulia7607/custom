from odoo import models, fields, api, _


# _ untuk translate

class book(models.Model):  # inherit dari Model
    _name = 'library.book'  # attribut dari class Model (lihat dokumen odoo)
    _description = 'Book Data'

    name = fields.Char(string="Book Title", size=64, required=True, index=True)
    isbn = fields.Char(string="ISBN", size=10, required=True)
    page = fields.Integer(string="Num of page")
    active = fields.Boolean('Active', default=True)
    rentprice = fields.Integer(string="Rent Price", default=0)
    cover=fields.Binary ("Cover", filters='*.png,*.gif')
    publisher_id = fields.Many2one('library.publisher', string='Publisher')
    author_id = fields.Many2one('res.partner', string='Author', ondelete="cascade")

    _sql_constraints = [('isbn_unik', 'unique(isbn)', _('The ISBN already exist!'))]
