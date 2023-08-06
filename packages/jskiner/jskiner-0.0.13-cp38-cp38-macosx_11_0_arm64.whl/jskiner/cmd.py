import argparse
import subprocess
from .jsonl import JsonlProcessor


def get_args():
    parser = argparse.ArgumentParser(description="Inferencing Json Schema")

    parser.add_argument(
        "--jsonl",
        type=str,
        required=True,
        help="Inference Json Schema from .jsonl file",
    )

    parser.add_argument(
        "--nworkers", type=int, required=False, default=1, help="Inference Worker Count"
    )

    parser.add_argument(
        "--verbose",
        type=bool,
        required=False,
        default=False,
        help="Showing the Result by Pretty Print",
    )

    parser.add_argument(
        "--out",
        type=str,
        required=False,
        default="out.schema",
        help="Saving the json schema into a output file",
    )

    parser.add_argument(
        "--format",
        type=bool,
        required=False,
        default=True,
        help="formatting the output schema using `black`",
    )

    parser.add_argument(
        "--split",
        type=int,
        required=False,
        default=1,
        help="Number of splitted jsonl file (1 for no splitting)",
    )
    parser.add_argument(
        "--split_path",
        type=str,
        required=False,
        default="/tmp/split",
        help="Path to store the temporary splitted jsonl files",
    )
    args = parser.parse_args()
    return args


def run() -> None:
    args = get_args()
    if args.verbose:
        print(f"Loading {args.jsonl}")
    schema_str = JsonlProcessor(args).run()
    store(schema_str, output_path=args.out, verbose=args.verbose, format=args.format)


def store(schema_str, output_path="out.schema", verbose=False, format=True):
    if output_path != "":
        with open(output_path, "w") as f:
            f.write(schema_str)
        if verbose:
            print("Result saved into", output_path)
        if format:
            try:
                exec("import black")
            except ImportError:
                subprocess.run(["pip", "install", "black"])
            subprocess.run(["black", output_path])
