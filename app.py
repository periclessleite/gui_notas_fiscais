import pandas as pd
import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
import io

#Credenciais do Google API
escopo = ['https://www.googleapis.com/auth/drive']
conta_servico = 'credenciais.json'
creds = service_account.Credentials.from_service_account_file(
    conta_servico, scopes=escopo)
service = build('drive','v3',credentials=creds)

#Início do site
st.title('Dados Notas Fiscais')

#Caixas de seleção
sb_ano = ['','2018','2019','2020','2021','2022','2023']
uf_dest = ['','SE','RJ','SP','ES','MG','PR','SC','RS','MS',
            'GO','AC','AL','AP','AM','BA','CE','DF','MA',
            'MT','PA','PB','PE','PI','RN','RO','RR','TO']
uf_emit = ['','SE','RJ','SP','ES','MG','PR','SC','RS','MS',
            'GO','AC','AL','AP','AM','BA','CE','DF','MA',
            'MT','PA','PB','PE','PI','RN','RO','RR','TO']

mun_dest = ['','AMPARO DE SAO FRANCISCO','AQUIDABA','ARACAJU','ARAUA', 
            'AREIA BRANCA','BARRA DOS COQUEIROS','BOQUIM','BREJO GRANDE', 
            'CAMPO DO BRITO','CANHOBA','CANINDE DE SAO FRANCISCO', 
            'CAPELA','CARIRA','CARMOPOLIS','CEDRO DE SAO JOAO','CRISTINAPOLIS', 
            'CUMBE','DIVINA PASTORA','ESTANCIA','FEIRA NOVA','FREI PAULO', 
            'GARARU','GENERAL MAYNARD','GRACCHO CARDOSO','ILHA DAS FLORES', 
            'INDIAROBA','ITABAIANA','ITABAIANINHA','ITABI','ITAPORANGA DAJUDA',
            'JAPARATUBA','JAPOATA','LAGARTO','LARANJEIRAS','MACAMBIRA','MALHADA DOS BOIS', 
            'MALHADOR','MARUIM','MOITA BONITA','MONTE ALEGRE DE SERGIPE','MURIBECA', 
            'NEOPOLIS','NOSSA SENHORA APARECIDA','NOSSA SENHORA DA GLORIA', 
            'NOSSA SENHORA DAS DORES','NOSSA SENHORA DE LOURDES','NOSSA SENHORA DO SOCORRO', 
            'PACATUBA','PEDRA MOLE','PEDRINHAS','PINHAO','PIRAMBU','POÇO REDONDO', 
            'POÇO VERDE','PORTO DA FOLHA','PROPRIA','RIACHAO DO DANTAS','RIACHUELO', 
            'RIBEIROPOLIS','ROSARIO DO CATETE','SALGADO','SANTA LUZIA DO ITANHY', 
            'SANTA ROSA DE LIMA','SANTANA DO SAO FRANCISCO','SANTO AMARO DAS BROTAS', 
            'SAO CRISTOVAO','SAO DOMINGOS','SAO FRANCISCO','SAO MIGUEL DO ALEIXO', 
            'SIMAO DIAS','SIRIRI','TELHA','TOBIAS BARRETO','TOMAR DO GERU','UMBAUBA']
mun_emit = ['','AMPARO DE SAO FRANCISCO','AQUIDABA','ARACAJU','ARAUA', 
            'AREIA BRANCA','BARRA DOS COQUEIROS','BOQUIM','BREJO GRANDE', 
            'CAMPO DO BRITO','CANHOBA','CANINDE DE SAO FRANCISCO', 
            'CAPELA','CARIRA','CARMOPOLIS','CEDRO DE SAO JOAO','CRISTINAPOLIS', 
            'CUMBE','DIVINA PASTORA','ESTANCIA','FEIRA NOVA','FREI PAULO', 
            'GARARU','GENERAL MAYNARD','GRACCHO CARDOSO','ILHA DAS FLORES', 
            'INDIAROBA','ITABAIANA','ITABAIANINHA','ITABI','ITAPORANGA DAJUDA',
            'JAPARATUBA','JAPOATA','LAGARTO','LARANJEIRAS','MACAMBIRA','MALHADA DOS BOIS', 
            'MALHADOR','MARUIM','MOITA BONITA','MONTE ALEGRE DE SERGIPE','MURIBECA', 
            'NEOPOLIS','NOSSA SENHORA APARECIDA','NOSSA SENHORA DA GLORIA', 
            'NOSSA SENHORA DAS DORES','NOSSA SENHORA DE LOURDES','NOSSA SENHORA DO SOCORRO', 
            'PACATUBA','PEDRA MOLE','PEDRINHAS','PINHAO','PIRAMBU','POÇO REDONDO', 
            'POÇO VERDE','PORTO DA FOLHA','PROPRIA','RIACHAO DO DANTAS','RIACHUELO', 
            'RIBEIROPOLIS','ROSARIO DO CATETE','SALGADO','SANTA LUZIA DO ITANHY', 
            'SANTA ROSA DE LIMA','SANTANA DO SAO FRANCISCO','SANTO AMARO DAS BROTAS', 
            'SAO CRISTOVAO','SAO DOMINGOS','SAO FRANCISCO','SAO MIGUEL DO ALEIXO', 
            'SIMAO DIAS','SIRIRI','TELHA','TOBIAS BARRETO','TOMAR DO GERU','UMBAUBA']

cod_bec = ['','41','521','111','121','21','22','31','322','42','53','61','51','522','62','63','112','122','321','7']
flag_bec = 0 #Flag
#Cria duas colunas no Streamlit
col1, col2, col3, col4 = st.columns(4)

#Separação das colunas
with col1:
    ano = st.selectbox('Ano',sb_ano)
    cbec = st.selectbox('Código BEC', cod_bec)
with  col2:
    mun_d = st.selectbox('Município de destino',mun_dest)
    mun_e = st.selectbox('Município emitente',mun_emit)
with  col3:
    uf_d = st.selectbox('UF de destino',uf_dest)
    uf_e = st.selectbox('UF de emissão',uf_emit)
with  col4:
    ncm = str(st.text_input('Código NCM'))
    cnae = str(st.text_input('Código CNAE'))
    if  len(cnae) > 7:
        st.write(f'Não há correspondentes para essa busca.')

#Espera uma resposta
if ano == '':
    st.stop()

#Direcionamento para os arquivos no Drive
id = {
    'pib_2018_NFe.csv': '1G-kiN3ohykICWGXuymJvwGN-zkGoUvpq',
    'pib_2019_NFe.csv': '1w1ndeTTi870A_7s71kr35SHjKa7LZxBy',
    'pib_2020_NFe.csv': '1LYjoS6QHruCfi7NJ0KHoBeEqyaGGFc6h',
    'pib_2021_NFe.csv': '1qEcoHW0CDiXWM9IgLfKq4vjrmfubHcJk',
    'pib_2022_NFe.csv': '1QuO5DZFcXyC9ex46aYWJs3hIFlzOcyW6',
    'pib_2023_NFe.csv': '1dH0yQhjxIphV84LqzVom0c0DUbDCJiFU',
}

#Cria variáveis de caminho
notas = f'pib_{int(ano)}_NFe.csv'
arquivoID = id[notas]

#Tamanho a ser lido em blocos (tentativa de otimização)
request_nota = service.files().get_media(fileId=arquivoID)
request_BEC = service.files().get_media(fileId='1O78mx-6wNbj7UU3TrKZbmzNOzq5ah76h')
tam = 100 * 1024 * 1024

#Criação da barra de progresso
var_atualizacao = st.empty()
progress_bar = var_atualizacao.progress(0)

#Download do arquivo BEC
with open('NCM_x_BEC.csv', 'wb') as file:
    downloader = MediaIoBaseDownload(file,request_BEC)
    done = False
    while not done:
        status,done = downloader.next_chunk()

#Download do arquivo e da tabela de Descrição
with open(f'pib_{ano}_NFe.csv', 'wb') as file:
    downloader = MediaIoBaseDownload(file,request_nota,chunksize=tam)
    done = False
    while not done:
        status,done = downloader.next_chunk()
        for i in range(100):
           progress_bar.progress(int(status.progress()*100))

#Lê o csv
notas= pd.read_csv(notas,delimiter=';',encoding='ISO-8859-1')
bec= pd.read_csv('NCM_x_BEC.csv',encoding='utf-8')

#Programação dos filtros dos códigos CNAE,NCM e UF  
if uf_d != '' and uf_e != '':
    filtro = notas.loc[(notas['CNAE_EMIT'].str.startswith(cnae)) & 
                   (notas['NCM'].astype(str).str.startswith(ncm)) & 
                   (notas['UF_DEST'] == uf_d) & (notas['UF_EMIT'] == uf_e)]
elif uf_d != '' and uf_e == '':
    filtro = notas.loc[(notas['CNAE_EMIT'].str.startswith(cnae)) & 
                   (notas['NCM'].astype(str).str.startswith(ncm)) & 
                   (notas['UF_DEST'] == uf_d)]
elif uf_d == '' and uf_e != '':
    filtro = notas.loc[(notas['CNAE_EMIT'].str.startswith(cnae)) & 
                   (notas['NCM'].astype(str).str.startswith(ncm)) & 
                   (notas['UF_EMIT'] == uf_e)]
else:
    filtro = notas.loc[(notas['CNAE_EMIT'].str.startswith(cnae)) & 
                   (notas['NCM'].astype(str).str.startswith(ncm))]

#Programação dos filtros dos municípios
if mun_d != '' and mun_e != '':
    filtro = notas.loc[(notas['XMUN_DEST'] == mun_d) & (notas['XMUN_EMIT'] == mun_e)]
elif mun_d != '' and mun_e == '':
    filtro = notas.loc[(notas['XMUN_DEST'] == mun_d)]
elif mun_d == '' and mun_e != '':
    filtro = notas.loc[(notas['XMUN_EMIT'] == mun_e)] 
    
#Une o filtro ao número BEC e descrições
filtro = pd.merge(filtro,bec,left_on='NCM',right_on='NCM',how='left')

#Filtro BEC
if cbec != '':
    filtro = filtro.loc[(filtro['BEC'] == cbec)]

#Se o dataframe for vazio
if  filtro.empty:
    st.write(f'Não há correspondentes para essa busca.')
else:
    
    st.write(f'Notas fiscais {ano}')
    st.dataframe(filtro.head(),use_container_width=True)

#Salva em arquivo Excel
def salvar(df):
    output = io.BytesIO()
    df.to_csv(output, index=False, sep=';')
    output.seek(0)
    return output

#Botão para baixar tabela
st.download_button(
    label='Baixar CSV',
    data=salvar(filtro),
    file_name=f'notas_fiscais_{ano}.csv',
    mime='text/csv'
)