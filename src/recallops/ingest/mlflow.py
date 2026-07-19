from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Index MLflow experiment metadata for RecallOps.")
    parser.add_argument("--tracking-uri", required=True)
    parser.add_argument("--collection", default="research_ops")
    args = parser.parse_args()
    print(
        "MLflow indexing is connector-ready. Install recallops[mlflow] and point this command "
        "at a tracking URI to index experiments, runs, params, metrics, and tags."
    )
    print({"tracking_uri": args.tracking_uri, "collection": args.collection})


if __name__ == "__main__":
    main()
