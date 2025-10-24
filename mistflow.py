
import json
import sys
import importlib
from pathlib import Path

from abc import ABC, abstractmethod

class Stage(ABC):
    @abstractmethod
    def run(self):
        pass

class StageEnv:
    BASE_PREFIX = "stages"
    
    def __init__(self, stage_id: str) -> None:
        self.path_segments = [self.BASE_PREFIX] + stage_id.split(".")

    def install_dependencies(self):
        path = Path("/".join(self.path_segments))
        req_path = path / "requirements.txt"
        import pip
        pip.main(["install", "pydantic"])
        pip.main(["install", "-r", str(req_path), "-qqq"])

    def import_lib(self, filename: str = "main"):
        mod_path = ".".join(self.path_segments + [filename])
        mod = importlib.import_module(mod_path)
        return mod

    def import_main(self):
        return self.import_lib("main")

    def import_models(self):
        return self.import_lib("models")

def main():
    args = sys.argv[1:]
    if len(args) == 0:
        return print("hello from mistflow")

    if args[:2] == ["stage", "run"]:
        stage_id, inp_json_string, *_ = args[2:]
        stage_env = StageEnv(stage_id)
        stage_env.install_dependencies()

        main_module = stage_env.import_main()
        models_module = stage_env.import_models()

        inp = models_module.Input.model_validate_json(inp_json_string)
        print()
        print("Input:")
        print(inp)

        out = main_module.Main().run(inp)
        assert isinstance(out, models_module.Output)

        print()
        print("Output:")
        print(out)


if __name__ == "__main__":
    main()