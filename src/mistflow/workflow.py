from typing import Callable, Any, TypedDict, Sequence, Optional, NamedTuple
import logging
from dataclasses import dataclass

from .runners.task_runner import TaskRunner

logger = logging.getLogger(__name__)

class Context(TypedDict):
    metadata: dict[str, Any]
    wf_input: dict[str, Any]
    stage_input: dict[str, Any]
    stage_output: dict[str, Any]

@dataclass
class Transition:
    to_stage: str
    condition: Optional[Callable[[Context], bool]] = None
    

class Stage:
    def __init__(
        self,
        stage_id: str,
        description: str,
        task_path: str,
        get_stage_input: Callable,
        next_stage: Optional[str] = None,
        next_stages: Optional[Sequence[Transition]] = None,
    ) -> None:
        self.stage_id = stage_id
        self.description = description
        self.task_path = task_path
        self.get_stage_input = staticmethod(get_stage_input)

        self.next_stage = next_stage
        self.next_stages = next_stages

        if not next_stage and not next_stages:
           raise AssertionError("Either 'next_stage' or 'next_stages' must be provided") 
        elif next_stage:
            get_next_stage = lambda *args: next_stage
        else:
            def get_next_stage(context: Context) -> str:
                *transitions, default_transition = next_stages
                for transition in transitions:
                    if transition.condition(context):
                        return transition.to_stage
                return default_transition.to_stage

        self.get_next_stage = get_next_stage

    def __str__(self) -> str:
        return f"Stage({self.stage_id!r} => {self.next_stages})"

    def __repr__(self) -> str:
        return self.__str__()

class Workflow:
    def __init__(self, name: str, start_stage: str, description: str = "") -> None:
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
            if stage.next_stage:
                child_stage_ids.add(stage.next_stage)
            for transition in stage.next_stages or []:
                child_stage_ids.add(transition.to_stage)
        if "finish" not in child_stage_ids:
            raise AssertionError(
                "At least one stage must lead to the 'finish' stage, but this is not the case."
            )

        # check that start_stage exists
        if self.start_stage not in self.stage_id_to_stage_map:
            raise AssertionError(
                f"Start stage {self.start_stage!r} doesn't exist. Please use .add_stage to add the start stage."
            )
