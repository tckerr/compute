from typing import Union, List
from fastapi import FastAPI
from operations.base import BaseModule
from operations.compute_max import Module as ComputeMax

modules: List[BaseModule] = [
    ComputeMax()
]

PostModel = Union[
    ComputeMax.PostModel,
]

ResponseModel = Union[
    ComputeMax.ResponseModel,
]


module_lookup = {}
for m in modules:
    for msg_type in m.supported_message_types:
        if msg_type in module_lookup:
            raise ValueError(f"Error registering module. Duplicate message type: {msg_type}")
        module_lookup[msg_type] = m

app = FastAPI()


@app.post("/")
def root(data: PostModel) -> ResponseModel:
    if data.type not in module_lookup:
        raise Exception("Unknown request type")

    module = module_lookup[data.type]
    return module.process(data)
