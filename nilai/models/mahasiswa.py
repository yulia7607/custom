from odoo import models, fields, api, _


# _ untuk translate

class mahasiswa(models.Model):  # inherit dari Model
    _name = 'nilai.mahasiswa'  # attribut dari class Model (lihat dokumen odoo)
    _description = 'class untuk menyimpan data mahasiswa'
    # _rec_name = 'name'
    name = fields.Char('Nrp', size=10, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})  # index true krn field ini yang biasanya sering dicari
    mhs_name = fields.Char('Nama Mahasiswa', size=60, required=True, index=True, readonly=True,
                           states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True,
                             default='draft')
    mhs_state = fields.Selection([('aktif', 'Aktif'),
                                  ('cuti', 'Cuti'),
                                  ('do', 'DO'),
                                  ('lulus', 'Lulus')], 'Status', required=True, readonly=True,
                           states={'draft': [('readonly', False)]}, default='aktif')
    IPK = fields.Float("IPK", compute="_compute_ipk", store=True, default=0)
    # khs_ids = fields.One2many('nilai.khs', 'khs_id', string='KHS')
    _sql_constraints = [('nrp_unik', 'unique(name)', _('NRP must be unique!'))]

    # @api.depends("voting_ids", "voting_ids.vote", "voting_ids.state")
    def _compute_ipk(self):
        pass

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'
