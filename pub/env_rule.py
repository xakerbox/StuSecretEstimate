import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

dotenv_path = Path('/Users/vladimirkuzin/StuProj/Vlad3ServREST/.env')
load_dotenv(dotenv_path=dotenv_path)

ENV = os.getenv('ENVIRONMENT')

if ENV == 'PROD':
    path_to_logo = '/app/pub/images'
    path_to_pdf = '/app/pub/estimate_reports'
if ENV == 'DEV':
    path_to_logo = '/Users/vladimirkuzin/StuProj/Vlad3ServREST/pub/images'
    path_to_pdf = '/Users/vladimirkuzin/StuProj/Vlad3ServREST/pub/estimate_reports'