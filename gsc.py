from __future__ import print_function
import os
import argparse
import sys
import pandas as pd
from datetime import datetime, timedelta
from googleapiclient import sample_tools

property_uri = 'https://www.evemilano.com/'
start_date = '2025-01-01'
end_date = '2025-01-15'

def main(argv):
    service, flags = sample_tools.init(
        argv,
        "searchconsole",
        "v1",
        __doc__,
        __file__,
        scope="https://www.googleapis.com/auth/webmasters.readonly",
    )

    # Convert start_date and end_date to datetime objects
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    # Initialize a list to store all query data
    all_data = []

    # Loop through each day in the date range
    for single_date in (start + timedelta(n) for n in range((end - start).days + 1)):
        single_day = single_date.strftime("%Y-%m-%d")

        # Query for the specific day
        request = {
            "startDate": single_day,
            "endDate": single_day,
            #"dimensions": ["query", "page", "device", "country"],
            "dimensions": ["query"],
            #"dimensionFilterGroups": [{"filters": [{"dimension": "query", "expression": "trovare indirizzo ip da link"}]}],,
            "rowLimit": 25000  # Richiedi fino a 25.000 righe, valore massimo
        }
        response = execute_request(service, property_uri, request)
        print(f"Processing data for {single_day}")
    
        row_count = 0  # Counter for the number of rows added
        if "rows" in response:
            for row in response["rows"]:
                keys = row.get("keys", ["Unknown", "Unknown", "Unknown", "Unknown"])
                query = keys[0]  # First key is the query
                page = keys[1] if len(keys) > 1 else "Unknown"  # Second key is the page
                #device = keys[2] if len(keys) > 2 else "Unknown"  # Third key is the device
                #country = keys[3] if len(keys) > 3 else "Unknown"  # Fourth key is the country
                all_data.append({
                    #"Date": single_day,  # Include date in the data
                    "Query": query,
                    #"Page": page,
                    #"Device": device,
                    #"Country": country,
                    "Click": row["clicks"],
                    "Impression": row["impressions"],
                    "CTR": row["ctr"],
                    "Position": row["position"]
                })
                row_count += 1  # Increment the row counter

        print(f"{row_count} rows received and added for {single_day}")

    # Create a DataFrame from the collected data
    df = pd.DataFrame(all_data, columns=["Date", "Query", "Page", "Device", "Country", "Click", "Impression", "CTR", "Position"])
    df = df.sort_values(by="Impression", ascending=False)

    # Creazione della tabella pivot
    # Somma di click e impression
    # CTR come percentuale basata su somme di click e impression
    # Posizione calcolata come media ponderata sulle impressioni
    df_pvt = df.groupby('Query').agg(
        Click=('Click', 'sum'),
        Impression=('Impression', 'sum'),
        CTR=('Click', lambda x: (x.sum() / df.loc[x.index, 'Impression'].sum()) * 100),
        Position=('Position', lambda x: (x * df.loc[x.index, 'Impression']).sum() / df.loc[x.index, 'Impression'].sum())
    ).reset_index()

    # Arrotondiamo la posizione a un intero come richiesto
    df_pvt['Position'] = df_pvt['Position'].round(0).astype(int)
    # Formattazione del CTR come percentuale
    df_pvt['CTR'] = df_pvt['CTR'].apply(lambda x: f"{x:.2f}%")
    # Ordinamento per Impression in ordine decrescente
    df_pvt = df_pvt.sort_values(by='Impression', ascending=False)
    # Visualizzazione del DataFrame risultante
    print(df_pvt)



    # Save the DataFrame to an Excel file in the same folder as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "search_analytics_data.xlsx")
    df_pvt.to_excel(output_path, index=False, engine="openpyxl")
    print(f"Data saved to {output_path}")

    # Print or save the DataFrame as needed
    print(df)
    df.to_csv("search_analytics_data.csv", index=False)

def execute_request(service, property_uri, request):
    """Executes a searchAnalytics.query request.

    Args:
      service: The searchconsole service to use when executing the query.
      property_uri: The site or app URI to request data for.
      request: The request to be executed.

    Returns:
      An array of response rows.
    """
    return service.searchanalytics().query(siteUrl=property_uri, body=request).execute()

if __name__ == "__main__":
    main(sys.argv)
