from odoo import models, fields, api, _


# _ untuk translate

class publisher(models.Model):  # inherit dari Model
    _name = 'library.publisher'  # attribut dari class Model (lihat dokumen odoo)
    _description = 'class for publisher data'
    _rec_name = 'name'

    name = fields.Char(string="Publisher", size=64, required=True, index=True)
    active = fields.Boolean('Active', default=True)
    _sql_constraints = [('publisher_unik', 'unique(publisher)', _('The publisher already exist!'))]


