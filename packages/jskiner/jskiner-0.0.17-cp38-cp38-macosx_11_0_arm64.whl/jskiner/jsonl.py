"""
XXX:
- [X] make staticmethod class method to increase performance
- [X] extract schema Reducer from jsonl.py and json_files.py
- [X] make pipeline to make code more understandable
"""
import os
import shutil
import subprocess
from .jskiner import InferenceEngine
from .reduce import SchemaReducer


class JsonlProcessor:
    def __init__(self, args):
        self._args = args
        self._engine = InferenceEngine(args.nworkers)
        self._reducer = SchemaReducer()

    def run(self) -> str:
        if self._args.split > 1:
            schema_str = self.get_schema_batchwise(
                self._args.in_path, self._args.split_path, self._args.split
            )
        else:
            json_batch = self.load_json_batch(self._args.in_path)
            schema_str = self._engine.run(json_batch)
        return schema_str

    def get_schema_batchwise(self, src_path, split_path, split_cnt):
        try:
            JsonlProcessor.refresh_split_path(split_path)
            JsonlProcessor.split(src_path, split_path, split_cnt)
            file_iter = os.listdir(split_path)
            if self._args.verbose:
                try:
                    import tqdm
                except ImportError:
                    subprocess.run(["pip", "install", "tqdm"])
                    import tqdm
                file_iter = tqdm.tqdm(file_iter)
            paths = map(lambda fn: f"{split_path}/{fn}", file_iter)
            json_batches = map(self.load_json_batch, paths)
            schema_strings = map(self._engine.run, json_batches)
            schema_str = self._reducer.reduce(schema_strings)
            return schema_str
        except BaseException as e:
            with open("log", "w") as f:
                f.write(schema_str)
            raise e
        finally:
            JsonlProcessor.refresh_split_path(split_path)

    def load_json_batch(self, jsonl_path):
        with open(jsonl_path, "r") as f:
            json_batch = [x for x in f]
        return json_batch

    @staticmethod
    def refresh_split_path(path):
        if not os.path.exists(path):
            os.mkdir(path)
        else:
            shutil.rmtree(path)
            os.mkdir(path)

    @staticmethod
    def split(src_path, split_path, split_cnt):
        total = JsonlProcessor.get_total_json_count(src_path)
        cnt_per_file = int(total / split_cnt)
        subprocess.run(["split", "-l", str(cnt_per_file), src_path, split_path + "/"])

    @staticmethod
    def get_total_json_count(path):
        out = subprocess.check_output(["wc", "-l", path])
        total = int(out.decode("utf-8").split(path)[0])
        return total
