import multiprocessing
from src.simtwin.broker import Broker


def __mock_remote_server__(port, api_key):
    broker = Broker(port, lambda x: x == api_key)
    broker.await_client()
    while True:
        if not broker.listen():
            break
    broker.socket.close()


def run_remote_server(port, key):
    process = multiprocessing.Process(target=__mock_remote_server__, args=(port, key))
    process.start()
    return process
