from .models import Input, Output

import requests

class Main:
    def run(self, inp: Input) -> Output:
        url: str = inp.url
        response = requests.get(url).json()
        return Output(response=response)

"""
python3 -m mistflow task run tasks.test.call_dummy_api '{"url": "https://dummyjson.com/products"}'
"""