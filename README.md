# Analysis of Research Publication Volume in Top-Ranked Universities (2000–2020)

This repository contains code supporting a research paper that investigates trends in research publication output among top-ranked universities over the past two decades. The analysis focuses on three research domains: Medicine, Computer Science, and Business (with a particular emphasis on Computer Science in the third hypothesis).

The code is modular and reusable, allowing users to load data into a local database for further analysis. **Note:** Update the database connection credentials as needed.

## Data Sources

- **OpenAlex API**  
    Free, publicly available database of millions of research papers from higher education institutions worldwide.

- **Times Higher Education**  
    Excel export of the 2026 global university rankings, used to segment universities by rank.

## Tools & Requirements

- **PostgreSQL**  
    Stores and queries the formatted data locally.

- **MATLAB**  
    Generates data visualizations for the research paper.

- **Python**  
    Transforms data and dynamically exports/imports CSV files.

## Hypotheses

- **H0A:** There is no significant difference in the volume of research publications among Medicine, Computer Science, and Business & Economy within the top 100 universities (2026 ranking).
- **H0B:** Universities with higher Times Higher Education rankings publish more research in these fields compared to lower-ranked universities.
- **H0C:** The rise of AI and LLMs has increased research output in Machine Learning & Neural Networks compared to established Computer Science topics (e.g., Software Engineering, Computer Networks, Cloud Computing).

## References

- [OpenAlex API Documentation](https://docs.openalex.org/how-to-use-the-api/api-overview)
- [Times Higher Education Rankings](https://www.timeshighereducation.com/world-university-rankings)
