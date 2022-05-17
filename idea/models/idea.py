from odoo import models, fields, api, _
from odoo.exceptions import UserError

# _ untuk translate

class idea(models.Model):  # inherit dari Model
    _name = 'idea.idea'  # attribut dari class Model (lihat dokumen odoo)
    _description = 'class untuk berlatih ttg idea'
    # _rec_name = 'name'
    _order = 'date desc'  # defaultnya adalah id, pengaruhnya saat List view
    # id = fields.Integer() #ini otomatis ada di odoo, akan jadi PK, tidak perlu ditulis, semua table odoo PK hanya 1, ID ini

    # membuat attribute field
    name = fields.Char('Number', size=64, required=True, index=True, readonly=True, default='new',
                       states={}) # index true krn field ini yang biasanya sering dicari
    date = fields.Date('Date Release', default=fields.Date.context_today, readonly=True,
                       help='Please fill the date here',
                       states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'),
                              # draft--> key, secara technical yang disimpan di dbase, Draft: value yang dilihat user
                              ('confirmed', 'Confirmed'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True,
                             # krn required, sebaiknya dikasi default
                             default='draft')  # tuple di dalam list, nama field harus state spy bisa diakses oleh states
    # Description is read-only when not draft!
    description = fields.Text('Description', readonly=True,
                              states={'draft': [('readonly', False)]})  # readOnly True kecuali saat draft
    # active ini adalah reserved field
    active = fields.Boolean('Active', default=True, readonly=True, states={'draft': [('readonly', False)]})
    confirm_date = fields.Date('Confirm date')
    # by convention, many2one fields end with '_id'
    confirm_partner_id = fields.Many2one('res.partner', 'Confirm By', readonly=True)
    # sponsor_ids = fields.Many2many('res.partner', 'idea_idea_res_partner_rel', 'idea_idea_id', 'res_partner_id', 'Sponsors')
    sponsor_ids = fields.Many2many('res.partner', string='Sponsors')

    score = fields.Integer('Score', default=0, readonly=True)
    owner = fields.Many2one('res.partner', 'Owner', index=True, readonly=True, states={'draft': [('readonly', False)]})

    voting_ids = fields.One2many('idea.voting', 'idea_id', string='Votes')
    total_yes = fields.Integer("Yes", compute="_compute_vote", store=True, default=0)
    total_no = fields.Integer("No", compute="_compute_vote", store=True, default=0)
    total_abstain = fields.Integer("Abstain", compute="_compute_vote", store=True, default=0)
    _sql_constraints = [('name_unik', 'unique(name)', _('Ideas must be unique!'))]

    @api.depends("voting_ids", "voting_ids.vote", "voting_ids.state")
    # function ini dijalankan jika record voting (voting_ids) berubah (new atau delete), atau
    # atau saat vote (voting_ids.vote) berubah, atau
    # saat state (voting_ids.state) berubah
    # @api.onchange("voting_ids", "voting_ids.vote", "voting_ids.state")
    # mirip dengan depends tp ini perubahannya jk hanya mell UI.
    # Kalau ondepends bisa lewat python code maupun UI, misal kita bikin function otomaticvote dari program,
    # ini tidak bisa dihandle oleh onchange
    def _compute_vote(self):
        for idea in self.filtered(lambda i: i.state == 'done'):
            val = {
                "total_yes": 0,
                "total_no": 0,
                "total_abstain": 0
            }
            # for rec in idea.voting_ids:
            for rec in idea.voting_ids.filtered(lambda s: s.state == 'voted'):
                # lambda adalah on the fly function dari python
                # s ini adalah self dari voting_ids, fungsi filtered ini akan memfilter khusus yang voting_ids.state='voted'
                # bisa juga pakai looping tp lebih lama, jd sebelum masuk loop dilakukan filter dulu
                if rec.vote == "yes":
                    val["total_yes"] += 1
                elif rec.vote == 'no':
                    val["total_no"] += 1
                else:
                    val["total_abstain"] += 1
            idea.update(val)  # untuk update 1 record mell python code hrs dalam bentuk dictionary

    def action_tes(self):

        # self.env['library.book']
        # contoh ambil active user
        print(self.env.user.name)
        # contoh ambil active company
        print(self.env.company.name)
        # contoh common orm method search
        a = self.env["res.partner"].search([('name', 'ilike', 'Gemini')])
        for rec in a:
            print(rec.name)
        a = self.env["res.partner"].search([], limit=2)
        # for rec in a:
        #     print(rec.name)

        # contoh context
        # print(self.env.context.get('lang'))
        # #
        # t = self.env.context.copy()
        # t["keterangan"] = 'Ideku'
        # self.with_context(t).action_done()
        # #
        # b=self.env["library.bookrent"]
        # b.with_context(t).tes_bookrent()

        # contoh query select
        query = "select name from res_partner order by name desc limit 3"
        self.env.cr.execute(query)
        res = self.env.cr.fetchall()
        for data in res:
            print(data[0])

        # contoh query update
        # query="update idea_idea set state='done' where state in ('confirmed','draft')"
        # self.env.cr.execute(query)
        # self.env.cr.rollback()

        # contoh query delete
        # query="delete from idea_idea where state='draft'"
        # self.env.cr.execute(query)
        # self.env.cr.rollback()

        # contoh browse
        query = "select * from res_partner limit 3"
        self.env.cr.execute(query)
        res = self.env['res.partner'].browse([row[0] for row in self.env.cr.fetchall()])
        for rec in res:
            print(rec.name)

        # contoh search
        # a = self.env["res.partner"]
        # res = a.search([], order="name asc", offset=2, limit=6) #offset ini adalah berapa rec yang tdk ditampilkan
        # for rec in res:
        #     print(rec.name)

        # contoh search_count
        # count = self.env['res.partner'].search_count([("name", "ilike", "Brandon")])
        # print(count)

        # contoh exists
        # res = self.env['res.partner'].search([("name","ilike","Brandon")])
        # if res.exists():
        #     for rec in res:
        #         print(rec.name)

        # contoh mapped
        # res=self.env['res.partner'].search([]).mapped('name')
        # for rec in res:
        #     print(rec.name)

        # contoh filter
        # res = self.env['idea.idea'].search([]).filtered((lambda r: r.total_yes >1))
        # for rec in res:
        #     print(rec.name)

        # contoh sorted
        # res = self.env['res.partner'].search([]).sorted(key=lambda r: r.name).mapped('name')
        # for rec in res:
        #     print(rec.name)

    def action_done(self):
        self.state = 'done'
        t = self.env.context
        print(t.get('keterangan'))

    def action_canceled(self):
        self.state = 'canceled'

    def action_confirmed(self):
        self.state = 'confirmed'
        if self.name == 'new' or not self.name:
            seq = self.env['ir.sequence'].search([("code", "=", "idea.idea")])
            if not seq:
                raise UserError(_("idea.idea sequence not found, please create idea.idea sequence"))
            self.name = seq.next_by_id(sequence_date=self.date)
            # self.name = seq.next_by_id()

    def action_settodraft(self):
        self.state = 'draft'
