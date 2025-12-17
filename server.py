from flask import *
import datetime, random
from datetime import datetime
from dao.usuarioDAO import UsuarioDAO
from dao.viagemDAO import ViagemDAO
from modelos.modelos import Usuario, Viagem, Assentos
from utils.utilidades import reservar_assentos
from dao.banco import Session, init_db

app= Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

usuarios = None

senha='123'
reserva_assento=[]

init_db()
@app.before_request
def pegar_sessao():
    g.session = Session()

@app.teardown_appcontext
def encerrar_sessao(exception=None):
    Session.remove()




@app.route('/')
def home():
    viagem_dao = ViagemDAO(g.session)
    viagens_aleatorias=random.sample(viagem_dao.listar_viagens(), min(len(viagem_dao.listar_viagens()),3))
    return render_template('cliente/homePage.html',viagens=viagens_aleatorias)
@app.route('/deslogar')
def deslogar():
    session.clear()
    viagem_dao = ViagemDAO(g.session)
    viagens_aleatorias = random.sample(viagem_dao.listar_viagens(), min(len(viagem_dao.listar_viagens()),3))
    return render_template('cliente/homePage.html',viagens=viagens_aleatorias)
@app.route('/loginuser')
def login_user():

    return render_template('cliente/loginUser.html')
@app.route('/cadastrouser')
def cadastro_user():
    return render_template('cliente/cadastroUser.html')
@app.route('/rotasHorarios')
def horarios():
    assentos_por_viagem = {}
    viagem_dao = ViagemDAO(g.session)
    lista_viagens= viagem_dao.listar_viagens()
    for viagem in lista_viagens:
        assentos_por_viagem[viagem.id]=viagem_dao.buscar_assentos_porid(viagem_id=viagem.id)
    return render_template('cliente/rotasHorarios.html',viagens=lista_viagens, assentos_por_viagem=assentos_por_viagem)

@app.route('/criarconta' ,methods=['post'])
def criarconta():

    usuario_dao= UsuarioDAO(g.session)

    nome = request.form.get('nome')
    cpf = request.form.get('cpf')
    email = request.form.get('email')
    senha_user = request.form.get('senha')

    novo_usuario= Usuario(email=email,nome=nome,senha=senha_user,tipo=False, cpf=cpf)

    usuario_dao.criar(novo_usuario)

    return render_template('cliente/loginUser.html')

@app.route('/verificarAdm')
def verificar_adm():
    return render_template('adm/verificacaoAdm.html')


@app.route('/login_adm', methods=['POST', 'GET'] )
def controle():
    if request.method == 'POST':
        senhaa= request.form.get('senhaAdm')
        if senhaa == senha:
            session['adm'] = senha
            return render_template('adm/controleAdm.html')
        else:
            return 'nao foi dessa vez'
    else:
        return render_template('adm/controleAdm.html')

@app.route('/login_usuario',methods=['POST'])
def login_usu():
    if 'cliente' in session:
        return 'vc ja ta logado'


    email= request.form.get('email')
    usuario_dao=UsuarioDAO(g.session)
    if usuario_dao.buscar_por_email(email) is None:
        return 'usuario não encontrado'
    else:
        viagem_dao = ViagemDAO(g.session)
        session['cliente'] = email
        viagens_aleatorias = random.sample(viagem_dao.listar_viagens(),min(len(viagem_dao.listar_viagens()),3))
        return render_template('cliente/homePage.html', viagens=viagens_aleatorias)


@app.route('/pagina_viagemCadastro', methods=['get'])
def acessar_viagem_cadastro():
    if 'adm' in session:
         return render_template('/adm/cadastrarViagem.html')
    else:
        return 'vc não tem autorização!'

@app.route('/cadastrar_viagem', methods=['POST'])
def cadastrar_viagem():
    viagem_dao = ViagemDAO(g.session)

    data = datetime.strptime(
        request.form.get('data'),
        "%Y-%m-%d"
    ).date()

    horario_partida = datetime.strptime(
        request.form.get('horario_partida'),
        "%H:%M"
    ).time()

    horario_chegada = datetime.strptime(
        request.form.get('horario_chegada'),
        "%H:%M"
    ).time()

    origem =  request.form.get('origem')
    destino = request.form.get('destino')
    motorista =  request.form.get('motorista')
    assentos_totais =  int( request.form.get('assentos_totais'))
    valor = float( request.form.get('valor'))
    duracao = int( request.form.get('duracao'))
    data =  data
    horario_partida =  horario_partida
    horario_chegada = horario_chegada

    viagem = Viagem( origem=origem,destino=destino,motorista=motorista,assentos_totais=assentos_totais,valor=valor,duracao=duracao,data=data,horario_partida=horario_partida,horario_chegada=horario_chegada
    )

    viagem_dao.criar(viagem)

    viagem_dao.criar_assentos(viagem)


    return render_template('adm/controleAdm.html')

@app.route('/dados_onibus', methods=['get'])
def verificar_dados_onibus():
    if 'adm' in session:
         viagem_dao = ViagemDAO(g.session)
         dados= viagem_dao.listar_viagens()
         return render_template('/dados/dados_onibus.html', dados_onibus=dados)
    else:
        return 'vc não tem autorização!'
@app.route('/dados_passageiros', methods=['get'])
def verificar_dados_passageiros():
    if 'adm' in session:
        usuario_dao = UsuarioDAO(g.session)
        dados=usuario_dao.listar_usuarios()
        return render_template('/dados/dados_passageiros.html', dados_passageiros=dados)
    else:
        return 'vc não tem autorização!'
@app.route('/assentos', methods=['get'])
def mostrar_assentos():
    if 'adm' in session:
        viagem_dao= ViagemDAO(g.session)
        viagem_id = request.args.get('viagem_id')
        assentos_todos= viagem_dao.buscar_assentos_porid(viagem_id)
    return render_template('/dados/assentos.html', assentos=assentos_todos)

@app.route('/dados_viagens')
def verificar_dados_viagens():
    if 'adm' in session:
        viagem_dao = ViagemDAO(g.session)
        dados = viagem_dao.listar_viagens()
        return render_template('/dados/dados_viagens.html', dados_viagens=dados,reserva_dados=reserva_assento)
    else:
        return 'vc não tem autorização!'

@app.route('/pagar', methods=['post'])
def fazer_pagamento():
    if 'cliente' in session:
        viagem_dao = ViagemDAO(g.session)
        viagens_aleatorias = random.sample(viagem_dao.listar_viagens(), min(len(viagem_dao.listar_viagens()),3))
        return render_template('cliente/homePage.html',viagens=viagens_aleatorias)
    else:
        return "vc não está logado"

@app.route('/buscar_rotas', methods=['POST', 'GET'])
def buscar_rotas():

    origem = request.values.get('opcoes_viagem_origem') or request.values.get('origem')
    destino = request.values.get('opcoes_viagem_destino') or request.values.get('destino')
    viagensmodif=[]
    assentos_por_viagem={}
    viagem_dao = ViagemDAO(g.session)
    viagens= viagem_dao.listar_viagens()

    for viagem in viagens:

        if viagem.origem== origem and viagem.destino==destino:
            viagensmodif.append(viagem)


    if not viagensmodif:
        return 'erro'
    else:
        for viagem in viagensmodif:
            assentos_por_viagem[viagem.id] = viagem_dao.buscar_assentos_porid(viagem_id=viagem.id)
        return render_template('cliente/viagens_filtradas.html',viagens=viagensmodif,assentos_por_viagem=assentos_por_viagem)

@app.route('/reservar_assento', methods=['post', 'get'])
def reservar_assento():
    assentos_selecionados = request.form.getlist("assentos")
    id_viagem = int(request.form.get("id_viagem"))

    if 'cliente' not in session:
        return render_template('cliente/loginUser.html')


    usuario_dao = UsuarioDAO(g.session)
    passageiros= usuario_dao.listar_usuarios()

    for passageiro in passageiros:
        if passageiro.email == session['cliente']:
            nomepassageiro= passageiro.nome
            passagem = reservar_assentos( id_viagem, assentos_selecionados, g.session)
            return render_template('cliente/pagamento_reserva.html',nome=nomepassageiro,assentos_select=len(assentos_selecionados), preco=passagem)

    return render_template('cliente/loginUser.html')





if __name__  == '__main__':
    app.run(debug=True)