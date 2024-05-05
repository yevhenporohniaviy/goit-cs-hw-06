import os

import socket
from concurrent import futures as cf
import pymongo
import json
import datetime

def run_server(ip='0.0.0.0', port=5000):

    def handle(sock: socket.socket, address: str):
        print(f'Connection established {address}')
        while True:
            received = sock.recv(1024)
            if not received:
                break
            data = json.loads(received.decode())
            print(f'Data received: {data}')

            # Connect to MongoDB
            username = os.getenv("DB_USERNAME", 'sa')
            password = os.getenv("DB_PASSWORD", 'test1234')
            db_host = os.getenv("DB_HOST", 'localhost')
            db_port = os.getenv("DB_PORT", '27017')

            with pymongo.MongoClient(f"mongodb://{username}:{password}@{db_host}:{db_port}/") as client:
                db = client["data"]
                collection = db["message"]

                # Insert data into MongoDB
                document = {
                    "username": data["username"],
                    "message": data["message"],
                    "date": datetime.datetime.now()
                    }
                collection.insert_one(document)
        print(f'Socket connection closed {address}')
        sock.close()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(10)
    print(f'Server Socket STARTED {server_socket.getsockname()}')
    with cf.ThreadPoolExecutor(10) as client_pool:
        try:
            while True:
                new_sock, address = server_socket.accept()
                client_pool.submit(handle, new_sock, address)
        except KeyboardInterrupt:
            print(f'Destroy server')
        finally:
            server_socket.close()


def run_socket_main():
    run_server()
    print('Server Socket FINISHED')