"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """
    import glob
    import pandas as pd
    import os

    input_directory = 'files/input'
    files = glob.glob(f"{input_directory}/*")
    dataframes = [
        pd.read_csv(
            file,
            delimiter=",",
            index_col=0,
        )
        for file in files
    ]

    dataframe = pd.concat(dataframes, ignore_index=True)
    print(dataframe.head())
    print(dataframe.columns)

    os.makedirs('files/output', exist_ok = True)

    client_csv = dataframe[['client_id','age','job','marital','education','credit_default','mortgage']].copy()
    client_csv['job'] = client_csv['job'].str.replace(".", "", regex=False).str.replace("-", "_", regex=False)
    client_csv["education"] = client_csv["education"].str.replace(".", "_", regex=False).replace("unknown", pd.NA)
    client_csv["credit_default"] = client_csv["credit_default"].apply(lambda x: 1 if x == "yes" else 0)
    client_csv["mortgage"] = client_csv["mortgage"].apply(lambda x: 1 if x == "yes" else 0)

    campaign_csv = dataframe[['client_id','number_contacts','contact_duration','previous_campaign_contacts','previous_outcome','campaign_outcome']]
    campaign_csv['previous_outcome'] = campaign_csv['previous_outcome'].apply(lambda x: 1 if x == 'success' else 0)
    campaign_csv['campaign_outcome'] = campaign_csv['campaign_outcome'].apply(lambda x: 1 if x == 'yes' else 0)
    campaign_csv['last_contact_date'] = pd.to_datetime('2022-'  + dataframe['month'].astype(str) + '-' + dataframe['day'].astype(str) , format="%Y-%b-%d")
    
    economics_csv = dataframe[['client_id', 'cons_price_idx', 'euribor_three_months']].copy()

    client_csv.to_csv('files/output/client.csv', index=False)
    campaign_csv.to_csv('files/output/campaign.csv', index=False)
    economics_csv.to_csv('files/output/economics.csv', index=False)



if __name__ == "__main__":
    clean_campaign_data()
