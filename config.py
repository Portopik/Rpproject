import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("8791714575:AAGf3wfNAmY3Cu7lYozYI2TSwwa8mX0oH0A")

# Папка с документами
DOCUMENTS_PATH = "documents"

# Ограничение по флуду (секунды)
RATE_LIMIT = 5
