import concurrent
from http.server import HTTPServer

from servers.socket import *
from servers.web import *
import asyncio


def run_socket_server():
    print('Starting Socket Server...')
    run_socket_main()


def run_web(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', 3000)
    httpd = server_class(server_address, handler_class)
    print(f'Starting http server on port 3000')
    httpd.serve_forever()


async def run_blocking_tasks(executor, fn):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, fn)
    return result


async def main():
    with concurrent.futures.ProcessPoolExecutor() as executor:
    # with concurrent.futures.ThreadPoolExecutor() as executor:
        # futures = [run_blocking_tasks(executor, run_web), run_socket_server()]
        futures = [run_blocking_tasks(executor, run_web), run_blocking_tasks(executor, run_socket_server)]
        results = await asyncio.gather(*futures)
        return results


if __name__ == "__main__":
    asyncio.run(main())