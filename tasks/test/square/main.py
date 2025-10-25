from .models import Input, Output

class Main:
    def run(self, inp: Input) -> Output:
        return Output(
            squared_number=inp.number ** 2,
        )


"""
python3 -m mistflow stage run stages.test.square '{"number": 5}'
"""