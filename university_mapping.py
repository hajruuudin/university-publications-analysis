import pandas as pd
import requests
import psycopg2
from psycopg2.extras import execute_values
import time

# Configuration
DB_PARAMS = {"dbname": "university_publications", "user": "hajrudin.imamovic", "password": "Lndrlh040344", "host": "localhost"}
MAILTO = "hajruuudin@gmail.com"
XLSX_FILE = "THE_2026_RANKINGS.xlsx"

def get_openalex_id(uni_name):
    """Search OpenAlex for the best matching education institution ID."""
    url = f"https://api.openalex.org/institutions?search={uni_name}&filter=type:education&mailto={MAILTO}"
    try:
        response = requests.get(url).json()
        if response.get('results'):
            # Return ONLY the ID string as requested
            return response['results'][0]['id']
    except Exception as e:
        print(f"Error searching {uni_name}: {e}")
    return None

def main():
    # Load only up to row 1003 (Rank 1000 + the 3 row offset)
    # nrows=1000 starting from header=3 gets you exactly to row 1003
    df = pd.read_excel(XLSX_FILE, skiprows=3, header=None, usecols="A,D,E", nrows=1000)
    
    # Clean headers to ensure string type
    df.columns = [str(c).strip().lower() for c in df.columns]

    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()

    records_dict = {} # Key: open_alex_id, Value: tuple of data

    for _, row in df.iterrows():
        rank = row.iloc[0] 
        name = row.iloc[1]
        
        if pd.isna(name): continue 
        
        oa_id = get_openalex_id(name)
        
        if oa_id:
            # CHECK: Only add if this ID hasn't been seen yet (First-Value rule)
            if oa_id not in records_dict:
                group = 'TOP100' if rank <= 100 else ('151TO500' if rank <= 500 else '500BELOW')
                records_dict[oa_id] = (rank, name, oa_id, group)
                print(f"Mapped (New): {name} -> {oa_id}")
            else:
                print(f"Skipping Duplicate ID: {oa_id} (Found again at {name})")
        
        # Polite delay to prevent 429 errors during the 1000-row loop
        time.sleep(0.05)

    final_records = list(records_dict.values())

    # Simplified Query: We remove the UPDATE part since you want to skip duplicates
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