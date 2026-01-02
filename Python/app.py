import app_components as ui
import pandas as pd
import streamlit as st
import io
#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* SISTEMA USUÁRIO *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
if 'switch' not in st.session_state:
    st.session_state.switch = 1
#--------------------------------------------------- SITE E INÍCIO --------------------------------------------------
ui.titulo()
#HTML do footer da página
ui.footer()
#Containers
c1 = c2 = c3 = c4 = c5 = st.empty()
col1, col2, col3, col4 = st.columns(4)
#----------------------------------------------- LISTAS E DICIONARIOS -----------------------------------------------
#Anos
sb_ano = ui.list_ano()
#Estado
uf = ui.list_uf()
#Município
mun = ui.list_municipio()
#Códigos BEC
dic_bec = ui.dict_bec()
#Produtos SCN
scn = ui.list_produtos()
#Produtos SCN (EX Setores)
importantes = ui.list_naosetores()
#38 setores 
serv_cnae = ui.list_setores()
#Meses
mes = ui.dict_mes()
#---------------------------------------------- OPÇÃO NORMAL DE FILTRO ----------------------------------------------
#Opções de filtros normal
if st.session_state.switch == 1:
#Aplicado ao primeiro container:
    with c1.container():
        
        with col1:
            ano = st.selectbox('Ano',sb_ano)
        
            dicB = st.selectbox('BEC',options=list(dic_bec.keys()))
            #  Globaliza o valor de dicB
            ui.estado('dicB',dicB)
            periodo = st.multiselect('Periodo',options=list(mes.keys()))
        
        with col2:
            ncm = str(st.text_input('Código NCM'))
            ui.estado('ncm',ncm)

            cnae_e = str(st.text_input('CNAE de emissão'))
            ui.estado('cnae_e',cnae_e)

            cnae_d = str(st.text_input('CNAE de destino'))
            ui.estado('cnae_d',cnae_d)

            if  len(cnae_e) > 7 or len(cnae_d) > 7:
                st.write(f'Não há correspondentes para essa busca.')

        with col3:
            uf_d = st.selectbox('UF de destino',uf,key='uf_dest')
            uf_e = st.selectbox('UF de emissão',uf,key='uf_emit')

        with col4:
            mun_d = st.selectbox('Município de destino',mun,key='mun_dest')
            mun_e = st.selectbox('Município de emissão',mun,key='mun_emit')
        
        periodo = [mes[chave] for chave in periodo]
        ui.estado('periodo',periodo)

        meses_corrigidos = pd.Series(periodo).explode().dropna().unique()
        ui.estado('meses_corrigidos',meses_corrigidos)
        

#Aplicados ao segundo container:
        with c2.container():
        #Botão de Filtros Avançados
            with col4:
                ui.botao_padrao()
                if st.button('Filtros avançados'):
                    st.session_state.switch = 0
                    ui.texto_padrao('Clique uma segunda vez\npara atualizar a execução')
        #Botão de Buscar
            with col3:
                ui.botao_padrao()
                if st.button('Buscar') and ano != '':
                    print('Click')
                else:
                    st.stop()
else:
    c3.empty()
    c4.empty()
#--------------------------------------------- OPÇÃO AVANÇADA DE FILTRO ---------------------------------------------
#Opções de filtros avançados
if st.session_state.switch == 0:
#Aplicado ao terceiro container:
    with c3.container():
    #Opções de filtros
        with col1:
            ano = st.selectbox('Ano',sb_ano)
            produto = st.multiselect('Produto SCN - 75',scn)
            scnae = st.selectbox('Setor SCN - 38', ['','Destino','Emissão'])

        with col2:
            uf_d = st.selectbox('UF de destino',uf,key='dest')
            uf_e = st.selectbox('UF de emissão',uf,key='emit')
            if scnae == 'Emissão':
               scnae = st.multiselect('Setor Emissão',serv_cnae,key='sc_emit')
            elif scnae == 'Destino':
               tipo = 'DEST'
               scnae = st.multiselect('Setor Destino',serv_cnae,key='Sc_dest') 

        with col3:
            mun_d = st.selectbox('Município de destino',mun,key='mun_dest')
            mun_e = st.selectbox('Município de emissão',mun,key='mun_emit')

    with c4.container():        
        with col4:
            ui.imagem_cafe("https://i.imgur.com/uPQQOkQ.gif",'img/cafe_filtro.png')
            ui.botao_padrao()
            if st.button('Voltar'):
               st.session_state.switch = 1
               ui.texto_padrao('Clique uma segunda vez\npara atualizar a execução')

        with col3:
            ui.botao_padrao()
            if st.button('Buscar') and ano != '':
               print('Click')
            else:
               st.stop()
else:
    c3.empty()
    c4.empty()
#---------------------------------------------- BARRA DE CARREGAMENTO ----------------------------------------------
a, b = ui.barra_progresso()

#----------------------------------------------- DATAFRAME PANDAS --------------------------------------------------
#Constantes
# EMIT para Recursos, DEST para Usos
TIPO = 'EMIT'
NFE = f'./data/pib_{int(ano)}_NFe.csv'
NCM_MERGED = './data/NCM_MERGED_LEFT.csv'
CNAE_MERGED = f'./data/SCN_CNAE_{TIPO}.csv'
ENCODING = 'ISO-8859-1'

#Leitura dos csvs Pandas
notas = pd.read_csv(NFE,delimiter=';',encoding=ENCODING,dtype={'NCM':str})
ncm_merg = pd.read_csv(NCM_MERGED,dtype={'NCM':str})
scn_cnae = pd.read_csv(CNAE_MERGED, dtype={f'CNAE_{TIPO}':str})

#Inicializa filtro como cópia do csv notas
df = notas.copy()
ui.progresso(1,a,b)
#---------------------------------------------------- MERGES ------------------------------------------------------
#Padronização da coluna NCM
df['NCM'] = ui.normalizar_ncm(df['NCM'])
ncm_merg['NCM'] = ui.normalizar_ncm(ncm_merg['NCM'])
ncm_merg['NCM'] = ncm_merg['NCM'].str.strip()

#Padronização da coluna CNAE
df[f'CNAE_{TIPO}'] = ui.normalizar_cnae(df[f'CNAE_{TIPO}'])
scn_cnae[f'CNAE_{TIPO}'] = ui.normalizar_cnae(scn_cnae[f'CNAE_{TIPO}'])
scn_cnae['SETORES SCN'] = scn_cnae['SETORES SCN'].str.strip()
ui.progresso(2,a,b)

#Merges
df = pd.merge(df, ncm_merg, on='NCM', how='left')
df = pd.merge(df, scn_cnae, on=f'CNAE_{TIPO}', how='left')
ui.progresso(3,a,b)

#-------------------------------------------- PROGRAMAÇÃO DOS dfS --------------------------------------------
#Tratamento dos NCMS inferiores a 7 digitos
df.loc[df['NCM'].str.len() < 7, 'NCM'] = ('NA')
ui.progresso(4,a,b)

if st.session_state.switch == 0:
    #Filtragem dos produtos por SCN 
    if len(produto) > 0:
        df['PRODUTOS SCN'] = df['PRODUTOS SCN'].str.strip()
        df = df[df['PRODUTOS SCN'].isin(produto)]
    if len(scnae) > 0:
        df['SETORES SCN'] = df['SETORES SCN'].str.strip()
        df = df[df['SETORES SCN'].isin(scnae)]

ui.progresso(5,a,b)

#Opções de filtros globais
ncm = st.session_state.get('ncm')
cnae_d = st.session_state.get('cnae_d')
cnae_e = st.session_state.get('cnae_e')
periodo = st.session_state.get('periodo')
meses_corrigidos = st.session_state.get('meses_corrigidos')
dicB = st.session_state.get('dicB')

#Filtragem dos meses
if len(meses_corrigidos) > 0:
    condicao = " | ".join([f"MES_EMI == ' {mes},'" for mes in meses_corrigidos])
    df = df.query(condicao)

#Filtragem da CNAE
if cnae_e != '':
    df = df[df['CNAE_EMIT'].str.startswith(cnae_e)] 
if cnae_d != '':
    df = df[df['CNAE_DEST'].str.startswith(cnae_d)] 

#Filtragem da NCM
if ncm != '':
    df = df[df['NCM'].astype(str).str.startswith(ncm)]

#Filtragem da UF
if uf_e != '':
    df = df[df['UF_EMIT'] == uf_e]
if uf_d != '':
    df = df[df['UF_DEST'] == uf_d]

#Filtragem do Município
if mun_d != '':
    df = df[df['XMUN_DEST'] == mun_d]
if mun_e != '':
    df = df[df['XMUN_EMIT'] == mun_e]

#Filtragem BEC (NOVO)
if dicB:
    codigos_filtrar = dic_bec[dicB]
    df = df[df['BEC'].isin(codigos_filtrar)]

ui.progresso(6,a,b)

#Preenche os valores faltantes com a string 'NA'
df = df.fillna('NA')
ui.progresso(7,a,b)

#Se o dataframe for vazio
if  df.empty:
    st.write(f'Não há correspondentes para essa busca.')
else:
    st.write(f'Notas fiscais {ano}')
    st.dataframe(df.head(),use_container_width=True)

    with st.expander('Total VPROD'):

        ui.normalizar_vprod(df)
        total = df['VPROD'].sum()
        df['PRODUTOS SCN'] = df['PRODUTOS SCN'].fillna('').str.strip().str.upper()

        # Síntese do valor de cada produto
        st.write("Vprod Total:",total)
        for produto in scn:
            if produto in importantes:
                vprod = df.loc[df['PRODUTOS SCN'] == produto, 'VPROD'].sum(skipna=True)

                st.write(f"{produto}: {vprod}")


#---------------------------------------------- PROGRAMAÇÃO SALVAR -----------------------------------------------
#Salva em arquivo em csv
def salvar_csv(df):
    output = io.BytesIO()
    df.to_csv(output, index=False, sep=';')
    output.seek(0)
    return output

# Botão para baixar tabela em csv
st.download_button(
    label='Baixar CSV',
    data=salvar_csv(df),
    file_name=f'notas_fiscais_{ano}.csv',
    mime='text/csv'
)
ui.progresso(8,a,b)