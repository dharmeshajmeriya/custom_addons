from odoo import models


class PropertyCardXlsx(models.AbstractModel):
    _name = 'report.real_estate.report_property_id_card_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, property):
        sheet = workbook.add_worksheet('Property ID Cards')
        bold = workbook.add_format({'bold': True})
        row = 3
        col = 3
        sheet.set_column('D:E',30)
        for obj in property:
            report_name = obj.name
            # One sheet by partner
            row += 1
            sheet.write(row, col, 'name' , bold)
            sheet.write(row, col+1, obj.name)
            row +=1
            sheet.write(row, col, 'expected price', bold)
            sheet.write(row, col + 1, obj.expected_price)