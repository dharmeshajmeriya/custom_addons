from odoo import api, fields, models, _


class CreateBanglowsWizard(models.TransientModel):
    _name = "create.banglows.wizard"
    _description = "Create Banglows Wizard"

    name = fields.Char(string="Name", required=True)

    def action_create_banglows(self):
        print("button is clicked")