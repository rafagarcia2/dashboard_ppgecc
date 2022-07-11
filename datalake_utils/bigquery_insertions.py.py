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


def create_table_schema_with_dataframe(dataframe: pd.DataFrame) -> list:
    """This function receives a dataframe object
    returning a schema to create a bigqueryTable object.

    Returns:
        list[bigquery.SchemaField]: lista de colunas para a criação do
        esquema da tabela
    """

    logger.info("starts array to stores the schema")
    schema = []
    logger.info("inserting dataframe columns to schema")
    for i in dataframe.columns:
        if dataframe[i].dtype == "float64":
            schema.append(bigquery.SchemaField(i, "FLOAT", mode="NULLABLE"))
        elif dataframe[i].dtype == "int64":
            schema.append(bigquery.SchemaField(i, "INTEGER", mode="NULLABLE"))
        else:
            schema.append(bigquery.SchemaField(i, "STRING", mode="NULLABLE"))

    return schema


def create_table_schema_with_csv(csv_path: str) -> list:
    """This function reads a csv file and returns a schema to
    create a bigquery table.

    Args:
        csv_path (str): path where is the csv file to insert data;

    Returns:
        list: list of bigQuery
    """ """ """
    logger.info("Reading the csv file to dataframe")
    df = pd.read_csv(csv_path)

    return create_table_schema_with_dataframe(df)


def create_empty_table_from_csv(
    csv_path: str, project_name: str, database_name: str, table_name: str
):
    """This function reads a csv file and creates a biquery
    empty table using.

    Args:
        csv_path (str): path where is the csv file to insert data
        project_name (str): project's where is the database and table
        database_name (str): database name on bigquery where is the table to insert;
        table_name (str): table name on bigquery where the data is inserted.
    """

    logger.info("create the bigquery client")
    client = bigquery.Client(project=project_name)

    logger.info("formatting the table_id in the bigquery format")
    table_id = project_name + "." + database_name + "." + table_name

    logger.info("creating the schema")
    schema = create_table_schema_with_csv(csv_path)

    logger.info("creating the bigquery table object")
    table = bigquery.Table(table_id, schema=schema)

    logger.info("creating the bigquery table")
    table = client.create_table(table)


def create_empty_table_from_dataframe(
    dataframe: pd.DataFrame, project_name: str, database_name: str, table_name: str
):
    """This function reads a pandas datafrane object and creates a biquery
    empty table using.

    Args:
        dataframe (pd.DataFrame): dataframe in order to create the table;
        project_name (str): project name where is the database and table
        to insert data;
        database_name (str): database name on bigquery where is the table to insert;
        table_name (str): table name on bigquery where the data is inserted.
    """

    logger.info("create the bigquery client")
    client = bigquery.Client(project=project_name)

    logger.info("let the table_id in the bigquery format")
    table_id = project_name + "." + database_name + "." + table_name

    logger.info("creating the schema")
    schema = create_table_schema_with_dataframe(dataframe)

    logger.info("creating the bigquery table object")
    table = bigquery.Table(table_id, schema=schema)

    logger.info("creating the bigquery table")
    table = client.create_table(table)


def insert_bigquery_from_csv(
    csv_path: str, project_name: str, database_name: str, table_name: str
):
    """This function insert data from a csv file
    into the bigqueryTable passed as argument.

    Args:
        csv_path (str): path where is the csv file to insert data;
        project_name (str): project name where is the database and table
        to insert data;
        database_name (str): database name on bigquery where is the table to insert;
        table_name (str): table name on bigquery where the data is inserted.
    """

    project_name = project_name

    logger.info("cretaing the bigquery client")
    client = bigquery.Client(project=project_name)

    logger.info("getting the database ref")
    dataset_ref = client.dataset(database_name)

    logger.info("getting the table ref")
    table_ref = dataset_ref.table(table_name)

    logger.info("define insertion options")
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.autodetect = True

    logger.info("opening the csv file and creting the insertion")
    with open(csv_path, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

    logger.info("insert the data")
    job.result()


def insert_bigquery_from_dataframe(
    dataframe: pd.DataFrame, project_name: str, database_name: str, table_name: str
):
    """This function insert data from a csv file
    into the bigqueryTable passed as argument.

    Args:
        dataframe (pd.DataFrame): pandas dataframe containing the data to insert;
        project_name (str): project on Google cloud platform where is the database and table
        to insert data;
        database_name (str): database name on bigquery;
        table_name (str): table name on bigquery.
    """

    logger.info("create the bigquery client")
    client = bigquery.Client(project=project_name)

    logger.info("formating the table id")
    table_id = project_name + "." + database_name + "." + table_name

    logger.info("create the table schema to job config")
    schema = create_table_schema_with_dataframe(dataframe)

    logger.info("defines the job_config")
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        # WRITE_TRUNCATE: overwritethe table if it already exists;
        # WRITE_APPEND: insert the data in the end of the table;
        # WRITE_EMPTY: doesn't insert the data if the table already have data.
        write_disposition="WRITE_APPEND",
    )

    job = client.load_table_from_dataframe(dataframe, table_id, job_config=job_config)

    logger.info("inserting the data")
    job.result()
    logger.info("insertion suceed")
