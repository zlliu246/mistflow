"""
start with a number
- square the number
- add 100 to the number
- repeat until number is larger than 1000000
"""
from typing import Any
from mistflow.workflow import Workflow, Stage
import workflows.test.number_magic2.utils as utils

workflow = Workflow(
    name="number_magic2",
    start_stage="square_the_number"
)

workflow.add_stage(
    Stage(
        stage_id="square_the_number",
        description="square the number lol",
        task_path="tasks.test.square",
        get_stage_input=utils.get_square_the_number_input,
        next_stages=["finish", "add_100_to_number"],
        get_next_stage=utils.get_square_the_number_next_stage,
    )
)

workflow.add_stage(
    Stage(
        stage_id="add_100_to_number",
        description="add 100 to number lol",
        task_path="tasks.test.add100",
        get_stage_input=utils.get_add_100_to_number_input,
        next_stages=["finish", "square_the_number"],
        get_next_stage=utils.get_add_100_to_number_next_stage,
    )
)

"""
python3 -m mistflow workflow run workflows.test.number_magic2 '{"start_number": 5}'
"""