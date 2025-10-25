from .models import Input, Output

class Main:
    def run(self, inp: Input) -> Output:
        return Output(
            new_number=inp.number + 100
        )
    
"""
python3 -m mistflow task run tasks.test.add100 '{"number": 6}'
"""