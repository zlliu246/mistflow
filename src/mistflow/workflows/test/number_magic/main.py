from mistflow import Workflow, Stage

workflow = Workflow(
    name="number_magic",
    start_stage="square_number",
)

workflow.add_stage(
    Stage(
        stage_id="square_number",
        description="square the number lol",
        task_path="mistflow.tasks.test.square",
        get_stage_input=lambda context: {
            "number": context["wf_input"]["magic_number"]
        },
        next_stage="add100"
    )
)

workflow.add_stage(
    Stage(
        stage_id="add100",
        description="add 100 to number lol",
        task_path="mistflow.tasks.test.add100",
        get_stage_input=lambda context: {
            "number": context["stage_output"]["square_number"]["squared_number"]
        },
        next_stage="finish",
    )
)

"""
python3 -m mistflow workflow run mistflow.workflows.test.number_magic '{"magic_number": 5}'
"""