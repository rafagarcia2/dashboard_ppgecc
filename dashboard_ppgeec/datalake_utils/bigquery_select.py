import pandas as pd
import os
import logging
from google.cloud import bigquery


# configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%d-%m-%Y %H:%M:%S"
)

# reference for a logging obj
logger = logging.getLogger()


def select_table_from_bigquery(
    project_name: str, database_name: str, table_name: str
) -> pd.DataFrame:
    """Select the table's data and return it as a pandas
    dataframe.
    Args:
        project_name (str): project name where is the database and table
        to insert data;
        database_name (str): database name on bigquery where is the target table;
        table_name (str): table name on bigquery where the data is inserted.

    Returns:
        pd.DataFrame: DataFrame resulted from the select query
    """

    logger.info("create the bigquery client")
    client = bigquery.Client(project=project_name)

    logger.info("formatting table id")
    table_id = f"{project_name}.{database_name}.{table_name}"

    logger.info("format the query string")
    sql = f"""SELECT * FROM `{table_id}`"""

    logger.info("creating the dataframe")
    df = client.query(sql).to_dataframe()

    return df


def select_features_to_dataframe(
    project_name: str, database_name: str, table_name: str, columns_list: list
) -> pd.DataFrame:
    """this functions makes a select of a list of columns of the target table
    and returns it as a pandas dataframe.

    Args:
        project_name (str): project name where is the database and table
        to insert data;
        database_name (str): database name on bigquery where is the target table;
        table_name (str): table name on bigquery where the data is inserted;
        columns_list (list): features to build the select query.

    Returns:
        pd.DataFrame: Pandas DataFrame resulted from select query filtering table
        fields
    """

    logger.info("formating the columns list as a string")
    colunas = columns_list[0]
    for i in columns_list[1:]:
        colunas = colunas + "," + i

    logger.info("creating the bigquery client")
    client = bigquery.Client(project=project_name)

    logger.info("formating the table id")
    table_id = f"{project_name}.{database_name}.{table_name}"

    logger.info("formating the query string")
    sql = f"""SELECT {colunas} FROM `{table_id}`"""

    logger.info("creting the dataframe from select query")
    df = client.query(sql).to_dataframe()

    return df
