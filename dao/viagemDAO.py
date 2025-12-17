from sqlalchemy.orm import scoped_session
from modelos.modelos import Viagem, Assentos


class ViagemDAO:

    def __init__(self, session: scoped_session):
        self.session = session

    def criar(self, viagem):

        self.session.add(viagem)

        self.session.commit()


    def criar_assentos(self,viagem):
        for i in range(1, viagem.assentos_totais + 1):
            assento = Assentos(
                numero=str(i),
                disponivel=True,
                viagem_id=viagem.id
            )
            self.session.add(assento)
        self.session.commit()

    def achar_assento_porid(self,viagem_id,numero):
        return self.session.query(Assentos).filter_by(viagem_id=viagem_id, numero=numero).first()

    def buscar_viagem_porid(self, viagem_id):
        return self.session.query(Viagem).filter_by(id=viagem_id).first()

    def buscar_assentos_porid(self,viagem_id):
       return self.session.query(Assentos).filter_by(viagem_id=viagem_id).all()



    def listar_viagens(self):
        return self.session.query(Viagem).all()



