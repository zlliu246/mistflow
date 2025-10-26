import importlib
from types import ModuleType
import logging

from mistflow.runners.task_runner import TaskRunner

logger = logging.getLogger(__name__)

class WorkflowRunner:
    def __init__(
        self, 
        workflow_full_name: str,
        input_json: str,
    ):
        self.path_segments: list[str] = workflow_full_name.split(".")
        self.input_json: str = input_json
        self.main_module: ModuleType = self.import_lib("main")
        self.models_module: ModuleType = self.import_lib("models")
        self.workflow: "Workflow" = self.main_module.workflow
        
    def import_lib(self, filename: str) -> ModuleType:
        import_path = ".".join(self.path_segments + [filename])
        return importlib.import_module(import_path)

    def install_dependencies(self) -> None:
        for stage in self.main_module.workflow.stage_id_to_stage_map.values():
            task_runner = TaskRunner(stage.task_path)
            task_runner.install_dependencies()

    def run(self) -> None:
        inp: "Input" = self.models_module.Input.model_validate_json(self.input_json)
        self.main_module.workflow.run(inp)