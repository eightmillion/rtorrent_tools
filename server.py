from types import FunctionType
import pprint
from collections.abc import Sequence
from .torrent import Torrent
from .torrentgroup import TorrentGroup
from .tracker import Tracker
from .fileutils import *
from .JsonRpcProxy import *
import re
import socket
import http.client
import sys
import xmlrpc.client

class UnixStreamHTTPConnection(http.client.HTTPConnection):

    def connect(self):
        self.sock = socket.socket(
            socket.AF_UNIX, socket.SOCK_STREAM
        )
        self.sock.connect(self.host)


class UnixStreamTransport(xmlrpc.client.Transport, object):

    def __init__(self, socket_path):
        self.socket_path = socket_path
        super().__init__()

    def make_connection(self, host):
        return UnixStreamHTTPConnection(self.socket_path)


class UnixStreamXMLRPCClient(xmlrpc.client.ServerProxy):

    def __init__(self, addr, **kwargs):
        transport = UnixStreamTransport(addr)
        super().__init__(
            "http://", transport=transport, **kwargs
        )

class Server:

    def __init__(self: object, server: str, jsonrpc=False) -> None:

        self.server = server
        if jsonrpc:
            self._rpc = JsonRpcProxy(self.server)
            self.multicall = JsonRpcMultiCall(self._rpc)
        else:
            self._rpc = xmlrpc.client.ServerProxy(self.server, allow_none=True)
            self.multicall = xmlrpc.client.MultiCall(self._rpc)
        self.jsonrpc = jsonrpc
        self.ui = self.__ui(self)
        self.view = self.__view(self)
        self.system = self.__system(self)
        self.convert = self.__convert(self)
        self.dht = self.__dht(self)
        self.ratio = self.__ratio(self)
        self.elapsed = self.__elapsed(self)
        self.encoding = self.__encoding(self)
        self.session = self.__session(self)
        self.group = self.__group(self)
        self.pieces = self.__pieces(self)
        self.throttle = self.__throttle(self)
        self.directory = self.__directory(self)
        self.choke_group = self.__choke_group(self)
        self.strings = self.__strings(self)
        self.network = self.__network(self)
        self.scheduler = self.__scheduler(self)
        self.protocol = self.__protocol(self)
        self.load = self.__load(self)
        self.update_views()

    def to_kb(self, value: str | int) -> str: return self._rpc.to_kb(value)
    def to_mb(self, value: str | int) -> str: return self._rpc.to_mb(value)
    def to_xb(self, value: str | int) -> str: return self._rpc.to_xb(value)
    def download_list(self) -> list: return self._rpc.download_list()
    def add_peer(self, arg1, arg2): return self._rpc.add_peer(arg1, arg2)
    def check_hash(self, value): return self._rpc.check_hash(int(value))
    def remove_untied(self): return self._rpc.remove_untied()
    def scgi_local(self, value): return self._rpc.scgi_local('', int(value))
    def scgi_port(self, port): return self._rpc.scgi_local(int(port))
    def ip(self, value): return self._rpc.ip(value)
    def fimport(self, file): return getattr(self._rpc, 'import')('', file)
    def try_import(self, file): return self._rpc.try_import('', file)
    def print(self, value): return self._rpc.print('', value)
    def port_random(self, port): return self._rpc.port_random('', port)
    def download_rate(self, rate: int) -> int:
        return self._rpc.download_rate('', rate)
    def upload_rate(self, rate: int) -> int:
        return self._rpc.upload_rate('', rate)
    def close_low_diskspace(self, space: int) -> int:
        return self._rpc.close_low_diskspace('', space)
    def close_untied(self) -> int: return self._rpc.close_untied()
    def encoding_list(self, value: str) -> int:
        return self._rpc.encoding_list(value)
    def max_memory_usage(self, value: str) -> int:
        return self._rpc.max_memory_usage(value)
    def proxy_address(self, address):
        return self._rpc.proxy_address('', address)

    class __load:

        def __init__(self, server):
            self.server = server
            self.normal = self.__normal
            self.raw = self.__raw
            self.start = self.__start
            self.start_verbose = self.__start_verbose
            self.raw_start = self.__raw_start
            self.raw_verbose = self.__raw_verbose
            self.verbose = self.__verbose

        def __normal(self, meta, torrent_file):
            return self.server._rpc.load.normal(meta, torrent_file)

        def __verbose(self, meta, torrent_file):
            return self.server._rpc.load.verbose(meta, torrent_file)

        def __raw(self, meta, torrent_data):
            return self.server._rpc.load.raw(meta, torrent_data)

        def __raw_verbose(self, meta, torrent_data):
            return self.server._rpc.load.raw_verbose(meta, torrent_data)

        def __raw_start(self, meta, torrent_data):
            return self.server._rpc.load.raw_start(meta, torrent_data)

        def __raw_start_verbose(self, meta, torrent_data):
            return self.server_rpc.load.raw_start_verbose(meta, torrent_data)

        def __start(self, meta, torrent_file):
            return self.server_rpc.load.start(meta, torrent_file)

        def __start_verbose(self, meta, torrent_file):
            return self.server._rpc.load.start_verbose(meta, torrent_file)

    class __protocol:

        def __init__(self, server):
            self.__server = server
            self.choke_heuristics = self.__choke_heuristics(server)
            self.connection = self.__connection(server)
            self.encryption = self.__encryption(server)
            self.pex = self.__pex(server)

        class __pex:

            def __init__(self, server): self.__server = server
            def __call__(self): return bool(self.__server._rpc.protocol.pex())
            def set(self, value: int | bool) -> bool:
                return bool(self.__server._rpc.protocol.pex.set('', int(value)))

        class __encryption:

            def __init__(self, server): self.__server = server
            def set(self, value) -> int:
                return self.__server._rpc.protocol.encryption.set('', value)

        class __connection:

            def __init__(self, server):
                self.__server = server
                self.leech = self.__leech(server)
                self.seed = self.__seed(server)

            class __leech:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.protocol.connection.leech()
                def set(self, value):
                    return self.__server._rpc.protocol.\
                            connection.leech.set('', value)

            class __seed:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.protocol.connection.seed()
                def set(self, value):
                    return self.__server._rpc.protocol.\
                            connection.seed.set('', value)

        class __choke_heuristics:

            def __init__(self, server):
                self.__server = server
                self.down = self.__down(server)
                self.up = self.__up(server)

            class __down:

                def __init__(self, server):
                    self.__server = server
                    self.leech = self.__leech(server)
                    self.seed = self.__seed(server)

                class __leech:

                    def __init__(self, server): self.__server = server
                    def __call__(self):
                        return self.__server._rpc.protocol.\
                                choke_heuristics.down.leech()
                    def set(self, value): return self.__server._rpc.protocol.\
                            choke_heuristics.down.leech.set('', value)

                class __seed:

                    def __init__(self, server): self.__server = server
                    def __call__(self):
                        return self.__server._rpc.protocol.\
                                choke_heuristics.down.seed()
                    def set(self, value):
                        return self.__server._rpc.protocol.\
                                choke_heuristics.down.seed.set('', value)

            class __up:

                def __init__(self, server):
                    self.__server = server
                    self.leech = self.__leech(server)
                    self.seed = self.__seed(server)

                class __leech:

                    def __init__(self, server): self.__server = server
                    def __call__(self):
                        return self.__server._rpc.protocol.\
                                choke_heuristics.up.leech()
                    def set(self, value):
                        return self.__server._rpc.protocol.\
                                choke_heuristics.up.leech.set('', value)

                class __seed:

                    def __init__(self, server): self.__server = server
                    def __call__(self):
                        return self.__server._rpc.protocol.\
                                choke_heuristics.up.seed()
                    def set(self, value):
                        return self.__server._rpc.protocol.\
                                choke_heuristics.up.seed.set('', value)

    class __scheduler:

        def __init__(self, server):
            self.__server = server
            self.simple = self.__simple(server)
            self.max_active = self.__max_active(server)

        class __simple:

            def __init__(self, server): self.__server = server
            """ I don't know what these do or how to use them """
            def added(self, value):
                return self.__server._rpc.scheduler.simple.added(value)
            def removed(self, value):
                return self.__server._rpc.scheduler.simple.removed(value)
            def update(self, value):
                return self.__server._rpc.scheduler.simple.update(value)

        class __max_active:

            def __init__(self, server): self.__server = server
            def __call__(self): return self.__server._rpc.scheduler.max_active()
            def set(self, value):
                return self.__server._rpc.scheduler.max_active.set('', value)

    def schedule(self, name, start, interval, command):
        return self._rpc.schedule(name, start, interval, command)

    def schedule2(self, name, start, interval, command):
        return self._rpc.schedule2(name, start, interval, command)

    def schedule_remove(self, name):
        return self._rpc.schedule_remove(name)

    def schedule_remove2(self, name):
        return self._rpc.schedule_remove2(name)

    class __network:

        def __init__(self, server):
            self.__server = server
            self.bind_address = self.__bind_address(server)
            self.http = self.__http(server)
            self.listen = self.__listen(server)
            self.local_address = self.__local_address(server)
            self.max_open_files = self.__max_open_files(server)
            self.max_open_sockets = self.__max_open_sockets(server)
            self.port_open = self.__port_open(server)
            self.port_random = self.__port_random(server)
            self.proxy_address = self.__proxy_address(server)
            self.receive_buffer = self.__receive_buffer(server)
            self.send_buffer = self.__send_buffer(server)
            self.tos = self.__tos(server)
            self.xmlrpc = self.__xmlrpc(server)

        open_sockets = lambda self: self.__server._rpc.network.open_sockets()

        class __xmlrpc:

            def __init__(self, server):
                self.__server = server
                self.size_limit = self.__size_limit(server)
                self.dialect = self.__dialect(server)

            class __dialect:

                def __init__(self, server): self.__server = server
                def set(self, value):
                    return self.__server._rpc.network.\
                            xmlrpc.dialect.set('', value)

            class __size_limit:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.network.xmlrpc.size_limit()
                def set(self, value):
                    return self.__server._rpc.network.\
                            xmlrpc.size_limit.set('', value)

        class __tos:

            def __init__(self, server): self.__server = server
            def set(self, value):
                return self.__server._rpc.network.tos.set('', value)

        class __send_buffer:

            def __init__(self, server):
                self.__server = server
                self.size = self.__size(server)

            class __size:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.network.send_buffer.size()
                def set(self, size):
                    return self.__server._rpc.network.send_buffer.size('', size)

        class __scgi:

            def __init__(self, server):
                self.__server = server
                self.dont_route = self.__dont_route(server)

            def open_local(self):
                self.__server._rpc.network.scgi.open_local('', '')
            def open_port(self, port):
                self.__server._rpc.network.scgi.open_port(port)

            class __dont_route:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.network.scgi.dont_route()
                def set(self, value):
                    return self.__server._rpc.network.\
                            scgi.dont_route.set('', int(value))

        class __receive_buffer:

            def __init__(self, server):
                self.__server = server
                self.size = self.__size(server)

            class __size:

                def __init__(self,server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.network.receive_buffer.size()
                def set(self, size):
                    return self.__server._rpc.network.\
                            receive_buffer.size.set('', size)

        class __local_address:

            def __init__(self, server): self.__server = server
            def __call__(self):
                return self.__server._rpc.network.local_address()
            def set(self, ip):
                return self.__server._rpc.network.local_address.set('', ip)

        class __port_open:

            def __init__(self, server): self.__server = server
            def __call__(self):
                return self.__server._rpc.network.port_open()
            def set(self, port):
                return self.__server._rpc.network.port_open.set('', port)

        class __port_random:

            def __init__(self, server): self.__server = server
            def __call__(self): return self.__server._rpc.network.port_random()
            def set(self, range):
                return self.__server._rpc.network.port_random.set('', range)

        class __port_range:

            def __init__(self, server): self.__server = server
            def __call__(self): return self.__server._rpc.network.port_range()
            def set(self, port):
                return self.__server._rpc.network.port_range.set('', port)

        class __proxy_address:

            def __init__(self, server): self.__server = server
            def __call__(self):
                return self.__server._rpc.network.proxy_address()
            def set(self, port):
                return self.__server._rpc.network.proxy_address.set('', port)

        class __max_open_files:

            def __init__(self, server): self.__server = server
            def __call__(self):
                return self.__server._rpc.network.max_open_files()
            def set(self, num):
                return self.__server._rpc.network.max_open_files.set('', num)

        class __max_open_sockets:

            def __init__(self, server): self.__server = server
            def __call__(self):
                return self.__server._rpc.network.max_open_sockets()
            def set(self, num):
                return self.__server._rpc.network.max_open_sockets.set('', num)

        class __listen:

            def __init__(self, server):
                self.__server = server
                self.backlog = self.__backlog(server)

            def port(self): return self.__server._rpc.network.listen.port()

            class __backlog:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.network.listen.backlog()
                def set(self, value):
                    return self.__server._rpc.network.\
                            listen.backlog.set('', value)

        class __bind_address:

            def __init__(self, server): self.__server = server
            def __call__(self):
                return self.__server._rpc.network.bind_address()
            def set(self, ip):
                return self.__server._rpc.network.bind_address.set('', ip)

        class __http:

            def __init__(self, server):
                self.__server = server
                self.cacert = self.__cacert(server)
                self.capath = self.__capath(server)
                self.dns_cache_timeout = self.__dns_cache_timeout(server)
                self.max_open = self.__max_open(server)
                self.proxy_address = self.__proxy_address(server)
                self.ssl_verify_host = self.__ssl_verify_host(server)
                self.ssl_verify_peer = self.__ssl_verify_peer(server)

            def current_open(self):
                return self.__server._rpc.network.http.current_open()

            class __cacert:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.network.http.cacert()
                def set(self, value):
                    return self.__server._rpc.network.http.cacert.set('', value)

            class __capath:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.network.http.capath()
                def set(self, value):
                    return self.__server._rpc.network.http.capath.set('', value)

            class __dns_cache_timeout:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.network.http.dns_cache_timeout()
                def set(self, value):
                    return self.__server._rpc.network.\
                            http.dns_cache_timeout.set('', value)

            class __max_open:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.network.http.max_open()
                def set(self, value):
                    return self.__server._rpc.network.\
                            http.max_open.set('', value)

            class __proxy_address:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.network.http.proxy_address()
                def set(self, value):
                    return self.__server._rpc.network.\
                            http.proxy_address.set('', value)

            class __ssl_verify_host:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.network.http.ssl_verify_host()
                def set(self, value):
                    return self.__server._rpc.network.\
                            http.ssl_verify_host.set('', int(value))

            class __ssl_verify_peer:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.network.http.ssl_verify_peer()
                def set(self, value):
                    return self.__server._rpc.network.\
                            http.ssl_verify_peer.set('', int(value))

    class __strings:

        def __init__(self, server):
            self.__server = server
            self.choke_heuristics = self.__choke_heuristics(server)

        def encryption(self): return self.__server._rpc.strings.encryption()
        def ip_filter(self): return self.__server._rpc.strings.ip_filter()
        def ip_tos(self): return self.__server._rpc.strings.ip_tos()
        def log_group(self): return self.__server._rpc.strings.log_group()
        def tracker_mode(self): return self.__server._rpc.strings.tracker_mode()
        def connection_type(self):
            return self.__server._rpc.strings.connection_type()
        def tracker_event(self):
            return self.__server._rpc.strings.tracker_event()

        class __choke_heuristics:

            def __init__(self, server): self.__server = server
            def __call__(self):
                return self.__server._rpc.strings.choke_heuristics()
            def download(self):
                return self.__server._rpc.strings.choke_heuristics.download()
            def upload(self):
                return self.__server._rpc.strings.choke_heuristics.upload()

    class __throttle:

        def __init__(self, server):
            self.__server = server
            self.down = self.__down(server)
            self.up = self.__up(server)
            self.global_down = self.__global_down(server)
            self.global_up = self.__global_up(server)
            self.max_uploads = self.__max_uploads(server)
            self.max_downloads = self.__max_downloads(server)
            self.min_uploads = self.__min_uploads(server)
            self.min_downloads = self.__min_downloads(server)
            self.max_peers = self.__max_peers(server)
            self.min_peers = self.__min_peers(server)

        def ip(self, throttle_name, ip):
            """adds a specific peer to a set throttle arg1
            is throttle name and arg2 is ip address as string"""
            return self.__server._rpc.throttle.ip('', throttle_name, ip)

        def unchoked_downloads(self):
            return self.__server._rpc.throttle.unchoked_downloads()
        def unchoked_uploads(self):
            return self.__server._rpc.throttle.unchoked_uploads()

        def names(self):
            return list(
                    set(
                        self.__server.view().each(lambda x: x.throttle_name())
                        )
                    )

        class __down:

            def __init__(self, server): self.__server = server
            def __call__(self, throttle_name, rate):
                """arg1 is throttle name and arg2 is the rate"""
                return self.__server._rpc.\
                        throttle.down('', throttle_name, rate)

            def max(self, throttle_name):
                return SizeBytes(self.__server._rpc.throttle.down.max('',
                                                          throttle_name))

            def rate(self, throttle_name):
                return SizeBytes(self.__server._rpc.throttle.down.rate('',
                                                          throttle_name))

        class __up:

            def __init__(self, server): self.__server = server
            def __call__(self, throttle_name, rate):
                """arg1 is throttle name and arg2 is the rate"""
                return self.__server._rpc.throttle.up('', throttle_name, rate)

            def max(self, throttle_name):
                return SizeBytes(self.__server._rpc.throttle.up.max('',
                                                          throttle_name))

            def rate(self, throttle_name):
                return SizeBytes(self.__server._rpc.throttle.up.rate('',
                                                          throttle_name))

        class __global_down:

            def __init__(self, server):
                self.__server = server
                self.max_rate = self.__max_rate(server)

            def total(self):
                return SizeBytes(
                    self.__server._rpc.throttle.global_down.total()
                    )
            def rate(self):
                return SizeBytes(
                    self.__server._rpc.throttle.global_down.rate()
                    )

            class __max_rate:
                
                def __init__(self, server): self.__server = server
                def __call__(self):
                    return SizeBytes(
                            self.__server._rpc.throttle.global_down.max_rate()
                            )
                def set(self, rate):
                    return self.__server._rpc.throttle.\
                            global_down.max_rate.set(rate)
                def set_kb(self, rate):
                    return self.__server._rpc.throttle.\
                            global_down.max_rate.set_kb(rate)

        class __global_up:

            def __init__(self, server):
                self.__server = server
                self.max_rate = self.__max_rate(server)

            def total(self):
                return SizeBytes(self.__server._rpc.throttle.global_up.total())
            def rate(self):
                return SizeBytes(self.__server._rpc.throttle.global_up.rate())

            class __max_rate:
                
                def __init__(self, server): self.__server = server
                def __call__(self):
                    return SizeBytes(
                            self.__server._rpc.throttle.global_up.max_rate()
                            )
                def set_kb(self, rate):
                    return self.__server._rpc.throttle.\
                            global_up.max_rate.set_kb(rate)
                def set(self, rate):
                    return getattr(self.__server._rpc,
                                   'throttle.global_up.max_rate.set')('', rate)

        class __max_uploads:

            def __init__(self, server):
                self.__server = server
                self.globl = self.__globl(server)
                self.div = self.__div(server)
            
            def __call__(self): return self.__server._rpc.throttle.max_uploads()

            class __globl:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return getattr(self.__server._rpc,
                                   'throttle.max_uploads.global')()
                def set(self, rate):
                    return getattr(self.__server._rpc,
                                   'throttle.max_uploads.global.set')('', rate)

            class __div:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.throttle.max_uploads.div()
                def set(self, rate):
                    return self.__server._rpc.throttle.\
                            max_uploads.div.set('', rate)

        class __max_downloads:

            def __init__(self, server):
                self.__server = server
                self.globl = self.__globl(server)
                self.div = self.__div(server)
            
            def __call__(self):
                return self.__server._rpc.throttle.max_downloads()

            class __globl:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return getattr(self.__server._rpc,
                                   'throttle.max_downloads.global')()
                def set(self, rate):
                    return getattr(self.__server._rpc,
                                 'throttle.max_downloads.global.set')('', rate)

            class __div:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.throttle.max_downloads.div()
                def set(self, rate):
                    return self.__server._rpc.throttle.\
                            max_downloads.div.set('', rate)

        class __min_uploads:

            def __init__(self, server): self.__server = server
            def __call__(self):
                return self.__server._rpc.throttle.min_uploads()
            def set(self, num):
                return self.__server._rpc.throttle.min_uploads.set('', num)

        class __min_downloads:

            def __init__(self, server): self.__server = server
            def __call__(self):
                return self.__server._rpc.throttle.max_uploads()
            def set(self, num):
                return self.__server._rpc.throttle.max_uploads.set('', num)

        class __max_peers:

            def __init__(self, server):
                self.__server = server
                self.normal = self.__normal(server)
                self.seed = self.__seed(server)

            class __normal:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.throttle.max_peers.normal()
                def set(self, num):
                    return self.__server._rpc.throttle.\
                            max_peers.normal.set('', num)

            class __seed:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.throttle.max_peers.seed()
                def set(self, num):
                    return self.__server._rpc.throttle.\
                            max_peers.seed.set('', num)

        class __min_peers:

            def __init__(self, server):
                self.__server = server
                self.normal = self.__normal(server)
                self.seed = self.__seed(server)

            class __normal:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.throttle.min_peers.normal()
                def set(self, num):
                    return self.__server._rpc.throttle.\
                            min_peers.normal.set('', num)

            class __seed:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.throttle.min_peers.seed()
                def set(self, num):
                    return self.__server._rpc.throttle.\
                            min_peers.seed.set('', num)

    class __choke_group:

        def __init__(self, server):
            self.__server = server
            self.down = self.__down(server)
            self.up = self.__up(server)
            self.general = self.__general(server)
            self.tracker = self.__tracker(server)

        list = lambda self: self.__server._rpc.choke_group.list()
        size = lambda self: self.__server._rpc.choke_group.size()
        insert = lambda self, group: self.__server._rpc.\
                choke_group.insert('', group)
        index_of = lambda self, group: self.__server._rpc.\
                choke_group.index_of('', group)

        class __general:

            def __init__(self, server): self.__server = server
            def size(self, group):
                return self.__server._rpc.choke_group.general.size('', group)

        class __tracker:

            def __init__(self, server):
                self.__server = server
                self.mode = self.__mode(server)

            class __mode:

                def __init__(self, server): self.__server = server
                def __call__(self, group):
                    return self.__server._rpc.choke_group.\
                            tracker.mode('', group)
                def set(self, group, value):
                    return self.__server._rpc.choke_group.\
                            tracker.mode.set('', group, value)

        class __down:

            def __init__(self, server):
                self.__server = server
                self.heuristics = self.__heuristics(server)
                self.max = self.__max(server)

            def queued(self, group):
                return self.__server._rpc.choke_group.down.queued('', group)

            def rate(self, group):
                return self.__server._rpc.choke_group.down.rate('', group)

            def total(self, group):
                return self.__server._rpc.choke_group.down.total('', group)

            def unchoked(self, group):
                return self.__server._rpc.choke_group.down.unchoked('', group)

            class __heuristics:

                def __init__(self, server): self.__server = server
                def __call__(self, group):
                    return self.__server._rpc.choke_group.\
                            down.heuristics('', group)
                def set(self, group, value): 
                    return self.__server._rpc.choke_group.\
                            down.heuristics.set('', group, value)

            class __max:

                def __init__(self, server): self.__server = server
                def __call__(self, group):
                    return self.__server._rpc.choke_group.down.max('', group)
                def set(self, group, value):
                    return self.__server._rpc.choke_group.\
                            down.max.set('', group, value)
                def unlimited(self, group): 
                    return self.__server._rpc.choke_group.\
                            down.max.unlimited('', group)

        class __up:

            def __init__(self, server):
                self.__server = server
                self.heuristics = self.__heuristics(server)
                self.max = self.__max(server)

            def queued(self, group):
                return self.__server._rpc.choke_group.up.queued('', group)

            def rate(self, group):
                return self.__server._rpc.choke_group.up.rate('', group)

            def total(self, group):
                return self.__server._rpc.choke_group.up.total('', group)

            def unchoked(self, group):
                return self.__server._rpc.choke_group.up.unchoked('', group)

            class __heuristics:

                def __init__(self, server): self.__server = server
                def __call__(self, group):
                    return self.__server._rpc.choke_group.\
                            up.heuristics('', group)
                def set(self, group, value): 
                    return self.__server._rpc.choke_group.\
                            up.heuristics.set('', group, value)

            class __max:

                def __init__(self, server): self.__server = server
                def __call__(self, group):
                    return self.__server._rpc.choke_group.up.max('', group)
                def set(self, group, value):
                    return self.__server._rpc.choke_group.\
                            up.max.set('', group, value)
                def unlimited(self, group): 
                    return self.__server._rpc.choke_group.\
                            up.max.unlimited('', group)


    class __pieces:

        def __init__(self, server):
            self.__server = server
            self.hash = self.__hash(server)
            self.memory = self.__memory(server)
            self.preload = self.__preload(server)
            self.stats = self.__stats(server)
            self.stats_not_preloaded = self.__stats_not_preloaded(server)
            self.stats_preloaded = self.__stats_preloaded(server)
            self.sync = self.__sync(server)

        class __hash:

            def __init__(self, server):
                self.__server = server
                self.on_completion = self.__on_completion(server)

            def queue_size(self):
                return self.__server._rpc.pieces.hash.queue_size()

            class __on_completion:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.pieces.hash.on_completion()
                def set(self, value):
                    return self.__server._rpc.pieces.hash.\
                            on_completion.set(value)

        class __memory:

            def __init__(self, server):
                self.__server = server
                self.max = self.__max(server)

            def sync_queue(self):
                return self.__server._rpc.pieces.memory.sync_queue()
            def current(self):
                return self.__server._rpc.pieces.memory.current()
            def block_count(self):
                return self.__server._rpc.pieces.memory.block_count()

            class __max:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.pieces.memory.max()
                def set(self, value):
                    return self.__server._rpc.pieces.memory.max.set(value)

        class __preload:

            def __init__(self, server):
                self.__server = server
                self.min_rate = self.__min_rate(server)
                self.min_size = self.__min_size(server)
                self.type = self.__type(server)

            class __min_rate:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.pieces.preload.min_rate()
                def set(self, value):
                    return self.__server._rpc.pieces.preload.min_rate.set(value)

            class __min_size:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.pieces.preload.min_size()
                def set(self, value):
                    return self.__server._rpc.pieces.preload.min_size.set(value)

            class __type:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.pieces.preload.type()
                def set(self, value):
                    return self.__server._rpc.pieces.preload.type.set(value)

        class __stats:

            def __init__(self, server): self.__server = server
            def total_size(self):
                return SizeBytes(self.__server._rpc.pieces.stats.total_size())

        class __stats_preloaded:

            def __init__(self, server): self.__server = server
            def __call__(self):
                return self.__server._rpc.pieces.stats_preloaded()

        class __stats_not_preloaded:

            def __init__(self, server): self.__server = server
            def __call__(self):
                return self.__server._rpc.pieces.stats_not_preloaded()

        class __sync:

            def __init__(self, server):
                self.__server = server
                self.always_safe = self.__always_safe(server)
                self.timeout = self.__timeout(server)
                self.timeout_safe = self.__timeout_safe(server)

            def queue_size(self):
                return self.__server._rpc.pieces.sync.queue_size()
            def safe_free_diskspace(self):
                return SizeBytes(self.__server._rpc.pieces.\
                        sync.safe_free_diskspace())

            class __always_safe:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.pieces.sync.always_safe()
                def set(self, value):
                    return self.__server._rpc.pieces.sync.always_safe.set(value)

            class __timeout:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.pieces.sync.timeout()
                def set(self, value):
                    return self.__server._rpc.pieces.sync.timeout.set(value)

            class __timeout_safe:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.pieces.sync.timeout_safe()
                def set(self, value):
                    return self.__server._rpc.pieces.sync.\
                            timeout_safe.set(value)

    class __group:

        def __init__(self, server):
            self.__server = server
            self.seeding = self.__seeding(server)

        def insert(self, comm):
            return self.__server._rpc.group.insert(comm)
        def insert(self, view):
            return self.__server._rpc.group.insert_persistent_view(view)

        class __seeding:
            
            def __init__(self, server):
                self.__server = server
                self.view = self.__view(server)
                self.ratio = self.__ratio(server)

            class __view:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.group.seeding.view()
                def set(self, view):
                    return self.__server._rpc.group.seeding.view.set(value)

            class __ratio:

                def __init__(self, server):
                    self.__server = server
                    self.max = self.__max(server)
                    self.min = self.__min(server)
                    self.upload = self.__upload(server)

                def command(self, com):
                    return self.__server._rpc.group.seeding.ratio.command(com)
                def disable(self):
                    return self.__server._rpc.group.seeding.ratio.disable()
                def enable(self):
                    return self.__server._rpc.group.seeding.ratio.enable()

                class __max:
                    
                    def __init__(self, server): self.__server = server
                    def __call__(self):
                        return self.__server._rpc.group.seeding.ratio.max()
                    def set(self, rat):
                        return self.__server._rpc.group.\
                                seeding.ratio.max.set(rat)

                class __min:
                    
                    def __init__(self, server): self.__server = server
                    def __call__(self):
                        return self.__server._rpc.group.seeding.ratio.min()
                    def set(self, rat):
                        return self.__server._rpc.group.\
                                seeding.ratio.min.set(rat)

                class __upload:
                    
                    def __init__(self, server): self.__server = server
                    def __call__(self):
                        return self.__server._rpc.group.seeding.ratio.upload()
                    def set(self, rat):
                        return self.__server._rpc.group.\
                                seeding.ratio.upload.set(rat)

    class __session:

        def __init__(self, server):
            self.__server = server
            self.name = self.__name(server)
            self.on_completion = self.__on_completion(server)
            self.path = self.__path(server)
            self.use_lock = self.__use_lock(server)
            
        def save(self): return self.__server._rpc.session.save()
        def __call__(self, value): return self.__server._rpc.session(value)

        class __name:

            def __init__(self, server): self.__server = server
            def __call__(self): return self.__server._rpc.session.name()
            def set(self, name):
                return self.__server._rpc.session.name.set(name)

        class __on_completion:

            def __init__(self, server): self.__server = server
            def __call__(self):
                return self.__server._rpc.session.on_completion()
            def set(self, value):
                return self.__server._rpc.session.on_completion.set(int(value))

        class __path:

            def __init__(self, server): self.__server = server
            def __call__(self): return self.__server._rpc.session.path()
            def set(self, value):
                return self.__server._rpc.session.path.set(value)

        class __use_lock:

            def __init__(self, server): self.__server = server
            def __call__(self):
                return bool(self.__server._rpc.session.use_lock())
            def set(self, value):
                return self.__server._rpc.session.use_lock.set(int(value))

    class __keys:

        def __init__(self, server):
            self.__server = server
            self.layout = self.__layout(server)

        class __layout:

            def __init__(self, server): self.__server = server
            def __call__(self): return self.__server._rpc.keys.layout()
            def set(self, layout):
                return self.__server._rpc.keys.layout.set('', layout)

    class __elapsed:

        def __init__(self, server): self.__server = server
        def greater(self, v1, v2):
            return self.__server._rpc.elapsed.greater('', v1, v2)
        def less(self, v1, v2):
            return self.__server._rpc.elapsed.less('', v1, v2)

    class __encoding:

        def __init__(self, server): self.__server = server
        def add(self, value): return self.__server._rpc.encoding.add('', value)

    class __ratio:

        def __init__(self, server):

            self.__server = server
            self.upload = self.__upload(server)
            self.min = self.__min(server)
            self.max = self.__max(server)

        enable = lambda self: self.__server._rpc.ratio.enable()
        disable = lambda self: self.__server._rpc.ratio.disable()

        class __upload:

            def __init__(self, server): self.__server = server
            def __call__(self): return self.__server._rpc.ratio.upload()
            def set(self, value):
                return self.__server._rpc.ratio.upload.set(value)

        class __min:

            def __init__(self, server): self.__server = server
            def __call__(self): return self.__server._rpc.ratio.min()
            def set(self, value): return self.__server._rpc.ratio.min.set(value)

        class __max:

            def __init__(self, server): self.__server = server
            def __call__(self): return self.__server._rpc.ratio.max()
            def set(self, value): return self.__server._rpc.ratio.max.set(value)


    class __convert:
 
        def __init__(self, server): self.__server = server
 
        def date(self, value): return self.__server._rpc.convert.date('', value)
        def gm_date(self, value):
            return self.__server._rpc.convert.gm_date('', value)
        def gm_time(self, value):
            return self.__server._rpc.convert.gm_time('', value)
        def elapse_time(self, value):
            return self.__server._rpc.convert.elapse_time('', value)
        def throttle(self, value):
            return self.__server._rpc.convert.throttle('', value)
        def time(self, value):
            return self.__server._rpc.convert.time('', value)
        def xb(self, value): return self.__server._rpc.convert.xb('', value)
        def mb(self, value): return self.__server._rpc.convert.mb('', value)
        def kb(self, value): return self.__server._rpc.convert.kb('', value)

    class __directory:

        def __init__(self, server):
            self.__server = server
            self.default = self.__default(server)
            self.watch = self.__watch(server)
        
        class __default:
            def __init__(self, server): self.__server = server
            def __call__(self): return self.__server._rpc.directory.default()
            def set(self, directory):
                return self.__server._rpc.directory.default.set(directory)

        class __watch:
            def __init__(self, server): self.__server = server
            def added(self, watch_dir, load):
                return self.__server._rpc.directory.\
                        watch.added('', watch_dir, load)

    class __dht:

        def __init__(self, server):
            self.__server = server
            self.port = self.__port(server)

        def __call__(self, value=None):
            """argument should be \"off\" or \"on\""""
            if value is not None:
                return self.__server._rpc.dht(value) 

            state = self.statistics()['dht']
            next_state = "off" if state == "on" else "on"
            return self.__server._rpc.dht(next_state)

        def add_node(self, value):
            """argument should be ip address"""
            return self.__server._rpc.dht.add_node('', value)

        def dht_port(self, value):
            """another method to set the dht port"""
            return self.__server._rpc.dht_port(value)

        class __port:

            def __init__(self, server): self.__server = server
            def __call__(self): return self.__server._rpc.dht.port()
            def set(self, value):
                return self.__server._rpc.dht.port.set('', value)

        def statistics(self): return self.__server._rpc.dht.statistics()

    class __system:

        def __init__(self, server):
            self.__server = server
            self.cwd = self.__cwd(server)
            self.files = self.__files(server)
            self.file = self.__file(server)
            self.file_status_cache = self.__file_status_cache(server)
            self.daemon = self.__daemon(server)

        time = lambda self: self.__server._rpc.system.time()
        time_seconds = lambda self: self.__server._rpc.system.time_seconds()
        time_usec = lambda self: self.__server._rpc.system.time_usec()
        hostame = lambda self: self.__server._rpc.system.hostname()
        client_version = lambda self: self.__server._rpc.system.client_version()
        library_version = lambda self: self.__server._rpc.\
                system.library_version()
        env = lambda self: self.__server._rpc.system.env()
        pid = lambda self: self.__server._rpc.system.pid()
        listMethods = lambda self: self.__server._rpc.system.listMethods()
        multicall = lambda self, *args: self.__server.\
                _rpc.system.multicall(args)
        env = lambda self: self.__server._rpc.system.env()
        methodHelp = lambda self, method: self.__server.\
                _rpc.system.methodHelp(method)
        methodExists = lambda self, method: self.__server.\
                _rpc.system.methodExist(method)
        methodSignature = lambda self, method: self.__server._rpc.\
                system.methodSignature(method)
        capabilities = lambda self: self.__server._rpc.system.capabilities()
        getCapabilities = lambda self: self.__server._rpc.\
                system.getCapabilities()

        class __cwd:

            def __init__(self, server): self.__server = server
            def __call__(self): return self.__server._rpc.system.cwd()
            def set(self, dir):
                return self.__server._rpc.system.cwd.set('', dir)

        class __files:

            def __init__(self, server): self.__server = server

            failed_counter = lambda self: self.__server.\
                    _rpc.system.files.failed_counter()
            opened_counter = lambda self: self.__server.\
                    _rpc.system.files.opened_counter()
            closed_counter = lambda self: self.__server.\
                    _rpc.system.files.closed_counter()

        class __file:

            def __init__(self, server):
                self.__server = server
                self.allocate = self.__allocate(server)
                self.max_size = self.__max_size(server)
                self.split_size = self.__split_size(server)
                self.split_suffix = self.__split_suffix(server)

            class __allocate:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.system.file.allocate()
                def set(self, value):
                    return self.__server._rpc.system.\
                            file.allocate.set('', value)

            class __max_size:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.system.file.max_size()
                def set(self, value):
                    return self.__server._rpc.system.\
                            file.max_size.set('', value)

            class __split_size:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.system.file.split_size()
                def set(self, value):
                    return self.__server._rpc.system.\
                            file.split_size.set('', value)

            class __split_suffix:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.system.file.split_suffix()
                def set(self, value):
                    return self.__server._rpc.system.\
                            file.split_suffix.set('', value)

        class __file_status_cache:

            def __init__(self, server): self.__server = server
            def size(self):
                return self.__server._rpc.system.file_status_cache.size()
            def prune(self):
                return self.__server._rpc.system.file_status_cache.prune()

        class __daemon:

            def __init__(self, server): self.__server = server
            def __call__(self):
                return bool(self.__server._rpc.system.daemon())
            def set(self, value):
                return self.__server._rpc.system.daemon.set('', int(value))

        class __umask:

            def __init__(self, server): self.__server = server
            def set(self, value): self.__server._rpc.system.umask.set('', value)


    class __view:

        def __init__(self, server):
            self.__server = server

        def __call__(self, view='main'):
    
            # Everything before the return is not necessary for
            # the function but caching the names now with one
            # multicall saves a lot of rpc calls later.
            hashes = self.__server.hash_list(view)
    
##            chunk_length = 5000
##            results = []
##            # rtorrent doesn't like to do these all at once if
##            # you have several 1000 so we split it up into chunks
##            chunks = chunk(hashes, chunk_length)
##            for c in chunks:
##                mc = self.__server.multicall
##                for hash in c:
##                    mc.d.name(hash)
##    
##                names = list(mc())
##                assert len(names) == len(chunks),\
##                    "response from server has incorrect length"
##                results += names
    
            return TorrentGroup(
                *[Torrent(self.__server, x) for x in hashes]
            )

        def size(self, view=None):

            if view is None: view = self.__server.ui.current_view()
            return self.__server._rpc.view.size('', view)

        def size_not_visible(self, view=None):

            if view is None: view = self.__server.ui.current_view()
            return self.__server._rpc.view.size_not_visible('', view)

        def add(self, view_name): return self.__server._rpc.view.add(view_name)

    class __views:

        def __init__(self, server):
            for i in server._rpc.view.list():
                self.__setattr__(i, i)
            self.server = server

        def __repr__(self):
            return repr(
                list(
                    set(self.__dict__.keys()).difference(['server'])
                ))

        def __iter__(self):
            return iter(
                set(self.__dict__.keys()).difference(['server'])
            )

    class __ui:

        def __init__(self, server):
            self.__server = server
            self.current_view = self.__current_view(server)
            self.torrent_list = self.__torrent_list(server)
            self.throttle = self.__throttle(server)

        class __current_view:

            def __init__(self, server):
                self.__server = server

            def set(self, view):
                self.__server.update_views()
                return self.__server._rpc.ui.current_view.set('', view)

            def __call__(self):
                return self.__server._rpc.ui.current_view()

        class __torrent_list:

            def __init__(self, server):
                self.__server = server
                self.layout = self.__layout(server)

            class __layout:

                def __init__(self, server): self.__server = server
                def __call__(self):
                    return self.__server._rpc.ui.torrent_list.layout()
                def set(self, layout):
                    return self.__server._rpc.\
                            ui.torrent_list.layout.set('', layout)

        class __throttle:

            def __init__(self, server):
                self.__server = server
                self.globl = self.__globl(server)

            class __globl:

                def __init__(self, server):
                    self.__server = server
                    self.step = self.__step(server)

                class __step:

                    def __init__(self, server):
                        self.__server = server
                        self.large = self.__large(server)
                        self.medium = self.__medium(server)
                        self.small = self.__small(server)

                    class __large:

                        def __init__(self, server): self.__server = server

                        # have to call it like this because python
                        # doesn't let you use global for anything else
                        def __call__(self):
                            return getattr(self.__server._rpc,
                                           "ui.throttle.global.step.large")()

                        def set(self, step):
                            return getattr(self.__server._rpc,
                                           "ui.throttle.global.step.large.set"
                                           )('', step)

                    class __medium:

                        def __init__(self, server): self.__server = server

                        def __call__(self):
                            return getattr(self.__server._rpc,
                                           "ui.throttle.global.step.medium")()

                        def set(self, step):
                            return getattr(self.__server._rpc,
                                           "ui.throttle.global.step.medium.set"
                                           )('', step)

                    class __small:

                        def __init__(self, server): self.__server = server

                        def __call__(self):
                            return getattr(self.__server._rpc,
                                           "ui.throttle.global.step.small")()

                        def set(self, step):
                            return getattr(self.__server._rpc,
                                           "ui.throttle.global.step.small.set"
                                           )('', step)

    def torrent_list_layout(self, value=None):
        if value is not None: return self._rpc.torrent_list_layout(value)
        state = self.ui.torrent_list.layout()
        next_state = "full" if state == "compact" else "compact"
        return self.ui.torrent_list.layout.set(next_state)

    def connection_leech(self, value): return self._rpc.connection_leech(value)
    def connection_seed(self, value): return self._rpc.connection_seed(value)

    def update_views(self):
        self.views = self.__views(self)

    def hash_list(self, view="main"):
        return [x[0] for x in self._rpc.d.multicall2('', view, 'd.hash=')]

    def get_name(self, hash):
        return self._rpc.d.name(hash)

    def matching_re(self, pattern, caseInsensitive=True, view="main"):
        '''pattern is a regex'''
        #matches = self.view(view)
        #for torrent in matches[:]:
        #    if not re.search(pattern, torrent.name, [0, 2][caseInsensitive]):
        #        matches.remove(torrent)
        #return matches
        matches = TorrentGroup()
        torrents = self._rpc.d.multicall2('',view, 'd.name=', 'd.hash=')
        for torrent in torrents:
            if re.search(pattern, torrent[0], [0, 2][caseInsensitive]):
                matches.append(Torrent(self, torrent[1]))
        return matches

    def matching_names(self, pattern, caseInsensitive=True, view="main"):

        matches = TorrentGroup()
        torrents = self._rpc.d.multicall2('',view, 'd.name=', 'd.hash=')
        for torrent in torrents:
            if re.search(pattern, torrent[0], [0, 2][caseInsensitive]):
                matches.append(Torrent(self, torrent[1]))
        return matches

    def get_torrent_by_hash(self, hash):
        return Torrent(self, hash)

    def matching_trackers(self, pattern, caseInsensitive=True,
                              view="main"):

        matches = TorrentGroup()
        torrents = self._rpc.d.multicall2('',view, 'd.name=', 'd.hash=',
                                          't.multicall=,t.url=')
        for torrent in torrents:
            for url in torrent[2][0]:
                if re.search(pattern, url, [0,2][caseInsensitive]):
                    matches.append(Torrent(self, torrent[1]))

        return matches


    def matching_throttle_name(self, pattern, caseInsensitive=True,
                                   view="main", exact=False):

        matches = TorrentGroup()
        torrents = self._rpc.d.multicall2('',view, 'd.name=', 'd.hash=',
                                          'd.throttle_name=')
        for torrent in torrents:
            if re.search(pattern, torrent[2], [0,2][caseInsensitive]):
                matches.append(Torrent(self, torrent[1]))

        return matches

    def matching_message(self, pattern, caseInsensitive=True,
                             view="main", exact=False):
        matches = TorrentGroup()
        torrents = self._rpc.d.multicall2('',view, 'd.name=', 'd.hash=',
                                          'd.message=')
        for torrent in torrents:
            if re.search(pattern, torrent[2], [0,2][caseInsensitive]):
                matches.append(Torrent(self, torrent[1]))

        return matches


    def unregistered(self, search='', view="main"):

        return TorrentGroup(*[ Torrent(self, y[0])
                              for y in self._rpc.d.multicall2('',
                                                              'main',
                                                              'd.hash=',
                                                              'd.message=')
                              if 'Unregistered' in y[1]])

    def __repr__(self):
        return 'rTorrent server: <{0}>'.format(self.server)
