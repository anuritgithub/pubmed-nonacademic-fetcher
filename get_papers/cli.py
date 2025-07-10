import argparse
from get_papers.fetcher import fetch_papers
from get_papers.filters import filter_non_academic
from get_papers.writer import output_results
def main():
    parser = argparse.ArgumentParser(
        description="Fetch PubMed papers with at least one non-academic author."
    )
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-f", "--file", help="Filename to save output (CSV or JSON)")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logging")
    parser.add_argument(
        "--format",
        choices=["csv", "json"],
        default="csv",
        help="Output format: csv (default) or json",
    )
    args = parser.parse_args()
    if args.debug:
        print(f"[DEBUG] Query: {args.query}")
    papers = fetch_papers(args.query, debug=args.debug)
    filtered = filter_non_academic(papers)
    output_results(filtered, filename=args.file, output_format=args.format)

if __name__ == "__main__":
    main()
