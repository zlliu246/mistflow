from typing import Any, Optional
import importlib
from pathlib import Path
import logging 

from mistflow.utils.pip_installer import pip_install

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)

class TaskRunner:
    def __init__(self, task_path: str) -> None:
        self.path_segments = task_path.split(".")
        self.main_module = self.import_lib("main")
        self.models_module = self.import_lib("models")

    def install_dependencies(self):
        try:
            path = Path("/".join(self.path_segments))
            req_path = path / "requirements.txt"
            pip_install("pydantic")
            if req_path.exists():
                pip_install("-r", str(req_path), "-qqq")
        except Exception as e:
            print(str(e))

    def run(
        self, 
        input_json_string: Optional[str] = None, 
        input_dict: Optional[dict[str, Any]] = None,
    ) -> "Output":
        if input_json_string is None and input_dict is None:
            raise AssertionError("Either input_json_string or input_dict must be given")
        elif input_json_string:
            inp = self.models_module.Input.model_validate_json(input_json_string)
        else:
            inp = self.models_module.Input.model_validate(input_dict)

        logger.info(f"Task Input: {inp.json()}")

        out = self.main_module.Main().run(inp)
        assert isinstance(out, self.models_module.Output)
        logger.info(f"Task Output: {out}")

        return out

    def import_lib(self, filename: str = "main"):
        mod_path = ".".join(self.path_segments + [filename])
        mod = importlib.import_module(mod_path)
        return mod

    def import_main(self):
        return self.import_lib("main")

    def import_models(self):
        return self.import_lib("models")