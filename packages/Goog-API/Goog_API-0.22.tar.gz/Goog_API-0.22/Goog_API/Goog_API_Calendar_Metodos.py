#Imports de librerias propias de Python/C
from __future__ import print_function 
from concurrent.futures import ThreadPoolExecutor, as_completed


from datetime import datetime,timedelta,date

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

# Autorización gAPI Calendar 
# PRE:  [STR - ruta] Recibe ruta al archivo de credenciales - .JSON 
# POST: [Ret->TDA::SERVICE] Devuelve objeto de clase 'service' autenticado por la API. 
def Calendar_Build(archivo_credenciales):

    # Declaración de los "scopes" a autenticar (calendar).
    # <Nota> Los "scopes" a utilizar deben estar habilitados desde la Google Cloud Console. </Nota>
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    
    # Declaración del archivo de credenciales (JSON) descargado de la Google Cloud Console.

    SERVICE_ACCOUNT_FILE = archivo_credenciales
    
    #Llamada al método from_service_account_file propio de la API de Google
    montar_credenciales = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    try:
        calendar_autorizado = build('calendar', 'v3', credentials=montar_credenciales)
        return calendar_autorizado
    except HttpError as error:
        print(f"Ocurrió un error: {error}\n")
        return error

def Calcular_Fechas(ano,mes,dia,hora_inicio,duracion): #Duración en formato HH:MM
    hora_1 = datetime.strptime(hora_inicio, '%H:%M')
    hr_i= hora_1.hour()
    min_i = hora_1.minute()

    dura = datetime.strptime(duracion, '%H:%M')
    duracion_hr= dura.hour()
    duracion_min = dura.minute()


    fecha_1 = datetime(ano,mes,dia)
    fecha_2 = fecha_1+timedelta(hours=duracion_hr,minutes=duracion_min)
    ano_i=fecha_1.year()
    mes_i=fecha_1.month()
    dia_i=fecha_1.day()
    hr_i = fecha_1.time().strftime('%H:%M')
    ano_f=fecha_2.year()
    mes_f=fecha_2.month()
    dia_f=fecha_2.day()
    hr_f = fecha_2.time().strftime('%H:%M')



    Fecha_Inicio='{}-{}-{}T{}:00-03:00'.format(ano_i,mes_i,dia_i,hr_i)

    Fecha_Fin='{}-{}-{}T{}:00-03:00'.format(ano_f,mes_f,dia_f,hr_f)
    return Fecha_Inicio,Fecha_Fin        


def Calendar_Crear(calendar_autorizado,Titulo_del_Calendario,TZ="America/Argentina/Buenos_Aires"):
    try:
        
        calendar = {
            'summary': Titulo_del_Calendario,
            'timeZone': TZ,
        }



        calendario_creado = calendar_autorizado.calendars().insert(body=calendar).execute()
        CALENDAR_ID = calendario_creado["id"]
        print(f'Calendario creado con ID: {CALENDAR_ID}\n')
        print(f'{json.dumps(calendario_creado, indent=4,sort_keys=True)}\n')
        
        try:
            compartir = {
            "role": "reader",
            "scope": {
                "type": "default",
            }
        }
            calendario_compartido = calendar_autorizado.acl().insert(calendarId=CALENDAR_ID,body=compartir).execute()
            print(json.dumps(calendario_compartido, indent=4,sort_keys=True))
            print(f'Calendario publicado exitosamente\n')
        except HttpError as error:
            print(f'Ocurrió un error al publicar el calendario: {error}\n')

    except HttpError as error:
        print(f'Ocurrió un error al crear el calendario: {error}\n')
        CALENDAR_ID = None

    return CALENDAR_ID

def Crear_Evento(Titulo, Descripcion,Fecha_Inicio,Fecha_Fin,TZ="America/Argentina/Buenos_Aires",DV="public"):
    evento = {
                'summary': f'{Titulo}',
                'description': f'{Descripcion}.',
                'start': {
                    'dateTime': f'{Fecha_Inicio}',
                    'timeZone': TZ,
                    'defaultVisibility': DV,
                },
                'end': {
                    'dateTime': f'{Fecha_Fin}',
                    'timeZone': TZ,
                },
            }
    return evento

def Calendar_Nuevo_Evento(calendar_autorizado,evento:dict,CALENDAR_ID:str):
    try:

        evento_creado = calendar_autorizado.events().insert(calendarId=CALENDAR_ID, body=evento).execute()
        print(f'{json.dumps(evento_creado, indent=4,sort_keys=True)}\n')
        print(f"{evento['summary']} agregado al calendario\n")
    except HttpError as error:
        evento_creado = None
        print(f'Se produjo un ERROR: {error}\n')
    return evento_creado

def main():
    pass

if __name__ == "__main__":
    main()