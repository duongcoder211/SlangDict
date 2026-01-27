from typing import Annotated
from sqlmodel import Session
from fastapi import Depends
from .engine import engine
from sqlalchemy.orm import sessionmaker

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# # Create a session factory
# SessionLocal = sessionmaker(bind=engine)

# # Get a session whenever you need one
# session = SessionLocal()

# try:
#     # Perform operations
#     new_entry = Slang(slang='no cap', mean='truthfully')
#     session.add(new_entry)
#     session.commit()
# finally:
#     # Always manually close if not using a context manager
#     session.close()