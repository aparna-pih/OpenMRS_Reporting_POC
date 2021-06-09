import sqlalchemy
import pandas as pd
from pandasql import sqldf
import pyarrow

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

#Configuration
from config import container_token, container_url, blob_token, blob_url
from config import location_ip_dict, schema, table_list
from config import dwh_user, password


def get_data():
    for location in location_ip_dict:
        print("Connecting to DB ", location)
        db_uri_loc = f"mysql+pymysql://{dwh_user}:{password}@{location_ip_dict[location]}/openmrs"
        engine = sqlalchemy.create_engine(db_uri_loc)  # ,echo=True)

        for table in table_list:
            result = engine.execute(
                #sqlalchemy.text("SELECT * FROM openmrs.location;")
                sqlalchemy.text(f"SELECT * FROM {schema}.{table};"))
                #test select into outfile in blob

            print(table, "", f"Rows: {result.rowcount}")
            rows = result.fetchall()
            df = pd.DataFrame(rows, columns=result.keys())
            print(df.shape)
            # print(df.head(2))
            save_table_data(location, table, df)

    return True


def save_table_data(location, table, df):
    file_path = "raw_data" + "/" + location + "_" + table
    csv_file = file_path + ".csv"
    pq_file = file_path + ".pq"
    df.to_csv(csv_file)
    df.to_parquet(pq_file)

    #Azure #Azure config file
    container_name = "cesdwstore"
    account_url = "https://pihstoragelake.blob.core.windows.net"

    blob_service_client = BlobServiceClient(account_url=account_url, credential=container_token)
    container_client = blob_service_client.get_container_client(container_name)
    blob_list = container_client.list_blobs()
    print("blob service", list(blob_list))

    local_file_name = location + "_" + table
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data)

    #Gcp

    return True


def generate_reports():

    df_location = pd.read_csv("data/Soledad/location.csv")

    # query config file {"report":"query"}
    query = "select distinct name from df_location"

    #df_report
    df_location_name = sqldf(query)
    print(df_location_name)

    # concatenate table from all locations + no. of columns #pyspark
    return True


if __name__ == '__main__':

    print("Data Back Up")

    # get_data()

    generate_reports()
