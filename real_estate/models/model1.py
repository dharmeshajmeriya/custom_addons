from odoo import fields, models

class TestModel(models.Model):
    _name = "test.model"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Test Model"
    last_seen = fields.Datetime("Last Seen", default=lambda self: fields.Datetime.now())

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Available From', copy=False,
                                    default=lambda self: fields.Datetime.add(fields.Datetime.now(), months=3))
    expected_price = fields.Float(required=True, string='Expected Price')
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer(default=2, string='Bedrooms')
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




