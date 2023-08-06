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
from googleapiclient.http import MediaFileUpload

#Librería mimetypes con tipos de archivos
import mimetypes

#Imports librerías HTML-Requessts y JSON
import requests
import json


# Autorización gAPI Drive
# PRE:  [STR - ruta] Recibe ruta al archivo de credenciales - .JSON // Arg: str
# POST: [TDA] Devuelve *sheet_autorizada*:
#       objeto de clase 'service'->service='drive' autenticado por la API. // Ret: TDA::'service'
def Drive_Build(archivo_credenciales):
    """
    Instanciación de objeto service drive autorizado por la API.

    :param archivo_credenciales: STR | ruta al archivo de credenciales de la cuenta de servicio. JSON. 
    :return: drive_autenticado: TDA | objeto de clase service autenticado por la api.
    """
    

    # Declaración de los "scopes" a autenticar (drive,sheets,docs).
    # <Nota> Los "scopes" a utilizar deben estar habilitados desde la Google Cloud Console. </Nota>
    SCOPES = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/documents']
    
    # Declaración del archivo de credenciales (JSON) descargado de la Google Cloud Console.
    # <Nota> Se debe crear la cuenta de servicio y autorizarla para la manipulación de los 
    # directorios o archivos específicos sobre los que se desea operar </Nota>
    SERVICE_ACCOUNT_FILE = archivo_credenciales
    
    #Llamada al método from_service_account_file propio de la API de Google
    montar_credenciales = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    # Montado del 'servicio' con los scopes, y credenciales relevantes 
    try:
        drive_autenticado = build('drive', 'v3', credentials=montar_credenciales)
        

    except HttpError as error:
        print(f"Ocurrió un error: {error}\n")
        drive_autenticado = None
    return drive_autenticado



def Drive_crear_carpeta(drive_autenticado,nombre:str, id_carpeta_padre:str=None,compartir_gmail:str=None,es_publica:bool=True):
    """
    Crea una carpeta en Google Drive y devuelve su ID único.
    Si Ud. especifica un ID de carpeta principal, la carpeta se creará como una subcarpeta de aquella.
    Nota: Si Ud. no comparte la carpeta, deberá mantenerla pública para la lectura, caso contrario solo será accesible para la 'cuenta de servicio' con la que fue creada.
    :param drive_autenticado: TDA | objeto de clase service devuelto por el método Drive_Build()
    :param nombre: STR | nombre de la carpeta que se creará
    :param id_carpeta_padre: STR (=None) | ID de la carpeta padre (opcional)
    :param compartir_gmail: STR (=None) | cuenta de gMail que se desea sea 'editor' de la carpeta (opcional)
    :param es_publica: BOOL (=True) | define si la carpeta es pública para la lectura (opcional)
    :return carpeta_id: STR | ID único de la carpeta que se crea
    
    """
    drive = drive_autenticado
    metadata = {'name': nombre, 'mimeType': 'application/vnd.google-apps.folder'}
    if id_carpeta_padre:
        metadata['parents'] = [id_carpeta_padre]
    if es_publica:
        metadata['permissions'] = [{'type': 'anyone', 'role': 'reader', 'withLink': True}]
    try:
        carpeta = drive.files().create(body=metadata, fields='id').execute()
        carpeta_id = carpeta.get('id')
        try:
            compartir = {
                "type":"user",
                "emailAddress":compartir_gmail,
                "role":'writer'
            }
            drive.permissions().create(fileId=carpeta_id,body=compartir).execute()
            print(f'Se creó la carpeta "{nombre}", con el ID: {carpeta_id} y se compartió con {compartir_gmail}\n')
            
        except HttpError as error:
            print(f'Error al compartir la carpeta: {json.dumps(error, indent=4,sort_keys=True)}\n')
            carpeta_id = carpeta.get('id')
        
    except HttpError as error:
        print(f'Error al crear la carpeta: {json.dumps(error, indent=4,sort_keys=True)}\n')
        carpeta_id = None
    return carpeta_id


def Drive_crear_doc_en_carpeta(drive_autenticado,nombre:str, carpeta_id:str):
    """
    Crea un documento en una carpeta existente en Google Drive.
    :param drive_autenticado: TDA | objeto de clase service devuelto por el método Drive_Build()
    :param nombre: STR | nombre del documento que se creará
    :param carpeta_id: STR | ID de la carpeta en la que se creará el documento
    :return doc_id: STR | ID único del documento que se crea
    """
    drive = drive_autenticado
    metadata = {'name': nombre, 'parents': [carpeta_id], 'mimeType': 'application/vnd.google-apps.document'}
    try:
        doc = drive.files().create(body=metadata).execute()
        doc_id = doc.get('id')
    except HttpError as error:
        print(f'Error al crear el documento: {error}\n')
        doc_id=None
    return doc_id

def Drive_crear_sheet_en_carpeta(drive_autenticado,nombre:str,carpeta_id:str):
    """
    Crea una hoja de cálculo en una carpeta existente en Google Drive.
    :param drive_autenticado: TDA | objeto de clase service devuelto por el método Drive_Build()
    :param nombre: STR | nombre del documento que se creará
    :param carpeta_id: STR | ID de la carpeta en la que se creará el documento
    :return sheet_id: STR | ID único de la hoja de cálculo que se crea
    """
    drive = drive_autenticado
    metadata = {'name': nombre, 'parents': [carpeta_id], 'mimeType': 'application/vnd.google-apps.spreadsheet'}
    try:
        sheet = drive.files().create(body=metadata).execute()
        sheet_id = sheet.get('id')
    except HttpError as error:
        print(f'Error al crear la hoja de cálculo: {json.dumps(error, indent=4,sort_keys=True)}\n')
        sheet_id=None
    return sheet_id

def Drive_subir_archivo(drive_autenticado,archivo_a_subir:str,nombre_del_archivo:str,convertir_archivo:bool=True,carpeta_id:str=None)->str:
    """
    Sube un archivo a Google Drive. Si se proporciona un ID de carpeta, se incluye a esta, de lo contrario se sube al directorio raiz.
    Para cierto tipo de archivo se ofrece la opción convertir_archivo, para subirlo en formato nativo de Google Drive análogo.
    :param drive_autenticado: TDA | objeto de clase service devuelto por el método Drive_Build()
    :param archivo_a_subir: STR | ruta del archivo local que se subirá al Google Drive
    :param nombre_del_archivo: STR | nombre que tendrá el archivo en el Google Drive
    :param convertir_archivo: BOOL | especifica si se debe convertir el archivo en un formato nativo de Google Drive
    :param carpeta_id: STR | ID de la carpeta de Google Drive en la que se creará el archivo. Si no se especifica, se subirá a la raíz del Drive.
    : ID_archivo_subido: STR | ID único del archivo subido en el Google Drive del usuario autenticado.
    """
    
    # Diccionario que mapea los tipos MIME de los archivos de Office a los tipos MIME de Google Workspace.
    tipos_mime_traducidos = {    
        'application/vnd.ms-excel': 'application/vnd.google-apps.spreadsheet',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'application/vnd.google-apps.spreadsheet',
        'application/vnd.ms-powerpoint': 'application/vnd.google-apps.presentation',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'application/vnd.google-apps.presentation',
        'application/msword': 'application/vnd.google-apps.document',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'application/vnd.google-apps.document',
    }

    # Se establece la variable 'drive' con la instancia autenticada del cliente de Drive API.
    drive = drive_autenticado

    # Se adivina el tipo MIME del archivo a subir.
    tipo_mime_adivinar, encoding = mimetypes.guess_type(archivo_a_subir)
    

    # Si el tipo MIME a adivinar está en la lista de tipos MIME de Office que se pueden traducir, y se quiere convertir el archivo, se establece el tipo MIME de subida en la traducción correspondiente.
    # De lo contrario, el tipo MIME de subida se establece en el tipo MIME adivinado.
    try:
        if (tipo_mime_adivinar in tipos_mime_traducidos) and convertir_archivo==True:
            tipo_mime_subir = tipos_mime_traducidos[tipo_mime_adivinar]
        else:
            tipo_mime_subir = tipo_mime_adivinar
        
        # Se crea un diccionario 'metadata' que contiene la información del archivo que se va a subir, como el nombre del archivo, el título, la ID de la carpeta en la que se va a subir y el tipo MIME de subida.
        metadata = {
            'name' : nombre_del_archivo,
            'title': nombre_del_archivo,
            'parents': [carpeta_id],
            'mimeType': tipo_mime_subir,
        }

        # Se crea una instancia de MediaFileUpload con el archivo a subir y el tipo MIME adivinado.
        media = MediaFileUpload(archivo_a_subir,mimetype=tipo_mime_adivinar)

        # Se utiliza el método 'create' de la API de Drive para subir el archivo a Google Drive, pasando el diccionario 'metadata', la instancia de MediaFileUpload y especificando el campo 'id' para obtener la ID del archivo recién subido.
        archivo = drive.files().create(body=metadata, media_body=media, fields='id').execute()
        
        # Se imprime la información del archivo subido, como la ID, el título y la fecha de creación.
        print(json.dumps(archivo, indent=4,sort_keys=True))

        # Se obtiene la ID del archivo subido a partir del objeto 'archivo' y se imprime el mensaje que indica que el archivo se subió correctamente.
        ID_Archivo_subido:str = archivo.get('id')
        print(f'Se subío el archivo en la carpeta https://drive.google.com/drive/folders/{carpeta_id} y se le asignó el Id: {ID_Archivo_subido}\n')
    
    #Excepciones por error en la solicitud a la API
    except HttpError as error:
        print(f'Error al subir el archivo: {error}\n')
        ID_Archivo_subido=None

    return ID_Archivo_subido
