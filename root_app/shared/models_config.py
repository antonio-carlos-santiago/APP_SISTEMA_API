from sqlalchemy import Column, Integer, String, Boolean

from root_app import Base


class Configlogin(Base):
    __tablename__ = 'configlogin'

    id_conf = Column(Integer(), autoincrement=True, primary_key=True)
    email_user = Column(String(), nullable=True)
    status = Column(Boolean(), default=True)
    senha = Column(String(), nullable=True)
