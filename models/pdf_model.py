from odoo import models, fields, api

class PdfDocument(models.Model):
    _name = 'pdf.document'
    _description = 'Documento PDF'
    
    name = fields.Char('Nombre', required=True)
    file = fields.Binary('Archivo PDF', required=True)
    filename = fields.Char('Nombre del archivo')
    json_output = fields.Text('Salida JSON')
    processed = fields.Boolean('Procesado', default=False)
    process_date = fields.Datetime('Fecha de Procesamiento')
    
    def action_process_pdf(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Procesar PDF',
            'res_model': 'pdf.process.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_pdf_id': self.id},
        }