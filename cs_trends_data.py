# =========== Computer Science Research Topics Skimmer  ===========
#
# This script retrieves the number of research papers regarding each specified
# computer science related topic within the the frame of 1990 to 2025. The 
# topics specified below are multi-worded and compund to the total number of volume.
#
# For example: Software engieering is anything which has the keyword of
# "Software Engineering" or "Software". The same idea is done with the other topics.
# The topic keywords can be changed at will but these were used for the first edition of the paper.
#
# Important note: It is possible to have overlap within topics as a paper can be multiple topics
# at the same time. Its important to take this into account and not use keywords that are vague and cover
# multilpe things. An example would be using the keyword "Artificial Intelligenge" isntead of "NLP" as
# that can conver any possible segment of research not only in CS but also in other fields.
#
# =========== Computer Science Research Topics Skimmer  ===========

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
    "dbname": "DB_NAME", 
    "user": "USERNAME", 
    "password": "PASS", 
    "host": "HOST"
}

def fetch_thematic_counts(keywords):
    """Fetches global annual counts for a cluster of keywords from OpenAlex."""
    url = (
        f"https://api.openalex.org/works?"
        f"filter=title_and_abstract.search:{keywords},publication_year:1990-2025"
        f"&group-by=publication_year"
    )
    try:
        response = requests.get(url).json()
        if 'group_by' in response:
            return {int(item['key']): item['count'] for item in response.get('group_by', [])}
        return {}
    except Exception as e:
        print(f"Error fetching keywords {keywords}: {e}")
        return {}

def main():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

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