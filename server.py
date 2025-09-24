from flask import *
import datetime

app= Flask(__name__)
#BANCO DE DADOS:
senha='123' #adm
#origem, destino, id, motorista,quantAssentos,data, horarioSaida, horarioChegada, valor, assentos disponiveis
viagens=[
          ['Sousa', 'Tenente Ananias','001','Luís', 40,  datetime.date(2025, 8, 28, ),datetime.time(5,45),datetime.time(6,30),345.99,
          [ "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
            "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
            "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
            "31", "32", "33", "34", "35", "36", "37", "38", "39", "40"]],
          ['Santa Cruz', 'Vieropolis','002','Rafael', 45,  datetime.date(2025, 10, 5, ),datetime.time(10,30),datetime.time(12,30),200.99,
           [ "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
            "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
            "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
            "31", "32", "33", "34", "35", "36", "37", "38", "39", "40","41", "42", "43", "44", "45"]]]

#cpf[0]  assento_selecionado[1]
reserva_assento=[]
onibus=[['32332332', 40, 'Luís'], [ '2132323', 45,  'Rafael'] ] # [0] id, [1] assentos, [2] motorista
passageiros=[]     #[0] nome  #[1] cpf
#login true ou false[0]  [1] cpf do passageiro
login=[False,'null']



@app.route('/')
def iframe():
    return render_template('paginaIframe.html')
@app.route('/homePage')
def home():
    return render_template('homePage.html')
@app.route('/loginuser')
def login_user():
    return render_template('loginUser.html')
@app.route('/cadastrouser')
def cadastro_user():
    return render_template('cadastroUser.html')
@app.route('/rotasHorarios')
def horarios():
    return render_template('rotasHorarios.html',viagens=viagens)

@app.route('/criarconta' ,methods=['post'])
def criarconta():
    global passageiros
    nome = request.form.get('nome')
    cpf = request.form.get('cpf')
    email = request.form.get('email')
    senha_user = request.form.get('senha')

    passageiros.append([nome, cpf, email, senha_user])

    return render_template('loginUser.html')

@app.route('/verificarAdm')
def verificar_adm():
    return render_template('verificacaoAdm.html')


@app.route('/login_adm', methods=['POST'] )
def controle():
    senhaa= request.form.get('senhaAdm')
    if senhaa == senha:
        return render_template('controleAdm.html')
    else:
        return 'nao foi dessa vez'

@app.route('/login_usuario',methods=['POST'])
def login_usu():
    global login
    usu_senha= request.form.get('senha')
    email= request.form.get('email')
    for passageiro in passageiros:
        if usu_senha == passageiro[3] and email == passageiro[2] and login[0] == True:
            return 'vc ja ta logado'
        elif usu_senha == passageiro[3] and email == passageiro[2]:
            login[0]= True
            login[1]= passageiro[1]
            return render_template('homePage.html')

    return 'usuario não encontrado'

@app.route('/dados_onibus', methods=['get'])
def verificar_dados_onibus():
    return render_template('/dados/dados_onibus.html', dados_onibus=onibus)

@app.route('/dados_passageiros', methods=['get'])
def verificar_dados_passageiros():
    return render_template('/dados/dados_passageiros.html', dados_passageiros=passageiros)

@app.route('/dados_viagens')
def verificar_dados_viagens():
    return render_template('/dados/dados_viagens.html', dados_viagens=viagens,reserva_dados=reserva_assento)

@app.route('/pagar', methods=['post'])
def fazer_pagamento():
    return render_template('/homePage.html')
@app.route('/buscar_rotas', methods=['post'])
def buscar_rotas():
    global viagens
    origem=request.form.get('opcoes_viagem_origem')
    destino=request.form.get('opcoes_viagem_destino')
    viagensmodif=[]
    verificador=False
    contador=0
    for viagem in viagens:
        if origem== 'Sousa' and destino== 'Tenente Ananias':
            if viagem[0]== 'Sousa' and viagem[1]== 'Tenente Ananias':
                viagensmodif.append(viagem)
                verificador= True
                contador=1
                break
            elif contador == 0 :
                verificador=False
        elif origem == 'Santa Cruz' and destino=='Vieropolis':
            if viagem[0]== 'Santa Cruz' and viagem[1]== 'Vieropolis':
                viagensmodif.append(viagem)
                verificador= True
                contador=1
            elif  contador == 0 :
                verificador=False

        else:
            verificador= False
        contador=0

    if not verificador:
        return 'erro'
    else:
        return render_template('/viagens_filtradas.html',viagens=viagensmodif,reserva=reserva_assento)

@app.route('/reservar_assento', methods=['post'])
def reservar_assento():
    global reserva_assento
    assentos_selecionados = request.form.getlist("assentos") #lista de assentos selecionados
    id_viagem = request.form.get("id_viagem")
    nomepassageiro= 'null'
    preco_passagem=0
    for passageiro in passageiros:
        if passageiro[1] == login[1]:
            nomepassageiro= passageiro[0]
    if login[0]:
        for viagem in viagens:
            if viagem[2] == id_viagem:
                preco_passagem=viagem[8]
                for assento in assentos_selecionados:
                        viagem[9].remove(assento)
        if not reserva_assento:
            reserva_assento=[[login[1],assentos_selecionados,id_viagem]]
        else:
            reserva_assento.append([login[1],assentos_selecionados,id_viagem])
        return render_template('/pagamento_reserva.html',nome=nomepassageiro,assentos_select=len(assentos_selecionados), preco=preco_passagem)


    else:
        return render_template('/loginUser.html') #não ta logado


if __name__  == '__main__':
    app.run(debug=True)