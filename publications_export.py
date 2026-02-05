# =========== Research Paper Skimmer  ===========
#
# This script retrieves the values of the volume of research papers published
# each year for each mapped university within the dataset for three categories:
# Medicine, Computer Science and Business
#
# For this script to work, university_mapping.py needs to have executed successfully with both 
# the exact same schema structure and results.
#
# This script inserts values for each uni and each number of records per years as specified (default
# here is 2006 to 2026). The end results as of Feb 5th 2026 is roughly 17000 rows.
#
# =========== Research Paper Skimmer ===========

import requests
import psycopg2
import time

FIELDS = {
    'medicine': '27',
    'computer_science': '17',
    'business': '14'
}

DB_PARAMS = {
    "dbname": "DB_NAME",
    "user": "USERNAME",
    "password": "PASS",
    "host": "HOST"}

def fetch_field_counts(oa_id, field_id):
    """Fetches annual publication counts for a specific field and uni."""
    url = f"https://api.openalex.org/works?filter=authorships.institutions.id:{oa_id},topics.field.id:{field_id},publication_year:2006-2026&group-by=publication_year"
    try:
        response = requests.get(url).json()
        return {int(item['key']): item['count'] for item in response.get('group_by', [])}
    except Exception as e:
        print(f"Error fetching {oa_id} for field {field_id}: {e}")
        return {}

def main():
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()

    cur.execute("SELECT open_alex_id, uni_name FROM university_index")
    unis = cur.fetchall()

    for oa_id, name in unis:
        print(f"Processing: {name}...")
        
        for field_name, field_id in FIELDS.items():
            counts = fetch_field_counts(oa_id, field_id)
            column = f"total_{field_name}_publications"
            
            for year, count in counts.items():
                query = f"""
                INSERT INTO university_annual_publications (open_alex_id, publication_year, {column})
                VALUES (%s, %s, %s)
                ON CONFLICT (open_alex_id, publication_year) 
                DO UPDATE SET {column} = EXCLUDED.{column};
                """
                cur.execute(query, (oa_id, year, count))
        
        conn.commit()
        time.sleep(0.1)

    cur.close()
    conn.close()
    print("Data collection complete!")

if __name__ == "__main__":
    main()