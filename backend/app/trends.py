# trends.py
def detect_emerging_sectors(db):
    query = """
    SELECT raw_data->>'tags'
    FROM company_snapshots
    WHERE scraped_at > NOW() - INTERVAL '90 days'
    """

    # cluster embeddings
    # pass to LLM for explanation