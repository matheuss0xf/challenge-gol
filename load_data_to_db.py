import logging
import uuid
from io import StringIO
import pandas as pd
import requests
from app.database.connection import DBConnectionHandler
from app.models.flight import FlightModel

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def clean_and_process_data(df):
    """Limpa e processa o DataFrame conforme os requisitos."""
    df = df.query("EMPRESA_SIGLA == 'GLO' & GRUPO_DE_VOO == 'REGULAR' & NATUREZA == 'DOMÉSTICA'")

    if df.empty:
        logging.warning('Nenhum dado correspondente encontrado após o filtro.')
        return None

    df['MERCADO'] = df.apply(
        lambda row: ''.join(sorted([row['AEROPORTO_DE_ORIGEM_SIGLA'], row['AEROPORTO_DE_DESTINO_SIGLA']])), axis=1
    )

    df.rename(columns={'ANO': 'ano', 'MES': 'mes', 'MERCADO': 'mercado', 'RPK': 'rpk'}, inplace=True)

    df = df.dropna(subset=['rpk'])

    return df


def load_data_to_db(csv_url):
    """Carrega dados de um arquivo CSV de uma URL para o banco de dados."""

    try:
        with DBConnectionHandler() as db:
            if db.session.query(FlightModel).count() > 0:
                logging.info('Banco de dados já populado. Pulando a carga de dados.')
                return

        logging.info(f'Baixando arquivo CSV de: {csv_url}')
        response = requests.get(csv_url)

        if response.status_code != 200:
            logging.error(f'Erro ao baixar o arquivo CSV. Status Code: {response.status_code}')
            return


        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data, sep=';', skiprows=1, low_memory=False)

        df = clean_and_process_data(df)
        if df is None:
            return

        flights_data = df[['ano', 'mes', 'mercado', 'rpk']].to_dict(orient='records')

        logging.info(f'{len(flights_data)} registros preparados para inserção.')

        with DBConnectionHandler() as db:
            try:
                flights = [FlightModel(id=uuid.uuid4().hex, **data) for data in flights_data]
                db.session.bulk_save_objects(flights)
                db.session.commit()
                logging.info(f'{len(flights)} registros inseridos com sucesso.')
            except Exception as e:
                db.session.rollback()
                logging.error(f'Erro ao inserir dados no banco: {e}')

    except requests.exceptions.RequestException as e:
        logging.error(f'Erro ao fazer o download do arquivo CSV: {e}')
    except pd.errors.EmptyDataError:
        logging.error('O arquivo CSV está vazio ou mal formatado.')
    except Exception as e:
        logging.error(f'Erro inesperado: {e}')


csv_url = "https://sistemas.anac.gov.br/dadosabertos/Voos%20e%20opera%C3%A7%C3%B5es%20a%C3%A9reas/Dados%20Estat%C3%ADsticos%20do%20Transporte%20A%C3%A9reo/Dados_Estatisticos.csv"

load_data_to_db(csv_url)
