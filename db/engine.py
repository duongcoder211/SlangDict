from sqlmodel import create_engine
from config.setting import setting

sqlite_url = f"sqlite:///{setting.SQL_FILE_NAME}"

connect_args = {"check_same_thread": False}

engine = create_engine(sqlite_url, connect_args=connect_args)
