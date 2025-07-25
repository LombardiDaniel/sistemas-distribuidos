import calculator_pb2
import calculator_pb2_grpc
import grpc


def main():
    with grpc.insecure_channel("localhost:443") as channel:
        stub = calculator_pb2_grpc.CalculatorStub(channel)
        request = calculator_pb2.AddRequest(x=2, y=5)
        response = stub.Add(request)
        print(response)


if __name__ == "__main__":
    main()
