import streamlit as st
import pandas as pd
import requests


def fetch_pubmed_id(doi: str):
    """Return the PubMed ID for a DOI if it exists."""
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "pubmed", "term": f"{doi}[DOI]", "retmode": "json"}
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        ids = response.json().get("esearchresult", {}).get("idlist", [])
        return ids[0] if ids else None
    except Exception:
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
