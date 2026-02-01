import pandas as pd
import psycopg2

# Database connection parameters
DB_PARAMS = {"dbname": "university_publications", "user": "hajrudin.imamovic", "password": "Lndrlh040344", "host": "localhost"}

def export_h2_data():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        
        # Query: Get the total amount of publications per category for each university range.
        # The number of unis should be in the ranges: 1 to 150, 151 to 300 and 300 to 450.
        # This gives equal ranges in order to avoid bias towards larger uni groups.
        query = """
        SELECT 
            p.publication_year,
            CASE 
                WHEN i.the_ranking <= 150 THEN 'Tier 1: 1-150'
                WHEN i.the_ranking > 150 AND i.the_ranking <= 300 THEN 'Tier 2: 151-300'
                WHEN i.the_ranking > 300 AND i.the_ranking <= 450 THEN 'Tier 3: 301-450'
            END AS uni_range,
            SUM(p.total_computer_science_publications) as total_cs,
            SUM(p.total_medicine_publications) as total_med,
            SUM(p.total_business_publications) as total_bus
        FROM university_annual_publications p
        JOIN university_index i ON p.open_alex_id = i.open_alex_id
        WHERE i.the_ranking <= 450
        GROUP BY p.publication_year, uni_range
        ORDER BY p.publication_year, uni_range;
        """
        
        df = pd.read_sql(query, conn)
        
        df.to_csv("h2_uni_range_trends.csv", index=False)
        
        print("Success! 'h2_uni_range_trends.csv' is ready for MATLAB.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()


def export_h2_heatmap_data():
    try:
        conn = psycopg2.connect(**DB_PARAMS)

        # Query: Get data for heatmap visualization. This includes getting 50 universities from each group, skipping every
        # 2 universities to get a spread out sample (with exception of the first group since we look at the top 50). Then, we
        # get their publication counts per year for all three categories combined. 
        query = """
        SELECT 
            floor((i.the_ranking - 1) / 50) * 50 + 1 || '-' || floor((i.the_ranking - 1) / 50) * 50 + 50 AS rank_bin,
            p.publication_year,
            SUM(p.total_medicine_publications + p.total_computer_science_publications + p.total_business_publications) as total_pubs
        FROM university_annual_publications p
        JOIN university_index i ON p.open_alex_id = i.open_alex_id
        WHERE i.the_ranking <= 450 
        AND p.publication_year < 2026
        GROUP BY rank_bin, p.publication_year
        ORDER BY MIN(i.the_ranking), p.publication_year;
        """

        # Load into a DataFrame
        df = pd.read_sql(query, conn)
        
        # Export for MATLAB (Years as Rows, Categories as Columns)
        df.to_csv("h2_heatmap_data.csv", index=False)
        
        print("Success! 'h2_heatmap_data.csv' is ready for MATLAB.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    export_h2_data()
    export_h2_heatmap_data()