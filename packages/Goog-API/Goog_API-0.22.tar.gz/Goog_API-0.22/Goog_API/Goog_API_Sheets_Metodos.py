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



        
    

# Autorización gAPI Sheets 
# PRE:  [STR - ruta] Recibe ruta al archivo de credenciales - .JSON // Arg: str
# POST: [TDA] Devuelve *sheet_autorizada*:
#       objeto de clase 'service'->service='sheets' autenticado por la API. // Ret: TDA::'service'
def Sheets_Build(archivo_credenciales):

    # Declaración de los "scopes" a autenticar (sheets,drive).
    # <Nota> Los "scopes" a utilizar deben estar habilitados desde la Google Cloud Console. </Nota>
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
    
    # Declaración del archivo de credenciales (JSON) descargado de la Google Cloud Console.
    # <Nota> Se debe creear la cuenta de servicio y autorizarla para la manipulación de los 
    # directorios o archivos específicos sobre los que se desea operar </Nota>
    SERVICE_ACCOUNT_FILE = archivo_credenciales
    
    #Llamada al método from_service_account_file propio de la API de Google
    montar_credenciales = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    # Montado del 'servicio' con los scopes, y credenciales relevantes 
    try:
        service = build('sheets', 'v4', credentials=montar_credenciales)
        sheet_autorizada = service.spreadsheets()
    except HttpError as error:
        print(f"Ocurrió un error: {error}\n")
        sheet_autorizada = None
    return sheet_autorizada

# Crear Sheets
# PRE: Recibe: 
#       1.  sheet_autorizada    |   [TDA] objeto devuelto por el método Sheets_Build() // Arg: TDA::'service'
#       2.  titulo_nueva_hoja   |   [STR] Título que se desea dar a la neuva hoja // Arg: str
# POST: [STR/TDA] Devuelve el ID ÚNICO identificador de la hoja creada. Devuelve ERROR en caso de error.
def Sheets_Crear(sheet_autorizada,titulo_nueva_hoja:str):
    sheet = sheet_autorizada 
    metadata = {
            'properties': {
                'title': titulo_nueva_hoja
            }
        }
    try:
        nueva_hoja = sheet.create(body=metadata,fields='spreadsheetId')
        print(f"Se creó la hoja {nueva_hoja.get('title')}. Id único: {nueva_hoja.get('spreadsheetId')}\n")
        hoja_id = nueva_hoja.get('spreadsheetId')
    except HttpError as error:
        print(f"Ocurrió un error al tratar crear la hoja {titulo_nueva_hoja}: {error}\n")
        hoja_id=None
    return hoja_id

# Leer Sheets
# PRE: Recibe: 
#       1.  sheet_autorizada    |   [TDA] objeto devuelto por el método Sheets_Build() // Arg: TDA::'service'
#       2.  sheet_id            |   [STR] id único de la hoja de cálculo sobre la cual se desea operar // Arg: str
#       3.  rango_celdas        |   [STR] rango de celdas sobre el cual se desea operar // Arg: str
# POST: [LST/BOOL/NONE] Devuelve una LISTA que contiene los valores para cada celda del rango especificado.  Devuelve FALSE si el resultado de la lectura está vacío. Devuelve NONE en caso de error.
def Sheets_Leer(sheet_autorizada,sheet_id,rango_celdas:str):
    sheet = sheet_autorizada
    try:
        result = sheet.values().get(spreadsheetId=sheet_id,range=rango_celdas).execute()
        valores = result.get('values', [])
        if not valores:
            valores = False 
    except HttpError as error:
        print(f"Ocurrió un error al tratar de leer los valores del rango {rango_celdas}, de la hoja de ID {sheet_id}: {error}\n")
        valores = None
    return valores    

#Escribir Sheets
# PRE: Recibe: 
#       1.  sheet_autorizada    |   [TDA] objeto devuelto por el método Sheets_Build() // Arg: TDA::'service'
#       2.  sheet_id            |   [STR] id único de la hoja de cálculo sobre la cual se desea operar // Arg: str
#       3.  rango_celdas        |   [STR] rango de celdas sobre el cual se desea operar // Arg: str
#       4.  data_a_escribir     |   [LST] lista (o lista de listas) que contiene los valores a escribir en cada celda del rango // Arg: lst
#       5.  modo                |   [STR] modo de escritura, "Actualizar" para sobrescribir valores existentes o "Agregar" para agregar valores nuevos. // Arg: str
# POST: [DICT/NONE] Escribe los valores entregados en el rango deseado. Printea a consola la 'request' y la devuelve. Devuelve NONE en caso de error.
def Sheets_Escribir(sheet_autorizada,sheet_id,rango_celdas,data_a_escribir,modo="Actualizar"):
    sheet = sheet_autorizada
    try:
        if modo == "Actualizar":
            request = sheet.values().update(spreadsheetId=sheet_id, range=rango_celdas, valueInputOption="USER_ENTERED", body={"values":data_a_escribir}).execute()
            print(f'Se actualizó la hoja satisfactoriamente: \n{json.dumps(request, indent=4,sort_keys=True)}\n')
        elif modo == "Agregar":
            request = sheet.values().append(spreadsheetId=sheet_id, range=rango_celdas, valueInputOption="USER_ENTERED", body={"values":data_a_escribir}).execute()
            print(f'Se agregaron los valores a la hoja satisfactoriamente:\n {json.dumps(request, indent=4,sort_keys=True)}\n')
        
    except HttpError as error:
        print(f"Ocurrió un error al tratar de escribir en la hoja de ID {sheet_id}: {error}\n")
        request = None
    return request

#Borrar Sheets
# PRE: Recibe: 
#       1.  sheet_autorizada    |   [TDA] objeto devuelto por el método Sheets_Build() // Arg: TDA::'service'
#       2.  sheet_id            |   [STR] id único de la hoja de cálculo sobre la cual se desea operar // Arg: str
#       3.  rango_celdas        |   [STR] rango de celdas sobre el cual se desea operar // Arg: str
# POST: [DICT/NONE] Borra los valores de las celdas dentro del rango deseado. Printea a consola la 'request' y la devuelve. Devuelve NONE en caso de error.
def Sheets_Borrar(sheet_autorizada,sheet_id,rango_celdas):
    try:
        sheet = sheet_autorizada
        request = sheet.values().clear(spreadsheetId=sheet_id, range=rango_celdas).execute()
        print(f'Se borraron los valores del rango indicado satisfactoriamente: \n{json.dumps(request, indent=4,sort_keys=True)}\n')
    except HttpError as error:
        print(f"Ocurrió un error al tratar de borrar los valores del rango {rango_celdas}, de la hoja de ID {sheet_id}: {error}\n")
        request = None
    return request

#Eliminar Sheets
# PRE: Recibe: 
#       1.  sheet_autorizada    |   [TDA] objeto devuelto por el método Sheets_Build() // Arg: TDA::'service'
#       2.  sheet_id            |   [STR] id único de la hoja de cálculo sobre la cual se desea operar // Arg: str
# POST: [DICT/NONE] Elimina la hoja de cálculo indicada. Printea a consola la 'request' hecha a la API y la devuelve. Devuelve NONE en caso de error.

def Sheets_Eliminar(sheet_autorizada,sheet_id): #TODO: Escribir método
    sheet = sheet_autorizada
    try:
        request =sheet.delete(spreadsheetId=sheet_id)
        print(f'Se eliminó la hoja satisfactoriamente: \n{json.dumps(request, indent=4,sort_keys=True)}\n')

    except HttpError as error:
        print(f"Ocurrió un error al tratar de eliminar la hoja de ID {sheet_id}: {error}\n")
        request = None
    print()
    return request

def main():
    pass

if __name__ == "__main__":
    main()