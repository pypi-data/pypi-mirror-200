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

#Import objetos y métodos MIME para crear el mail con adjuntos
import mimetypes
from email.message import EmailMessage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

#Import base64 para encriptar el correo (requerido por la API)
import base64

#Imports librerías HTML-Requessts y JSON
import os.path
import requests
import json



# Autorización gAPI Sheets 
# PRE:  [STR - ruta] Recibe ruta al archivo de credenciales - .JSON 
# POST: [Ret->TDA::SERVICE] Devuelve objeto de clase 'service' autenticado por la API. 
def gMail_Build(archivo_credenciales,mail_envio):

    # Declaración de los "scopes" a autenticar (gmail).
    # <Nota> Los "scopes" a utilizar deben estar habilitados desde la Google Cloud Console. </Nota>
    SCOPES = ['https://www.googleapis.com/auth/gmail.send','https://mail.google.com']
    
    # Declaración del archivo de credenciales (JSON) descargado de la Google Cloud Console.
    # <Nota> Se debe creear la cuenta de servicio y autorizarla para la manipulación de los 
    # directorios o archivos específicos sobre los que se desea operar 
    # En el caso partiular de gMail debe configurarse la delegación del dominio
    # en Google Workplace o autorizar a la cuenta de servicio a "suplantar" el mail que 
    # se quiere utilizar como remitente. </Nota>
    SERVICE_ACCOUNT_FILE = archivo_credenciales
    
    #Llamada al método from_service_account_file propio de la API de Google
    montar_credenciales = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES,subject=mail_envio)
    
    try:
        gmail_autorizado = build('gmail', 'v1', credentials=montar_credenciales)
    except HttpError as error:
        print(f"Ocurrió un error: {error}")
        gmail_autorizado = None
    return gmail_autorizado



def Crear_Correo(mail_envio:str,mail_destinatario:str,asunto:str,cuerpo:str) -> EmailMessage:

    mensaje = EmailMessage()
    mensaje['To'] = mail_destinatario
    mensaje['From'] = mail_envio
    mensaje['Subject'] = asunto
    mensaje.set_content(cuerpo)
    
    return mensaje

def Anadir_Adjunto(mensaje:EmailMessage,ruta_adjunto:str)-> EmailMessage:
    type_subtype, _ = mimetypes.guess_type(ruta_adjunto)
    maintype, subtype = type_subtype.split('/')
    with open(ruta_adjunto, 'rb') as f:
        archivo_data = f.read()
        
    mensaje.add_attachment(archivo_data, maintype, subtype,filename=ruta_adjunto)
    return mensaje

def Crear_Correo_JSON(archivo_correo:str, mail_envio:str) -> EmailMessage:
    if os.path.isfile(archivo_correo):
        with open(archivo_correo, 'r') as f:
            data_del_mail = json.load(f)
    else:
        print(f'[ERROR]: no se encontró el archivo {archivo_correo}\n')
        exit()

    mensaje = EmailMessage()
    mensaje['To'] = data_del_mail['Destinatario']
    mensaje['From'] = mail_envio
    mensaje['Subject'] = data_del_mail['Asunto']
    mensaje.set_content(data_del_mail['Mensaje'])

    if 'Adjuntos' in data_del_mail:
        archivos = data_del_mail['Adjuntos']
        for archivo in archivos:
            print(f'{archivo}\n')
            type_subtype, _ = mimetypes.guess_type(archivo)
            maintype, subtype = type_subtype.split('/')
            with open(archivo, 'rb') as f:
                archivo_data = f.read()
                
            mensaje.add_attachment(archivo_data, maintype, subtype,filename=archivo)
    
    return mensaje

def Encriptar_Correo(mensaje):
     # Encriptado base64 como pide la documentación
    mensaje_64 = {'raw': base64.urlsafe_b64encode(mensaje.as_bytes()).decode()}
    return mensaje_64

def gMail_Enviar(gmail_autorizado,mensaje_64):
    try:
        enviar_mensaje = gmail_autorizado.users().messages().send(userId="me", body=mensaje_64).execute()
        print(f'Mensaje enviado satisfactoriamente: \n{json.dumps(enviar_mensaje, indent=4,sort_keys=True)}')

    except HttpError as error: 
        print(F'Ocurrió un error: {error}\n')
        enviar_mensaje = None


    return enviar_mensaje 

def main():
    pass

if __name__ == "__main__":
    main()
