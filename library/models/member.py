from odoo import models, fields, api, _


# _ untuk translate

class member(models.Model):  # inherit dari Model
    _name = 'library.member'  # attribut dari class Model (lihat dokumen odoo)
    _description = 'class for member'
    # _rec_name = 'name'
    name = fields.Char('Member Name', size=40, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})  # index true krn field ini yang biasanya sering dicari
    ktp = fields.Char('KTP', size=60, required=True, index=True, readonly=True,
                           states={'draft': [('readonly', False)]})
    address = fields.Char('Address', size=60, required=True, index=True, readonly=True,
                      states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True,
                             default='draft')
    _sql_constraints = [('ktp_unik', 'unique(ktp)', _('KTP must be unique!'))]


