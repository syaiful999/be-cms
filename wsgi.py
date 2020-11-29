''' Root App '''
import os
from pathlib import Path
from dotenv import load_dotenv
from app import app

envPath = Path("app/env/.env")
load_dotenv(envPath)
port = os.getenv("SERVER_PORT")
debug = os.getenv('DEBUG_SERVER') == 'true'
if __name__ == '__main__':
    app.run(port=port, debug=debug)
