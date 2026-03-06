import urllib.parse
from sqlalchemy import create_engine, text, inspect 
import io
import zipfile
import requests
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# --- 1. CONFIGURAÇÕES DO BANCO ---
USUARIO = 'postgres'
SENHA = 'post123'  # Sua senha atual
HOST = 'localhost'
PORTA = '5432'
BANCO = 'dw_consorcio_bcb'

conn_string = f'postgresql://{USUARIO}:{SENHA}@{HOST}:{PORTA}/{BANCO}'
engine = create_engine(conn_string)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/115.0.0.0"}

# --- 2. FUNÇÃO DE EXTRAÇÃO E LIMPEZA ---
def processar_e_salvar(conteudo_zip, data_base):
    with zipfile.ZipFile(io.BytesIO(conteudo_zip)) as z:
        for nome_arq in z.namelist():
            # Apenas arquivos CSV
            if not nome_arq.endswith('.csv'):
                continue

            # Whitelisting
            tabela = None
            if 'Segmentos_Consolidados' in nome_arq:
                tabela = 'segmentos_consolidados'
            elif 'Bens_Imoveis_Grupos' in nome_arq:
                tabela = 'imoveis_grupos'
            elif 'Bens_Moveis_Grupos' in nome_arq:
                tabela = 'moveis_grupos'
            elif 'UF' in nome_arq and 'Significado' not in nome_arq:
                tabela = 'dados_uf'

            if tabela:
                with z.open(nome_arq) as f:
                    df = pd.read_csv(f, sep=';', encoding='latin-1', low_memory=False)
                    
                    # Padroniza as colunas
                    df.columns = df.columns.str.replace(r'[\s#]', '_', regex=True).str.lower()
                    df['data_base_consorcio'] = data_base
                    
                    # Idempotência
                    inspetor = inspect(engine)
                    if inspetor.has_table(tabela, schema='raw'):
                        with engine.connect() as conn:
                            conn.execute(text(f"DELETE FROM raw.{tabela} WHERE data_base_consorcio = '{data_base}'"))
                            conn.commit()
                    
                    # Salva no banco
                    df.to_sql(tabela, engine, schema='raw', if_exists='append', index=False)
                    print(f"   [OK] {nome_arq} -> raw.{tabela}")

# --- 3. MOTOR DE ATUALIZAÇÃO HISTÓRICA ---
def executar_pipeline_consorcio():
    data_alvo = datetime.now()
    arquivos_atualizados = 0
    limite_meses = 72 # Histórico de 6 anos
    
    # Sessão inteligente para contornar quedas do BCB
    session = requests.Session()
    retry = Retry(total=5, backoff_factor=1, status_forcelist=[ 500, 502, 503, 504 ])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    session.headers.update(headers)
    
    print(f"--- Buscando a última atualização disponível e processando {limite_meses} meses ---")

    while arquivos_atualizados < limite_meses:
        db_format = data_alvo.strftime('%Y%m')
        url_principal = f"https://www.bcb.gov.br/Fis/Consorcios/Port/BD/{db_format}Consorcios.zip"
        url_uf = f"https://www.bcb.gov.br/Fis/Consorcios/Port/BD/{db_format}Consorcios_UF.zip"

        try:
            res_principal = session.get(url_principal, timeout=30)
            
            if res_principal.status_code == 200 and res_principal.content.startswith(b'PK'):
                print(f"\n[{arquivos_atualizados + 1}/{limite_meses}] Processando data-base: {db_format}")
                processar_e_salvar(res_principal.content, db_format)
                
                time.sleep(1) # Pausa amigável
                
                res_uf = session.get(url_uf, timeout=30)
                if res_uf.status_code == 200 and res_uf.content.startswith(b'PK'):
                    processar_e_salvar(res_uf.content, db_format)
                    
                arquivos_atualizados += 1
                
            else:
                if arquivos_atualizados == 0:
                    print(f" -> Mês {db_format} ainda não publicado pelo BCB. Buscando mês anterior...")
                else:
                    print(f" [!] Aviso: Arquivo consolidado de {db_format} não encontrado no histórico.")

            data_alvo -= relativedelta(months=1)
            time.sleep(2) # Pausa amigável entre meses
            
        except requests.exceptions.RequestException as e:
            # AGORA SIM: Captura apenas erros reais de conexão/internet
            print(f"\n [!] O servidor do BCB derrubou a conexão. Erro: {e}")
            print(" -> Pausando por 10 segundos para o servidor respirar antes de tentar novamente...")
            time.sleep(10)

    print("\n--- Atualização Histórica concluída com sucesso! ---")

if __name__ == "__main__":
    executar_pipeline_consorcio()