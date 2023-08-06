from setuptools import setup, find_packages

setup(
    name='Goog_API',
    description="Librería Python con métodos para las APIs de Google. Docs, Sheets, Drive, Gmail y Calendar. Desarrollada por Hernán A. Teszkiewicz Novick, para el equipo dev. de Ch'aska.",
    version='0.22',
    author           = 'Hernán A. Teszkiewicz Novick',
    author_email     = 'herni@cajadeideas.ar',
    license          =  'MIT'    ,
    url= 'https://github.com/Chaska-de-ideas/Goog_API',
    download_url     =  'https://github.com/Chaska-de-ideas/Goog_API/raw/main/dist/Goog_API-0.22.tar.gz',
    packages=['Goog_API'],
    install_requires=[
        'google-api-python-client',
        'google-auth',
        'google-auth-oauthlib',
        'google-auth-httplib2',
        'requests',
    ],
    extras_require ={
    'Goog_API_Sheets_Metodos': ['pandas'],
    'Goog_API_gMail_Metodos': ['mimetypes','email','base64'],
    'Goog_API_Calendar_Metodos': ['datetime'],
    
    },
)
