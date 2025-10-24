"""
Takes in a number, returns the square of that number
"""
from .models import Input, Output

class Main:
    def run(self, inp: Input) -> Output:
        return Output(
            squared_number=inp.number ** 2,
            message=inp.message + "!!!"
        )


"""
python3 mistflow.py stage run test.square '{"number": 5, "message": "hello"}'
"""