from odoo import models, fields, api, _


# _ untuk translate

class khs(models.Model):  # inherit dari Model
    _name = 'nilai.khs'  # attribut dari class Model (lihat dokumen odoo)
    _description = 'class untuk menyimpan data KHS'
    _rec_name = 'name'

    name = fields.Char(compute="_compute_name", store=True, recursive=True)
    semester = fields.Selection([('Genap', 'Genap'),
                                 ('Gasal', 'Gasal')], 'Semester', required=True, readonly=True,
                                default='Genap', states={'draft': [('readonly', False)]}, )
    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Approved'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True,
                             default='draft')
    ips = fields.Float("IPS", compute="_compute_ips", store=True, default=0)
    tahun = fields.Char("Tahun", size=15, default="2021/2022", required=True, readonly=True,
                          states={'draft': [('readonly', False)]})

    mhs_id = fields.Many2one('nilai.mahasiswa', string='Mahasiswa', readonly=True, ondelete="cascade",
                             states={'draft': [('readonly', False)]},
                             domain="[('state', '=', 'done')]")
    nilai_mhs_ids = fields.One2many('nilai.nilai_mhs', 'khs_id', string='Nilai mhs', readonly=True,
                             states={'draft': [('readonly', False)]})
    _sql_constraints = [('name_unik', 'unique(mhs_id, semester, tahun)', _('The KHS already exist!'))]

    @api.depends( "nilai_mhs_ids", "nilai_mhs_ids.mk_id", "nilai_mhs_ids.grade", "state")
    def _compute_ips(self):
        self.ips=0
        total_sks=0
        for nilai_mhs1 in self.nilai_mhs_ids:
            self.ips+=nilai_mhs1.subtotal
            total_sks+=nilai_mhs1.mk_sks
        if(total_sks==0):
            self.ips=0
        else:
            self.ips=self.ips/total_sks

    def action_done(self):
        self.state = 'done'


    def action_canceled(self):
        self.state = 'canceled'


    def action_settodraft(self):
        self.state = 'draft'

    @api.depends('mhs_id.name', 'semester', 'tahun')
    def _compute_name(self):
        for s in self:
            s.name = "%s - %s - %s" % (s.mhs_id.name, s.semester, s.tahun)

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = list(args or [])
        # optimize out the default criterion of ``ilike ''`` that matches everything
        if not (name == '' and operator == 'ilike'):
            args += [(self._rec_name, operator, name)]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)
