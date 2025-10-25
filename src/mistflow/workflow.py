from typing import Callable, Any, TypedDict, Sequence, Optional
import logging

from .runners.task_runner import TaskRunner

logger = logging.getLogger(__name__)

class Context(TypedDict):
    metadata: dict[str, Any]
    wf_input: dict[str, Any]
    stage_input: dict[str, Any]
    stage_output: dict[str, Any]

class Stage:
    def __init__(
        self,
        stage_id: str,
        description: str,
        task_path: str,
        get_stage_input: Callable,
        next_stages: Sequence[str],
        get_next_stage: Optional[Callable] = None,
    ) -> None:
        self.stage_id = stage_id
        self.description = description
        self.task_path = task_path
        self.get_stage_input = staticmethod(get_stage_input)
        self.next_stages = next_stages
        if len(self.next_stages) == 1:
            self.get_next_stage = lambda *args: self.next_stages[0]
        else:
            assert get_next_stage is not None, "If there are more than 1 posisble next stages, the function 'get_next_stage' must be provided"
            self.get_next_stage = staticmethod(get_next_stage)

    def __str__(self) -> str:
        return f"Stage({self.stage_id!r} => {self.next_stages})"

    def __repr__(self) -> str:
        return self.__str__()

class Workflow:
    def __init__(self, name: str, start_stage: str) -> None:
        self.wf_name = name
        self.start_stage = start_stage
        self.stage_id_to_stage_map: dict[str, Stage] = {}
        self.context: Context = {
            "metadata": {},
            "wf_input": {},
            "stage_input": {},
            "stage_output": {},
        }

    def add_stage(self, stage: Stage) -> None:
        if stage.stage_id in self.stage_id_to_stage_map:
            raise AssertionError(
                f"Stage id {stage.stage_id} already exists. Not allowed to have 2 stages with the same ID"
            )
        self.stage_id_to_stage_map[stage.stage_id] = stage

    def run(self, inp) -> None:
        logger.info(f"Starting to run workflow: {self.wf_name}")
        self.context["wf_input"] = inp.dict()
        self._validate_stages()

        current_stage_id = self.start_stage
        while current_stage_id != "finish":
            
            logger.info(f"Running stage {current_stage_id!r}")
            current_stage = self.stage_id_to_stage_map[current_stage_id]

            task_runner = TaskRunner(current_stage.task_path)
            inp: dict = current_stage.get_stage_input(self.context)
            self.context["stage_input"][current_stage_id] = inp

            out: "Output" = task_runner.run(input_dict=inp)
            
            self.context["stage_output"][current_stage_id] = out.dict()
            next_stage_id = current_stage.get_next_stage(self.context)
            current_stage_id = next_stage_id

    def _validate_stages(self) -> None:
        # check that at least one stage leads to "finish"
        child_stage_ids = set()
        for stage in self.stage_id_to_stage_map.values():
            child_stage_ids.update(set(stage.next_stages))
        if "finish" not in child_stage_ids:
            raise AssertionError(
                "At least one stage must lead to the 'finish' stage, but this is not the case."
            )

        # check that start_stage exists
        if self.start_stage not in self.stage_id_to_stage_map:
            raise AssertionError(
                f"Start stage {self.start_stage!r} doesn't exist. Please use .add_stage to add the start stage."
            )
