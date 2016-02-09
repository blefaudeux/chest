import asyncio
 
# See http://www.curiousefficiency.org/posts/2015/07/asyncio-tcp-echo-server.html


def run_in_foreground(task, *, loop=None):
    """
    Runs event loop in current thread until the given task completes

    Returns the result of the task.
    For more complex conditions, combine with asyncio.wait()
    To include a timeout, combine with asyncio.wait_for()
    """
    if loop is None:
        loop = asyncio.get_event_loop()
        
    return loop.run_until_complete(asyncio.ensure_future(task, loop=loop))

async def handle_tcp_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print("-> Server received %r from %r" % (message, addr))
    print("<- Server sending: %r" % message)
    writer.write(data)
    await writer.drain()
    print("-- Terminating connection on server")
    writer.close()

async def tcp_echo_client(message, port, loop=None):
    reader, writer = await asyncio.open_connection('127.0.0.1', port, loop=loop)
    print('-> Client sending: %r' % message)
    writer.write(message.encode())
    data = (await reader.read(100)).decode()
    print('<- Client received: %r' % data)
    print('-- Terminating connection on client')
    writer.close()
    return data

if __name__ == "__main__":
    make_server = asyncio.start_server(handle_tcp_echo, '127.0.0.1')
    server = run_in_foreground(make_server)

