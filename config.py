import os
from pathlib import Path

basedir = Path(__file__).resolve().parent

class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY') or "cbd535a731c27deae6fc9e9c2fbb12225cb321c530fddcf272c6a606b24dca58"
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or f"sqlite:///{basedir / 'site.db'}"
    UPLOAD_FOLDER=os.environ.get('UPLOAD_FOLDER') or f"{basedir}/uploads"
    MAIL_SERVER="smtp.gmail.com"
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USE_SSL=False
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER=os.environ.get('MAIL_DEFAULT_SENDER')