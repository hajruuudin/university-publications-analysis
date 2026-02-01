import psycopg2
import os

# Your DB Connection Params
DB_PARAMS = {
    "dbname": "university_publications", 
    "user": "hajrudin.imamovic", 
    "password": "Lndrlh040344", 
    "host": "localhost"
}

# The target file path
OUTPUT_FILE = os.path.abspath("h3_trends_1990_2025.csv")

def export_pivoted_csv():
    # The SQL Pivot Query
    # This transforms the "long" database format into a "wide" CSV format
    query = """
    COPY (
        SELECT 
            publication_year,
            SUM(CASE WHEN segment_name = 'SE' THEN work_count ELSE 0 END) as SE,
            SUM(CASE WHEN segment_name = 'MLDM' THEN work_count ELSE 0 END) as MLDM,
            SUM(CASE WHEN segment_name = 'NLP' THEN work_count ELSE 0 END) as NLP,
            SUM(CASE WHEN segment_name = 'CN' THEN work_count ELSE 0 END) as CN,
            SUM(CASE WHEN segment_name = 'CC' THEN work_count ELSE 0 END) as CC,
            SUM(CASE WHEN segment_name = 'SEC' THEN work_count ELSE 0 END) as SEC
        FROM cs_thematic_trends
        WHERE publication_year BETWEEN 1990 AND 2025
        GROUP BY publication_year
        ORDER BY publication_year ASC
    ) TO STDOUT WITH CSV HEADER;
    """

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        
        with open(OUTPUT_FILE, 'w') as f:
            # copy_expert is the fastest way to pipe SQL results to a file
            cur.copy_expert(query, f)
            
        print(f"Success! Data exported to: {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"Export failed: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    export_pivoted_csv()