from odoo import models, fields, api, _
from odoo.exceptions import UserError


class voting(models.Model):  # inherit dari Model
    _name = 'idea.voting'  # attribut dari class Model (lihat dokumen odoo)
    _description = 'Class berisi voting terhadap sebuah idea'

    # membuat attribute field
    name = fields.Char('Number', size=64, required=True, index=True, readonly=True, default='new',
                       states={})
    date = fields.Date('Date Release', default=fields.Date.context_today, help='Please fill the date here',
                       readonly=True,
                       states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'),
                              ('voted', 'Voted'),
                              ('canceled', 'Canceled')],
                             string='State', default='draft', readonly=True)

    vote = fields.Selection([('yes', 'Yes'),
                             ('no', 'No'),
                             ('abstain', 'Abstain')], required=True,
                            readonly=True,
                            states={'draft': [('readonly', False)]})
    voter_id = fields.Many2one('res.users', 'Voted By', readonly=True, ondelete="cascade",
                               default=lambda self: self.env.user)
    idea_id = fields.Many2one('idea.idea', string='Idea', readonly=True, ondelete="cascade",
                              states={'draft': [('readonly', False)]},
                              domain="[('state', '=', 'done'),('active', '=', 'True')]")
    # field ini adalah related field, merefer ke date yang ada di model idea_idea. Sifatnya readonly, user tidak bisa input
    # field ini tidak meng-create field baru di table, jk mau disimpan, berikan attribute store=True
    # related field yang store=false tidak bisa di sort, group by
    idea_date = fields.Date("Idea date", related='idea_id.date')

    # ondelete="restrict" jk master tidak boleh dihapus
    # ondelete="set null" , jk master dihapus maka nilainya akan menjadi null di database atau false di python, ini default
    def action_voted(self):
        self.state = 'voted'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    @api.model_create_multi
    def create(self, vals_list):
        if self.name == 'new' or not self.name:
            seq = self.env['ir.sequence'].search([("code", "=", "idea.voting")])
            if not seq:
                raise UserError(_("idea.voting sequence not found, please create idea.voting sequence"))
            for val in vals_list:
                val['name'] = seq.next_by_id(sequence_date=val['date'])
                # val['name'] = seq.next_by_id()

            return super(voting, self).create(vals_list)
