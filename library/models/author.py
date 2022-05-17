from odoo import models, fields, api, _


# _ untuk translate

class author(models.Model):  # inherit dari Model
    _name = 'library.author'  # attribut dari class Model (lihat dokumen odoo)
    _description = 'class for author data'
    _rec_name = 'name'

    name = fields.Char(string="author", size=64, required=True, index=True)
    active = fields.Boolean('Active', default=True)
    _sql_constraints = [('author_unik', 'unique(author)', _('The author already exist!'))]


