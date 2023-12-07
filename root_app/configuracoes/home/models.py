from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from root_app.shared.database import Base


class Cliente(Base):
    __tablename__ = 'clientes'

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, nullable=False, unique=True)
    matricula_relacionada = relationship('Matricula', back_populates='cliente_responsavel')
    emprestimo_relacionado = relationship('Emprestimo', back_populates='cliente_responsavel')


class Matricula(Base):
    __tablename__ = 'matriculas'

    id_matricula = Column(Integer, primary_key=True, autoincrement=True)
    matricula = Column(String, nullable=False, unique=True)

    cliente_responsavel_id = Column(Integer, ForeignKey('clientes.id_cliente'))
    cliente_responsavel = relationship('Cliente', back_populates='matricula_relacionada')
    emprestimo_relacionado = relationship('Emprestimo', back_populates='matricula_responsavel')


class Emprestimo(Base):
    __tablename__ = 'emprestimos'

    id_emprestimo = Column(Integer, primary_key=True, autoincrement=True)
    margem_emprestimo = Column(String, nullable=False)
    margem_cartao = Column(String, nullable=False)
    mes_referencia = Column(String, nullable=False)
    ade = Column(String, nullable=False)
    deferido = Column(String, nullable=False)
    servico = Column(String, nullable=False)
    consignataria = Column(String, nullable=False)
    pagas = Column(String, nullable=False)
    total = Column(String, nullable=False)
    valor = Column(String, nullable=False)
    status = Column(String, nullable=False)
    data_consulta = Column(Date, default=datetime.utcnow)
    cliente_responsavel = relationship('Cliente', back_populates='emprestimo_relacionado')
    cliente_responsavel_id = Column(Integer, ForeignKey('clientes.id_cliente'))
    matricula_responsavel = relationship('Matricula', back_populates='emprestimo_relacionado')
    matricula_responsavel_id = Column(Integer, ForeignKey('matriculas.id_matricula'))



class Consulta(Base):
    __tablename__ = 'consultas'

    id_consulta = Column(Integer(), autoincrement=True, primary_key=True)
    data_consulta = Column(Date, default=datetime.utcnow)
    cpf = Column(String, nullable=False)
    matricula = Column(String, nullable=False)
    convenio = Column(String, nullable=False)
    nome = Column(String, nullable=False)


class Selecionado(Base):
    __tablename__ = 'selecionados'
    id_selecionado = Column(Integer(), primary_key=True, autoincrement=True)
    matricula = Column(String, nullable=False)
