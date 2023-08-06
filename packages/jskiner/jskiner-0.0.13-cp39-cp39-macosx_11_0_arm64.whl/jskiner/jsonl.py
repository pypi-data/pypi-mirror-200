import os
import shutil
import subprocess
from .jskiner import InferenceEngine

exec("from .schema import *")


class JsonlProcessor:
    def __init__(self, args):
        self._args = args

    def run(self):
        if self._args.split > 1:
            schema_str = JsonlProcessor.get_schema_batchwise(
                self._args.jsonl,
                self._args.split_path,
                self._args.split,
                verbose=self._args.verbose,
                worker_cnt=self._args.nworkers,
            )
        else:
            schema_str = JsonlProcessor.get_schema_from_jsonl(
                self._args.jsonl, worker_cnt=self._args.nworkers
            )
        return schema_str

    @staticmethod
    def get_schema_batchwise(
        src_path, split_path, split_cnt, verbose=False, worker_cnt=1
    ):
        try:
            JsonlProcessor.refresh_split_path(split_path)
            JsonlProcessor.split(src_path, split_path, split_cnt)
            schema = eval("Unknown()")
            file_iter = os.listdir(split_path)
            if verbose:
                try:
                    import tqdm
                except ImportError:
                    subprocess.run(["pip", "install", "tqdm"])
                file_iter = tqdm.tqdm(file_iter)
            for file_name in file_iter:
                selected_path = f"{split_path}/{file_name}"
                if verbose:
                    print("Start Inferencing", selected_path)
                schema_str = JsonlProcessor.get_schema_from_jsonl(
                    selected_path, worker_cnt=worker_cnt
                )
                schema |= eval(schema_str)
                if verbose:
                    print("Finish Inferencing", selected_path)
            schema_str = schema.__repr__()
            return schema_str
        except BaseException as e:
            with open("log", "w") as f:
                f.write(schema_str)
            raise e
        finally:
            JsonlProcessor.refresh_split_path(split_path)

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

    @staticmethod
    def get_schema_from_jsonl(jsonl_path, worker_cnt=1):
        with open(jsonl_path, "r") as f:
            json_list = [x for x in f]
        engine = InferenceEngine(worker_cnt)
        schema_str = engine.run(json_list)
        return schema_str
