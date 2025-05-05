from odoo import http
from odoo.http import request
import json
import base64

class PdfProcessorController(http.Controller):
    
    @http.route('/pdf/upload', type='http', auth='user', methods=['POST'], csrf=False)
    def upload_pdf(self, **post):
        """
        Endpoint para subir PDFs via API
        Ejemplo de uso:
        POST /pdf/upload
        Parámetros:
        - file: Archivo PDF
        - name: Nombre del documento (opcional)
        """
        try:
            if not post.get('file'):
                return http.Response(
                    json.dumps({'error': 'No se proporcionó archivo PDF'}),
                    status=400,
                    mimetype='application/json'
                )
            
            PdfDocument = request.env['pdf.document']
            
            # Crear nuevo documento
            new_doc = PdfDocument.create({
                'name': post.get('name', post.get('filename', 'Nuevo PDF')),
                'file': base64.b64encode(post['file'].read()),
                'filename': post['file'].filename
            })
            
            return http.Response(
                json.dumps({
                    'success': True,
                    'document_id': new_doc.id,
                    'message': 'PDF subido correctamente'
                }),
                status=200,
                mimetype='application/json'
            )
            
        except Exception as e:
            return http.Response(
                json.dumps({'error': str(e)}),
                status=500,
                mimetype='application/json'
            )
    
    @http.route('/pdf/process/<int:doc_id>', type='json', auth='user')
    def process_pdf(self, doc_id, **kwargs):
        """
        Endpoint para procesar un PDF via API
        Ejemplo de uso:
        POST /pdf/process/1
        """
        try:
            pdf = request.env['pdf.document'].browse(doc_id)
            if not pdf.exists():
                return {'error': 'Documento no encontrado'}
            
            wizard = request.env['pdf.process.wizard'].create({
                'pdf_id': pdf.id,
                'batch_process': False
            })
            
            result = wizard.action_process()
            pdf.refresh()  # Actualizar datos después del procesamiento
            
            return {
                'success': True,
                'document_id': pdf.id,
                'json_output': pdf.json_output,
                'processed': pdf.processed,
                'process_date': pdf.process_date.isoformat() if pdf.process_date else None
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    @http.route('/pdf/download_json/<int:doc_id>', type='http', auth='user')
    def download_json(self, doc_id, **kwargs):
        """
        Descargar el JSON resultante
        Ejemplo de uso:
        GET /pdf/download_json/1
        """
        pdf = request.env['pdf.document'].browse(doc_id)
        if not pdf.exists() or not pdf.json_output:
            return request.not_found()
        
        filename = f"{pdf.name or 'output'}.json"
        return request.make_response(
            pdf.json_output,
            headers=[
                ('Content-Type', 'application/json'),
                ('Content-Disposition', f'attachment; filename="{filename}"')
            ]
        )
    
    @http.route('/pdf/batch_process', type='json', auth='user')
    def batch_process(self, doc_ids, **kwargs):
        """
        Procesar múltiples PDFs
        Ejemplo de uso:
        POST /pdf/batch_process
        Body: {"doc_ids": [1, 2, 3]}
        """
        try:
            if not doc_ids:
                return {'error': 'No se proporcionaron IDs de documentos'}
            
            pdfs = request.env['pdf.document'].browse(doc_ids)
            wizard = request.env['pdf.process.wizard'].create({
                'pdf_ids': [(6, 0, pdfs.ids)],
                'batch_process': True
            })
            
            result = wizard.action_process()
            
            return {
                'success': True,
                'processed_count': len(pdfs),
                'message': f'{len(pdfs)} documentos procesados'
            }
            
        except Exception as e:
            return {'error': str(e)}