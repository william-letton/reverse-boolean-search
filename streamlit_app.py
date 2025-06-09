import streamlit as st
import pandas as pd
import requests

import time
import logging


CONTACT_EMAIL = "william.letton@crystallise.com"
USER_AGENT = "reverse-boolean-search/1.0"
PMC_ID_CONVERTER_URL = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/"
DELAY_BETWEEN_CALLS = 3
MAX_RETRIES = 3

session = requests.Session()
session.headers.update({"User-Agent": USER_AGENT})



def fetch_pubmed_id(doi: str):
    """Return the PubMed ID for a DOI if it exists."""

    params = {
        "ids": doi,
        "format": "json",
        "tool": "reverse_boolean_search",
        "email": CONTACT_EMAIL,
    }
    for attempt in range(MAX_RETRIES):
        try:
            response = session.get(PMC_ID_CONVERTER_URL, params=params, timeout=10)
            if response.status_code in (429, 503):
                time.sleep(DELAY_BETWEEN_CALLS)
                continue
            response.raise_for_status()
            records = response.json().get("records", [])
            if records and "pmid" in records[0]:
                return records[0]["pmid"]
            return None
        except Exception:
            logging.exception("PubMed lookup failed")
            if attempt == MAX_RETRIES - 1:
                return None
        time.sleep(DELAY_BETWEEN_CALLS)
    return None


st.title("🎈 A Will App")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

# File uploader for a single table CSV
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV into a DataFrame
    try:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df, use_container_width=True, height=400)

        if st.button("Check records in PubMed"):
            if "DOI" not in df.columns:
                st.error("The uploaded file must contain a 'DOI' column.")
            else:
                result_df = df.copy()
                in_pubmed = []
                pmids = []
                for doi in result_df["DOI"].fillna(""):
                    pmid = fetch_pubmed_id(doi) if doi else None
                    in_pubmed.append(pmid is not None)
                    pmids.append(pmid)
                result_df["in_pubmed"] = in_pubmed
                result_df["PMID"] = pmids
                st.dataframe(result_df, use_container_width=True, height=400)
    except Exception as e:
        st.error(f"Failed to read CSV: {e}")
