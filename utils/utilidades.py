from dao.viagemDAO import ViagemDAO



def reservar_assentos(id_viagem, assentos_selecionados,session_db):
    preco_passagem=0

    viagem_dao = ViagemDAO(session_db)
    viagem = viagem_dao.buscar_viagem_porid(id_viagem)

    if not viagem:
        return 0

    preco_passagem = viagem.valor

    for numero in assentos_selecionados:
        assento = viagem_dao.achar_assento_porid(viagem_id=id_viagem, numero=numero)
        if assento and assento.disponivel:
            assento.disponivel = False

        session_db.commit()



    return preco_passagem