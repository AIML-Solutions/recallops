from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Create an arXiv research snapshot for RecallOps.")
    parser.add_argument("--query", required=True)
    parser.add_argument("--max-results", type=int, default=25)
    parser.add_argument("--collection", default="research_ops")
    args = parser.parse_args()
    print(
        "arXiv ingestion is connector-ready. "
        "Use ENABLE_NETWORK_TESTS=1 for live integration tests and configure the connector policy."
    )
    print({"query": args.query, "max_results": args.max_results, "collection": args.collection})


if __name__ == "__main__":
    main()
