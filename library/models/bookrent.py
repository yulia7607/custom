from odoo import models, fields, api, _


class bookrent(models.Model):  # inherit dari Model
    _name = 'library.bookrent'  # attribut dari class Model (lihat dokumen odoo)
    _description = 'class for the book rent'
    name = fields.Char(compute="_compute_name", store=True, recursive=True)
    member_id = fields.Many2one('res.partner', 'Member', ondelete="cascade")

    bookrent_detil_ids = fields.One2many('library.bookrent_detil', 'bookrent_id', string='Rent Detailed', readonly=True,
                                         states={'draft': [('readonly', False)]})
    date = fields.Date('Rent Date', default=fields.Date.context_today, readonly=True,
                       help='Please fill the date here',
                       states={'draft': [('readonly', False)]})

    total = fields.Integer('Total', compute="_compute_total", store=True, default=0)
    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Approved'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True,
                             default='draft')

    # _sql_constraints = [('book_rent_unik', 'unique(book_id, rent_id)', _('The rent for the book already exist!'))]

    @api.depends("bookrent_detil_ids", "bookrent_detil_ids.book_id","bookrent_detil_ids.bookrent_price")
    def _compute_total(self):
        self.total = 0
        for rec in self.bookrent_detil_ids:
            self.total += rec.bookrent_price

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    @api.depends('member_id', 'date')
    def _compute_name(self):
        for s in self:
            s.name = "%s - %s" % (s.member_id.name, s.date)


    def tes_bookrent(self):
        print("ini di bookrent")
        t = self.env.context.get("keterangan")
        print(t)

        t=self.env.context;
        print(t.keterangan)