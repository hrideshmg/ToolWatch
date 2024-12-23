from sqlalchemy import create_engine, Column, Integer, Boolean, TIMESTAMP, Text, String
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, mapped_column
from sqlalchemy import ForeignKey

import datetime
from config import config

engine = create_engine(config["MARIADB_URI"])
Session = sessionmaker(bind=engine)
Base = declarative_base()  # Use declarative_base from sqlalchemy.orm


class Tool(Base):
    __tablename__ = "tools"
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    title = Column(Text)
    description = Column(Text)
    url = Column(Text)
    keywords = Column(Text)
    author = Column(Text)
    repository = Column(Text)
    license = Column(Text)
    technology_used = Column(Text)
    bugtracker_url = Column(Text)
    web_tool = Column(Boolean, default=False)
    health_status = Column(Boolean, default=False)
    last_checked = Column(TIMESTAMP, default=datetime.datetime.now)
    page_num = Column(Integer)
    total_pages = Column(Integer)
    records = relationship("Record", back_populates="tool")
    tool_preferences = relationship("Tool_preferences", back_populates="tool")


class Record(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True)
    tool_id = mapped_column(ForeignKey("tools.id"))
    timestamp = Column(TIMESTAMP, default=datetime.datetime.now)
    health_status = Column(Boolean, default=False)
    tool = relationship("Tool", back_populates="records")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(500), unique=True, nullable=False)
    tool_preferences = relationship("Tool_preferences", back_populates="user")


class Tool_preferences(Base):
    __tablename__ = "tool_preferences"
    id = Column(Integer, primary_key=True)
    interval = Column(Integer, default=0)
    send_email = Column(Boolean, default=True)
    user = relationship("User", back_populates="tool_preferences")
    tool = relationship("Tool", back_populates="tool_preferences")
    tool_id = mapped_column(ForeignKey("tools.id"))
    user_id = mapped_column(ForeignKey("users.id"))
