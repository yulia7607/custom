from odoo import models, fields, api, _


# _ untuk translate

class nilai_mhs(models.Model):  # inherit dari Model
    _name = 'nilai.nilai_mhs'  # attribut dari class Model (lihat dokumen odoo)
    _description = 'class untuk menyimpan data nilai mahasiswa 1 semester'

    # state = fields.Selection([('draft', 'Draft'),
    #                           ('done', 'Done'),
    #                           ('canceled', 'Canceled')], 'State', required=True, readonly=True,
    #                          default='draft')
    subtotal = fields.Float("Total", compute="_compute_subtotal", store=True, default=0)

    khs_id = fields.Many2one('nilai.khs', string='KHS', ondelete="cascade")
    mk_id = fields.Many2one('nilai.mk', string='MK', ondelete="cascade")
    mk_sks = fields.Integer("SKS MK", related='mk_id.credit', store=1)
    grade = fields.Selection([('A', 'A'),
                              ('B+', 'B+'),
                              ('B', 'B'),
                              ('C+', 'C+'),
                              ('C', 'C'),
                              ('D', 'D'),
                              ('E', 'E')])
    _sql_constraints = [('name_unik', 'unique(khs_id, mk_id)', _('Grade for the course already exist!'))]

    @api.depends("khs_id", "mk_id", "mk_sks", 'grade')
    def _compute_subtotal(self):
        for s in self:
            if (s.grade == 'A'):
                s.subtotal = 4 * s.mk_sks
            elif (s.grade == "B+"):
                s.subtotal = 3.5 * s.mk_sks
            elif (s.grade == "B"):
                s.subtotal = 3 * s.mk_sks
            elif (s.grade == "C+"):
                s.subtotal = 2.5 * s.mk_sks
            elif (s.grade == "C"):
                s.subtotal = 2 * s.mk_sks
            elif (s.grade == "D"):
                s.subtotal = 1 * s.mk_sks
            elif (s.grade == "E"):
                s.subtotal = 0 * s.mk_sks


    #
    # @api.model
    # def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
    #     args = list(args or [])
    #     # optimize out the default criterion of ``ilike ''`` that matches everything
    #     if not (name == '' and operator == 'ilike'):
    #         args += [(self._rec_name, operator, name)]
    #     return self._search(args, limit=limit, access_rights_uid=name_get_uid)
