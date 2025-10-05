import streamlit as st
import pandas as pd

# Elementos de HTML -----------------------------------------------------------------
def titulo():
    st.title('Dados Notas Fiscais')

def estado(nome:str, valor):
    st.session_state[nome] = valor

def footer():
    st.markdown("""
        <style>
            footer {
                position: fixed;
                left: 0;
                z-index: 9999;
                bottom: 0;
                width: 100%;
                background-color: #2A2A33;
                
                text-align: center;
                padding: 10px;
                font-size: 14px;
            }
        </style>
        <footer>
            © UFS 2025
        </footer>
    """,unsafe_allow_html=True)

def botao_padrao():
     st.markdown("""
        <style>
        div.stButton > button {
            background-color: #4CAF50;
            margin-top: 10px;
            color: white;
            width: 165px;
        }
        </style>
    """, unsafe_allow_html=True)
     
def texto_padrao(texto:str):
    st.markdown(f"""
        <div style="font-size: 14px; color: white;">
        {texto}
        </div>
    """, unsafe_allow_html=True)

def imagem_cafe(gif:str, img:str):
    st.markdown(f"""
        <div style="text-align: center;">
            <img src={gif} width="36">
        </div>
    """,unsafe_allow_html=True)
    st.image(img)

def barra_progresso():
    st.markdown("""
        <style>
        div.stProgress > div > div > div > div {
            background-color: limegreen;
        }
        </style>
    """,unsafe_allow_html=True)
    cl1, cl2 = st.columns([20, 1])
    progress_bar = cl1.progress(0)
    porcentagem = cl2.empty()
    return progress_bar, porcentagem

def progresso(N:int, progress_bar, porcentagem):

    progress_bar.progress(N/8)
    porcentagem.markdown(
    f"""<div style="font-size: 15px; text-align: center; color: #4CAF50;">
        {int(N/8*100)}%
    </div>""",unsafe_allow_html=True)

# Funções de Normalização -----------------------------------------------------------

def prenormalizar(col):
    return col.fillna('').astype(str).str.strip().str.replace('.','',regex=False)
def normalizar_ncm (col):
    return prenormalizar(col).str.zfill(8)
def normalizar_cnae (col):
    return prenormalizar(col).str.zfill(7)
def normalizar_vprod(df):
    df['VPROD'] = (df['VPROD'].astype(str).str.strip().str.replace(',', '.', regex=False))
    df['VPROD'] = pd.to_numeric(df['VPROD'], errors='coerce')
    df.loc[:,'VPROD'] = df['VPROD'].astype(float)
    df['PRODUTOS SCN'] = df['PRODUTOS SCN'].fillna('').str.strip().str.upper()

# Listas e Dicionários --------------------------------------------------------------

def list_ano():
    anos = ['','2018','2019','2020','2021','2022','2023']
    return anos

def list_uf():
    uf = ['','SE','RJ','SP','ES','MG','PR','SC','RS','MS',
    'GO','AC','AL','AP','AM','BA','CE','DF','MA',
    'MT','PA','PB','PE','PI','RN','RO','RR','TO']
    return uf

def list_municipio():
    mun = [
        '',
        'AMPARO DE SAO FRANCISCO',
        'AQUIDABA',
        'ARACAJU',
        'ARAUA',
        'AREIA BRANCA',
        'BARRA DOS COQUEIROS',
        'BOQUIM',
        'BREJO GRANDE',
        'CAMPO DO BRITO',
        'CANHOBA',
        'CANINDE DE SAO FRANCISCO',
        'CAPELA',
        'CARIRA',
        'CARMOPOLIS',
        'CEDRO DE SAO JOAO',
        'CRISTINAPOLIS',
        'CUMBE',
        'DIVINA PASTORA',
        'ESTANCIA',
        'FEIRA NOVA',
        'FREI PAULO',
        'GARARU',
        'GENERAL MAYNARD',
        'GRACCHO CARDOSO',
        'ILHA DAS FLORES',
        'INDIAROBA',
        'ITABAIANA',
        'ITABAIANINHA',
        'ITABI',
        'ITAPORANGA DAJUDA',
        'JAPARATUBA',
        'JAPOATA',
        'LAGARTO',
        'LARANJEIRAS',
        'MACAMBIRA',
        'MALHADA DOS BOIS',
        'MALHADOR',
        'MARUIM',
        'MOITA BONITA',
        'MONTE ALEGRE DE SERGIPE',
        'MURIBECA',
        'NEOPOLIS',
        'NOSSA SENHORA APARECIDA',
        'NOSSA SENHORA DA GLORIA',
        'NOSSA SENHORA DAS DORES',
        'NOSSA SENHORA DE LOURDES',
        'NOSSA SENHORA DO SOCORRO',
        'PACATUBA',
        'PEDRA MOLE',
        'PEDRINHAS',
        'PINHAO',
        'PIRAMBU',
        'POÇO REDONDO',
        'POÇO VERDE',
        'PORTO DA FOLHA',
        'PROPRIA',
        'RIACHAO DO DANTAS',
        'RIACHUELO',
        'RIBEIROPOLIS',
        'ROSARIO DO CATETE',
        'SALGADO',
        'SANTA LUZIA DO ITANHY',
        'SANTA ROSA DE LIMA',
        'SANTANA DO SAO FRANCISCO',
        'SANTO AMARO DAS BROTAS',
        'SAO CRISTOVAO',
        'SAO DOMINGOS',
        'SAO FRANCISCO',
        'SAO MIGUEL DO ALEIXO',
        'SIMAO DIAS',
        'SIRIRI',
        'TELHA',
        'TOBIAS BARRETO',
        'TOMAR DO GERU',
        'UMBAUBA'
    ]
    return mun

def list_produtos():
    scn = [
        "ARROZ; TRIGO E OUTROS CEREAIS",
        "CANA-DE-ACUCAR",
        "OUTROS PRODUTOS E SERVICOS DA LAVOURA TEMPORARIA",
        "LARANJA",
        "PRODUTOS DA LAVOURA PERMANENTE",
        "BOVINOS E OUTROS ANIMAIS VIVOS; PRODS. ANIMAL; CACA E SERV.",
        "LEITE DE VACA E DE OUTROS ANIMAIS",
        "SUINOS",
        "AVES E OVOS",
        "PRODUTOS DA EXPLORACAO FLORESTAL E DA SILVICULTURA",
        "PESCA E AQUICULTURA (PEIXE; CRUSTACEOS E MOLUSCOS)",
        "PETROLEO; GAS NATURAL E SERVICOS DE APOIO",
        "OUTROS PRODUTOS DA INDUSTRIA EXTRATIVA",
        "LEITE E OUTRO PRODUTOS DO LATICINIO",
        "ACUCAR",
        "OUTRO PRODUTOS ALIMENTICIOS",
        "BEBIDAS",
        "PRODUTOS DO FUMO",
        "PRODUTOS TEXTEIS",
        "ARTIGOS DO VESTUARIO E ACESSORIOS",
        "CALCADOS E ARTEFATOS DE COURO",
        "PRODUTOS DE MADEIRA; EXCLUSIVE MOVEIS",
        "CELULOSE; PAPEL; PAPELAO; EMBALAGENS E ARTEFATOS DE PAPEL",
        "SERVICOS DE IMPRESSAO E REPRODUCAO",
        "PRODUTOS DO REFINO DO PETROLEO; ETANOL E OUTROS BIOCOMBUSTIVEIS",
        "PRODUTOS QUIMICOS ORGANICOS E INORGANICOS; RESINA; ELASTOMERO E FIBRAS ARTIF. E SINTETICAS",
        "PERFUMARIA; SABOES E ARTIGOS DE LIMPEZA",
        "PRODUTOS QUIMICOS DIVERSOS",
        "PRODUTOS FARMACEUTICOS",
        "ARTIGOS DE BORRACHA E PLASTICO",
        "CIMENTO",
        "OUTROS PRODUTOS DE MINERAIS NAO METALICOS",
        "PRODUTOS DA METALURGIA",
        "PRODUTOS DE METAL; EXCL. MAQUINAS E EQUIPAMENTOS",
        "EQUIPAMENTOS DE INFORMATICA; PRODUTOS ELETRONICOS E OPTICOS",
        "MAQUINAS; APARELHOS E MATERIAIS ELETRICOS",
        "MAQUINAS E EQUIPAMENTOS",
        "AUTOMOVEIS; CAMINHOES; ONIBUS; CARROCERIAS E REBOQUES",
        "PECAS; ACESSORIOS PARA VEICULOS AUTOMOTORES E OUTROS EQUIPAMENTOS DE TRANSPORTE",
        "MOVEIS",
        "PRODUTOS DE INDUSTRIAS DIVERSAS",
        "MANUTENCAO; REPARACAO E INSTALACAO DE MAQUINAS E EQUIPAMENTOS",
        "ELETRICIDADE; GAS E OUTRAS UTILIDADES",
        "AGUA; ESGOTO; RECICLAGEM E GESTAO DE RESIDUOS",
        "EDIFICACOES",
        "OBRAS DE INFRA-ESTRUTURA",
        "SERVICOS ESPECIALIZADOS PARA CONSTRUCAO",
        "COMERCIO E REPARACAO DE VEICULOS",
        "COMERCIO POR ATACADO E A VAREJO; EXCETO VEICULOS AUTOMOTORES",
        "TRANSPORTE TERRESTRE DE CARGA",
        "TRANSPORTE RODOVIARIO DE PASSAGEIROS",
        "TRANSPORTE AQUAVIARIO",
        "TRANSPORTE AEREO",
        "ARMAZENAMENTO E SERVICOS AUXILIARES AOS TRANSPORTES",
        "CORREIO E OUTROS SERVICOS DE ENTREGA",
        "SERVICOS DE ALOJAMENTO EM HOTEIS E SIMILARES",
        "SERVICOS DE ALIMENTACAO",
        "LIVROS; JORNAIS E REVISTAS",
        "SERVICOS CINEMATOGRAFICOS; MUSICA; RADIO E TELEVISAO",
        "SERVICOS DE TELECOMUNICACOES",
        "TELECOMUNICACOES; TV POR ASSINATURA; DESENVOLVIMENTO DE SISTEMAS E OUTROS SERVICOS DE INFORMACAO",
        "INTERMEDIACAO FINANCEIRA; SEGUROS E PREVIDENCIA COMPLEMENTAR",
        "ALUGUEL EFETIVO E SERVICOS IMOBILIARIOS",
        "ATIVIDADES PROFISSIONAIS; CIENTIFICAS E TECNICAS",
        "ATIVIDADES ADMINISTRATIVAS E SERVICOS COMPLEMENTARES",
        "SERVICOS COLETIVOS DA ADMINISTRACAO PUBLICA E SEGURIDADE SOCIAL",
        "EDUCACAO PUBLICA",
        "EDUCACAO PRIVADA",
        "SAUDE PUBLICA",
        "SAUDE PRIVADA",
        "SERVICOS DE ARTES; CULTURA; ESPORTE E RECREACAO",
        "ORGANIZACOES PATRONAIS; SINDICAIS E OUTROS SERVICOS ASSOCIATIVOS",
        "MANUTENCAO DE COMPUTADORES; TELEFONES E OBJETOS DOMESTICOS",
        "SERVICOS PESSOAIS",
        "SERVICOS DOMESTICOS",
    ]
    return scn

def list_naosetores():
    importantes = [
        "ARROZ; TRIGO E OUTROS CEREAIS",
        "CANA-DE-ACUCAR",
        "OUTROS PRODUTOS E SERVICOS DA LAVOURA TEMPORARIA",
        "LARANJA",
        "PRODUTOS DA LAVOURA PERMANENTE",
        "BOVINOS E OUTROS ANIMAIS VIVOS; PRODS. ANIMAL; CACA E SERV.",
        "LEITE DE VACA E DE OUTROS ANIMAIS",
        "SUINOS",
        "AVES E OVOS",
        "PRODUTOS DA EXPLORACAO FLORESTAL E DA SILVICULTURA",
        "PESCA E AQUICULTURA (PEIXE; CRUSTACEOS E MOLUSCOS)",
        "PETROLEO; GAS NATURAL E SERVICOS DE APOIO",
        "OUTROS PRODUTOS DA INDUSTRIA EXTRATIVA",
        "LEITE E OUTRO PRODUTOS DO LATICINIO",
        "ACUCAR",
        "OUTRO PRODUTOS ALIMENTICIOS",
        "BEBIDAS",
        "PRODUTOS DO FUMO",
        "PRODUTOS TEXTEIS",
        "ARTIGOS DO VESTUARIO E ACESSORIOS",
        "CALCADOS E ARTEFATOS DE COURO",
        "PRODUTOS DE MADEIRA; EXCLUSIVE MOVEIS",
        "CELULOSE; PAPEL; PAPELAO; EMBALAGENS E ARTEFATOS DE PAPEL",
        "SERVICOS DE IMPRESSAO E REPRODUCAO",
        "PRODUTOS DO REFINO DO PETROLEO; ETANOL E OUTROS BIOCOMBUSTIVEIS",
        "PRODUTOS QUIMICOS ORGANICOS E INORGANICOS; RESINA; ELASTOMERO E FIBRAS ARTIF. E SINTETICAS",
        "PERFUMARIA; SABOES E ARTIGOS DE LIMPEZA",
        "PRODUTOS QUIMICOS DIVERSOS",
        "PRODUTOS FARMACEUTICOS",
        "ARTIGOS DE BORRACHA E PLASTICO",
        "CIMENTO",
        "OUTROS PRODUTOS DE MINERAIS NAO METALICOS",
        "PRODUTOS DA METALURGIA",
        "PRODUTOS DE METAL; EXCL. MAQUINAS E EQUIPAMENTOS",
        "EQUIPAMENTOS DE INFORMATICA; PRODUTOS ELETRONICOS E OPTICOS",
        "MAQUINAS; APARELHOS E MATERIAIS ELETRICOS",
        "MAQUINAS E EQUIPAMENTOS",
        "AUTOMOVEIS; CAMINHOES; ONIBUS; CARROCERIAS E REBOQUES",
        "PECAS; ACESSORIOS PARA VEICULOS AUTOMOTORES E OUTROS EQUIPAMENTOS DE TRANSPORTE",
        "MOVEIS",
        "PRODUTOS DE INDUSTRIAS DIVERSAS",
    ]
    return importantes

def list_setores():
    serv_cnae = [
        "AGRICULTURA",
        "PECUARIA",
        "PRODUCAO FLORESTAL; PESCA E AQUICULTURA",
        "OUTROS DA INDUSTRIA EXTRATIVA",
        "EXTRACAO DE PETROLEO E GAS",
        "ALIMENTOS",
        "BEBIDAS E FUMO",
        "TEXTEIS E VESTUARIO",
        "CALCADOS E ARTEFATOS DE COURO",
        "PRODUTOS DE MADEIRA; CELULOSE; PAPEL; IMPRESSAO E GRAVACAO",
        "REFINO DE PETROLEO E BIOCOMBUSTIVEIS",
        "QUIMICOS; BORRACHA E PLASTICO",
        "CIMENTO",
        "OUTROS MINERAIS NAO METALICOS E SIDERURGIA",
        "MAQUINAS; EQUIPAMENTOS E MANUTENCAO",
        "AUTOMOVEIS; PECAS E ACESSORIOS",
        "MOVEIS E PRODUTOS DE INDUSTRIAS DIVERSAS",
        "ENERGIA ELETRICA; GAS NATURAL E OUTRAS UTILIDADES",
        "AGUA; ESGOTO E GESTAO DE RESIDUOS",
        "CONSTRUCAO",
        "COMERCIO",
        "TRANSPORTE TERRESTRE",
        "TRANSPORTE AQUAVIARIO",
        "TRANSPORTE AEREO",
        "ARMAZENAMENTO; ATIVIDADES AUXILIARES DOS TRANSPORTES E CORREIO",
        "ALOJAMENTO",
        "ALIMENTACAO",
        "SERVICOS DE INFORMACAO",
        "INTERMEDIACAO FINANCEIRA",
        "ATIVIDADES IMOBILIARIAS",
        "SERVICOS AS IMPRESAS",
        "ALUGUEIS NAO-IMOBILIARIOS E OUTRAS ATIVIDADES ADMINISTRATIVAS",
        "SAUDE PUBLICA; EDUCACAO PUBLICA E ADMINISTRACAO PUBLICA",
        "EDUCACAO PRIVADA",
        "SAUDE PRIVADA",
        "SERVICOS AS FAMILIAS"
    ]
    return serv_cnae

def dict_bec():
    dic_bec = {
        'TODOS' : ['','0','41','521','111','121','21','22','31','322','42','53','61','51','522','62','63','112','122','321','7'],
        # 'BENS DE CAPITAL' : ['41','521'],
        # 'BENS INTERMEDIARIOS' : ['111','121','21','22','31','322','42','53'],
        # 'BENS DE CONSUMO' : ['61','51','522','62','63','112','122','321'],
    }
    return dic_bec

def dict_mes():
    mes = {
        ' ': ' ',
        'JANEIRO': '01',
        'FEVEREIRO': '02',
        'MARÇO': '03',
        'ABRIL': '04',
        'MAIO': '05',
        'JUNHO': '06',
        'JULHO': '07',
        'AGOSTO': '08',
        'SETEMBRO': '09',
        'OUTUBRO': '10',
        'NOVEMBRO': '11',
        'DEZEMBRO': '12',
    }
    return mes