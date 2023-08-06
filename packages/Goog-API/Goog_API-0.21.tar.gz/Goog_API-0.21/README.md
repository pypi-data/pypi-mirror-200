
# Librería `Goog_API` para Python.

La librería Goog_API es una herramienta de Python que permite interactuar con las distintas APIs de Google a través de métodos personalizados que simplifican las tareas más comunes que un script puede solicitar a las diversas APIs de Google. Los módulos incluidos en esta librería son específicos para las aplicaciones de Docs, Sheets, Drive, Gmail y Calendar.

*La librería fue desarrollada por Hernán A. Teszkiewicz Novick, para el equipo dev. de [Ch'aska](https://cajadeideas.ar) y está disponible para su uso y distribución bajo [**LICENCIA MIT**](https://github.com/Chaska-de-ideas/Goog_API/blob/main/LICENCE.TXT)*


## Módulos 
La librería incluye los siguientes módulos:

* Goog_API_Drive_Metodos
* Goog_API_Sheets_Metodos
* Goog_API_Docs_Metodos
* Goog_API_gMail_Metodos
* Goog_API_Calendar_Metodos


Además, la librería incluye un método general, `Goog_API_Build`, que permite autenticar la conexión con la API de Google. Este método utiliza los métodos propios de autenticación de cada módulo específico de la aplicación.

### Prerequisitos y configuración de la API
Antes de utilizar esta librería, Ud. debe realizar las siguientes configuraciones preliminares:

1. Crear una cuenta de servicio en la [Google Cloud Console](https://console.cloud.google.com/);
2. Crear un **`PROYECTO`** y habilitar las **`APIs`** y los **`SCOPES`** que desea utilizar;
3. Crear una *`'Cuenta de Servicio'`* y otorgarle acceso a los documentos con los que se desea operar.   ***Ver más: [**Documentación de Cuentas de Servicio**](https://cloud.google.com/iam/docs/service-account-overview?hl=es-419)***; y
4. Descargar el archivo de credenciales de su cuenta de *`'Cuenta de Servicio'`* en formato **`JSON`**; y

>Nota: El método de autenticación que utilizan TODOS los módulos de esta librería es el método `service_account.Credentials.from_service_account_file()`. Un método propio de la API de Google que permite crear credenciales de autenticación a partir de un archivo JSON que contiene la información necesaria para la conexión a la API. Para poder utilizar correctamente esta librería Ud. deberá configurar la Cuenta de Servicio [^1].


### Instalación
Ud. puede optar por instalar la librería completa o sólo alguno de sus módulos.

>Tenga en cuenta que si Ud. decide instalar sólo algunos de sus módulos, puden surgir errores al intentar  instalar las dependencias que el paquete necesita para funcionar. Se recomienda realizar previamente la instalación manual, aunque no sea estrictamente necesario.

#### Métodos de instalación:

#### a.1 Toda la librería (Automático)
Puede instalar la librería completa desde la web utilizando `PIP`, según se indica a continuación:
1.  **Ejecute** el siguiente comando en la `terminal`:

``` Bash
pip install Goog_API
``` 

#### a.2 Toda la librería (Manual)
Puede instalar la librería completa a partir del paquete `.tar.gz` utilizando `PIP`, según se indica a continuación:
1. **Descargue** el archivo [**`Goog_API-0.2.tar.gz`**](https://github.com/Chaska-de-ideas/Goog_API/raw/main/dist/Goog_API-0.2.tar.gz)
2.  **Ejecute** el siguiente comando en la `terminal`:

``` Bash
pip install /ruta/al/archivo/Goog_API-02.tar.gz
``` 

#### b. Módulos particulares
1.  Antes de utilizar cualquiera de los módulos, es recomendable que Ud. instale las siguientes librerías de Python:

    * google-api-python-client  
    * google-auth  
    * google-auth-oauthlib
    * google-auth-httplib2
    * requests

    ##### Estas librerías se pueden instalar utilizando `PIP`:
``` Bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client requests
```

2. Luego, deberá instalar el módulo que desea agregando al comando `PIP` el sufijo `#egg` para indicar el módulo correspondiente:

```Bash
pip install /ruta/al/archivo/Goog_API.tar.gz#egg=Goog_API[Goog_API_Sheets_Metodos]
```
>*Ejemplo de instalación del Módulo **`Sheets_Metodos`***

***

## Método General `Goog_API_Build()`:
```Python
Goog_API_Build(archivo_credenciales,app,gMail_Build_Mail_envio=None)
```
>El método **`Goog_API_Build()`** se utiliza para construir y devolver un objeto de clase service autenticado por la API de Google especificada, utilizando los métodos de autenticación propios de cada uno de los módulos específicos de la librería.

**Recibe:**
* **STR `archivo_credenciales`**: Ruta al archivo de credenciales [**JSON**] descargado de la [Google Cloud Console](https://console.cloud.google.com/).
* **STR `app`** : Nombre de la aplicación de Google (Sheets, Docs, gMail, Calendar o Drive) para la que se desea crear el objeto de clase service.
* **STR `gMail_Build_Mail_envio`** (*opcional*): Dirección de correo electrónico para la aplicación gMail. *Se utilizará como dirección de envío predeterminada en el método gMail_Build().* Por defecto es `None`.

**Devuelve:**
* **TDA `app_autenticada`**: Objeto de clase service autenticado por la API de Google especificada. Este objeto se puede utilizar para interactuar con la API de Google correspondiente.


##### Ejemplo de Uso
```python
from Goog_API import Goog_API_Build

archivo_credenciales = 'ruta/al/archivo/creds.json'
app = 'Sheets'
sheet_autorizada = Goog_API_Build(archivo_credenciales,app)

```

***

## Módulo `Drive_Metodos` de Goog_API para Python
Este módulo proporciona métodos para interactuar con la API de Google Drive y realizar operaciones como crear carpetas, documentos y hojas de cálculo en Google Drive.

### Métodos:

#### 1. Método `Drive_Build()` :
```python
Drive_Build(archivo_credenciales)
```
>Método que construye y devuelve un objeto de servicio de Google Drive con credenciales autorizadas a partir del archivo de credenciales proporcionado.

**Recibe:**
* **STR `archivo_credenciales` :** Ruta al archivo de credenciales [**JSON**] descargado de la [Google Cloud Console](https://console.cloud.google.com/).

**Devuelve:**
* **TDA `drive_autenticado` :** objeto de servicio autorizado de Google Drive.

#### 2. Método `Drive_crear_carpeta()` :
```python
Drive_crear_carpeta(drive_autenticado, nombre:str, id_carpeta_padre:str=None)
```
>Método que crea una carpeta en Google Drive y devuelve su ID único. Si se especifica un ID de carpeta principal, la carpeta se creará como una subcarpeta de aquella.

**Recibe:**
* **TDA `drive_autenticado` :** objeto de servicio autorizado de Google Drive, devuelto por el método Drive_Build()
* **STR `nombre` :** nombre de la carpeta que se creará.
* **STR `id_carpeta_padre` (opcional) :**  el ID de la carpeta padre donde se creará la carpeta. Por defecto es `None`.
* **STR `compartir_gmail` (opcional) :** cuenta de gMail que se desea sea 'editor' de la carpeta. Por defecto es `None`.
* **BOOL `es_publica` (opcional) :** define si la carpeta es pública para la lectura. Por defecto es `True`.

**Devuelve:**
* **STR `carpeta_id`:** el ID único de la carpeta creada.
>Nota: Si Ud. no comparte la carpeta o no la crea como 'hija' de una carpeta con permisos previamente determinados, deberá mantenerla pública para la lectura, caso contrario solo será accesible para la 'cuenta de servicio' con la que fue creada.

#### 3. Método `Drive_crear_doc_en_carpeta()` :
```python
Drive_crear_doc_en_carpeta(drive_autenticado, nombre:str, carpeta_id:str)
```
>Método que crea un documento en una carpeta existente en Google Drive.

**Recibe:**
* **TDA `drive_autenticado` :** objeto de servicio autorizado de Google Drive, devuelto por el método Drive_Build()
* **STR `nombre` :** nombre del documento que se creará.
* **STR `carpeta_id` :**  el ID de la carpeta padre donde se creará el documento.

**Devuelve:**
* **STR   `doc_id`** : ID único del documento creado.


#### 4. Método `Drive_crear_sheet_en_carpeta()` :
```python
Drive_crear_sheet_en_carpeta(drive_autenticado, nombre:str, carpeta_id:str)
```
>Método que crea una hoja de cálculo en una carpeta existente en Google Drive.

**Recibe:**
* **TDA `drive_autenticado` :** objeto de servicio autorizado de Google Drive, devuelto por el método Drive_Build()
* **STR `nombre` :** nombre del documento que se creará.
* **STR `carpeta_id` :**  el ID de la carpeta padre donde se creará la hoja de cálculo.

**Devuelve:**
* **STR   `sheet_id`** : ID único de la hoja de cálculo creada.

#### 5. Método `Drive_subir_archivo()` :
```python
Drive_subir_archivo(drive_autenticado,archivo_a_subir:str,nombre_del_archivo:str,convertir_archivo:bool=True,carpeta_id:str=None)
```
>Método que sube un archivo a Google Drive y devuelve su ID único. Si se especifica un ID de carpeta, el archivo se creará como un archivo en esa carpeta.

**Recibe:**
* **TDA `drive_autenticado`** : objeto de servicio autorizado de Google Drive, devuelto por el método `Drive_Build()`
* **STR `archivo_a_subir`** : ruta al archivo que se desea subir
* **STR `nombre_del_archivo`** : nombre del archivo que se desea subir
* **STR `carpeta_id`** (*opcional*) : el ID de la carpeta donde se subirá el archivo. Por defecto es `None`.

**Devuelve:**
* **STR `ID_Archivo_subido`**: el ID único del archivo subido.
>Nota: Si no se especifica el ID de una carpeta, el archivo se subirá en la carpeta raíz de la cuenta de servicio utilizada para la autenticación.

##### Ejemplo de uso:
```python
# Importación del módulo personalizado
from Goog_API_Drive_Metodos import *

# Definición de la ruta del archivo de credenciales
archivo_credenciales = 'ruta/al/archivo/creds.json'

# Construcción del servicio de Google Drive
drive = Drive_Build(archivo_credenciales)

# Creación de una carpeta en Google Drive
nombre_carpeta = 'Ejemplo Carpeta'
carpeta_id = Drive_crear_carpeta(drive, nombre_carpeta)

# Creación de un documento en la carpeta creada anteriormente
nombre_documento = 'Ejemplo Documento'
doc_id = Drive_crear_doc_en_carpeta(drive, nombre_documento, carpeta_id)

# Creación de una hoja de cálculo en la carpeta creada anteriormente
nombre_sheet = 'Ejemplo Sheet'
sheet_id = Drive_crear_sheet_en_carpeta(drive, nombre_sheet, carpeta_id)

# Impresión de los IDs de la carpeta, documento y hoja de cálculo creados
print(f'La carpeta "{nombre_carpeta}" fue creada con el ID "{carpeta_id}"')
print(f'El documento "{nombre_documento}" fue creado con el ID "{doc_id}"')
print(f'La hoja de cálculo "{nombre_sheet}" fue creada con el ID "{sheet_id}"')
```

***


## Módulo `Sheets_Metodos` de Goog_API para Python
Este módulo proporciona métodos de lectura, escritura y eliminación para interactuar con la API de Google Sheets en Python.

* `Sheets_Build`. Método para autenticar frente a la API.
* `Sheets_Crear`. Método para crear hojas de cálculo.
* `Sheets_Leer`. Método para leer valores de celdas/rangos de hojas de cálculo
* `Sheets_Escribir`. Método escribir valores a celdas/rangos de hojas de cálculo
* `Sheets_Borrar`. Método para borrar valores de celdas/rangos de hojas de cálculo

### Métodos:  
#### 1. Método `Sheets_Build()` :
``` Python
Sheets_Build(archivo_credenciales)
```
>Método que realiza la autenticación en la API de Sheets de Google utilizando el archivo de credenciales en formato JSON de la Cuenta de Servicio habilitada.

**Recibe:**
* **STR `archivo_credenciales` :** Ruta al archivo de credenciales [**JSON**] descargado de la [Google Cloud Console](https://console.cloud.google.com/).

**Devuelve:**
* **TDA `sheet_autorizada` :** Objeto de clase ***'service.spreadsheets'***. representa la conexión autorizada con la API de Sheets de Google.


#### 2. Método `Sheets_Crear()` :
```Python
Sheets_Crear(sheet_autorizada: service, titulo_nueva_hoja: str)
```
>Método que crea una nueva hoja de cálculo y devuelve su ID único identificador.
>>*Nota: Este método crea una hoja de cálculo en la carpeta raiz 'Mi Unidad' de la cuenta en la que fue autorizado. Si Ud. desea crear la hoja de cálculo en una carpeta específica, deberá usar en su lugar el método **`Drive_crear_sheet_en_carpeta()`** del módulo **`Drive_Metodos`** de esta misma librería.*

**Recibe:**
* **TDA `sheet_autorizada` :** Objeto "service" previamente construido con el método `Sheets_Build()`.
* **STR `titulo_nueva_hoja` :** Título deseado para la nueva hoja.

**Devuelve:**
* **STR `sheet_id` :** ID único identificador de la nueva hoja creada. Devuelve `None` en caso de error.

#### 3. Método `Sheets_Leer()` :
``` Python
Sheets_Leer(sheet_autorizada, sheet_id, rango_celdas)
```
>Método que devuelve una lista que contiene los valores para cada celda del rango especificado en la hoja de cálculo con el ID proporcionado.

**Recibe:**
* **TDA   `sheet_autorizada`** : Objeto devuelto por el método `Sheets_Build()`.
* **STR   `sheet_id`** : ID único de la hoja de cálculo sobre la cual se desea operar.
* **STR `rango_celdas`** : Rango de celdas sobre el cual se desea operar.

**Devuelve:**
* **LISTA `valores`** : Lista que contiene los valores para cada celda del rango especificado. Devolverá **`FALSE`** si el resultado de la lectura fuera una **lista vacía**. 


#### 4. Método `Sheets_Escribir()` :
``` Python
Sheets_Escribir(sheet_autorizada, sheet_id, rango_celdas, data_a_escribir, modo="Actualizar")
```
>Método que escribe los datos proporcionados en el rango de celdas especificado en la hoja de cálculo con el ID proporcionado. El modo de escritura puede ser "Actualizar" o "Agregar".

**Recibe:**    
* **TDA   `sheet_autorizada`** : Objeto devuelto por el método `Sheets_Build()`.
* **STR   `sheet_id`** : ID único de la hoja de cálculo sobre la cual se desea operar.
* **STR `rango_celdas`** : Rango de celdas sobre el cual se desea operar.
* **LISTA `data_a_escribir`**: Lista que contiene los datos que se escribirán en la hoja de cálculo.
* **STR `modo`** : Modo de escritura, `"Actualizar"` para sobrescribir los valores existentes en el rango o celda deseados o `"Agregar"` para agregar valores nuevos, en las filas vacías inmeditamente siiguientes al rango declarado.

**Devuelve:**
* **DICT `request` :** diccionario con la información de la respuesta del servidor de la API de Sheets a la solicitud de escritura.

#### 5. Método `Sheets_Borrar()` :
``` Python
Sheets_Borrar(sheet_autorizada, sheet_id, rango_celdas)
``` 
>Método que borra los valores de las celdas dentro del rango especificado en la hoja de cálculo con el ID proporcionado.

**Recibe:**    
* **TDA   `sheet_autorizada`** : Objeto devuelto por el método `Sheets_Build()`.
* **STR   `sheet_id`** : ID único de la hoja de cálculo sobre la cual se desea operar.
* **STR `rango_celdas`** : Rango de celdas sobre el cual se desea operar.

**Devuelve:**
* **DICT `request` :** diccionario con la información de la respuesta del servidor de la API de Sheets a la solicitud de borrado.

#### Ejemplo de uso:
```python
from .Goog_API_Sheets_Metodos import Sheets_Build,Sheets_Crear,Sheets_Escribir,Sheets_Leer

# Autenticar y autorizar el cliente de Sheets
sheet_autorizada = Sheets_Build("ruta/al/archivo_credenciales/creds.json")

# Crear la hoja de cálculo
sheet_id = Sheets_Crear(sheet_autorizada,"Nueva_Hoja_de_Calculo")

# Crear una lista con datos a escribir
data_a_escribir=[
    ["Empleados","Salario"],
    ["Juan",150000],
    ["José",285000],
    ["Homero",372000]
]

#Escribir data a la hoja, a partir de la celda A1 de la Hoja 1.
Sheets_Escribir(sheet_autorizada, sheet_id,"'Hoja 1'!A1", data_a_escribir, modo="Actualizar")

#Leer y printear la data que se escribrió en el rango A1:B4 de la Hoja 1.
tabla_salarios = Sheets_Leer(sheet_autorizada, sheet_id,"'Hoja 1'!A1:B4")
print(tabla_salarios)
```

***

## Módulo `Docs_Metodos` de Goog_API para Python
Este módulo proporciona métodos para interactuar con la API de Google Docs.

### Métodos:
#### 1. Método `Docs_Build()`:
```Python
Docs_Build(archivo_credenciales)
```
>Método que realiza la autenticación en la API de Docs de Google utilizando el archivo de credenciales en formato JSON de la Cuenta de Servicio habilitada.

**Recibe:**
* **STR `archivo_credenciales` :** Ruta al archivo de credenciales [**JSON**] descargado de la [Google Cloud Console](https://console.cloud.google.com/).

**Devuelve:**
* **TDA `doc_autorizado` :** Objeto de clase ***'service.documents'***. representa la conexión autorizada con la API de Docs de Google.

#### 2. Método `Docs_Crear()`:
```Python
Docs_Crear(doc_autorizado, titulo_nuevo_doc)
```
>Método que crea un nuevo documento de Google Docs y devuelve el ID único identificador del documento creado.
>>*Nota: Este método crea un documento en la carpeta raiz 'Mi Unidad' de la cuenta en la que fue autorizado. Si Ud. desea crear el documento en una carpeta específica, deberá usar en su lugar el método **`Drive_crear_doc_en_carpeta()`** del módulo **`Drive_Metodos`** de esta misma librería.*

**Recibe:**
* **TDA `doc_autorizado` :**  Objeto "service" previamente construido con el método `Docs_Build()`.
* **STR `titulo_nuevo_doc` :** Título que se desea dar al nuevo documento.

**Devuelve:**
* **STR `doc_id` :** ID único identificador del documento creado. Devuelve None en caso de error.

#### 3. Método `Docs_Escribir()`:
```Python
Docs_Escribir(doc_autorizado, doc_id, texto_a_escribir)
```
>Método que agrega texto a un documento de Google Docs.

**Recibe**
* **TDA `doc_autorizado` :** Objeto de clase 'service' autenticado por la API.
* **STR `doc_id` :** ID único identificador del documento.
* **STR `texto_a_escribir` :** Texto que desea agregar al documento.

**Devuelve**
* **DICT `response` :** Respuesta de la API a la solicitud batchUpdate. Devuelve None en caso de error.

#### 4. Método `Docs_Leer()`:
```Python
Docs_Leer(doc_autorizado, doc_id)
```
>Método que lee texto de un documento de Google Docs.

**Recibe**
* **TDA `doc_autorizado` :** Objeto de clase 'service' autenticado por la API.
* **STR `doc_id` :** ID único identificador del documento.

**Devuelve**
* **STR `texto_contenido` :** contenido del documento. Devuelve None en caso de error.


##### Ejemplo de uso
```Python
from Goog_API_Docs_Metodos import *

# Archivo de credenciales de la cuenta de serivio
archivo_credenciales = 'ruta/al/archivo/creds.json'

# Construir el 'service' con el método Docs_Build
doc_autorizado = Docs_Build(archivo_credenciales)

# Crear un nuevo documento en blanco
titulo_nuevo_doc = 'Nuevo documento de prueba'
doc_id = Docs_Crear(doc_autorizado, titulo_nuevo_doc)

# Escribir en el documento recién creado
texto_a_escribir = 'Este texto de prueba fue creado con la librería Goog_API de Python'
Docs_Escribir(doc_autorizado, doc_id, texto_a_escribir)

# Imprimir el texto del documento.
print(Docs_Leer(doc_autorizado, doc_id))

```

***

## Módulo `gMail_Metodos` de Goog_API para Python 
Este módulo contiene una serie de métodos para crear correos electrónicos y enviarlos con la API de Gmail de Google.

### Métodos:
#### 1. Método `gMail_Build()` :
``` Python
gMail_Build(archivo_credenciales,mail_envio)
```
>Método que crea una instancia de la API de Gmail de Google y devuelve un objeto autorizado para enviar correos electrónicos desde la cuenta especificada.

**Recibe:**   
* **STR `archivo_credenciales` :** Ruta al archivo de credenciales [**JSON**] descargado de la [Google Cloud Console](https://console.cloud.google.com/).
* **STR `mail_envio` :** Correo electrónico del usuario que se desea figure como remitente.

**Devuelve:**
* **TDA `gmail_autorizado` :** Objeto de clase ***'service'*** que representa la conexión autorizada con la API de Gmail de Google.

#### 2. Método `Crear_Correo()` :
```Python
Crear_Correo(mail_envio, mail_destinatario, asunto, cuerpo)
```
>Método que crea y devuelve un objeto 'EmailMessage' con los campos especificados.

**Recibe:** 
* **STR `mail_envio` :** Dirección de correo electrónico que se utilizará como remitente.
* **STR `mail_destinatario` :** Dirección de correo electrónico del destinatario.
* **STR `asunto` :** El asunto del correo electrónico.
* **STR `cuerpo` :** El cuerpo del correo electrónico.

**Devuelve:**
* **TDA `mensaje` :** Un objeto 'EmailMessage' con los campos especificados.

#### 3. Método `Anadir_Adjunto()` :
```Python
Anadir_Adjunto(mensaje, ruta_adjunto)
```
>Método que agrega un archivo adjunto al objeto EmailMessage especificado.

**Recibe:**
* **TDA `mensaje` :** Un objeto 'EmailMessage' al cual se adjuntará el archivo especidicado
* **STR `ruta_adjunto` :** Ruta del archivo adjunto a agregar.

**Devuelve:**
* **TDA `mensaje` :** El objeto **'EmailMessage'** con el archivo adjunto


#### 4. Método `Crear_Correo_JSON()` :
```Python
Crear_Correo_JSON(archivo_correo, mail_envio)
```
>Método que crea y devuelve un objeto **'EmailMessage'** a partir de un archivo JSON que contiene los campos del correo electrónico.

**Recibe:**
* **STR `archivo_correo` :** Ruta al archivo JSON que contiene los campos del correo electrónico.
* **STR `mail_envio` :** Dirección de correo electrónico que se utilizará como remitente.

**Devuelve:**
* **TDA `mensaje` :** Un objeto 'EmailMessage' con los campos especificados.

##### Ejemplo de archivo JSON para el metodo Crear_Correo_JSON:
```JSON
{
    "Destinatario":"correo@dominio.com",
    "Asunto":"Prueba Mail Automatico v5",
    "Mensaje":"Este es un mail de prueba enviado automaticamente, debiera incluir el archivo 'hola.txt' y 'mundo.jpg'",
    "Adjuntos":["ruta/alArchivo/hola.txt","ruta/alArchivo/mundo.jpg"]
}
```

#### 4. Método `Encriptar_Correo()` : 
```Python
Encriptar_Correo(mensaje)
```
>Método que recibe como entrada un mensaje de correo electrónico en formato **EmailMessage**, lo encripta usando el algoritmo base64 como se indica en la documentación de la API de Gmail, y devuelve el mensaje encriptado en un diccionario con una clave raw.

**Recibe:**
* **TDA `mensaje` :** mensaje de correo electrónico en formato **'EmailMessage'**.

**Devuelve:**
* **DICT `mensaje_64` :** diccionario que contiene el mensaje de correo electrónico encriptado, con la clave raw.

#### 5. Método `gMail_Enviar()` : 
```Python
gMail_Enviar(gmail_autorizado, mensaje_64)
```
>Método que envía el mensaje de correo electrónico al destinatario correspondiente.

**Recibe:**
* **TDA `gmail_autorizado` :** Objeto de clase ***'service'*** que representa la conexión autorizada con la API de Gmail de Google.
* **DICT `mensaje_64` :** diccionario que contiene el mensaje de correo electrónico encriptado, con la clave raw.

**Devuelve:**
* **DICT `enviar_mensaje` :** diccionario con la información de la respuesta del servidor de la API gMAil a la solicitud de envío del mensaje  enviado.

#### Ejemplo de uso:
```python
from Goog_API_gMail_Metodos import gMail_Build,Crear_Correo,Anadir_Adjunto,Encriptar_Correo,gMail_Enviar

# Autenticar y autorizar el cliente de Gmail
gmail_autorizado = gMail_Build("ruta/al/archivo_credenciales/creds.json", "remitente@dominio.com")

# Crear el mensaje de correo electrónico
mensaje = Crear_Correo("remitente@dominio.com", "mail@destinatario.com", "Mail de Prueba", "Este es un mail de prueba generado automáticamente")

# Adjuntar archivo al mensaje
mensaje_con_adj = Anadir_Adjuntos(mensaje,"ruta/al/archivo/holaMundo.txt")

# Encriptar el mensaje de correo electrónico
mensaje_encriptado = Encriptar_Correo(mensaje_con_adj)

# Enviar el mensaje de correo electrónico
enviar_mensaje = gMail_Enviar(gmail_autorizado, mensaje_encriptado)
```

***

## Módulo `Calendar_Metodos` de Goog_API para Python 
Este módulo proporciona métodospara interactuar con la API de Google Calendar y realizar operaciones como crear un nuevo calendario o un nuevo evento en un calendario.


### Métodos: 

#### 1. Método `Calendar_Build()` :
``` Python
Calendar_Build(archivo_credenciales)
```
>Método que construye y retorna un objeto 'servie'->calendar autorizado para realizar operaciones en la API de Google Calendar. Para ello se utiliza el archivo de credenciales (JSON) descargado de la Google Cloud Console.

**Recibe:**   
* **STR `archivo_credenciales` :** Ruta al archivo de credenciales [**JSON**] descargado de la [Google Cloud Console](https://console.cloud.google.com/).
**Devuelve:**
* **TDA `calendar_autorizado` :** Objeto de clase ***'service'*** que representa la conexión autorizada con la API de Calendar de Google.


#### 2. Método `Calendar_Crear()` :
``` Python
Calendar_Crear(calendar_autorizado,Titulo_del_Calendario,TZ="America/Argentina/Buenos_Aires")
```
>Método que crea un nuevo calendario en la cuenta de Google Calendarautenticada, y devuelve su identificador.

**Recibe:**
* **TDA `calendar_autorizado` :** Objeto de clase ***'service'*** que representa la conexión autorizada con la API de Calendar de Google.
* **STR `Titulo_del_Calendario` :** Título que se le dará al calendario.

**Devuelve:**
* **STR `CALENDAR_ID` :** ID único de identificación del calendario creado.



#### 3. Método `Crear_Evento()` :
``` Python
Crear_Evento(Titulo, Descripcion, Fecha_Inicio, Fecha_Fin)
```
>Método que crea y retorna un diccionario con los datos necesarios para crear un nuevo evento en un calendario de Google.

**Recibe:**   
* **STR `Titulo` :** el título del evento.
* **STR `Descripción` :**  la descripción del evento.
* **STR `Fecha_Inicio` :**  la fecha y hora de inicio del evento **en formato [ISO 8601](https://es.wikipedia.org/wiki/ISO_8601).**
* **STR `Fecha_Fin` :** la fecha y hora de finalización del evento **en formato [ISO 8601](https://es.wikipedia.org/wiki/ISO_8601).**

**Devuelve:**
* **DICT `Evento` :** Un diccionario con los datos del evento.


#### 4. Método `Calendar_Nuevo_Evento()` :
```Python
Calendar_Nuevo_Evento(calendar_autorizado, evento, CALENDAR_ID)
```
>Método que crea un nuevo evento en un calendario de Google utilizando el objeto calendar_autorizado y los datos del evento proporcionados en un diccionario.

**Recibe:** 
* **TDA `calendar_autorizado` :** Objeto de clase ***'service'*** que representa la conexión autorizada con la API de Calendar de Google. Creado con el método `Calendar_Build()`.
* **DICT `Evento` :** En diccionario con los datos del evento creado con el método `Crear_Evento()`.
* **STR `CALENDAR_ID` :** el ID del calendario en el que se creará el evento.

**Devuelve:**
* **DICT `evento_creado` :** diccionario con la información de la respuesta del servidor de la API de Calendar a la solicitud de creación del evento.



#### 5. Método `Calcular_Fechas()` :
```Python
Calcular_Fechas(ano, mes, dia, hora_inicio, duracion)
```
>Método para calcular la fecha y hora de inicio y fin de un evento en formato [ISO 8601](https://es.wikipedia.org/wiki/ISO_8601) requerido por la API de Google Calendar. 

**Recibe:**
* **INT `ano` :** el año de la fecha de inicio del evento.
* **INT `mes` :** el mes de la fecha de inicio del evento.
* **INT `dia` :** el día de la fecha de inicio del evento.
* **STR `hora_inicio` :** la hora de inicio del evento **en formato HH:MM.**
* **STR `duracion` :**  la duración del evento **en formato HH:MM.**

**Devuelve:**
* **STR `Fecha_Inicio` :** Fecha de inicio del evento **en formato [ISO 8601](https://es.wikipedia.org/wiki/ISO_8601).**
* **STR `Fecha_Fin` :** Fecha de finalización del evento **en formato [ISO 8601](https://es.wikipedia.org/wiki/ISO_8601).**

#### Ejemplo de uso:
```Python
from Goog_API_Calendar_Metodos import Calendar_Build,Crear_Calendario,Crear_Evento,Calendar_Nuevo_Evento,Calcular_Fechas

#Autorización frente a la API
calendar_autorizado = Calendar_Build('ruta/al/archivo/credenciales.json')

#Cración de nuevo calendario y recupero de ID.
CALENDAR_ID = Crear_Calendario(calendar_autorizado,"Calendario de Prueba")


#Cálculo de fechas del evento
Fecha = Calcular_Fechas(2023,4,1,"17:30","01:30")[0]
Fecha_i = Fecha[0]
Fecha_f = Fecha[1]

#Formación del diccionario con la información del evento
evento = Crear_Evento('Reunión de Prueba', 'Descripción de la Reunión de Prueba',Fecha_i, Fecha_f)

#Creación del evento en el calendario
Calendar_Nuevo_Evento(calendar_autorizado, evento, CALENDAR_ID)

```

***

[^1]: **Pasos a seguir para crear su *`'Cuenta de Servicio'`*:**
    >1. **Acceder a la Consola de Google Cloud:** Acceda a la Consola de Google Cloud en https://console.cloud.google.com/ e inicie sesión con su cuenta de Google.
    >2. **Crear un nuevo proyecto:** Si aún no tiene un proyecto, deberá creaar uno nuevo haciendo clic en "Seleccionar Proyecto" en la parte superior de la pantalla y luego haciendo clic en "Nuevo proyecto".
    >3. **Habilitar la API que desea utilizar:** Haga clic en "Explorar y habilitar APIs" en la parte superior de la pantalla y busque la API que deseas utilizar. Haga clic en ella y luego haga clic en "Habilitar".
    >4. **Crear una *`'Cuenta de Servicio'`*:** En el panel de navegación de la izquierda, haga clic en "IAM y administración" y luego en "Cuentas de servicio". Haga clic en "Crear cuenta de servicio" y proporcione un nombre y una descripción para la cuenta de servicio. Haga clic en "Crear".
    >5. **Configurar los permisos:** Una vez creada la cuenta de servicio, seleccione la cuenta de servicio en la lista y haga clic en "Agregar rol" para agregar permisos. Elija los roles que desea otorgar a la cuenta de servicio y haga clic en "Guardar".
    >6. **Generar la clave privada:** Haga clic en la cuenta de servicio que acaba de crear y luego vaya en la pestaña "Claves". Haga clic en "Agregar clave" y elija "Crear nueva clave". Elija "JSON" como tipo de clave y créela. Se descargará un archivo JSON con las credenciales de la cuenta de servicio.
        >>***Ese archivo JSON es el que usarán todos los métodos _Build() de esta librería para autenticarse frente a la API***
    >7. **Compartir directorios y archivos con la *`'Cuenta de Servicio'`*:** Si Ud. desea operar sobre directorios o archivos previamente existentes, es decir que no fueran creados por la cuenta de servicio utilizando los métodos de esta librería, Ud. deberá otorgar acceso de edición a la cuenta de servicio para cada uno de esos directorios. 

