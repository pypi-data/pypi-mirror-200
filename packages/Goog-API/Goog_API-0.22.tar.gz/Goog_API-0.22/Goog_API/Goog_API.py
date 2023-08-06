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

#Import del Propio Módulo
from .Goog_API_Sheets_Metodos import Sheets_Build
from .Goog_API_Docs_Metodos import Docs_Build
from .Goog_API_gMail_Metodos  import gMail_Build
from .Goog_API_Calendar_Metodos  import Calendar_Build
from .Goog_API_Drive_Metodos  import Drive_Build

# Autorización gAPI General. Usa los métodos propios de cada una.
# PRE:  [STR - ruta] Recibe ruta al archivo de credenciales - .JSON //  [STR] Nombre de la APP a utilizar. // [STR] (opcional) Mail de envio para el método gMail_Build()
# POST: [Ret->TDA::SERVICE] Devuelve objeto de clase 'service' autenticado por la API. // Ret: TDA::'service'
def Goog_API_Build(archivo_credenciales,app,gMail_Build_Mail_envio=None):

    # <Nota> Los "scopes" a utilizar deben estar habilitados desde la Google Cloud Console. </Nota>
    if app == "Sheets":
        app_autenticada = Sheets_Build(archivo_credenciales)
    elif app == "Docs":
        app_autenticada = Docs_Build(archivo_credenciales)
    elif app == "gMail":
        if gMail_Build_Mail_envio != None:
            gMail_Build(archivo_credenciales,gMail_Build_Mail_envio)
        else:
            app_autenticada = None
            print(f'Por favor indique un correo electrónico para utilizar con la API de gMail  (Ver LÉAME.MD para más información.)\n')
    elif app == "Calendar":
        app_autenticada = Calendar_Build(archivo_credenciales)
    elif app == "Drive":
        app_autenticada = Drive_Build(archivo_credenciales)
    else:
        app_autenticada = None
        print(f'Por favor indique una App soportada por la API. (Ver LÉAME.MD para más información.)\n')
    return app_autenticada





