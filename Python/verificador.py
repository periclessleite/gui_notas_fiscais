import pandas as pd
import app_components as ui

ANO = 2020
NFE = f'./data/pib_{int(ANO)}_NFe.csv'
NCM_MERGED = './data/NCM_MERGED_LEFT.csv'
TIPO = 'DEST'
CNAE_MERGED = f'./data/SCN_CNAE_{TIPO}.csv'
PRODUTO = "LARANJA"

df = pd.read_csv(NFE,delimiter=';',encoding='ISO-8859-1',dtype={'NCM':str})
ncm_merge = pd.read_csv(NCM_MERGED,dtype={'NCM':str})
cnae_merge = pd.read_csv(CNAE_MERGED, dtype={f'CNAE_{TIPO}':str})

df['NCM'] = ui.normalizar_ncm(df['NCM'])
# df[f'CNAE_{TIPO}'] = ui.normalizar_cnae(df[f'CNAE_{TIPO}'])
cnae_merge[f'CNAE_{TIPO}'] = ui.normalizar_cnae(cnae_merge[f'CNAE_{TIPO}'])
ncm_merge['NCM'] = ui.normalizar_ncm(ncm_merge['NCM'])
ncm_merge['NCM'] = ncm_merge['NCM'].str.strip()

df = pd.merge(df, ncm_merge, on='NCM', how='left')
df = pd.merge(df, cnae_merge, on=f'CNAE_{TIPO}', how='left')
df['PRODUTOS SCN'] = df['PRODUTOS SCN'].astype(str).str.strip().str.upper()
PRODUTO = PRODUTO.upper()

valores_unicos = df.loc[df['PRODUTOS SCN'] == PRODUTO, 'NCM'].unique()

valores_unicos = list(valores_unicos)
print(valores_unicos)