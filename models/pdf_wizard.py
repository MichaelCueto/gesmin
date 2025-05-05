import os
import tempfile
import subprocess
from odoo import models, fields, api, _

class PdfProcessWizard(models.TransientModel):
    _name = 'pdf.process.wizard'
    _description = 'Asistente para procesar PDF'
    
    pdf_id = fields.Many2one('pdf.document', string='PDF a procesar')
    pdf_ids = fields.Many2many('pdf.document', string='Múltiples PDFs')
    batch_process = fields.Boolean('Procesamiento por lotes')
    
    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        if self._context.get('active_model') == 'pdf.document' and self._context.get('active_id'):
            res['pdf_id'] = self._context['active_id']
        return res
    
    def action_process(self):
        if self.batch_process:
            return self._process_batch()
        else:
            return self._process_single()
    
    def _process_single(self):
        self.ensure_one()
        if not self.pdf_id:
            raise ValueError("No se seleccionó ningún PDF")
        
        return self._process_pdf(self.pdf_id)
    
    def _process_batch(self):
        if not self.pdf_ids:
            raise ValueError("No se seleccionaron PDFs")
        
        for pdf in self.pdf_ids:
            self._process_pdf(pdf)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Proceso completado',
                'message': f'{len(self.pdf_ids)} PDF(s) procesados',
                'sticky': False,
            }
        }
    
    def _process_pdf(self, pdf):
        try:
            # Crear directorio temporal
            with tempfile.TemporaryDirectory() as tmp_dir:
                pdf_path = os.path.join(tmp_dir, pdf.filename or 'document.pdf')
                
                # Guardar el PDF en temporal
                with open(pdf_path, 'wb') as f:
                    f.write(pdf.file.decode('base64'))
                
                # Ejecutar script de procesamiento
                script_path = os.path.join(
                    os.path.dirname(__file__),
                    '../../scripts/procesar_pdfs.py'
                )
                
                result = subprocess.run(
                    ['python3', script_path, '--input', pdf_path],
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                # Guardar resultado
                pdf.write({
                    'json_output': result.stdout,
                    'processed': True,
                    'process_date': fields.Datetime.now(),
                })
                
                return {
                    'effect': {
                        'fadeout': 'slow',
                        'message': 'PDF procesado correctamente',
                        'type': 'rainbow_man',
                    }
                }
                
        except subprocess.CalledProcessError as e:
            raise models.ValidationError(
                _("Error al procesar PDF: %s\n%s") % (e.stderr, e.stdout)
            )