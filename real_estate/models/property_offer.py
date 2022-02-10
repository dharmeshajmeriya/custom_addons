from odoo import api, fields, models

class TestModel(models.Model):
    _name = "estate.property.offer"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Property Offer"

    price = fields.Float(string="Price", tracking=True)
    status = fields.Selection(string="Status", selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('test.model', required=True)
    validity = fields.Integer(string="Validity (days)", default="7")
    date_deadline = fields.Date(string="Deadline", compute="_compute_date", inverse="_inverse_date")

    @api.depends("validity")
    def _compute_date(self):
        for rec in self:
            rec.date_deadline = fields.Datetime.add(rec.create_date, days=rec.validity)

    def _inverse_date(self):
        for rec in self:
            diff = fields.Datetime.subtract(rec.date_deadline, rec.create_date)
            rec.validity = diff.days

    def action_accept(self):
        self.status = 'accepted'
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id

    def action_reject(self):
        self.status = 'refused'

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        self.name = "Document for %s" % (self.partner_id.name)
        self.description = "Default description for %s" % (self.partner_id.name)
