import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time
import matplotlib.pyplot as plt
from fpdf import FPDF
import os
import base64
import json
import shutil


# Configuração inicial da página
st.set_page_config(page_title="Sistema de Balança e Controle - Padaria", layout="wide")

# Dados dos produtos (agora sem valores fixos)
produtos = {
    "1096": {"nome": "BEIJINHO", "valor_kg": 0.0, "tara": 0.0},
    "17834": {"nome": "BISCOITO CACETINHO", "valor_kg": 0.0, "tara": 0.0},
    "5913": {"nome": "BISCOITO CHAMPAGNE", "valor_kg": 0.0, "tara": 0.0},
    "3056": {"nome": "BOLACHA CAMELO", "valor_kg": 0.0, "tara": 0.0},
    "7481": {"nome": "BOLACHA DE COCO", "valor_kg": 0.0, "tara": 0.0},
    "7207": {"nome": "BOLACHA MIMOSA", "valor_kg": 0.0, "tara": 0.0},
    "2566": {"nome": "BOLACHA REG INTEGRAL", "valor_kg": 0.0, "tara": 0.0},
    "7214": {"nome": "BOLACHA REGALIA", "valor_kg": 0.0, "tara": 0.0},
    "7153": {"nome": "BOLACHA ROSQUINHA", "valor_kg": 0.0, "tara": 0.0},
    "9300": {"nome": "BOLINHO DE BACALHAU", "valor_kg": 0.0, "tara": 0.0},
    "9324": {"nome": "BOLINHO DE CHARQUE", "valor_kg": 0.0, "tara": 0.0},
    "4724": {"nome": "BOLINHO DE PIZZA", "valor_kg": 0.0, "tara": 0.0},
    "9331": {"nome": "BOLINHO DE QUEIJO", "valor_kg": 0.0, "tara": 0.0},
    "17874": {"nome": "BOLO AIPIM KG", "valor_kg": 0.0, "tara": 0.0},
    "73309": {"nome": "BOLO BACIA C/1 UN", "valor_kg": 0.0, "tara": 0.0},
    "73305": {"nome": "BOLO BACIA C/4 UN", "valor_kg": 0.0, "tara": 0.0},
    "17870": {"nome": "BOLO CAÇAROLA C/QUEIJO", "valor_kg": 0.0, "tara": 0.0},
    "1427": {"nome": "BOLO CENOURA", "valor_kg": 0.0, "tara": 0.0},
    "17320": {"nome": "BOLO CENOURA SIMPLES", "valor_kg": 0.0, "tara": 0.0},
    "17295": {"nome": "BOLO CHOC CREMOSO", "valor_kg": 0.0, "tara": 0.0},
    "6927": {"nome": "BOLO COM LARANJA", "valor_kg": 0.0, "tara": 0.0},
    "1001": {"nome": "BOLO COM PASSAS", "valor_kg": 0.0, "tara": 0.0},
    "9751": {"nome": "BOLO DE ABACAXI", "valor_kg": 0.0, "tara": 0.0},
    "9492": {"nome": "BOLO DE BANANA", "valor_kg": 0.0, "tara": 0.0},
    "7450": {"nome": "BOLO DE CHOCOLATE", "valor_kg": 0.0, "tara": 0.0},
    "7016": {"nome": "BOLO DE COCADA", "valor_kg": 0.0, "tara": 0.0},
    "3674": {"nome": "BOLO DE FRUTAS VERMELHAS", "valor_kg": 0.0, "tara": 0.0},
    "6293": {"nome": "BOLO DE MACAXEIRA", "valor_kg": 0.0, "tara": 0.0},
    "6347": {"nome": "BOLO DE MASSA PUBA", "valor_kg": 0.0, "tara": 0.0},
    "6361": {"nome": "BOLO DE MILHO", "valor_kg": 0.0, "tara": 0.0},
    "6198": {"nome": "BOLO FORMIGUEIRO", "valor_kg": 0.0, "tara": 0.0},
    "6149": {"nome": "BOLO GOIABADA", "valor_kg": 0.0, "tara": 0.0},
    "2300": {"nome": "BOLO INDIANO", "valor_kg": 0.0, "tara": 0.0},
    "6217": {"nome": "BOLO INGLES", "valor_kg": 0.0, "tara": 0.0},
    "6088": {"nome": "BOLO MASSA PUBA", "valor_kg": 0.0, "tara": 0.0},
    "7177": {"nome": "BOLO MESCLADO", "valor_kg": 0.0, "tara": 0.0},
    "7108": {"nome": "BOLO PÉ DE MOLEQUE PAÇOCA", "valor_kg": 0.0, "tara": 0.0},
    "3063": {"nome": "BRASILEIRA", "valor_kg": 0.0, "tara": 0.0},
    "1070": {"nome": "BRIGADEIRO", "valor_kg": 0.0, "tara": 0.0},
    "4121": {"nome": "BRIOCHE COM CÔCO", "valor_kg": 0.0, "tara": 0.0},
    "4145": {"nome": "BRIOCHE COM FRUTAS", "valor_kg": 0.0, "tara": 0.0},
    "6095": {"nome": "BRIOCHE CREME CHOC", "valor_kg": 0.0, "tara": 0.0},
    "6514": {"nome": "BROA DA CASA", "valor_kg": 0.0, "tara": 0.0},
    "8174": {"nome": "CAROLINA", "valor_kg": 0.0, "tara": 0.0},
    "9851": {"nome": "COXINHA CATUPIRY", "valor_kg": 0.0, "tara": 0.0},
    "5227": {"nome": "COXINHA DE CARNE", "valor_kg": 0.0, "tara": 0.0},
    "9837": {"nome": "COXINHA DE FRANGO", "valor_kg": 0.0, "tara": 0.0},
    "1695": {"nome": "DELICIA DE ABACAXI", "valor_kg": 0.0, "tara": 0.0},
    "6000": {"nome": "DIPLOMATA", "valor_kg": 0.0, "tara": 0.0},
    "1020": {"nome": "DOCE MARIA MOLE", "valor_kg": 0.0, "tara": 0.0},
    "3410": {"nome": "DOCINHO", "valor_kg": 0.0, "tara": 0.0},
    "998949": {"nome": "EMPADA", "valor_kg": 0.0, "tara": 0.0},
    "8419": {"nome": "ENROLADINHO", "valor_kg": 0.0, "tara": 0.0},
    "6613": {"nome": "FARINHA DE ROSCA", "valor_kg": 0.0, "tara": 0.0},
    "1823": {"nome": "FOCACCIA", "valor_kg": 0.0, "tara": 0.0},
    "9913": {"nome": "FOLHADO DE FRANGO", "valor_kg": 0.0, "tara": 0.0},
    "6965": {"nome": "GALETO", "valor_kg": 0.0, "tara": 0.0},
    "596": {"nome": "KIELZ", "valor_kg": 0.0, "tara": 0.0},
    "6615": {"nome": "MINI COXINHA", "valor_kg": 0.0, "tara": 0.0},
    "953": {"nome": "MINI CROISSANT", "valor_kg": 0.0, "tara": 0.0},
    "1631": {"nome": "MOUSSE DE CHOCOLATE", "valor_kg": 0.0, "tara": 0.0},
    "1488": {"nome": "MOUSSE DE MARACUJA", "valor_kg": 0.0, "tara": 0.0},
    "3346": {"nome": "MOUSSE DE MORANGO", "valor_kg": 0.0, "tara": 0.0},
    "4144": {"nome": "PAINETTOME CINCO LATE", "valor_kg": 0.0, "tara": 0.0},
    "6873": {"nome": "PÃO BAGUETE", "valor_kg": 0.0, "tara": 0.0},
    "9690": {"nome": "PÃO BATATA", "valor_kg": 0.0, "tara": 0.0},
    "7078": {"nome": "PÃO BOLACHÃO", "valor_kg": 0.0, "tara": 0.0},
    "17864": {"nome": "PÃO BRIOCHE", "valor_kg": 0.0, "tara": 0.0},
    "20139": {"nome": "PÃO DE ALHO", "valor_kg": 0.0, "tara": 0.0},
    "7030": {"nome": "PÃO DE FORMA", "valor_kg": 0.0, "tara": 0.0},
    "21933": {"nome": "PÃO DE LEITE", "valor_kg": 0.0, "tara": 0.0},
    "34083": {"nome": "PÃO DE MILHO COQU", "valor_kg": 0.0, "tara": 0.0},
    "7115": {"nome": "PÃO DE QUEIJO", "valor_kg": 0.0, "tara": 0.0},
    "7496": {"nome": "PÃO DELICIA", "valor_kg": 0.0, "tara": 0.0},
    "949": {"nome": "PÃO DOCE", "valor_kg": 0.0, "tara": 0.0},
    "4251": {"nome": "PÃO FRANCÊS", "valor_kg": 0.0, "tara": 0.0},
    "3822": {"nome": "PÃO HAMBÚRGUER", "valor_kg": 0.0, "tara": 0.0},
    "3073": {"nome": "PÃO HAMBÚRGUER GERGELIM", "valor_kg": 0.0, "tara": 0.0},
    "3957": {"nome": "PÃO HOT DOG RECHEADO", "valor_kg": 0.0, "tara": 0.0},
    "7092": {"nome": "PÃO INTEGRAL", "valor_kg": 0.0, "tara": 0.0},
    "6835": {"nome": "PÃO ITALIANO", "valor_kg": 0.0, "tara": 0.0},
    "6316": {"nome": "PÃO MANTEIGA", "valor_kg": 0.0, "tara": 0.0},
    "21931": {"nome": "PÃO PORTUGUÊS", "valor_kg": 0.0, "tara": 0.0},
    "7122": {"nome": "PÃO RECIFE", "valor_kg": 0.0, "tara": 0.0},
    "9317": {"nome": "PÃO SALADA RUSSA", "valor_kg": 0.0, "tara": 0.0},
    "1984": {"nome": "PASTEL DE PORNAS", "valor_kg": 0.0, "tara": 0.0},
    "9713": {"nome": "PETIT-FOUR DE COMBA", "valor_kg": 0.0, "tara": 0.0},
    "4985": {"nome": "PIZZA SABORES", "valor_kg": 0.0, "tara": 0.0},
    "7061": {"nome": "PUDIM", "valor_kg": 0.0, "tara": 0.0},
    "9157": {"nome": "ROCAMBOLE", "valor_kg": 0.0, "tara": 0.0},
    "6989": {"nome": "SALGADINHO DE QUEIJO", "valor_kg": 0.0, "tara": 0.0},
    "1023": {"nome": "SANDUICHE NATURAL", "valor_kg": 0.0, "tara": 0.0},
    "408": {"nome": "SOBREMESA", "valor_kg": 0.0, "tara": 0.0},
    "7893": {"nome": "SUSPINO", "valor_kg": 0.0, "tara": 0.0},
    "8648": {"nome": "TORRADA DE BOLO", "valor_kg": 0.0, "tara": 0.0},
    "6781": {"nome": "TORRADA SIMPLES", "valor_kg": 0.0, "tara": 0.0},
    "1441": {"nome": "TORTA DE ABACAXI", "valor_kg": 0.0, "tara": 0.0},
    "7160": {"nome": "TORTA DE BANANA", "valor_kg": 0.0, "tara": 0.0},
    "7054": {"nome": "TORTA DE CHOCOLATE", "valor_kg": 0.0, "tara": 0.0},
    "1821": {"nome": "TORTA DE MARACUJA", "valor_kg": 0.0, "tara": 0.0},
    "6491": {"nome": "TORTA DE MORANGO", "valor_kg": 0.0, "tara": 0.0},
    "1907": {"nome": "TORTA DOCE DE LEITE", "valor_kg": 0.0, "tara": 0.0},
    "1785": {"nome": "TORTA HOLANDESA", "valor_kg": 0.0, "tara": 0.0},
    "6422": {"nome": "TORTA LEITE CONDENS", "valor_kg": 0.0, "tara": 0.0},
    "1549": {"nome": "TORTA MOUSSE DE LIMAO", "valor_kg": 0.0, "tara": 0.0},
    "69231": {"nome": "TORTA SABORES", "valor_kg": 0.0, "tara": 0.0},
    "5104": {"nome": "TORTA SALGADA", "valor_kg": 0.0, "tara": 0.0},
    "8485": {"nome": "TORTILETE", "valor_kg": 0.0, "tara": 0.0},
    "34096": {"nome": "TORTILLE", "valor_kg": 0.0, "tara": 0.0}
}

# Inicialização do DataFrame para armazenar as pesagens
if 'pesagens' not in st.session_state:
    st.session_state.pesagens = pd.DataFrame(columns=[
        'DataHora', 'Funcionario', 'Codigo', 'Produto', 'Peso', 'Tara',
        'PesoLiquido', 'ValorKg', 'ValorTotal', 'TipoOperacao',
        'Sobra', 'FarinhaRosca', 'Torrada', 'DiferencaPeso',
        'DiferencaValor', 'ImpactoCusto'
    ])

# Inicialização do histórico diário
if 'historico_diario' not in st.session_state:
    st.session_state.historico_diario = {}


# Funções para persistência de dados
def salvar_dados():
    """Salva os dados atuais em um arquivo JSON"""
    try:
        # Criar backup antes de salvar
        if os.path.exists('dados_padaria.json'):
            backup_file = f"backup_dados_padaria_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            shutil.copy2('dados_padaria.json', backup_file)

        dados = {
            'pesagens': st.session_state.pesagens.to_dict(orient='records'),
            'produtos': produtos,
            'historico_diario': st.session_state.historico_diario
        }

        with open('dados_padaria.json', 'w') as f:
            json.dump(dados, f, default=str, indent=4)

        return True
    except Exception as e:
        st.error(f"Erro ao salvar dados: {str(e)}")
        return False
def carregar_dados():
    """Carrega os dados do arquivo JSON se existir"""
    try:
        with open('dados_padaria.json', 'r') as f:
            dados = json.load(f)
            st.session_state.pesagens = pd.DataFrame(dados['pesagens'])
            st.session_state.pesagens['DataHora'] = pd.to_datetime(st.session_state.pesagens['DataHora'])

            # Atualizar os produtos com os valores salvos
            for codigo, info in dados['produtos'].items():
                if codigo in produtos:
                    produtos[codigo].update(info)

            # Carregar histórico diário se existir
            if 'historico_diario' in dados:
                st.session_state.historico_diario = dados['historico_diario']
            return True
    except (FileNotFoundError, json.JSONDecodeError):
        return False
def salvar_historico_diario():
    """Salva os dados do dia atual no histórico"""
    hoje = datetime.now().strftime('%Y-%m-%d')
    df_hoje = st.session_state.pesagens[
        st.session_state.pesagens['DataHora'].dt.strftime('%Y-%m-%d') == hoje
        ]

    if not df_hoje.empty:
        st.session_state.historico_diario[hoje] = df_hoje.to_dict(orient='records')
        salvar_dados()
def limpar_dados_dia():
    """Limpa os dados do dia atual"""
    hoje = datetime.now().strftime('%Y-%m-%d')
    st.session_state.pesagens = st.session_state.pesagens[
        st.session_state.pesagens['DataHora'].dt.strftime('%Y-%m-%d') != hoje
        ]
    salvar_historico_diario()
    st.success(f"Dados do dia {hoje} salvos no histórico e limpos!")
# Limpar histórico diário
def limpar_todos_dados():
    """Limpa todos os dados do sistema de forma definitiva"""
    # Confirmar ação em duas etapas
    if not st.session_state.get('confirmar_limpeza', False):
        st.session_state.confirmar_limpeza = True
        st.warning("⚠️ ATENÇÃO: Esta ação é irreversível e apagará TODOS os dados permanentemente!")
        st.warning("Clique novamente em 'Limpar TODOS os Dados' para confirmar.")
        return

    # Limpeza completa dos dados
    try:
        # 1. Limpar DataFrame de pesagens
        st.session_state.pesagens = pd.DataFrame(columns=[
            'DataHora', 'Funcionario', 'Codigo', 'Produto', 'Peso', 'Tara',
            'PesoLiquido', 'ValorKg', 'ValorTotal', 'TipoOperacao',
            'Sobra', 'FarinhaRosca', 'Torrada', 'DiferencaPeso',
            'DiferencaValor', 'ImpactoCusto'
        ])

        # 2. Resetar valores e taras dos produtos para 0
        for codigo in produtos:
            produtos[codigo]['valor_kg'] = 0.0
            produtos[codigo]['tara'] = 0.0

        # 3. Limpar histórico diário
        st.session_state.historico_diario = {}

        # 4. Limpar arquivo de dados JSON
        if os.path.exists('dados_padaria.json'):
            os.remove('dados_padaria.json')

        # 5. Criar novo arquivo JSON vazio com estrutura básica
        dados_iniciais = {
            'pesagens': [],
            'produtos': {codigo: {'nome': info['nome'], 'valor_kg': 0.0, 'tara': 0.0}
                         for codigo, info in produtos.items()},
            'historico_diario': {}
        }

        with open('dados_padaria.json', 'w') as f:
            json.dump(dados_iniciais, f, indent=4)

        # 6. Limpar cache e variáveis de sessão
        keys_to_clear = [
            'codigo_selecionado', 'produto_selecionado', 'valor_kg', 'tara',
            'confirmar_limpeza', 'dados_carregados', 'produtos_carregados'
        ]

        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]

        st.success("✅ Todos os dados foram limpos com sucesso! O sistema será recarregado.")
        time.sleep(2)

        # Forçar recarregamento completo da página
        st.rerun()

    except Exception as e:
        st.error(f"❌ Ocorreu um erro ao limpar os dados: {str(e)}")
        st.error("Por favor, tente novamente ou reinicie o aplicativo manualmente.")# Painel lateral com lista de produtos e busca
def painel_lateral():
    st.sidebar.title("🔍 Busca de Produtos")

    # Menu vertical simplificado
    st.sidebar.markdown("### Navegação")
    if st.sidebar.button("⚖️ Balança", use_container_width=True):
        st.session_state.menu_choice = "balanca"
    if st.sidebar.button("📊 Análises", use_container_width=True):
        st.session_state.menu_choice = "visualizacao"
    if st.sidebar.button("📄 Relatórios", use_container_width=True):
        st.session_state.menu_choice = "relatorio"
    if st.sidebar.button("🗃️ Histórico", use_container_width=True):
        st.session_state.menu_choice = "historico"
    if st.sidebar.button("⚙️ Configurar Produtos", use_container_width=True):
        st.session_state.menu_choice = "produtos"

    # Lista completa de produtos para referência
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Lista de Produtos")

    # Criar DataFrame com produtos
    df_produtos = pd.DataFrame.from_dict(produtos, orient='index').reset_index()
    df_produtos.columns = ['Código', 'Produto', 'Valor/kg', 'Tara']
    df_produtos = df_produtos[['Código', 'Produto']]  # Mostrar apenas código e nome na lista

    # Barra de busca
    busca = st.sidebar.text_input("Filtrar produtos:")
    if busca:
        df_filtrado = df_produtos[
            df_produtos['Código'].astype(str).str.contains(busca, case=False) |
            df_produtos['Produto'].str.contains(busca, case=False)
            ]
    else:
        df_filtrado = df_produtos

    # Exibir lista com scroll e seleção
    selected_index = st.sidebar.selectbox(
        "Selecione um produto:",
        range(len(df_filtrado)),
        format_func=lambda x: f"{df_filtrado.iloc[x]['Código']} - {df_filtrado.iloc[x]['Produto']}",
        index=0,
        key="produto_select"
    )

    # Botão para carregar produto selecionado
    if st.sidebar.button("Carregar Produto Selecionado", use_container_width=True):
        codigo_selecionado = df_filtrado.iloc[selected_index]['Código']
        st.session_state.codigo_selecionado = codigo_selecionado
        st.session_state.produto_selecionado = produtos[codigo_selecionado]['nome']
        st.session_state.valor_kg = produtos[codigo_selecionado]['valor_kg']
        st.session_state.tara = produtos[codigo_selecionado]['tara']
        st.success(f"Produto {codigo_selecionado} - {produtos[codigo_selecionado]['nome']} carregado!")

    # Controles de dados
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Gerenciamento")

    if st.sidebar.button("💾 Salvar Dados", use_container_width=True):
        salvar_dados()
        st.sidebar.success("Dados salvos!")

    if st.sidebar.button("📂 Carregar Dados", use_container_width=True):
        carregar_dados()
        st.sidebar.success("Dados carregados!")

    if st.sidebar.button("🧹 Limpar TODOS os Dados", use_container_width=True,
                         help="Limpa todos os dados, incluindo valores e taras cadastrados"):
        limpar_todos_dados()
        if st.sidebar.checkbox("CONFIRMAR: Limpar TODOS os dados permanentemente?"):
            limpar_todos_dados()# Função para gerenciar a base de produtos
# Função para gerenciar a base de produtos
def gerenciar_produtos():
    st.title("⚙️ Configuração de Produtos")

    # Carregar produtos existentes ao iniciar
    if not st.session_state.get('produtos_carregados', False):
        carregar_dados()
        st.session_state.produtos_carregados = True

    # Seção para adicionar/editar produtos
    st.subheader("Adicionar/Editar Produto")

    col1, col2, col3 = st.columns(3)

    with col1:
        codigo = st.text_input("Código do Produto", key="prod_codigo")
    with col2:
        # Buscar nome do produto se o código existir
        nome_produto = produtos.get(codigo, {}).get('nome', '') if codigo else ''
        produto = st.text_input("Nome do Produto", value=nome_produto, key="prod_nome")
    with col3:
        # Mostrar tara e valor atual se o produto existir
        tara = st.number_input("Tara (kg)",
                               min_value=0.0,
                               step=0.001,
                               format="%.3f",
                               value=produtos.get(codigo, {}).get('tara', 0.0) if codigo else 0.0,
                               key="prod_tara")

    col4, col5 = st.columns(2)
    with col4:
        valor_kg = st.number_input("Valor por kg (R$)",
                                   min_value=0.0,
                                   step=0.01,
                                   format="%.2f",
                                   value=produtos.get(codigo, {}).get('valor_kg', 0.0) if codigo else 0.0,
                                   key="prod_valor")
    with col5:
        st.write("")  # Espaço vazio para alinhamento
        if st.button("💾 Salvar Produto", use_container_width=True, key="salvar_prod"):
            if codigo and produto:
                # Atualizar ou criar o produto
                produtos[codigo] = {
                    "nome": produto,
                    "valor_kg": valor_kg,
                    "tara": tara
                }
                if salvar_dados():  # Garantir que os dados sejam salvos
                    st.success(f"Produto {codigo} - {produto} salvo com sucesso!")
                    # Forçar atualização imediata dos valores na sessão
                    st.session_state.codigo_selecionado = codigo
                    st.session_state.produto_selecionado = produto
                    st.session_state.valor_kg = valor_kg
                    st.session_state.tara = tara
                    st.rerun()
            else:
                st.error("Código e nome do produto são obrigatórios!")
def gerar_pdf_tabela(df_tabela):
    # Configurações do PDF
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Fonte personalizada (Arial)
    pdf.set_font('Arial', 'B', 16)

    # Cabeçalho profissional
    pdf.cell(0, 10, 'RELATÓRIO DE PRODUÇÃO - PADARIA', 0, 1, 'C')
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 8, f"Período: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 1, 'C')
    pdf.ln(5)

    # Tabela principal - Cabeçalho
    pdf.set_font('Arial', 'B', 9)
    col_widths = [25, 25, 30, 45, 20, 20, 25, 25, 25, 25]  # Larguras ajustadas
    headers = list(df_tabela.columns)

    # Cores profissionais (cinza para cabeçalho)
    pdf.set_fill_color(220, 220, 220)

    # Desenhar cabeçalhos
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 10, header, 1, 0, 'C', True)
    pdf.ln()

    # Dados da tabela
    pdf.set_font('Arial', '', 8)
    for _, row in df_tabela.iterrows():
        for i, col in enumerate(headers):
            # Truncar textos muito longos
            text = str(row[col])[:25] + '...' if len(str(row[col])) > 25 else str(row[col])
            pdf.cell(col_widths[i], 8, text, 1, 0, 'C')
        pdf.ln()

    # Página de totais
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'TOTAIS POR PRODUTO', 0, 1, 'C')
    pdf.ln(8)

    # Calcular totais
    totais = st.session_state.pesagens.groupby('Produto').agg({
        'PesoLiquido': 'sum',
        'ValorTotal': 'sum'
    }).reset_index()

    # Tabela de totais - Cabeçalho
    pdf.set_font('Arial', 'B', 10)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(100, 8, 'PRODUTO', 1, 0, 'C', True)
    pdf.cell(40, 8, 'PESO TOTAL (kg)', 1, 0, 'C', True)
    pdf.cell(40, 8, 'VALOR TOTAL (R$)', 1, 1, 'C', True)

    # Dados dos totais
    pdf.set_font('Arial', '', 9)
    for _, row in totais.iterrows():
        # Formatação profissional
        peso_formatado = f"{row['PesoLiquido']:,.3f}".replace(".", "X").replace(",", ".").replace("X", ",")
        valor_formatado = f"R$ {row['ValorTotal']:,.2f}".replace(".", "X").replace(",", ".").replace("X", ",")

        pdf.cell(100, 8, row['Produto'], 1)
        pdf.cell(40, 8, peso_formatado, 1, 0, 'R')
        pdf.cell(40, 8, valor_formatado, 1, 0, 'R')
        pdf.ln()

    # Total geral
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(100, 8, 'TOTAL GERAL', 1)
    pdf.cell(40, 8, f"{totais['PesoLiquido'].sum():,.3f}".replace(".", "X").replace(",", ".").replace("X", ","), 1, 0,
             'R')
    pdf.cell(40, 8, f"R$ {totais['ValorTotal'].sum():,.2f}".replace(".", "X").replace(",", ".").replace("X", ","), 1, 0,
             'R')

    # Rodapé profissional
    pdf.set_y(-15)
    pdf.set_font('Arial', 'I', 8)
    pdf.cell(0, 10, f"Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')} - Sistema de Balança", 0, 0, 'C')

    # Salvar arquivo
    nome_arquivo = f"relatorio_producao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(nome_arquivo)
    return nome_arquivo
# Função para exibir a tabela de produtos cadastrados
def exibir_tabela_produtos():
    if not st.session_state.pesagens.empty:
        st.subheader("📋 Tabela de Produtos Cadastrados")

        # Ordenar por data mais recente primeiro
        df_tabela = st.session_state.pesagens.sort_values('DataHora', ascending=False)

        # Selecionar e renomear colunas para exibição
        df_tabela = df_tabela[[
            'DataHora', 'Funcionario', 'Codigo', 'Produto', 'Peso', 'Tara',
            'PesoLiquido', 'ValorKg', 'ValorTotal', 'TipoOperacao'
        ]]

        df_tabela.columns = [
            'Data/Hora', 'Funcionário', 'Código', 'Produto', 'Peso Bruto (kg)', 'Tara (kg)',
            'Peso Líquido (kg)', 'Valor por kg (R$)', 'Valor Total (R$)', 'Tipo de Operação'
        ]

        # Formatar valores
        df_tabela['Peso Bruto (kg)'] = df_tabela['Peso Bruto (kg)'].apply(lambda x: f"{x:.3f}".replace(".", ","))
        df_tabela['Tara (kg)'] = df_tabela['Tara (kg)'].apply(lambda x: f"{x:.3f}".replace(".", ","))
        df_tabela['Peso Líquido (kg)'] = df_tabela['Peso Líquido (kg)'].apply(lambda x: f"{x:.3f}".replace(".", ","))
        df_tabela['Valor por kg (R$)'] = df_tabela['Valor por kg (R$)'].apply(lambda x: f"R$ {x:.2f}".replace(".", ","))
        df_tabela['Valor Total (R$)'] = df_tabela['Valor Total (R$)'].apply(lambda x: f"R$ {x:.2f}".replace(".", ","))

        # Exibir tabela principal
        st.dataframe(
            df_tabela,
            use_container_width=True,
            height=600,
            column_config={
                "Data/Hora": st.column_config.DatetimeColumn(
                    "Data/Hora",
                    format="DD/MM/YYYY HH:mm:ss"
                )
            }
        )

        # Botão para gerar PDF da tabela visível
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("📄 Gerar PDF desta Tabela", use_container_width=True):
                with st.spinner("Gerando relatório..."):
                    nome_arquivo = gerar_pdf_tabela(df_tabela)

                    with open(nome_arquivo, "rb") as f:
                        st.success("Relatório gerado com sucesso!")
                        st.download_button(
                            label="⬇️ Baixar Relatório Completo",
                            data=f,
                            file_name=nome_arquivo,
                            mime="application/pdf",
                            use_container_width=True
                        )

                    os.remove(nome_arquivo)

        # Seção de Totais por Produto
        st.subheader("📊 Totais por Produto")

        # Calcular totais
        df_totais = st.session_state.pesagens.groupby('Produto').agg({
            'PesoLiquido': 'sum',
            'ValorTotal': 'sum',
            'Codigo': 'first'
        }).reset_index()

        # Formatar valores
        df_totais['PesoLiquido'] = df_totais['PesoLiquido'].apply(lambda x: f"{x:.3f} kg".replace(".", ","))
        df_totais['ValorTotal'] = df_totais['ValorTotal'].apply(lambda x: f"R$ {x:.2f}".replace(".", ","))

        # Ordenar por maior valor total
        df_totais = df_totais.sort_values('ValorTotal', ascending=False)

        # Exibir tabela de totais
        st.dataframe(
            df_totais[['Codigo', 'Produto', 'PesoLiquido', 'ValorTotal']],
            column_config={
                "Codigo": "Código",
                "Produto": st.column_config.TextColumn("Produto", width="medium"),
                "PesoLiquido": st.column_config.TextColumn("Peso Total", width="small"),
                "ValorTotal": st.column_config.TextColumn("Valor Total", width="small")
            },
            hide_index=True,
            use_container_width=True
        )

        # Exibir totais gerais
        st.markdown("---")
        col_total1, col_total2 = st.columns(2)
        with col_total1:
            st.metric("Total em Peso",
                      f"{st.session_state.pesagens['PesoLiquido'].sum():.3f} kg".replace(".", ","))

        with col_total2:
            st.metric("Total em Valor",
                      f"R$ {st.session_state.pesagens['ValorTotal'].sum():.2f}".replace(".", ","))

    else:
        st.info("Nenhum produto cadastrado ainda. Use a simulação de balança para registrar produtos.")
# Função para simulação de balança
def simulacao_balanca():
    st.title("⚖️ Gestão e Controle de produção ")

    # Seção de busca do produto
    col_busca1, col_busca2 = st.columns([1, 3])
    with col_busca1:
        codigo_busca = st.text_input("Digite o código para buscar", key="codigo_busca",
                                     placeholder="Ex: 1096 para BEIJINHO")
    with col_busca2:
        if st.button("🔍 Buscar Produto", key="buscar_produto"):
            if codigo_busca in produtos:
                st.session_state.produto_selecionado = produtos[codigo_busca]['nome']
                st.session_state.codigo_selecionado = codigo_busca
                st.session_state.valor_kg = produtos[codigo_busca]['valor_kg']
                st.session_state.tara = produtos[codigo_busca]['tara']
                st.success(f"Produto encontrado: {produtos[codigo_busca]['nome']}")
            else:
                st.warning("Código não encontrado")

    # Formulário principal de pesagem
    with st.form("balanca_form", clear_on_submit=True):  # Limpar formulário ao enviar
        col1, col2, col3 = st.columns(3)

        with col1:
            codigo = st.text_input("Código do Produto",
                                   value=st.session_state.get('codigo_selecionado', ''),
                                   key="codigo_input")

            produto = st.text_input("Produto",
                                    value=st.session_state.get('produto_selecionado', ''),
                                    key="produto_input")

            peso = st.number_input("Peso (kg)", min_value=0.0, step=0.001, format="%.3f",
                                   value=0.0)

        with col2:
            tara = st.number_input("Tara (kg)", min_value=0.0, step=0.001, format="%.3f",
                                   value=st.session_state.get('tara', 0.0),
                                   key="tara_input")

            valor_kg = st.number_input("Valor por kg (R$)", min_value=0.0, step=0.01,
                                       value=st.session_state.get('valor_kg', 0.0),
                                       format="%.2f",
                                       key="valor_kg_input")

            funcionario = st.text_input("Funcionário Responsável", "Padrão")

        with col3:
            tipo_operacao = st.selectbox("Tipo de Operação", ["Controle", "Quebra"])

            if tipo_operacao == "Quebra":
                sobra = st.number_input("Sobra (kg)", min_value=0.0, step=0.001, format="%.3f",
                                        value=0.0)
                farinha_rosca = st.number_input("Transformado em Farinha de Rosca (kg)",
                                                min_value=0.0, step=0.001, format="%.3f",
                                                value=0.0)
                torrada = st.number_input("Transformado em Torrada (kg)",
                                          min_value=0.0, step=0.001, format="%.3f",
                                          value=0.0)
            else:
                sobra = 0.0
                farinha_rosca = 0.0
                torrada = 0.0

        submitted = st.form_submit_button("📝 Calcular e Registrar")

        if submitted:
            if not codigo or not produto:
                st.error("Código e nome do produto são obrigatórios!")
                return

            peso_liquido = max(0, peso - tara)
            valor_total = peso_liquido * valor_kg

            nova_pesagem = {
                'DataHora': datetime.now(),
                'Funcionario': funcionario,
                'Codigo': codigo,
                'Produto': produto,
                'Peso': peso,
                'Tara': tara,
                'PesoLiquido': peso_liquido,
                'ValorKg': valor_kg,
                'ValorTotal': valor_total,
                'TipoOperacao': tipo_operacao,
                'Sobra': sobra,
                'FarinhaRosca': farinha_rosca,
                'Torrada': torrada,
                'DiferencaPeso': sobra - (farinha_rosca + torrada) if tipo_operacao == "Quebra" else 0,
                'DiferencaValor': (sobra - (farinha_rosca + torrada)) * valor_kg if tipo_operacao == "Quebra" else 0,
                'ImpactoCusto': (sobra - (farinha_rosca + torrada)) * valor_kg if tipo_operacao == "Quebra" else 0
            }

            st.session_state.pesagens = pd.concat([
                st.session_state.pesagens,
                pd.DataFrame([nova_pesagem])
            ], ignore_index=True)

            st.success("Pesagem registrada com sucesso!")

            # Exibir resultados
            st.subheader("Resultados da Pesagem")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Peso Líquido (kg)", f"{peso_liquido:.3f}".replace(".", ","))
                st.metric("Valor Total (R$)", f"R$ {valor_total:.2f}".replace(".", ","))
            with col2:
                if tipo_operacao == "Quebra":
                    st.metric("Diferença de Peso (kg)", f"{(sobra - (farinha_rosca + torrada)):.3f}".replace(".", ","))
                    st.metric("Impacto no Custo (R$)",
                              f"R$ {(sobra - (farinha_rosca + torrada)) * valor_kg:.2f}".replace(".", ","))

    # Exibir tabela de produtos cadastrados
    exibir_tabela_produtos()
# Função para visualização de dados e relatórios
def visualizacao_dados():
    st.title("📊 Visualização de Dados")

    if st.session_state.pesagens.empty:
        st.warning("Nenhum dado disponível para visualização.")
        return

    # Filtros
    st.subheader("Filtros")
    col1, col2, col3 = st.columns(3)

    with col1:
        data_inicio = st.date_input("Data inicial", value=st.session_state.pesagens['DataHora'].min())

    with col2:
        data_fim = st.date_input("Data final", value=st.session_state.pesagens['DataHora'].max())

    with col3:
        tipo_operacao_filtro = st.multiselect(
            "Tipo de Operação",
            options=st.session_state.pesagens['TipoOperacao'].unique(),
            default=st.session_state.pesagens['TipoOperacao'].unique()
        )

    # Aplicar filtros
    df_filtrado = st.session_state.pesagens[
        (st.session_state.pesagens['DataHora'].dt.date >= data_inicio) &
        (st.session_state.pesagens['DataHora'].dt.date <= data_fim) &
        (st.session_state.pesagens['TipoOperacao'].isin(tipo_operacao_filtro))
        ]

    if df_filtrado.empty:
        st.warning("Nenhum dado encontrado com os filtros aplicados.")
        return

    # Métricas resumidas
    st.subheader("Métricas Gerais")
    col_met1, col_met2, col_met3, col_met4 = st.columns(4)

    with col_met1:
        st.metric("Total Pesado (kg)", f"{df_filtrado['PesoLiquido'].sum():.3f}".replace(".", ","))

    with col_met2:
        st.metric("Valor Total (R$)", f"R$ {df_filtrado['ValorTotal'].sum():.2f}".replace(".", ","))

    with col_met3:
        st.metric("Sobras (kg)", f"{df_filtrado['Sobra'].sum():.3f}".replace(".", ","))

    with col_met4:
        st.metric("Perdas Financeiras (R$)", f"R$ {df_filtrado['ImpactoCusto'].sum():.2f}".replace(".", ","))

    # Gráficos
    st.subheader("Análise Gráfica")

    tab1, tab2, tab3 = st.tabs(["Produção x Sobras", "Distribuição por Produto", "Evolução Diária"])

    with tab1:
        fig, ax = plt.subplots()
        df_prod_sobra = df_filtrado.groupby('TipoOperacao').agg({'PesoLiquido': 'sum', 'Sobra': 'sum'}).reset_index()
        ax.bar(df_prod_sobra['TipoOperacao'], df_prod_sobra['PesoLiquido'], label='Produção')
        ax.bar(df_prod_sobra['TipoOperacao'], df_prod_sobra['Sobra'], label='Sobras',
               bottom=df_prod_sobra['PesoLiquido'])
        ax.set_title("Produção vs Sobras por Tipo de Operação")
        ax.set_ylabel("Peso (kg)")
        ax.legend()
        st.pyplot(fig)

    with tab2:
        top_produtos = st.slider("Mostrar top", 5, 20, 10)
        df_prod = df_filtrado.groupby('Produto').agg({'PesoLiquido': 'sum', 'Sobra': 'sum'}).nlargest(top_produtos,
                                                                                                      'PesoLiquido').reset_index()

        fig, ax = plt.subplots(figsize=(10, 6))
        width = 0.35
        x = np.arange(len(df_prod))
        ax.bar(x - width / 2, df_prod['PesoLiquido'], width, label='Produção')
        ax.bar(x + width / 2, df_prod['Sobra'], width, label='Sobras')
        ax.set_xticks(x)
        ax.set_xticklabels(df_prod['Produto'], rotation=45, ha='right')
        ax.set_title(f"Top {top_produtos} Produtos - Produção vs Sobras")
        ax.set_ylabel("Peso (kg)")
        ax.legend()
        st.pyplot(fig)

    with tab3:
        df_diario = df_filtrado.set_index('DataHora').resample('D').agg(
            {'PesoLiquido': 'sum', 'Sobra': 'sum'}).reset_index()

        fig, ax = plt.subplots()
        ax.plot(df_diario['DataHora'], df_diario['PesoLiquido'], label='Produção')
        ax.plot(df_diario['DataHora'], df_diario['Sobra'], label='Sobras')
        ax.set_title("Evolução Diária da Produção e Sobras")
        ax.set_ylabel("Peso (kg)")
        ax.legend()
        st.pyplot(fig)

    # Tabela detalhada
    st.subheader("Histórico Completo")
    st.dataframe(df_filtrado, use_container_width=True)
# Função para exibir histórico diário
def exibir_historico():
    st.title("🗃️ Histórico Diário")

    if not st.session_state.historico_diario:
        st.warning("Nenhum histórico disponível.")
        return

    # Selecionar data para visualização
    data_selecionada = st.selectbox(
        "Selecione a data para visualizar:",
        sorted(st.session_state.historico_diario.keys(), reverse=True)
    )

    if data_selecionada:
        df_historico = pd.DataFrame(st.session_state.historico_diario[data_selecionada])
        df_historico['DataHora'] = pd.to_datetime(df_historico['DataHora'])

        st.subheader(f"Registros do dia {data_selecionada}")

        # Mostrar métricas resumidas
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Pesado (kg)", f"{df_historico['PesoLiquido'].sum():.3f}".replace(".", ","))
        with col2:
            st.metric("Valor Total (R$)", f"R$ {df_historico['ValorTotal'].sum():.2f}".replace(".", ","))

        # Mostrar tabela
        st.dataframe(df_historico, use_container_width=True)

        # Opção para exportar
        if st.button("Exportar Dados desta Data"):
            nome_arquivo = f"historico_{data_selecionada}.csv"
            df_historico.to_csv(nome_arquivo, index=False, encoding='utf-8-sig')

            with open(nome_arquivo, "rb") as f:
                st.download_button(
                    label="Baixar CSV",
                    data=f,
                    file_name=nome_arquivo,
                    mime="text/csv"
                )

            os.remove(nome_arquivo)
# Função para gerar relatórios em PDF em modo paisagem (não implementada ainda)
def gerar_relatorio_pdf():
    if st.session_state.pesagens.empty:
        st.warning("Nenhum dado disponível para gerar relatório.")
        return

    # Filtros para o relatório
    st.subheader("Configuração do Relatório")

    col1, col2 = st.columns(2)

    with col1:
        data_inicio_rel = st.date_input("Data inicial", value=st.session_state.pesagens['DataHora'].min(),
                                        key="rel_inicio")

    with col2:
        data_fim_rel = st.date_input("Data final", value=st.session_state.pesagens['DataHora'].max(), key="rel_fim")

    tipo_operacao_rel = st.multiselect(
        "Tipo de Operação",
        options=st.session_state.pesagens['TipoOperacao'].unique(),
        default=st.session_state.pesagens['TipoOperacao'].unique(),
        key="rel_tipo_op"
    )

    # Aplicar filtros
    df_relatorio = st.session_state.pesagens[
        (st.session_state.pesagens['DataHora'].dt.date >= data_inicio_rel) &
        (st.session_state.pesagens['DataHora'].dt.date <= data_fim_rel) &
        (st.session_state.pesagens['TipoOperacao'].isin(tipo_operacao_rel))
        ]

    if df_relatorio.empty:
        st.warning("Nenhum dado encontrado com os filtros aplicados.")
        return

    # Definir categorias de produtos
    categorias = {
        "BOLOS": ["BOLO", "BOLINHO"],
        "PÃES": ["PÃO", "BRIOCHE", "BROA"],
        "SALGADOS": ["COXINHA", "EMPADA", "PASTEL", "SALGADINHO", "TORTA SALGADA"],
        "DOCES": ["BEIJINHO", "BRIGADEIRO", "DOCE", "MOUSSE", "TORTA DOCE"],
        "BISCOITOS": ["BISCOITO", "BOLACHA", "TORRADA"],
        "OUTROS": []
    }

    # Função para determinar a categoria do produto
    def determinar_categoria(produto):
        produto = produto.upper()
        for categoria, palavras_chave in categorias.items():
            for palavra in palavras_chave:
                if palavra in produto:
                    return categoria
        return "OUTROS"

    # Adicionar coluna de categoria ao DataFrame
    df_relatorio['Categoria'] = df_relatorio['Produto'].apply(determinar_categoria)

    # Gerar PDF
    if st.button("Gerar Relatório em PDF"):
        # Configurar PDF em modo paisagem
        pdf = FPDF(orientation='L')
        pdf.add_page()
        pdf.set_font("Arial", size=10)

        # Cabeçalho
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, txt="Relatório de Produção - Padaria", ln=1, align='C')
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, txt=f"Período: {data_inicio_rel.strftime('%d/%m/%Y')} a {data_fim_rel.strftime('%d/%m/%Y')}",
                 ln=1)
        pdf.cell(0, 10, txt=f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", ln=1)
        pdf.ln(10)

        # Dicionário para armazenar totais por categoria
        totais_categorias = {}

        # Gerar tabela para cada categoria
        for categoria in sorted(df_relatorio['Categoria'].unique()):
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, txt=f"Categoria: {categoria}", ln=1)
            pdf.set_font("Arial", size=8)

            # Filtrar por categoria
            df_categoria = df_relatorio[df_relatorio['Categoria'] == categoria]

            # Cabeçalho da tabela (ajustado para paisagem)
            colunas = ['Data', 'Produto', 'Peso (kg)', 'Tara (kg)', 'Líquido (kg)', 'Valor/kg (R$)', 'Total (R$)',
                       'Operação']
            larguras = [25, 70, 20, 20, 20, 25, 25, 20]

            # Cabeçalho
            for i in range(len(colunas)):
                pdf.cell(larguras[i], 10, txt=colunas[i], border=1, align='C')
            pdf.ln()

            # Dados
            pdf.set_font("Arial", size=8)
            total_categoria = 0
            peso_total_categoria = 0

            for _, row in df_categoria.iterrows():
                pdf.cell(larguras[0], 10, txt=row['DataHora'].strftime('%d/%m/%y'), border=1)
                pdf.cell(larguras[1], 10, txt=row['Produto'], border=1)
                pdf.cell(larguras[2], 10, txt=f"{row['Peso']:.3f}".replace(".", ","), border=1, align='R')
                pdf.cell(larguras[3], 10, txt=f"{row['Tara']:.3f}".replace(".", ","), border=1, align='R')
                pdf.cell(larguras[4], 10, txt=f"{row['PesoLiquido']:.3f}".replace(".", ","), border=1, align='R')
                pdf.cell(larguras[5], 10, txt=f"{row['ValorKg']:.2f}".replace(".", ","), border=1, align='R')
                pdf.cell(larguras[6], 10, txt=f"{row['ValorTotal']:.2f}".replace(".", ","), border=1, align='R')
                pdf.cell(larguras[7], 10, txt=row['TipoOperacao'], border=1, align='C')
                pdf.ln()

                total_categoria += row['ValorTotal']
                peso_total_categoria += row['PesoLiquido']

            # Total da categoria
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(sum(larguras[:7]), 10, txt="Total da Categoria:", border=1, align='R')
            pdf.cell(larguras[7], 10, txt=f"{total_categoria:.2f}".replace(".", ","), border=1, align='R')
            pdf.ln()

            # Armazenar totais para o resumo final
            totais_categorias[categoria] = {
                'total': total_categoria,
                'peso': peso_total_categoria
            }

            pdf.ln(5)

        # Resumo Geral
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, txt="Resumo Geral", ln=1)
        pdf.set_font("Arial", size=10)

        # Cabeçalho do resumo (ajustado para paisagem)
        colunas_resumo = ['Categoria', 'Peso Total (kg)', 'Valor Total (R$)']
        larguras_resumo = [100, 50, 50]

        for i in range(len(colunas_resumo)):
            pdf.cell(larguras_resumo[i], 10, txt=colunas_resumo[i], border=1, align='C')
        pdf.ln()

        # Dados do resumo
        pdf.set_font("Arial", size=10)
        total_geral = 0
        peso_total_geral = 0

        for categoria, valores in totais_categorias.items():
            pdf.cell(larguras_resumo[0], 10, txt=categoria, border=1)
            pdf.cell(larguras_resumo[1], 10, txt=f"{valores['peso']:.3f}".replace(".", ","), border=1, align='R')
            pdf.cell(larguras_resumo[2], 10, txt=f"{valores['total']:.2f}".replace(".", ","), border=1, align='R')
            pdf.ln()

            total_geral += valores['total']
            peso_total_geral += valores['peso']

        # Total Geral
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(larguras_resumo[0], 10, txt="TOTAL GERAL:", border=1, align='R')
        pdf.cell(larguras_resumo[1], 10, txt=f"{peso_total_geral:.3f}".replace(".", ","), border=1, align='R')
        pdf.cell(larguras_resumo[2], 10, txt=f"{total_geral:.2f}".replace(".", ","), border=1, align='R')
        pdf.ln()

        # Salvar PDF
        nome_arquivo = f"relatorio_padaria_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf.output(nome_arquivo)

        # Disponibilizar para download
        with open(nome_arquivo, "rb") as f:
            st.success("Relatório gerado com sucesso!")
            st.download_button(
                label="Baixar Relatório PDF",
                data=f,
                file_name=nome_arquivo,
                mime="application/pdf"
            )

        # Remover arquivo temporário
        os.remove(nome_arquivo)
# Função para exportar dados
def exportar_dados():
    if st.session_state.pesagens.empty:
        st.warning("Nenhum dado disponível para exportar.")
        return

    st.subheader("Exportar Dados")

    formato = st.radio("Formato de exportação:", ["CSV", "Excel"])

    if st.button("Exportar Dados"):
        if formato == "CSV":
            nome_arquivo = f"dados_padaria_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            st.session_state.pesagens.to_csv(nome_arquivo, index=False, encoding='utf-8-sig')
        else:
            nome_arquivo = f"dados_padaria_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            st.session_state.pesagens.to_excel(nome_arquivo, index=False)

        with open(nome_arquivo, "rb") as f:
            st.download_button(
                label=f"Baixar Arquivo {formato}",
                data=f,
                file_name=nome_arquivo,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" if formato == "Excel" else "text/csv"
            )

        # Remover arquivo temporário
        os.remove(nome_arquivo)
# Função principal
def main():
    if 'menu_choice' not in st.session_state:
        st.session_state.menu_choice = "balanca"

    # Carregar dados ao iniciar
    if not st.session_state.get('dados_carregados', False):
        if carregar_dados():
            st.session_state.dados_carregados = True

    painel_lateral()

    if st.session_state.menu_choice == "balanca":
        simulacao_balanca()
    elif st.session_state.menu_choice == "visualizacao":
        visualizacao_dados()
    elif st.session_state.menu_choice == "relatorio":
        gerar_relatorio_pdf()
    elif st.session_state.menu_choice == "historico":
        exibir_historico()
    elif st.session_state.menu_choice == "produtos":
        gerenciar_produtos()

if __name__ == "__main__":
    main()