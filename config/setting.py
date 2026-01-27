from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Setting(BaseSettings):
    APP_NAME: str = "Young Slang Web"
    ADMIN_EMAIL: str = "daomanhduong02112005@gmail.com"
    ITEMS_PER_USER: int = 50
    SQL_FILE_NAME: str = "database.db"
    CHAT_GPT_TOKEN: str
    model_config = SettingsConfigDict(env_file=".env", extra='allow')

# Using @lru_cache lets you avoid reading the dotenv file again and again for each request, while allowing you to override it during testing.
# we would create that object for each request, and we would be reading the .env file for each request. ⚠️
# But as we are using the @lru_cache decorator on top, the Settings object will be created only once, the first time it's called. ✔️

@lru_cache
def get_setting():
    return Setting()

setting = get_setting()
