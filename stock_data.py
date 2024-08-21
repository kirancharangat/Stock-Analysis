import requests
import csv
import time
from datetime import datetime
import os

def fetch_stock_data(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching data: {str(e)}")
        return None

def append_csv(file_path, new_data):
    new_rows = list(csv.reader(new_data.decode('utf-8').splitlines()))
    header = new_rows[0]
    header.insert(0, "Timestamp")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows_to_append = []
    for row in new_rows[1:]:
        row.insert(0, current_time)
        rows_to_append.append(row)

    file_exists = os.path.isfile(file_path)

    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(header)
        writer.writerows(rows_to_append)

def main():
    api_url = "https://elite.finviz.com/export.ashx?v=151&p=i1&f=cap_0.01to,geo_usa|china|france|europe|australia|belgium|canada|chinahongkong|germany|hongkong|iceland|japan|newzealand|ireland|netherlands|norway|singapore|southkorea|sweden|taiwan|unitedarabemirates|unitedkingdom|switzerland|spain,sh_curvol_o100,sh_relvol_o2,ta_change_u&ft=4&o=sharesfloat&ar=10&c=0,1,2,5,6,7,25,26,27,28,29,30,84,90,91,92,93,95,96,97,98,99,42,43,44,45,46,47,49,50,51,52,53,54,68,60,61,63,64,67,81,87,88,65,66,71,72-5c21-4aba-8ba7-ed5a&auth=d5fb4592-b104-4c42-a68b-50faab3b002d"
    file_path = "test.csv" 

    while True:
        print(f"Fetching data at {datetime.now()}")
        data = fetch_stock_data(api_url)
        if data:
            append_csv(file_path, data)
            print("Data appended to CSV file successfully.")
        else:
            print("Failed to fetch data. Skipping this update.")

        # Wait for 15 minutes
        time.sleep(900)

if __name__ == "__main__":
    main()