# models/folder.py
import subprocess
import os
from odoo import models, fields

class PdfFolder(models.Model):
    _name = 'pdf.folder'
    _description = 'Carpeta para documentos PDF'

    name = fields.Char(string='Nombre de la carpeta', required=True)
    document_ids = fields.One2many('pdf.document', 'folder_id', string='Documentos')

    def action_process_folder(self):
        for doc in self.document_ids:
            if doc.file:
                # Guardar archivo temporal
                filepath = f"/tmp/{doc.filename}"
                with open(filepath, 'wb') as f:
                    f.write(doc.file.decode('base64'))

                # Ejecutar script externo
                script_path = '../../scripts/procesar_pdfs.py'
                subprocess.run(['python3', script_path, filepath])

                # (Opcional: mover el JSON a Mongo desde dentro del script)