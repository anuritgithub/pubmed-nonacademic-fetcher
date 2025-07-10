import pandas as pd
from tabulate import tabulate
from typing import List, Dict
import textwrap

def output_results(papers: List[Dict], filename: str = None, output_format: str = "csv") -> None:
    if not papers:
        print("[INFO] No results to display.")
        return
    df = pd.DataFrame(papers)
    for col in ["Non-academic Authors", "Company Affiliations", "Email"]:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)
    for col in ["Title", "Company Affiliations"]:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: textwrap.shorten(str(x), width=100, placeholder="..."))

    if filename:
        if output_format == "json":
            df.to_json(filename, orient="records", indent=2)
        else:
            df.to_csv(filename, index=False)
        print(f"[INFO] Saved results to {filename}")
    else:
        print(tabulate(df, headers="keys", tablefmt="grid", showindex=False))


def print_debug_output(papers: List[Dict]) -> None:
    if not papers:
        print("[INFO] No results to display.")
        return

    headers = [
        "PubmedID",
        "Title",
        "Date",
        "Non-academic Authors",
        "Company Affiliations",
        "Email"
    ]

    table_data = []
    for paper in papers:
        table_data.append([
            paper.get("PubmedID", ""),
            textwrap.shorten(paper.get("Title", ""), width=100, placeholder="..."),
            paper.get("Date", paper.get("Publication Date", "")),
            ", ".join(paper.get("Non-academic Authors", [])),
            ", ".join(paper.get("Company Affiliations", [])),
            ", ".join(paper.get("Email", paper.get("Corresponding Author Email", [])))
        ])

    print(tabulate(table_data, headers=headers, tablefmt="grid"))
