import pandas as pd

def limpar_dados_aids(caminho_do_arquivo):
    try:
        df = pd.read_csv(caminho_do_arquivo, delimiter=';', encoding='latin-1')
        print(f"Arquivo '{caminho_do_arquivo}' carregado com sucesso.")
        print(f"O conjunto de dados original possui {df.shape[0]} linhas e {df.shape[1]} colunas.")
        print("-" * 50)

    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_do_arquivo}' não foi encontrado.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao ler o arquivo: {e}")
        return None

    colunas_data = ['dt_notific', 'dt_diag', 'dt_nasc', 'dt_obito']
    print("Convertendo colunas de data para o formato datetime...")
    for col in colunas_data:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    colunas_numericas = ['nu_idade_n', 'criterio']
    print("Convertendo colunas numéricas (com vírgula decimal)...")
    for col in colunas_numericas:
        if df[col].dtype == 'object':
            df[col] = df[col].str.replace(',', '.', regex=False).astype(float)
    
    df.rename(columns={'nu_idade_n': 'idade'}, inplace=True)
    print("Coluna 'nu_idade_n' renomeada para 'idade'.")
    print("-" * 50)
    
    colunas_para_preencher = ['cs_raca', 'cs_escol_n', 'ant_rel_ca']
    print("Tratando valores ausentes em colunas categóricas...")
    for col in colunas_para_preencher:
        df[col].fillna('Não Informado', inplace=True)
        
    mediana_idade = df['idade'].median()
    df['idade'].fillna(mediana_idade, inplace=True)
    print(f"Valores ausentes na coluna 'idade' preenchidos com a mediana ({mediana_idade:.1f}).")
    print("-" * 50)

    print("Padronizando valores em colunas de texto (ex: 'cs_sexo')...")
    if 'cs_sexo' in df.columns:
        df['cs_sexo'] = df['cs_sexo'].str.lower().str.strip()

    if 'dt_diag' in df.columns and 'dt_nasc' in df.columns:
        print("Criando nova coluna 'idade_no_diagnostico'...")
        df['idade_no_diagnostico'] = (df['dt_diag'] - df['dt_nasc']).dt.days / 365.25

    print("-" * 50)
    print("Limpeza e pré-processamento concluídos!")
    
    return df

caminho_arquivo = 'dados_aids_hiv.csv' 
df_limpo = limpar_dados_aids(caminho_arquivo)


if df_limpo is not None:
    
    nome_arquivo_saida_csv = 'dados_aids_limpos.csv'
    
    print(f"\nSalvando os dados limpos no arquivo: '{nome_arquivo_saida_csv}'...")
    
df_limpo.to_csv(nome_arquivo_saida_csv, index=False, sep=';', encoding='utf-8')    

print("Arquivo salvo com sucesso!")