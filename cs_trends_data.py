import requests
import psycopg2
import time

# Keywords for each of your 6 segments
SEGMENTS = {
    'SE': 'software+engineering|software',
    'MLDM': 'machine+learning|discrete+mathematics',
    'NLP': 'neural+networks|natural+language+processing',
    'CN': 'computer+networks|computer+networking|wireless|ip',
    'CC' : 'cloud+computing|edge+computing|parallel+computing|internet+of+things|iot|virtualization',
    'SEC': 'cryptography|network+security|malware|intrusion+detection'
}

DB_PARAMS = {
    "dbname": "university_publications", 
    "user": "hajrudin.imamovic", 
    "password": "Lndrlh040344", 
    "host": "localhost"
}

def fetch_thematic_counts(keywords):
    """Fetches global annual counts for a cluster of keywords from OpenAlex."""
    # We filter by concepts.display_name and group by year
    url = (
        f"https://api.openalex.org/works?"
        f"filter=title_and_abstract.search:{keywords},publication_year:1990-2025"
        f"&group-by=publication_year"
        f"&mailto=your_email@example.com"
    )
    try:
        response = requests.get(url).json()
        if 'group_by' in response:
            # key = year, count = total works
            return {int(item['key']): item['count'] for item in response.get('group_by', [])}
        return {}
    except Exception as e:
        print(f"Error fetching keywords {keywords}: {e}")
        return {}

def main():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        # Step 1: Create the table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS cs_thematic_trends (
                id SERIAL PRIMARY KEY,
                publication_year INT NOT NULL,
                segment_name VARCHAR(100) NOT NULL,
                work_count INT DEFAULT 0,
                CONSTRAINT uq_year_segment UNIQUE (publication_year, segment_name)
            );
        """)

        # Step 2: Fetch and Insert Data
        for name, keywords in SEGMENTS.items():
            print(f"Syncing Segment: {name}...")
            counts = fetch_thematic_counts(keywords)
            
            for year, count in counts.items():
                cur.execute("""
                    INSERT INTO cs_thematic_trends (publication_year, segment_name, work_count)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (publication_year, segment_name) 
                    DO UPDATE SET work_count = EXCLUDED.work_count;
                """, (year, name, count))
            
            conn.commit()
            time.sleep(1)

        print("\nTable 'cs_thematic_trends' is now fully populated.")
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Script Error: {e}")

if __name__ == "__main__":
    main()