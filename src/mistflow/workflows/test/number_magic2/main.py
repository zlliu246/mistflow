from mistflow import Workflow, Stage, Transition

workflow = Workflow(
    name="number_magic2",
    start_stage="square",
    description="""
        Square a number and add 100 until the number > 1000000
    """
)

workflow.add_stage(
    Stage(
        stage_id="square",
        description="square the number lol",
        task_path="mistflow.tasks.test.square",
        get_stage_input=lambda context: {
            "number": (
                context.get("stage_output", {}).get("add100", {}).get("new_number")
                or context["wf_input"]["start_number"]
            )
        },
        transitions=[
            Transition(
                condition=lambda context: context["stage_output"]["square"]["squared_number"] < 1000000,
                to_stage="add100", 
            ),
            Transition(to_stage="finish")
        ]
    )
)

workflow.add_stage(
    Stage(
        stage_id="add100",
        description="add 100 to number lol",
        task_path="mistflow.tasks.test.add100",
        get_stage_input=lambda context: {
            "number": context["stage_output"]["square"]["squared_number"]
        },
        transitions=[
            Transition(
                condition=lambda context: context["stage_output"]["add100"]["new_number"] < 1000000,
                to_stage="square",
            ),
            Transition(to_stage="finish")
        ]
    )
)

"""
python3 -m mistflow workflow run mistflow.workflows.test.number_magic2 '{"start_number": 3}'
"""