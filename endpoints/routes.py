from fastapi import APIRouter, Request, Response, FastAPI
from fastapi.requests import Request
from typing import Optional
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel
from sqlalchemy import delete, select
from db.engine import engine
from db.session import SessionDep
from models.slang import Slang
from pathlib import Path
from config.setting import setting
from utils.readcsv import read_csv
from openai import OpenAI

routes = APIRouter()
templates = Jinja2Templates(directory="templates")

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=setting.CHAT_GPT_TOKEN,
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_slangs(
    session: SessionDep,
    offset: int = 0, # Start
    limit: Optional[int] = None,  # Change default to None, if None => get all
) -> list[Slang]:
    alphabet = ["А","Б","В","Г","Д","Е","Ё","Ж","З","И","Й","К","Л","М","Н","О","П","Р","С","Т","У","Ф","Х","Ц","Ч","Ш","Щ","Ъ","Ы","Ь","Э","Ю","Я"]
    # slangs = []
    # key_slangs = []
    # for char in alphabet:
    # # Build the base statement
    #     statement = select(Slang).offset(offset).where(Slang.slang[0].lower() == char)
    #     slangs = session.exec(statement).all()
    #     print(slangs)
    #     if slangs != None | []:
    #         key_slangs.append({"char": char, "slangs": slangs})
    # Получаем все сленги один раз
    all_slangs = session.exec(select(Slang)).all()

    # Группируем в словаре
    grouped = {}
    for item in all_slangs:
        first_char = item[0].slang[0].upper()
        grouped.setdefault(first_char, []).append(item)

    # Формируем итоговый список
    key_slangs = [{"char": char, "slangs": grouped.get(char.upper(), [])} for char in alphabet if char.upper() in grouped]
    first_chars = [char.upper() for char in alphabet if char.upper() in grouped]

    # Only apply limit if a value is provided
    # if limit is not None:
    #     statement = statement.limit(limit)
    #     slangs = session.exec(statement.order_by(Slang.slang)).all()
        
    return tuple([first_chars, key_slangs])

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    create_db_and_tables()
    yield
    # Shutdown: Add cleanup logic here if needed

# In 202"6", the @app.on_event("startup") decorator is considered deprecated in FastAPI.
# The modern standard is to use a lifespan context manager, which handles both startup and shutdown logic in one place.
# @routes.on_event("startup")
# def on_startup():
#     create_db_and_tables()
    
@routes.get('/')
def home(request: Request, session: SessionDep):

    # path = Path().resolve() / "static" / "csv" / "data.csv"
    # data = read_csv(path)
    # session.exec(delete(Slang)) # delete all
    # for item in data:
    #     slang = Slang(**item)
    #     session.add(slang) # add one
    #     session.commit() # commit
    #     session.refresh(slang) #Expire and refresh attributes on the given instance.

    first_chars, key_slangs = get_slangs(session=session) # Get all

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "fisrt_chars": first_chars,
            "key_slangs": key_slangs,
        }
    )

@routes.post("/chat")
async def chat_llm(request: Request, response: Response):
    req = await request.json()
    message = req.get("message", "")

    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b:groq",
        messages=[
            {
                "role": "user",
                "content": f"{message}"
            }
        ],
    )

    response.status_code = 200

    return {"response": completion.choices[0].message.content}

# @routes.get("/items/{id}", response_class=HTMLResponse)
# async def read_item(request: Request, id: str):
#     return templates.TemplateResponse(
#         request=request, name="item.html", context={"id": id}
#     )
