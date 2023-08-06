"""
    aiominecraft
    ============
    Async minecraft status retriever
"""
import asyncio
import cubelib
from json import loads
from time import time

class ServerError(RuntimeError):
    """Error during communicating with server"""
    pass

class AsyncStatusRetriever:

    @staticmethod
    async def read_packet_async(reader):
        buffer = b""
        try:
            while 7:
                buffer += await reader.read(65535)
                packets = []
                buffer = cubelib.readPacketsStream(buffer,
                    -1, cubelib.bound.Client, packets)
                if buffer:                        
                    continue                
                return packets[0].resolve(cubelib.state.Status, cubelib.proto)

        except Exception as e:
            raise ServerError("Error occured during recieving a packet") from e

    @staticmethod
    async def retrieve(host: str, port: int = 25565, protocol: int = -1, timeout: float = 1.0) -> str:
        """
            Retrieve minecraft server status

            Args:
                host (str): Server hostname
                port (int): Server port
                timeout (float): Execution timeout

            Raises:
                ConnectionError: Failed to connect to the server
                TimeoutError: Connection timeout
                ServerError: Error during communicating with server

            Returns:
                JsonRsp (str): Server status json
        """
        try:            
            reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout = 5)            

            writer.write(cubelib.proto.ServerBound.Handshaking.Handshake(protocol,
                         host, port, cubelib.NextState.Status).build())
            writer.write(cubelib.proto.ServerBound.Status.Request().build())
            await writer.drain()
            status = await asyncio.wait_for(AsyncStatusRetriever.read_packet_async(reader), timeout=timeout)

            writer.write(cubelib.proto.ServerBound.Status.Ping(1337).build())
            await writer.drain()
            ping_sent = time()
            pong = await asyncio.wait_for(AsyncStatusRetriever.read_packet_async(reader), timeout=timeout)
            pong_rcvd = time()
            if pong.Uniq != 1337:
                raise ServerError("Invalid pong?")        

            writer.close()

        except Exception as e:
            raise ConnectionError("Connection Timeout" if isinstance(e, asyncio.TimeoutError) else e) from e

        return loads(status.JsonRsp), round((pong_rcvd - ping_sent) * 1000), writer.transport._sock.family
