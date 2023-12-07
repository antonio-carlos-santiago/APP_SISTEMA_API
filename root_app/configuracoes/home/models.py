from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, ForeignKey, JSON
from sqlalchemy.orm import relationship

from root_app.shared.database import Base


class Cliente(Base):
    __tablename__ = 'clientes'

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, nullable=False, unique=True)
    matricula_relacionada = relationship('Matricula', back_populates='cliente_responsavel')


class Matricula(Base):
    __tablename__ = 'matriculas'

    id_matricula = Column(Integer, primary_key=True, autoincrement=True)
    matricula = Column(String, nullable=False, unique=True)
    cliente_responsavel_id = Column(Integer, ForeignKey('clientes.id_cliente'))
    cliente_responsavel = relationship('Cliente', back_populates='matricula_relacionada')


class Consulta(Base):
    __tablename__ = 'consultas'

    id_consulta = Column(Integer(), autoincrement=True, primary_key=True)
    data_consulta = Column(Date, default=datetime.utcnow)
    cpf = Column(String, nullable=False)
    matricula = Column(String, nullable=False)
    convenio = Column(String, nullable=False)
    nome = Column(String, nullable=False)
    margem_emprestimo = Column(String, nullable=False)
    margem_cartao = Column(String, nullable=False)
    mes_referencia = Column(String, nullable=False)
    emprestimos = Column(JSON)
    cartoes = Column(JSON)


class Selecionado(Base):
    __tablename__ = 'selecionados'
    id_selecionado = Column(Integer(), primary_key=True, autoincrement=True)
    matricula = Column(String, nullable=False)
