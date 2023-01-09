import os
from pathlib import Path
from dotenv import load_dotenv
import base64

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
token = os.environ['TOKEN']
token = base64.b64encode(token.encode('ascii')).decode('utf8')
