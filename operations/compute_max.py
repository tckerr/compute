import dataclasses
import uuid
from typing import Union, Dict

from pydantic import BaseModel

from operations.base import BaseModule


class InputComputeMax(BaseModel):
    type: str = "compute_max"
    length: int


class InputComparisonResult(BaseModel):
    type: str = "comparison_result"
    answer: bool
    request_id: str


class ResponseCompare(BaseModel):
    left: int
    right: int
    request_id: str
    type: str = "compare"


class ResponseDone(BaseModel):
    result: int
    type: str = "done"


@dataclasses.dataclass
class Request:
    length: int
    max: int
    next: int


PostModel = Union[InputComputeMax, InputComparisonResult]
ResponseModel = Union[ResponseCompare, ResponseDone]


class Module(BaseModule):
    PostModel = PostModel
    ResponseModel = ResponseModel
    supported_message_types = ['compute_max', 'comparison_result']

    def __init__(self) -> None:
        super().__init__()
        self.__memory_store: Dict[str, Request] = {}

    def process(self, data: PostModel) -> ResponseModel:
        if data.type == "compute_max":
            request_id = str(uuid.uuid4())
            request = Request(length=data.length, max=0, next=1)
            self.__memory_store[request_id] = request
            return self.compare_or_resolve(request, request_id)

        elif data.type == "comparison_result":
            request = self.__memory_store[data.request_id]
            if data.answer:
                request.max = request.next

            request.next += 1
            return self.compare_or_resolve(request, data.request_id)

        else:
            raise ValueError(f"Unknown message type: {data.type}")

    @staticmethod
    def compare_or_resolve(request: Request, request_id: str) -> ResponseModel:
        if request.next < request.length:
            return ResponseCompare(
                left=request.max,
                right=request.next,
                request_id=request_id)

        return ResponseDone(result=request.max)
