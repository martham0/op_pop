from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import datetime
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

