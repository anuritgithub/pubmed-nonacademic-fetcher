from typing import List, Dict

def is_non_academic(affiliation: str) -> bool:
    academic_keywords = ["university", "college", "institute", "school", "department", "faculty"]
    return not any(word in affiliation.lower() for word in academic_keywords)

def filter_non_academic(papers: List[Dict]) -> List[Dict]:
    filtered = []

    for paper in papers:
        affiliations = paper.get("Affiliations", [])
        emails = paper.get("Email", [])
        authors = paper.get("Authors", [])
        non_acad_affils = [aff for aff in affiliations if is_non_academic(aff)]

        if non_acad_affils:
            filtered.append({
                "PubmedID": paper.get("PubmedID"),
                "Title": paper.get("Title"),
                "Date": paper.get("Date"),
                "Non-academic Authors": ", ".join(authors),
                "Company Affiliations": "; ".join(non_acad_affils),
                "Email": ", ".join(emails),
            })

    return filtered
