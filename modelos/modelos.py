from sys import intern
from sqlalchemy import Column, String, Integer, Boolean, Float, Time, Date
from sqlalchemy.ext.declarative import declarative_base




Base = declarative_base()
class Usuario(Base):
    __tablename__ = 'usuarios'

    email = Column(String, primary_key=True)
    nome = Column(String)
    senha = Column(String)
    tipo= Column(Boolean)
    cpf= Column(String)

    def __repr__(self):
        return f"<Usuario(email='{self.email}', nome='{self.nome}')>"

class Viagem(Base):
    __tablename__ = 'viagem'

    id = Column(Integer, primary_key=True)
    origem= Column(String)
    destino=Column(String)
    motorista= Column(String)
    assentos_totais=Column(Integer)
    valor = Column(Float)
    duracao= Column(Integer)
    data = Column(Date)
    horario_partida=Column(Time)
    horario_chegada= Column(Time)




class Assentos(Base):
    __tablename__ = 'assento'

    id = Column(Integer, primary_key=True)
    numero = Column(String)
    disponivel = Column(Boolean, default=True)
    viagem_id = Column(Integer)







    def __repr__(self):
        return f"<Viagem(id='{self.id}')>"

