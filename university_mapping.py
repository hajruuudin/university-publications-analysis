# =========== University Skimmer & Mapping File ===========
#
# This script skimms universities from OpenAlex API, combines the data with 
# university rankings from the Times Higer Education list (THE_2026_RANKING,xlsx)
# and inserts the following data for each university into the database:
# - ranking, university name, OpenAlexId and generates the ranking group
#
# Due to the nature of querying unversities (by name and not by ID), some universities
# may be mapped twice. This is avoided by using a dictionary that, by default, stores the first
# found university into the set. Naturally, this means some universities (primairly lower ranked ones)
# will get skipped. The end set based on this code consists of 822 mapped universities as of Feb 5th 2026
#
# =========== University Skimmer & Mapping File ===========

import pandas as pd
import requests
import psycopg2
from psycopg2.extras import execute_values
import time

DB_PARAMS = {
    "dbname": "DB_NAME", 
    "user": "USER", 
    "password": "PASSWORD", 
    "host": "HOST"}
MAILTO = "MAIL@SERVER.DOMAIN"
XLSX_FILE = "THE_2026_RANKINGS.xlsx"

def get_openalex_id(uni_name):
    """Search OpenAlex for the best matching education institution ID."""
    url = f"https://api.openalex.org/institutions?search={uni_name}&filter=type:education&mailto={MAILTO}"
    try:
        response = requests.get(url).json()
        if response.get('results'):
            return response['results'][0]['id']
    except Exception as e:
        print(f"Error searching {uni_name}: {e}")
    return None

def main():
    # Load only up to row 1003 (Rank 1000 + the 3 row offset. Look at the file structure to understand why this is it)
    df = pd.read_excel(XLSX_FILE, skiprows=3, header=None, usecols="A,D,E", nrows=1000)
    # Authors note: MIT for some reason kept getting skipped as the first university, so it was added mannualy to the set
    
    df.columns = [str(c).strip().lower() for c in df.columns]

    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()

    records_dict = {}

    for _, row in df.iterrows():
        rank = row.iloc[0] 
        name = row.iloc[1]
        
        if pd.isna(name): continue 
        
        oa_id = get_openalex_id(name)
        
        if oa_id:
            if oa_id not in records_dict:
                group = 'TOP100' if rank <= 100 else ('151TO500' if rank <= 500 else '500BELOW')
                records_dict[oa_id] = (rank, name, oa_id, group)
                print(f"Mapped (New): {name} -> {oa_id}")
            else:
                print(f"Skipping Duplicate ID: {oa_id} (Found again at {name})")
        
        time.sleep(0.05)

    final_records = list(records_dict.values())

    query = """
    INSERT INTO university_index (the_ranking, uni_name, open_alex_id, ranking_group)
    VALUES %s ON CONFLICT (open_alex_id) DO NOTHING;
    """
    
    if final_records:
        execute_values(cur, query, final_records)
        conn.commit()
        print(f"Finalized: {len(final_records)} unique universities inserted.")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()