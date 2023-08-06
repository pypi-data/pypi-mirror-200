import argparse
import subprocess
from .jsonl import JsonlProcessor
from .folder import JsonFileProcessor


def get_args():
    parser = argparse.ArgumentParser(description="Inferencing Json Schema")

    parser.add_argument(
        "--in-path",
        type=str,
        required=True,
        help="Path to inference json schema from (a .jsonl file or a folder of json files)",
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
        "--split-path",
        type=str,
        required=False,
        default="/tmp/split",
        help="Path to store the temporary splitted jsonl files",
    )
    parser.add_argument(
        "--cuckoo-path",
        type=str,
        required=False,
        default="cuckoo.pickle",
        help="Path to store pickled Cuckoo Filter",
    )
    parser.add_argument(
        "--cuckoo-size",
        type=int,
        required=False,
        default=10000000,
        help="Approximated json file count for build a Cuckoo Filter with enough capacity",
    )
    parser.add_argument(
        "--cuckoo-fpr",
        type=float,
        required=False,
        default=0.01,
        help="False Positive Rate of the Cuckoo Filter",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        required=False,
        default=None,
        help="Batch Size of Inferencing (required when input is a folder of json files)",
    )
    parser.add_argument(
        "--sample-size",
        type=int,
        required=False,
        default=None,
        help="Number of json files to be sampled (a approach to avoid slow inferencing)",
    )
    args = parser.parse_args()
    return args


def run() -> None:
    args = get_args()
    if args.verbose:
        print(f"Loading {args.in_path}")
    if ".jsonl" in args.in_path:
        schema_str = JsonlProcessor(args).run()
    else:
        schema_str = JsonFileProcessor(args).run()
    store(schema_str, output_path=args.out, verbose=args.verbose, format=args.format)


def store(schema_str: str, output_path="out.schema", verbose=False, format=True):
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
