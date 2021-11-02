import argparse
import requests
from dataclasses import asdict, dataclass


@dataclass
class Compare:
    request_id: int
    left: int
    right: int
    type: str = "compare"


@dataclass
class ComparisonResult:
    request_id: int
    answer: bool
    type: str = "comparison_result"


@dataclass
class ComputeMax:
    length: int
    type: str = "compute_max"


@dataclass
class Done:
    result: int
    type: str = "done"


def message_to_struct(message):
    if message["type"] == "compare":
        return Compare(**message)
    elif message["type"] == "comparison_result":
        return ComparisonResult(**message)
    elif message["type"] == "compute_max":
        return ComputeMax(**message)
    elif message["type"] == "done":
        return Done(**message)


class Client:
    def __init__(self, address, log=False):
        self.address = address if address else "http://localhost:5000"
        self.log = log

    def send(self, data):
        response = requests.post(self.address, json=asdict(data))
        json = response.json()
        if self.log:
            print(json)
        return message_to_struct(json)

    def compute(self, values, op):
        req = None
        if op == "max":
            req = ComputeMax(len(values))
        else:
            assert False, "not supported operation: " + op
        next_message = self.send(req)

        while True:
            if next_message.type == "done":
                return values[next_message.result]
            elif next_message.type == "compare":
                request_id = next_message.request_id
                left = next_message.left
                right = next_message.right
                next_message = self.send(ComparisonResult(request_id, values[left] < values[right]))
            else:
                raise Exception("Unexpected message: ", next_message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the max computer')
    parser.add_argument('--address', type=str, required=False,
                        help='address of the max computer (defaults to http://localhost:5000)')

    args = parser.parse_args()
    client = Client(args.address, log=True)
    assert 31 == client.compute([10, 25, 31, 10], op="max")
