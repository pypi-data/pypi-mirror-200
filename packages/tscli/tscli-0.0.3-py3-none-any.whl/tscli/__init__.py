
import grpc
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from . import secure_operate_pb2
from . import secure_operate_pb2_grpc
sys.path.pop(0)
from . import packer


class TensorClient:
    def __init__(self, serving_address) -> None:
        self.__serving_address = serving_address

    def expressions(self) -> secure_operate_pb2.ExpressionsResponse:
        chl = grpc.insecure_channel(self.__serving_address)
        stub = secure_operate_pb2_grpc.CallStub(chl)
        req = secure_operate_pb2.ExpressionsRequest()
        return stub.expressions(req)

    def execute(self, req: secure_operate_pb2.ExecuteRequest) -> secure_operate_pb2.ExecuteResponse:
        chl = grpc.insecure_channel(self.__serving_address)
        stub = secure_operate_pb2_grpc.CallStub(chl)
        return stub.execute(req)

    def query(self, req: secure_operate_pb2.TaskTabRequest) -> secure_operate_pb2.ExecuteResponse:
        chl = grpc.insecure_channel(self.__serving_address)
        stub = secure_operate_pb2_grpc.CallStub(chl)
        return stub.query(req)

    def kill(self, req: secure_operate_pb2.TaskTabRequest) -> secure_operate_pb2.ExecuteResponse:
        chl = grpc.insecure_channel(self.__serving_address)
        stub = secure_operate_pb2_grpc.CallStub(chl)
        return stub.kill(req)


class AsyncTensorClient:
    def __init__(self, serving_address) -> None:
        self.__serving_address = serving_address

    async def expressions(self) -> secure_operate_pb2.ExpressionsResponse:
        async with grpc.aio.insecure_channel(self.__serving_address) as chl:
            stub = secure_operate_pb2_grpc.CallStub(chl)
            req = secure_operate_pb2.ExpressionsRequest()
            return await stub.expressions(req)

    async def execute(self, req: secure_operate_pb2.ExecuteRequest) -> secure_operate_pb2.ExecuteResponse:
        async with grpc.aio.insecure_channel(self.__serving_address) as chl:
            stub = secure_operate_pb2_grpc.CallStub(chl)
            return await stub.execute(req)

    async def query(self, req: secure_operate_pb2.TaskTabRequest) -> secure_operate_pb2.ExecuteResponse:
        async with grpc.aio.insecure_channel(self.__serving_address) as chl:
            stub = secure_operate_pb2_grpc.CallStub(chl)
            return await stub.query(req)

    async def kill(self, req: secure_operate_pb2.TaskTabRequest) -> secure_operate_pb2.ExecuteResponse:
        async with grpc.aio.insecure_channel(self.__serving_address) as chl:
            stub = secure_operate_pb2_grpc.CallStub(chl)
            return await stub.kill(req)
