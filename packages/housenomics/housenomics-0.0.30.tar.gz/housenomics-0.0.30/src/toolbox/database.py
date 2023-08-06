import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Database:
    # TODO: the databasefile, must be an option of the constructor
    def __init__(self) -> None:
        try:
            sqlite_file_name = os.environ["DATABASE"]
        except KeyError:
            p = Path.home()
            p = p / "Library/Application Support/Housenomics"
            p.mkdir(parents=True, exist_ok=True)
            sqlite_file_name = str(p / "database.db")

        sqlite_url = f"sqlite:///{sqlite_file_name}"
        engine = create_engine(sqlite_url, echo=False)
        Base.metadata.create_all(engine)
        self.engine = engine

    def remove(self):
        p = Path.home()
        p = p / "Library/Application Support/Housenomics/database.db"
        p.unlink(missing_ok=True)
