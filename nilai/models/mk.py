from odoo import models, fields, api, _


# _ untuk translate

class mk(models.Model):  # inherit dari Model
    _name = 'nilai.mk'  # attribut dari class Model (lihat dokumen odoo)
    _description = 'class untuk menyimpan data mata kuliah'
    # _rec_name = 'name'
    name = fields.Char('Nama MK', size=10, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})  # index true krn field ini yang biasanya sering dicari
    code = fields.Char('Kode MK', size=60, required=True, index=True, readonly=True,
                           states={'draft': [('readonly', False)]})
    credit = fields.Integer('SKS', required=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True,
                             default='draft')
    active = fields.Boolean('Active', default=True, readonly=True, states={'draft': [('readonly', False)]})


    _sql_constraints = [('kode_unik', 'unique(code)', _('Course ID must be unique!'))]

    # @api.depends("voting_ids", "voting_ids.vote", "voting_ids.state")
    def _compute_vote(self):
        pass

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'
