#Imports de librerias propias de Python/C
from __future__ import print_function 
from concurrent.futures import ThreadPoolExecutor, as_completed

#Imports de la API de Google
from googleapiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.errors import HttpError

#Imports librerías HTML-Requessts y JSON
import requests
import json



# Autorización Docs
# PRE: Recibe archivo de credenciales - .JSON
# POST: Devuelve *sheet_autorizada*:
#   objeto de clase 'service'->service='docs' autenticado por la API.
def Docs_Build(archivo_credenciales):

    # Declaración de los "scopes" a autenticar (docs,drive).
    # <Nota> Los "scopes" a utilizar deben estar habilitados desde la Google Cloud Console. </Nota>
    SCOPES = ['https://www.googleapis.com/auth/documents','https://www.googleapis.com/auth/drive']
    
    # Declaración del archivo de credenciales (JSON) descargado de la Google Cloud Console.
    # <Nota> Se debe creear la cuenta de servicio y autorizarla para la manipulación de los 
    # directorios o archivos específicos sobre los que se desea operar </Nota>
    SERVICE_ACCOUNT_FILE = archivo_credenciales
    
    #Llamada al método from_service_account_file propio de la API de Google
    montar_credenciales = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    # Montado del 'servicio' con los scopes, y credenciales relevantes 
    service = build('docs', 'v1', credentials=montar_credenciales)
    doc_autorizado = service.documents()
    return doc_autorizado


# Crear Docs
# PRE: Recibe: 
#       1.  doc_autorizado    |   [TDA::SERVICE] objeto devuelto por el método Docs_Build()
#       2.  titulo_nuevo_doc  |   [STR] Título que se desea dar a la nuevo documento.
# POST: [STR/TDA] Devuelve el ID ÚNICO identificador del documento creado. Devuelve NONE en caso de error.
def Docs_Crear(doc_autorizado,titulo_nuevo_doc):
    doc = doc_autorizado 
    metadata =  {
        'title': titulo_nuevo_doc
    }
    try:
        nuevo_doc = doc.create(body=metadata,fields='documentId').excecute()
        print(f"Se creó el documento {nuevo_doc.get('title')}. Id único: {nuevo_doc.get('documentId')}\n")
        doc_id = nuevo_doc.get('documentId')
    except HttpError as error:
        print(f"Ocurrió un error al tratar crear el documento {titulo_nuevo_doc}: {error}\n")
        doc_id = None
    return doc_id

# Escribir Docs
# PRE: Recibe: 
#       1.  doc_autorizado    |   [TDA::SERVICE] objeto devuelto por el método Docs_Build()
#       2.  doc_id            |   [STR] ID ÚNICO identificador del documento.
#       3.  texto_a_escribir  |   [STR] Texto que se agregar al documento.
# POST: [DICT/NONE] Devuelve la respuesta de la API a la solicitud batchUpdate. Devuelve NONE en caso de error.
def Docs_Escribir(doc_autorizado,doc_id,texto_a_escribir):
    doc = doc_autorizado 
    request = [
    {
        "insertText": {
            "location": {
                "index": 1
            },
            "text": texto_a_escribir
        }
    }
]
    try:
        response = doc.batchUpdate(documentId=doc_id, body={'requests': request}).execute()
        print(f"Se ha agregado el texto '{texto_a_escribir}' al documento con ID '{doc_id}\n'")
    except HttpError as error:
        print(f"Se ha producido un error: {error}\n")
        response = None
    return response

# Leer Docs
# PRE: Recibe: 
#       1.  doc_autorizado    |   [TDA::SERVICE] objeto devuelto por el método Docs_Build()
#       2.  doc_id            |   [STR] ID ÚNICO identificador del documento.
# POST: [STR/NONE] Devuelve el contenido del documento. Devuelve NONE en caso de error.
def Docs_Leer(doc_autorizado, doc_id):
    doc = doc_autorizado
    try:
        response = doc.get(documentId=doc_id).execute()
        doc_contenido = response.get('body').get('content')
        texto_contenido = ''
        for contenido in doc_contenido:
            if 'paragraph' in contenido:
                elementos = contenido.get('paragraph').get('elements')
                for elem in elementos:
                    texto_contenido += elem.get('textRun').get('content')
            elif 'table' in contenido:
                rows = contenido.get('table').get('tableRows')
                for row in rows:
                    celdas = row.get('tableCells')
                    for cel in celdas:
                        texto_contenido += cel.get('content')[0].get('paragraph').get('elements')[0].get('textRun').get('content')
            texto_contenido += '\n'
        print(f"Se ha leído el contenido del documento con ID '{doc_id}\n'")
    except HttpError as error:
        print(f"Se ha producido un error: {error}\n")
        texto_contenido = None
    return texto_contenido


def main():
    pass

if __name__ == "__main__":
    main()



