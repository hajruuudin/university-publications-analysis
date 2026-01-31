import pandas as pd
import psycopg2

# Database connection parameters
DB_PARAMS = {"dbname": "university_publications", "user": "hajrudin.imamovic", "password": "Lndrlh040344", "host": "localhost"}

def export_h1_data():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        
        # SQL query to aggregate Top 100 publications by year
        query = """
        SELECT 
            p.publication_year,
            SUM(p.total_medicine_publications) AS medicine,
            SUM(p.total_computer_science_publications) AS computer_science,
            SUM(p.total_business_publications) AS business
        FROM university_annual_publications p
        JOIN university_index u ON p.open_alex_id = u.open_alex_id
        WHERE u.ranking_group = 'TOP100'
        AND p.publication_year < 2026
        GROUP BY p.publication_year
        ORDER BY p.publication_year ASC;
        """
        
        # Load into a DataFrame
        df = pd.read_sql(query, conn)
        
        # Export for MATLAB (Years as Rows, Categories as Columns)
        df.to_csv("h1_top_100_trends.csv", index=False)
        
        print("Success! 'h1_top_100_trends.csv' is ready for MATLAB.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()


def export_refined_3d_categories():
    conn = psycopg2.connect(**DB_PARAMS)
    query = """
    SELECT 
        u.the_ranking as rank,
        p.publication_year,
        p.total_medicine_publications as medicine,
        p.total_computer_science_publications as computer_science,
        p.total_business_publications as business
    FROM university_annual_publications p
    JOIN university_index u ON p.open_alex_id = u.open_alex_id
    WHERE u.the_ranking IN (1, 10, 25, 50, 75)
      AND p.publication_year < 2026
    ORDER BY u.the_ranking ASC, p.publication_year ASC;
    """
    df = pd.read_sql(query, conn)
    df.to_csv("bonus_3d_categories.csv", index=False)
    conn.close()

if __name__ == "__main__":
    export_h1_data()
    export_refined_3d_categories()