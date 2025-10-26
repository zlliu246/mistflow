from mistflow.workflow import Context

def get_square_the_number_input(context: Context) -> str:
    if "add_100_to_number" not in context["stage_output"]:
        number = context["wf_input"]["start_number"]
    else:
        number = context["stage_output"]["add_100_to_number"]["new_number"]
    return {"number": number}

def get_square_the_number_next_stage(context: Context) -> str:
    squared_number = context["stage_output"]["square_the_number"]["squared_number"]
    if squared_number > 1000000:
        return "finish"
    return "add_100_to_number"

def get_add_100_to_number_input(context: Context) -> str:
    number = context["stage_output"]["square_the_number"]["squared_number"] 
    return {"number": number}

def get_add_100_to_number_next_stage(context: Context) -> str:
    new_number = context["stage_output"]["add_100_to_number"]["new_number"]
    if new_number > 1000000:
        return "finish"
    return "square_the_number"
