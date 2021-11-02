from unittest import TestCase
from operations.compute_max import Module as ComputeMax, InputComputeMax, InputComparisonResult, ResponseCompare, \
    ResponseDone


class TestComputeMax(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.subject = ComputeMax()

    def test_empty(self):
        input = InputComputeMax(length=0)

        result = self.subject.process(input)

        expected_result = ResponseDone(result=0)
        self.assertEqual(result, expected_result)

    def test_single(self):
        input = InputComputeMax(length=1)

        result = self.subject.process(input)

        expected_result = ResponseDone(result=0)
        self.assertEqual(result, expected_result)

    def test_max_at_end(self):
        response = InputComputeMax(length=3)

        result = self.subject.process(response)
        req_id = result.request_id

        self.assertEqual(result.left, 0)
        self.assertEqual(result.right, 1)

        response = InputComparisonResult(request_id=req_id, answer=True)
        result = self.subject.process(response)

        self.assertEqual(result.left, 1)
        self.assertEqual(result.right, 2)

        response = InputComparisonResult(request_id=req_id, answer=True)
        result = self.subject.process(response)

        self.assertEqual(result.result, 2)

    def test_max_in_middle(self):
        response = InputComputeMax(length=3)

        result = self.subject.process(response)
        req_id = result.request_id

        self.assertEqual(result.left, 0)
        self.assertEqual(result.right, 1)

        response = InputComparisonResult(request_id=req_id, answer=True)
        result = self.subject.process(response)

        self.assertEqual(result.left, 1)
        self.assertEqual(result.right, 2)

        response = InputComparisonResult(request_id=req_id, answer=False)
        result = self.subject.process(response)

        self.assertEqual(result.result, 1)
