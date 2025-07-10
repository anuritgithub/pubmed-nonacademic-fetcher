from typing import List, Dict
from Bio import Entrez
import re
Entrez.email = "anamikasingh16052000@gmail.com"

def fetch_papers(query: str, debug: bool = False) -> List[Dict]:
    try:
        search_handle = Entrez.esearch(db="pubmed", term=query, retmax=20)
        search_results = Entrez.read(search_handle)
        ids = search_results.get("IdList", [])
    except Exception as e:
        print(f"[ERROR] Failed to search PubMed: {e}")
        return []

    if debug:
        print(f"[DEBUG] Found {len(ids)} papers")

    if not ids:
        return []

    try:
        fetch_handle = Entrez.efetch(
            db="pubmed", id=",".join(ids), rettype="medline", retmode="xml"
        )
        records = Entrez.read(fetch_handle)
    except Exception as e:
        print(f"[ERROR] Failed to fetch details: {e}")
        return []

    papers = []

    for article in records.get("PubmedArticle", []):
        try:
            citation = article.get("MedlineCitation", {})
            article_info = citation.get("Article", {})

            pubmed_id = citation.get("PMID", "")
            title = article_info.get("ArticleTitle", "")
            pub_date = article_info.get("Journal", {}).get("JournalIssue", {}).get("PubDate", {})
            year = pub_date.get("Year", "")
            month = pub_date.get("Month", "")
            day = pub_date.get("Day", "")
            date = f"{year}-{month}-{day}".strip("-")

            author_list = article_info.get("AuthorList", [])
            authors: List[str] = []
            affiliations: List[str] = []
            emails: List[str] = []

            for author in author_list:
                if "ForeName" in author and "LastName" in author:
                    full_name = f"{author['ForeName']} {author['LastName']}"
                    authors.append(full_name)
                for aff in author.get("AffiliationInfo", []):
                    aff_text = aff.get("Affiliation", "")
                    if aff_text:
                        affiliations.append(aff_text)
                        matches = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", aff_text)
                        emails.extend(matches)

            papers.append({
                "PubmedID": pubmed_id,
                "Title": title,
                "Date": date,
                "Authors": authors,
                "Affiliations": affiliations,
                "Email": list(set(emails)),
            })

        except Exception as e:
            if debug:
                print(f"[DEBUG] Skipped paper due to error: {e}")

    return papers
