from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class TestModel(models.Model):
    _name = "test.model"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Test Model"
    _order = "name, expected_price"

    name = fields.Char(string="Title", required=True)
    reference = fields.Char(string="Reference", required=True, readonly=True, copy=False, default=lambda self: _('New'))
    last_seen = fields.Datetime("Last Seen", default=lambda self: fields.Datetime.now())
    active = fields.Boolean(string="Active", default=True)
    tag_ids = fields.Many2many(comodel_name="res.partner", string="Tags")
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Available From', copy=False,
                                    default=lambda self: fields.Datetime.add(fields.Datetime.now(), months=3))
    expected_price = fields.Float(required=True, string='Expected Price')
    selling_price = fields.Float(string='Selling Price', copy=False)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Estate property offers')
    seller_id = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True,
                                default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', tracking=True, copy=False)
    total_area = fields.Float(compute="_compute_total", string="Total Area (sqm)")
    best_price = fields.Integer(compute="_compute_price", string="Best Offer")
    bedrooms = fields.Integer(default=0, string='Bedrooms')
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
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('test.model') or _('New')
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

    @api.constrains('name', 'description')
    def _check_description(self):
        for record in self:
            bname = self.env['test.model'].search([('name', '=', record.name), ('id', '!=', record.id)])
            if bname:
                raise ValidationError("Fields name already exists. ")

    @api.constrains('bedrooms')
    def _check_bedrooms(self):
        for record in self:
            if record.bedrooms == 0:
                raise ValidationError("please input how many bedrooms are there?")

    @api.constrains('expected_price')
    def _check_expected_price(self):
        for record in self:
            if record.expected_price <= 0:
                raise ValidationError("A property expected price must be strictly positive")

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price <= 0:
                raise ValidationError("A property selling price must be positive")

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for rec in self:
            if rec.selling_price != 0:
                value = 0.9 * rec.expected_price
                if rec.selling_price < value:
                    #rec.selling_price = 0
                    raise ValidationError("The selling price should not be less than 90% of expected price.")

    def name_get(self):
        result = []
        for rec in self:
            name = rec.reference + rec.name
            result.append((rec.id, name))
        return result

    def action_url(self):
        return{
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'https://www.odoo.com/',
        }



