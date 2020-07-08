from dotenv import load_dotenv  # Import library untuk mengakses file .env
import os  # Import library untuk mengambil variabel dari komputer
from enum import Enum  # Yang ini udah ikutin aja dulu

load_dotenv()  # Memproses file .env semudah memanggil fungsi ini aja


class GENERAL_ACCESS_TOKEN(Enum):
    DISCORD = os.getenv("ACCESS_TOKEN_DISCORD")
    YOUTUBE = os.getenv("ACCESS_TOKEN_YOUTUBE")
    GENIUS = os.getenv("ACCESS_TOKEN_GENIUS")
    RAPIDAPI = os.getenv("ACCESS_KEY_RAPIDAPI")
    MUSIXMATCH = os.getenv("ACCESS_KEY_MUSIXMATCH")
    DEVELOPERID = os.getenv("ACCESS_ID_DEVELOPER")
