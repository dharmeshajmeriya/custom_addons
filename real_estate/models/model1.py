from odoo import api, fields, models

class TestModel(models.Model):
    _name = "test.model"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Test Model"
    last_seen = fields.Datetime("Last Seen", default=lambda self: fields.Datetime.now())
    active = fields.Boolean(string="Active", default=True)
    tag_ids = fields.Many2many(comodel_name="res.partner", string="Tags")
    name = fields.Char(string="Title", required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Available From', copy=False,
                                    default=lambda self: fields.Datetime.add(fields.Datetime.now(), months=3))
    expected_price = fields.Float(required=True, string='Expected Price')
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Estate property offers')
    seller_id = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True,
                                default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', tracking=True, copy=False)
    total_area = fields.Float(compute="_compute_total", string="Total Area (sqm)")
    best_price = fields.Integer(compute="_compute_price", string="Best Offer")
    bedrooms = fields.Integer(default=2, string='Bedrooms')
    status = fields.Char(string='Status')
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(string='Garden Orientation',
                                          selection=[('north', 'North'), ('south', 'South'), ('east', 'East'),
                                                     ('west', 'West')], default='north')
    state = fields.Selection(string="State", selection=[('new', 'New'), ('offer_received', 'Offer Received'),
                                                        ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'),
                                                        ('Cancelled', 'Cancelled')], default='new')

    responsible_id = fields.Many2one('res.partner', string="Responsible")

    def action_received(self):
        self.state = 'offer_received'

    def action_accepted(self):
        self.state = 'offer_accepted'

    def action_sold(self):
        self.state = 'sold'

    def action_done(self):
        self.state = 'done'

    def action_test(self):
        print('test button')

    def action_do_something(self):
        for record in self:
            record.name = "Something"
        return True


    def action_cancel(self):
        self.state = 'cancelled'

    def action_new(self):
        self.state = 'new'

    @api.model
    def create(self, vals):
        if not vals.get('description'):
            vals['description'] = 'New Property'
        res = super(TestModel, self).create(vals)
        return res

    @api.depends('living_area', 'garden_area')
    def _compute_total(self):
        self.total_area = self.living_area + self.garden_area

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden is True:
            self.garden_area = 10
            self.garden_orientation = 'north'
        elif self.garden is False:
            self.garden_area = 0
            self.garden_orientation = ''

    @api.depends("offer_ids.partner_id")
    def _compute_price(self):
        if self.offer_ids.partner_id:
            self.best_price = max(i.price for i in self.offer_ids)
        else:
            self.best_price = 0


