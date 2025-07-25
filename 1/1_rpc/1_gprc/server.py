from concurrent import futures

import calculator_pb2
import calculator_pb2_grpc
import grpc


class CalculatorServicer(calculator_pb2_grpc.CalculatorServicer):
    def Add(self, request, context):
        return calculator_pb2.AddResponse(result=request.x + request.y)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServicer_to_server(CalculatorServicer(), server)
    print(server.add_insecure_port("[::]"))
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
