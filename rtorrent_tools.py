#!/usr/bin/env python

from types import FunctionType
import pprint
from collections.abc import Sequence
from collections import namedtuple
import re
import datetime
import sys
import time

if sys.version_info < (3, 0):
    import xmlrpclib
else:
    import xmlrpc.client as xmlrpclib


class Server:

    def __init__(self, server):

        self.server = server
        self._rpc = xmlrpclib.Server(server)
        #self._rpc.network.xmlrpc.size_limit.set('', 2**24)
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
        self.update_views()
        self._nameCache = {}
        self._trackerCache = {}

    def to_kb(self, value): return self._rpc.to_kb(value)
    def to_mb(self, value): return self._rpc.to_mb(value)
    def to_xb(self, value): return self._rpc.to_xb(value)
    def download_list(self): return self._rpc.download_list()
    def download_rate(self, rate): return self._rpc.download_rate(rate)
    def upload_rate(self, rate): return self._rpc.upload_rate(rate)
    def close_low_diskspace(self, space): return self._rpc.close_low_diskspace('', space)
    def close_untied(self, space): return self._rpc.close_untied()
    def encoding_list(self): return self._rpc.encoding_list('')
    def max_memory_usage(self, value): return self._rpc.max_memory_usage(value)
    def add_peer(self, arg1, arg2): return self._rpc.add_peer(arg1, arg2)
    def check_hash(self, value): return self._rpc.check_hash(int(value))
    def remove_untied(self): return self._rpc.remove_untied()
    def scgi_local(self, value): return self._rpc.scgi_local('', int(value))
    def scgi_port(self, port): return self._rpc.scgi_local(int(port))
    def proxy_address(self, address): return self._rpc.proxy_address('', address)
    def ip(self, value): return self._rpc.ip(value)
    def fimport(self, file): return getattr(self._rpc, 'import')('', file)
    def try_import(self, file): return self._rpc.try_import('', file)
    def print(self, value): return self._rpc.print('', value)
    def port_random(self, port): return self._rpc.port_random('', port)

    class __protocol:

        def __init__(self, server):
            self.__server = server
            self.choke_heuristics = self.__choke_heuristics(server)
            self.connection = self.__connection(server)
            self.encryption = self.__encryption(server)
            self.pex = self.__pex(server)

        class __pex:

            def __init__(self, server): self.__server = server
            def __call__(self): return self.__server._rpc.protocol.pex()
            def set(self, value): return self.__server._rpc.protocol.pex.set('', value)

        class __encryption:

            def __init__(self, server): self.__server = server
            def set(self, value): return self.__server._rpc.protocol.encryption.set('', value)

        class __connection:

            def __init__(self, server):
                self.__server = server
                self.leech = self.__leech(server)
                self.seed = self.__seed(server)

            class __leech:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.protocol.connection.leech()
                def set(self, value): return self.__server._rpc.protocol.connection.leech.set('', value)

            class __seed:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.protocol.connection.seed()
                def set(self, value): return self.__server._rpc.protocol.connection.seed.set('', value)

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
                    def __call__(self): return self.__server._rpc.protocol.choke_heuristics.down.leech()
                    def set(self, value): return self.__server._rpc.protocol.choke_heuristics.down.leech.set('', value)

                class __seed:

                    def __init__(self, server): self.__server = server
                    def __call__(self): return self.__server._rpc.protocol.choke_heuristics.down.seed()
                    def set(self, value): return self.__server._rpc.protocol.choke_heuristics.down.seed.set('', value)

            class __up:

                def __init__(self, server):
                    self.__server = server
                    self.leech = self.__leech(server)
                    self.seed = self.__seed(server)

                class __leech:

                    def __init__(self, server): self.__server = server
                    def __call__(self): return self.__server._rpc.protocol.choke_heuristics.up.leech()
                    def set(self, value): return self.__server._rpc.protocol.choke_heuristics.up.leech.set('', value)

                class __seed:

                    def __init__(self, server): self.__server = server
                    def __call__(self): return self.__server._rpc.protocol.choke_heuristics.up.seed()
                    def set(self, value): return self.__server._rpc.protocol.choke_heuristics.up.seed.set('', value)

    class __scheduler:

        def __init__(self, server):
            self.__server = server
            self.simple = self.__simple(server)
            self.max_active = self.__max_active(server)

        class __simple:

            def __init__(self, server): self.__server = server
            """ I don't know what these do or how to use them """
            def added(self, value): return self.__server._rpc.scheduler.simple.added(value)
            def removed(self, value): return self.__server._rpc.scheduler.simple.removed(value)
            def update(self, value): return self.__server._rpc.scheduler.simple.update(value)

        class __max_active:

            def __init__(self, server): self.__server = server
            def __call__(self): return self.__server._rpc.scheduler.max_active()
            def set(self, value): return self.__server._rpc.scheduler.max_active.set('', value)

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
                def set(self, value): return self.__server._rpc.network.xmlrpc.dialect.set('', value)

            class __size_limit:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.network.xmlrpc.size_limit()
                def set(self, value): return self.__server._rpc.network.xmlrpc.size_limit.set('', value)

        class __tos:

            def __init__(self, server): self.__server = server
            def set(self, value): return self.__server._rpc.network.tos.set('', value)

        class __send_buffer:

            def __init__(self, server):
                self.__server = server
                self.size = self.__size(server)

            class __size:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.network.send_buffer.size()
                def set(self, size): return self.__server._rpc.network.send_buffer.size('', size)

        class __scgi:

            def __init__(self, server):
                self.__server = server
                self.dont_route = self.__dont_route(server)

            def open_local(self): self.__server._rpc.network.scgi.open_local('', '')
            def open_port(self, port): self.__server._rpc.network.scgi.open_port(port)

            class __dont_route:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.network.scgi.dont_route()
                def set(self, value): return self.__server._rpc.network.scgi.dont_route.set('', int(value))

        class __receive_buffer:

            def __init__(self, server):
                self.__server = server
                self.size = self.__size(server)

            class __size:

                def __init__(self,server): self.__server = server
                def __call__(self): return self.__server._rpc.network.receive_buffer.size()
                def set(self, size): return self.__server._rpc.network.receive_buffer.size.set('', size)

        class __local_address:

            def __init__(self, server): self.__server = server
            def __call__(self): return self.__server._rpc.network.local_address()
            def set(self, ip): return self.__server._rpc.network.local_address.set('', ip)

        class __port_open:

            def __init__(self, server): self.__server = server
            def __call__(self): return self.__server._rpc.network.port_open()
            def set(self, port): return self.__server._rpc.network.port_open.set('', port)

        class __port_random:

            def __init__(self, server): self.__server = server
            def __call__(self): return self.__server._rpc.network.port_random()
            def set(self, range): return self.__server._rpc.network.port_random.set('', range)

        class __port_range:

            def __init__(self, server): self.__server = server
            def __call__(self): return self.__server._rpc.network.port_range()
            def set(self, port): return self.__server._rpc.network.port_range.set('', port)

        class __proxy_address:

            def __init__(self, server): self.__server = server
            def __call__(self): return self.__server._rpc.network.proxy_address()
            def set(self, port): return self.__server._rpc.network.proxy_address.set('', port)

        class __max_open_files:

            def __init__(self, server): self.__server = server
            def __call__(self): return self.__server._rpc.network.max_open_files()
            def set(self, num): return self.__server._rpc.network.max_open_files.set('', num)

        class __max_open_sockets:

            def __init__(self, server): self.__server = server
            def __call__(self): return self.__server._rpc.network.max_open_sockets()
            def set(self, num): return self.__server._rpc.network.max_open_sockets.set('', num)

        class __listen:

            def __init__(self, server):
                self.__server = server
                self.backlog = self.__backlog(server)

            def port(self): return self.__server._rpc.network.listen.port()

            class __backlog:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.network.listen.backlog()
                def set(self, value): return self.__server._rpc.network.listen.backlog.set('', value)

        class __bind_address:

            def __init__(self, server): self.__server = server
            def __call__(self): return self.__server._rpc.network.bind_address()
            def set(self, ip): return self.__server._rpc.network.bind_address.set('', ip)

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

            def current_open(self): return self.__server._rpc.network.http.current_open()

            class __cacert:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.network.http.cacert()
                def set(self, value): return self.__server._rpc.network.http.cacert.set('', value)

            class __capath:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.network.http.capath()
                def set(self, value): return self.__server._rpc.network.http.capath.set('', value)

            class __dns_cache_timeout:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.network.http.dns_cache_timeout()
                def set(self, value): return self.__server._rpc.network.http.dns_cache_timeout.set('', value)

            class __max_open:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.network.http.max_open()
                def set(self, value): return self.__server._rpc.network.http.max_open.set('', value)

            class __proxy_address:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.network.http.proxy_address()
                def set(self, value): return self.__server._rpc.network.http.proxy_address.set('', value)

            class __ssl_verify_host:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.network.http.ssl_verify_host()
                def set(self, value): return self.__server._rpc.network.http.ssl_verify_host.set('', int(value))

            class __ssl_verify_peer:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.network.http.ssl_verify_peer()
                def set(self, value): return self.__server._rpc.network.http.ssl_verify_peer.set('', int(value))

    class __strings:

        def __init__(self, server):
            self.__server = server
            self.choke_heuristics = self.__choke_heuristics(server)

        def connection_type(self): return self.__server._rpc.strings.connection_type()
        def encryption(self): return self.__server._rpc.strings.encryption()
        def ip_filter(self): return self.__server._rpc.strings.ip_filter()
        def ip_tos(self): return self.__server._rpc.strings.ip_tos()
        def log_group(self): return self.__server._rpc.strings.log_group()
        def tracker_mode(self): return self.__server._rpc.strings.tracker_mode()
        def tracker_event(self): return self.__server._rpc.strings.tracker_event()

        class __choke_heuristics:

            def __init__(self, server): self.__server = server
            def __call__(self): return self.__server._rpc.strings.choke_heuristics()
            def download(self): return self.__server._rpc.strings.choke_heuristics.download()
            def upload(self): return self.__server._rpc.strings.choke_heuristics.upload()

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

        def unchoked_downloads(self): return self.__server._rpc.throttle.unchoked_downloads()
        def unchoked_uploads(self): return self.__server._rpc.throttle.unchoked_uploads()

        def names(self):
            return list(set(self.__server.view().each(lambda x: x.throttle_name())))

        class __down:

            def __init__(self, server): self.__server = server
            def __call__(self, throttle_name, rate):
                """arg1 is throttle name and arg2 is the rate"""
                return self.__server._rpc.throttle.down('', throttle_name, rate)

            def max(self, throttle_name):
                return SizeBytes(self.__server._rpc.throttle.down.max('', throttle_name))

            def rate(self, throttle_name):
                return SizeBytes(self.__server._rpc.throttle.down.rate('', throttle_name))

        class __up:

            def __init__(self, server): self.__server = server
            def __call__(self, throttle_name, rate):
                """arg1 is throttle name and arg2 is the rate"""
                return self.__server._rpc.throttle.up('', throttle_name, rate)

            def max(self, throttle_name):
                return SizeBytes(self.__server._rpc.throttle.up.max('', throttle_name))

            def rate(self, throttle_name):
                return SizeBytes(self.__server._rpc.throttle.up.rate('', throttle_name))

        class __global_down:

            def __init__(self, server):
                self.__server = server
                self.max_rate = self.__max_rate(server)

            def total(self): return SizeBytes(self.__server._rpc.throttle.global_down.total())
            def rate(self): return SizeBytes(self.__server._rpc.throttle.global_down.rate())

            class __max_rate:
                
                def __init__(self, server): self.__server = server
                def __call__(self): return SizeBytes(self.__server._rpc.throttle.global_down.max_rate())
                def set(self, rate): return self.__server._rpc.throttle.global_down.max_rate.set(rate)

        class __global_up:

            def __init__(self, server):
                self.__server = server
                self.max_rate = self.__max_rate(server)

            def total(self): return SizeBytes(self.__server._rpc.throttle.global_up.total())
            def rate(self): return SizeBytes(self.__server._rpc.throttle.global_up.rate())

            class __max_rate:
                
                def __init__(self, server): self.__server = server
                def __call__(self): return SizeBytes(self.__server._rpc.throttle.global_up.max_rate())
                def set(self, rate): return self.__server._rpc.throttle.global_up.max_rate.set(rate)

        class __max_uploads:

            def __init__(self, server):
                self.__server = server
                self.globl = self.__globl(server)
                self.div = self.__div(server)
            
            def __call__(self): return self.__server._rpc.throttle.max_uploads()

            class __globl:

                def __init__(self, server): self.__server = server
                def __call__(self): return getattr(self.__server._rpc, 'throttle.max_uploads.global')()
                def set(self, rate): return getattr(self.__server._rpc, 'throttle.max_uploads.global.set')('', rate)

            class __div:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.throttle.max_uploads.div()
                def set(self, rate): return self.__server._rpc.throttle.max_uploads.div.set('', rate)

        class __max_downloads:

            def __init__(self, server):
                self.__server = server
                self.globl = self.__globl(server)
                self.div = self.__div(server)
            
            def __call__(self): return self.__server._rpc.throttle.max_downloads()

            class __globl:

                def __init__(self, server): self.__server = server
                def __call__(self): return getattr(self.__server._rpc, 'throttle.max_downloads.global')()
                def set(self, rate): return getattr(self.__server._rpc, 'throttle.max_downloads.global.set')('', rate)

            class __div:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.throttle.max_downloads.div()
                def set(self, rate): return self.__server._rpc.throttle.max_downloads.div.set('', rate)

        class __min_uploads:

            def __init__(self, server): self.__server = server
            def __call__(self): return self.__server._rpc.throttle.min_uploads()
            def set(self, num): return self.__server._rpc.throttle.min_uploads.set('', num)

        class __min_downloads:

            def __init__(self, server): self.__server = server
            def __call__(self): return self.__server._rpc.throttle.max_uploads()
            def set(self, num): return self.__server._rpc.throttle.max_uploads.set('', num)

        class __max_peers:

            def __init__(self, server):
                self.__server = server
                self.normal = self.__normal(server)
                self.seed = self.__seed(server)

            class __normal:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.throttle.max_peers.normal()
                def set(self, num): return self.__server._rpc.throttle.max_peers.normal.set('', num)

            class __seed:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.throttle.max_peers.seed()
                def set(self, num): return self.__server._rpc.throttle.max_peers.seed.set('', num)

        class __min_peers:

            def __init__(self, server):
                self.__server = server
                self.normal = self.__normal(server)
                self.seed = self.__seed(server)

            class __normal:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.throttle.min_peers.normal()
                def set(self, num): return self.__server._rpc.throttle.min_peers.normal.set('', num)

            class __seed:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.throttle.min_peers.seed()
                def set(self, num): return self.__server._rpc.throttle.min_peers.seed.set('', num)

    class __choke_group:

        def __init__(self, server):
            self.__server = server
            self.down = self.__down(server)
            self.up = self.__up(server)
            self.general = self.__general(server)
            self.tracker = self.__tracker(server)

        list = lambda self: self.__server._rpc.choke_group.list()
        size = lambda self: self.__server._rpc.choke_group.size()
        insert = lambda self, group: self.__server._rpc.choke_group.insert('', group)
        index_of = lambda self, group: self.__server._rpc.choke_group.index_of('', group)

        class __general:

            def __init__(self, server): self.__server = server
            def size(self, group): return self.__server._rpc.choke_group.general.size('', group)

        class __tracker:

            def __init__(self, server):
                self.__server = server
                self.mode = self.__mode(server)

            class __mode:

                def __init__(self, server): self.__server = server
                def __call__(self, group): return self.__server._rpc.choke_group.tracker.mode('', group)
                def set(self, group, value):
                    return self.__server._rpc.choke_group.tracker.mode.set('', group, value)

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
                    return self.__server._rpc.choke_group.down.heuristics('', group)
                def set(self, group, value): 
                    return self.__server._rpc.choke_group.down.heuristics.set('', group, value)

            class __max:

                def __init__(self, server): self.__server = server
                def __call__(self, group):
                    return self.__server._rpc.choke_group.down.max('', group)
                def set(self, group, value):
                    return self.__server._rpc.choke_group.down.max.set('', group, value)
                def unlimited(self, group): 
                    return self.__server._rpc.choke_group.down.max.unlimited('', group)

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
                    return self.__server._rpc.choke_group.up.heuristics('', group)
                def set(self, group, value): 
                    return self.__server._rpc.choke_group.up.heuristics.set('', group, value)

            class __max:

                def __init__(self, server): self.__server = server
                def __call__(self, group):
                    return self.__server._rpc.choke_group.up.max('', group)
                def set(self, group, value):
                    return self.__server._rpc.choke_group.up.max.set('', group, value)
                def unlimited(self, group): 
                    return self.__server._rpc.choke_group.up.max.unlimited('', group)


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

            def queue_size(self): return self.__server._rpc.pieces.hash.queue_size()

            class __on_completion:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.pieces.hash.on_completion()
                def set(self, value): return self.__server._rpc.pieces.hash.on_completion.set(value)

        class __memory:

            def __init__(self, server):
                self.__server = server
                self.max = self.__max(server)

            def sync_queue(self): return self.__server._rpc.pieces.memory.sync_queue()
            def current(self): return self.__server._rpc.pieces.memory.current()
            def block_count(self): return self.__server._rpc.pieces.memory.block_count()

            class __max:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.pieces.memory.max()
                def set(self, value): return self.__server._rpc.pieces.memory.max.set(value)

        class __preload:

            def __init__(self, server):
                self.__server = server
                self.min_rate = self.__min_rate(server)
                self.min_size = self.__min_size(server)
                self.type = self.__type(server)

            class __min_rate:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.pieces.preload.min_rate()
                def set(self, value): return self.__server._rpc.pieces.preload.min_rate.set(value)

            class __min_size:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.pieces.preload.min_size()
                def set(self, value): return self.__server._rpc.pieces.preload.min_size.set(value)

            class __type:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.pieces.preload.type()
                def set(self, value): return self.__server._rpc.pieces.preload.type.set(value)

        class __stats:

            def __init__(self, server): self.__server = server
            def total_size(self): return SizeBytes(self.__server._rpc.pieces.stats.total_size())

        class __stats_preloaded:

            def __init__(self, server): self.__server = server
            def __call__(self): return self.__server._rpc.pieces.stats_preloaded()

        class __stats_not_preloaded:

            def __init__(self, server): self.__server = server
            def __call__(self): return self.__server._rpc.pieces.stats_not_preloaded()

        class __sync:

            def __init__(self, server):
                self.__server = server
                self.always_safe = self.__always_safe(server)
                self.timeout = self.__timeout(server)
                self.timeout_safe = self.__timeout_safe(server)

            def queue_size(self): return self.__server._rpc.pieces.sync.queue_size()
            def safe_free_diskspace(self): return SizeBytes(self.__server._rpc.pieces.sync.safe_free_diskspace())

            class __always_safe:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.pieces.sync.always_safe()
                def set(self, value): return self.__server._rpc.pieces.sync.always_safe.set(value)

            class __timeout:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.pieces.sync.timeout()
                def set(self, value): return self.__server._rpc.pieces.sync.timeout.set(value)

            class __timeout_safe:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.pieces.sync.timeout_safe()
                def set(self, value): return self.__server._rpc.pieces.sync.timeout_safe.set(value)

    class __group:

        def __init__(self, server):
            self.__server = server
            self.seeding = self.__seeding(server)

        def insert(self, comm): return self.__server._rpc.group.insert(comm)
        def insert(self, view): return self.__server._rpc.group.insert_persistent_view(view)

        class __seeding:
            
            def __init__(self, server):
                self.__server = server
                self.view = self.__view(server)
                self.ratio = self.__ratio(server)

            class __view:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.group.seeding.view()
                def set(self, view): return self.__server._rpc.group.seeding.view.set(value)

            class __ratio:

                def __init__(self, server):
                    self.__server = server
                    self.max = self.__max(server)
                    self.min = self.__min(server)
                    self.upload = self.__upload(server)

                def command(self, com): return self.__server._rpc.group.seeding.ratio.command(com)
                def disable(self): return self.__server._rpc.group.seeding.ratio.disable()
                def enable(self): return self.__server._rpc.group.seeding.ratio.enable()

                class __max:
                    
                    def __init__(self, server): self.__server = server
                    def __call__(self): return self.__server._rpc.group.seeding.ratio.max()
                    def set(self, rat): return self.__server._rpc.group.seeding.ratio.max.set(rat)

                class __min:
                    
                    def __init__(self, server): self.__server = server
                    def __call__(self): return self.__server._rpc.group.seeding.ratio.min()
                    def set(self, rat): return self.__server._rpc.group.seeding.ratio.min.set(rat)

                class __upload:
                    
                    def __init__(self, server): self.__server = server
                    def __call__(self): return self.__server._rpc.group.seeding.ratio.upload()
                    def set(self, rat): return self.__server._rpc.group.seeding.ratio.upload.set(rat)

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
            def set(self, name): return self.__server._rpc.session.name.set(name)

        class __on_completion:

            def __init__(self, server): self.__server = server
            def __call__(self): return self.__server._rpc.session.on_completion()
            def set(self, value): return self.__server._rpc.session.on_completion.set(int(value))

        class __path:

            def __init__(self, server): self.__server = server
            def __call__(self): return self.__server._rpc.session.path()
            def set(self, value): return self.__server._rpc.session.path.set(value)

        class __use_lock:

            def __init__(self, server): self.__server = server
            def __call__(self): return bool(self.__server._rpc.session.use_lock())
            def set(self, value): return self.__server._rpc.session.use_lock.set(int(value))

    class __keys:

        def __init__(self, server):
            self.__server = server
            self.layout = self.__layout(server)

        class __layout:

            def __init__(self, server): self.__server = server
            def __call__(self): return self.__server._rpc.keys.layout()
            def set(self, layout):  return self.__server._rpc.keys.layout.set('', layout)

    class __elapsed:

        def __init__(self, server): self.__server = server
        def greater(self, v1, v2): return self.__server._rpc.elapsed.greater('', v1, v2)
        def less(self, v1, v2): return self.__server._rpc.elapsed.less('', v1, v2)

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
            def set(self, value): return self.__server._rpc.ratio.upload.set(value)

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
        def gm_date(self, value): return self.__server._rpc.convert.gm_date('', value)
        def gm_time(self, value): return self.__server._rpc.convert.gm_time('', value)
        def elapse_time(self, value): return self.__server._rpc.convert.elapse_time('', value)
        def throttle(self, value): return self.__server._rpc.convert.throttle('', value)
        def time(self, value): return self.__server._rpc.convert.time('', value)
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
            def set(self, directory): return self.__server._rpc.directory.default.set(directory)

        class __watch:
            def __init__(self, server): self.__server = server
            def added(self, watch_dir, load):
                return self.__server._rpc.directory.watch.added('', watch_dir, load)

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
            def set(self, value): return self.__server._rpc.dht.port.set('', value)

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
        library_version = lambda self: self.__server._rpc.system.library_version()
        env = lambda self: self.__server._rpc.system.env()
        pid = lambda self: self.__server._rpc.system.pid()
        listMethods = lambda self: self.__server._rpc.system.listMethods()
        multicall = lambda self, *args: self.__server._rpc.system.multicall(args)
        env = lambda self: self.__server._rpc.system.env()
        methodHelp = lambda self, method: self.__server._rpc.system.methodHelp(method)
        methodExists = lambda self, method: self.__server._rpc.system.methodExist(method)
        methodSignature = lambda self, method: self.__server._rpc.system.methodSignature(method)
        capabilities = lambda self: self.__server._rpc.system.capabilities()
        getCapabilities = lambda self: self.__server._rpc.system.getCapabilities()

        class __cwd:

            def __init__(self, server): self.__server = server
            def __call__(self): return self.__server._rpc.system.cwd()
            def set(self, dir): return self.__server._rpc.system.cwd.set('', dir)

        class __files:

            def __init__(self, server): self.__server = server

            failed_counter = lambda self: self.__server._rpc.system.files.failed_counter()
            opened_counter = lambda self: self.__server._rpc.system.files.opened_counter()
            closed_counter = lambda self: self.__server._rpc.system.files.closed_counter()

        class __file:

            def __init__(self, server):
                self.__server = server
                self.allocate = self.__allocate(server)
                self.max_size = self.__max_size(server)
                self.split_size = self.__split_size(server)
                self.split_suffix = self.__split_suffix(server)

            class __allocate:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.system.file.allocate()
                def set(self, value): return self.__server._rpc.system.file.allocate.set('', value)

            class __max_size:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.system.file.max_size()
                def set(self, value): return self.__server._rpc.system.file.max_size.set('', value)

            class __split_size:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.system.file.split_size()
                def set(self, value): return self.__server._rpc.system.file.split_size.set('', value)

            class __split_suffix:

                def __init__(self, server): self.__server = server
                def __call__(self): return self.__server._rpc.system.file.split_suffix()
                def set(self, value): return self.__server._rpc.system.file.split_suffix.set('', value)

        class __file_status_cache:

            def __init__(self, server): self.__server = server
            def size(self): return self.__server._rpc.system.file_status_cache.size()
            def prune(self): return self.__server._rpc.system.file_status_cache.prune()

        class __daemon:

            def __init__(self, server): self.__server = server
            def __call__(self): return bool(self.__server._rpc.system.daemon())
            def set(self, value): return self.__server._rpc.system.daemon.set('', int(value))

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
            mc = xmlrpclib.MultiCall(self.__server._rpc)
            uncached = []
            for hash in hashes:
                if hash not in self.__server._nameCache:
                    mc.d.name(hash)
                    uncached.append(hash)
    
            names = list(mc())
            assert len(names) == len(uncached),\
                "response from server has incorrect length"
            for i in zip(uncached, names):
                self.__server._nameCache[i[0]] = i[1]
    
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
                def __call__(self): return self.__server._rpc.ui.torrent_list.layout()
                def set(self, layout): return self.__server._rpc.ui.torrent_list.layout.set('', layout)

        class __throttle:

            def __init__(self, server):
                self.__server = server
                self.globl = self.__globl(server) #global is a reserved word in python

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

                        # have to call it like this because python doesn't let you use global for anything else
                        def __call__(self):
                            return getattr(self.__server._rpc, "ui.throttle.global.step.large")()

                        def set(self, step):
                            return getattr(self.__server._rpc, "ui.throttle.global.step.large.set")('', step)

                    class __medium:

                        def __init__(self, server): self.__server = server

                        def __call__(self):
                            return getattr(self.__server._rpc, "ui.throttle.global.step.medium")()

                        def set(self, step):
                            return getattr(self.__server._rpc, "ui.throttle.global.step.medium.set")('', step)

                    class __small:

                        def __init__(self, server): self.__server = server

                        def __call__(self):
                            return getattr(self.__server._rpc, "ui.throttle.global.step.small")()

                        def set(self, step):
                            return getattr(self.__server._rpc, "ui.throttle.global.step.small.set")('', step)

    def torrent_list_layout(self, value=None):
        if value is not None: return self._rpc.torrent_list_layout(value)
        state = self.ui.torrent_list.layout()
        next_state = "full" if state == "compact" else "compact"
        return self.ui.torrent_list.layout.set(next_state)

    def connection_leech(self, value): return self._rpc.connection_leech(value)
    def connection_seed(self, value): return self._rpc.connection_seed(value)

    def update_views(self):
        self.views = self.__views(self)

    def _un_cache_hash(self, hash):
        if hash in self._nameCache:
            del self._nameCache[hash]
        if hash in self._trackerCache:
            del self._trackerCache[hash]

    def hash_list(self, view="main"):
        return [x[0] for x in self._rpc.d.multicall2('', view, 'd.hash=')]

    def get_name(self, hash):
        '''memoizes the names obtained from
        info hashes to minimize xmlrpc calls'''
        try:
            return self._nameCache[hash]
        except Exception:
            return self._nameCache.setdefault(hash, self._rpc.d.name(hash))

    def matching_re(self, pattern, caseInsensitive=True, view="main"):
        '''pattern is a regex'''
        matches = self.view(view)
        for torrent in matches[:]:
            if not re.search(pattern, torrent.name, [0, 2][caseInsensitive]):
                matches.remove(torrent)
        return matches

    def matching_names(self, pattern, view="main"):
        return self.view(view).filter(lambda t: pattern in t.name.lower())

    def matching_trackers(self, pattern, caseInsensitive=True,
                              view="main"):
        matches = self.view(view)

        for torrent in matches[:]:
            match = False
            if torrent.hash in self._trackerCache:
                for tracker in self._trackerCache[torrent.hash]:
                    if re.search(pattern, tracker.url,
                                 [0, 2][caseInsensitive]):
                        match = True

            else:
                trackers = []
                tracker_urls = [
                    x[0] for x in self._rpc.t.multicall(torrent.hash,
                                                        0, 't.url=')]
                for i, tracker_url in enumerate(tracker_urls):
                    trackers.append(Tracker(self.server, tracker_url,
                                            torrent.hash, i))
                self._trackerCache[torrent.hash] = trackers
                for tracker in trackers:
                    if re.search(pattern, tracker.url,
                                 [0, 2][caseInsensitive]):
                        match = True

            if not match:
                matches.remove(torrent)

        return matches

    def matching_throttle_name(self, pattern, caseInsensitive=True,
                                   view="main", exact=False):

        matches = self.view(view)
        matches_copy = matches[:]
        mc = xmlrpclib.MultiCall(self._rpc)
        for torrent in matches:
            mc.d.throttle_name(torrent.hash)

        resp = list(mc())
        assert len(matches_copy) == len(resp),\
            "response from server has incorrect length"
        for i, r in enumerate(resp):
            if exact:
                if r != pattern:
                    matches.remove(matches_copy[i])
            else:
                if not re.search(pattern, r, [0, 2][caseInsensitive]):
                    matches.remove(matches_copy[i])

        return matches

    def matching_message(self, pattern, caseInsensitive=True,
                             view="main", exact=False):

        matches = self.view(view)
        matches_copy = matches[:]
        mc = xmlrpclib.MultiCall(self._rpc)

        for torrent in matches:
            mc.d.message(torrent.hash)

        resp = list(mc())
        assert len(matches_copy) == len(resp),\
            "response from server has incorrect length"
        for i, r in enumerate(resp):
            if exact:
                if r != pattern:
                    matches.remove(matches_copy[i])
            else:
                if not re.search(pattern, r,
                                 [0, 2][caseInsensitive]):
                    matches.remove(matches_copy[i])

        return matches

    def unregistered(self, view="main"):

        matches = self.view(view)
        matches_copy = matches[:]
        mc = xmlrpclib.MultiCall(self._rpc)

        for torrent in matches:
            mc.d.message(torrent.hash)

        resp = list(mc())
        assert len(matches_copy) == len(resp),\
            "response from server has incorrect length"
        for i, r in enumerate(resp):
            if not re.match(
                          r'Tracker: \[Failure reason "Unregistered torrent.*',
                          r,
                          re.I):
                matches.remove(matches_copy[i])

        return matches

    def __repr__(self):
        return 'rTorrent server: <{0}>'.format(self.server)

class __checkConnected:

    '''decorator class to make sure that the server URI is set before
    calling funtions that depend on it'''

    def __init__(self, func):
        self.func = func
        self.__doc__ = self.func.__doc__

    def __call__(self, *args, **kwargs):
        if None is not None:
            return self.func(*args, **kwargs)
        else:
            raise ConnectionError("Please connect to a server first.")


class Torrent:

    '''must be initialized with a server, and an info hash.
    provides all of the torrent methods available through
    XML-RPC as instance methods.'''

    def __init__(self, server, hash):
        self.server = server
        self.hash = hash
        self.__files = []
        self.down = self.__down(server, hash)
        self.accepting_seeders = self.__accepting_seeders(server, hash)
        self.custom = self.__custom(server, hash)
        self.custom1 = self.__custom1(server, hash)
        self.custom2 = self.__custom2(server, hash)
        self.custom3 = self.__custom3(server, hash)
        self.custom4 = self.__custom4(server, hash)
        self.custom5 = self.__custom5(server, hash)
        self.disconnect = self.__disconnect(server, hash)
        self.connection_current = self.__connection_current(server, hash)
        self.directory = self.__directory(server, hash)
        self.directory_base = self.__directory_base(server, hash)
        self.downloads_max = self.__downloads_max(server, hash)
        self.downloads_min = self.__downloads_min(server, hash)
        self.hashing_failed = self.__hashing_failed(server, hash)
        self.ignore_commands = self.__ignore_commands(server, hash)
        self.peer_exchange = self.__peer_exchange(server, hash)
        self.peers_max = self.__peers_max(server, hash)
        self.peers_min = self.__peers_min(server, hash)
        self.message = self.__message(server, hash)
        self.priority = self.__priority(server, hash)
        self.skip = self.__skip(server, hash)
        self.tied_to_file = self.__tied_to_file(server, hash)
        self.throttle_name = self.__throttle_name(server, hash)
        self.group = self.__group(server, hash)
        self.close = self.__close(server, hash)

    def __eq__(self, other):
        return self.name.lower() == other.name.lower()

    def __lt__(self, other):
        return self.name.lower() < other.name.lower()

    class __peers_min:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash
        def __call__(self): return self.__server._rpc.d.peers_min(self.__hash)
        def set(self, value): return self.__server._rpc.d.peers_min.set(self.__hash)

    class __peers_max:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash
        def __call__(self): return self.__server._rpc.d.peers_max(self.__hash)
        def set(self, value): return self.__server._rpc.d.peers_max.set(self.__hash)

    class __ignore_commands:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash
        def __call__(self): return self.__server._rpc.d.ignore_commands(self.__hash)
        def set(self, value): return self.__server._rpc.d.ignore_commands.set(self.__hash)

    class __peer_exchange:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash
        def __call__(self): return self.__server._rpc.d.peer_exchange(self.__hash)
        def set(self, value): return self.__server._rpc.d.peer_exchange(self.__hash)

    class __hashing_failed:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash
        def __call__(self): return self.__server._rpc.d.hashing_failed(self.__hash)
        def set(self, value): return self.__server._rpc.d.hashing_failed.set(self.__hash, value)

    class __downloads_max:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash

        def __call__(self):
            return self.__server._rpc.d.downloads_max(self.__hash)

        def set(self, num):
            return self.__server._rpc.d.downloads_max.set(self.__hash, num)

    class __downloads_min:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash

        def __call__(self):
            return self.__server._rpc.d.downloads_min(self.__hash)

        def set(self, num):
            return self.__server._rpc.d.downloads_min.set(self.__hash, num)

    class __accepting_seeders:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash

        def __call__(self): return self.__server._rpc.d.accepting_seeders(self.__hash)
        def disable(self): return self.__server._rpc.d.accepting_seeders.disable(self.__hash)
        def enable(self): return self.__server._rpc.d.accepting_seeders.enable(self.__hash)

    class __custom:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash

        def if_z(self, key, default):
            return self.__server._rpc.d.custom.if_z(self.__hash, key, default)

        def __call__(self, key): return self.__server._rpc.d.custom(self.__hash, key)
        def set(self, key, value): return self.__server._rpc.d.custom.set(self.__hash, key, value)
        def keys(self): return self.__server._rpc.d.custom.keys(self.__hash)

    class __custom1:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash

        def __call__(self): return self.__server._rpc.d.custom1(self.__hash)
        def set(self, value): return self.__server._rpc.d.custom1.set(self.__hash, value)

    class __custom2:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash

        def __call__(self): return self.__server._rpc.d.custom2(self.__hash)
        def set(self, value): return self.__server._rpc.d.custom2.set(self.__hash, value)

    class __custom3:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash

        def __call__(self): return self.__server._rpc.d.custom3(self.__hash)
        def set(self, value): return self.__server._rpc.d.custom3.set(self.__hash, value)

    class __custom4:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash

        def __call__(self): return self.__server._rpc.d.custom4(self.__hash)
        def set(self, value): return self.__server._rpc.d.custom4.set(self.__hash, value)

    class __custom5:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash

        def __call__(self): return self.__server._rpc.d.custom5(self.__hash)
        def set(self, value): return self.__server._rpc.d.custom5.set(self.__hash, value)

    class __close:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash

        def __call__(self): self.__server._rpc.d.close(self.__hash)
        def directly(self): self.__server._rpc.d.close.directly(self.__hash)

    class __down:

        def __init__(self, server, hash):
            self.__server = server
            self.hash = hash
            self.choke_heuristics = self.__choke_heuristics(server, hash)

        def rate(self): return SizeBytes(self.__server._rpc.d.down.rate(self.hash))
        def total(self): return SizeBytes(self.__server._rpc.d.down.total(self.hash))

        class __choke_heuristics:

            def __init__(self, server, hash):
                self.__server = server
                self.hash = hash

            def __call__(self): return self.__server._rpc.d.down.choke_heuristics(self.hash)
            def leech(self): return self.__server._rpc.d.down.choke_heuristics.leech(self.hash)
            def seed(self): return self.__server._rpc.d.down.choke_heuristics.seed(self.hash)
            def set(self, value): return self.__server._rpc.d.down.choke_heuristics.set(self.hash, value)

    class __disconnect:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash

        def seeders(self): self.__server._rpc.d.disconnect.seeders(self.__hash)

    class __connection_current:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash

        def __call__(self): return self.__server._rpc.connection_current(self.__hash)
        def set(self, value): return self.__server._rpc.connection_current(self.__hash, value)

    class __directory:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash

        def __call__(self):
            return self.__server._rpc.d.directory(self.__hash)

        def set(self, directory):
            return self.__server._rpc.d.directory.set(self.__hash, directory)

    class __directory_base:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash

        def __call__(self):
            return self.__server._rpc.d.directory_base(self.__hash)

        def set(self, directory):
            return self.__server._rpc.d.directory_base.set(self.__hash, directory)

    class __group:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash

        def __call__(self):
            return self.__server._rpc.d.group(self.__hash)

        def name(self): 
            groups = self.__server.choke_group.list()
            return groups[self.__server._rpc.d.group.name(self.__hash)]

        def set(self, group):
            return self.__server._rpc.d.group.set(self.__hash, group)

    class __message:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash
        def __call__(self): return self.__server._rpc.d.message(self.__hash)
        def set(self, message): return self.__server._rpc.d.message.set(self.__hash, message)

    class __priority:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash
        def __call__(self): return self.__server._rpc.d.priority(self.__hash)
        def set(self, priority): return self.__server._rpc.d.priority.set(self.__hash, priority)

    class __skip:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash
        def total(self): return self.__server._rpc.d.skip.total(self.__hash)
        def rate(self): return self.__server._rpc.d.skip.rate(self.__hash)

    class __throttle_name:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash
        def __call__(self): return self.__server._rpc.d.throttle_name(self.__hash)
        def set(self, name): return self.__server._rpc.d.throttle_name.set(self.__hash, name)

    class __tied_to_file:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash
        def __call__(self): return self.__server._rpc.d.tied_to_file(self.__hash)
        def set(self, file): return self.__server._rpc.d.tied_to_file.set(self.__hash, file)

    def save_full_session(self):
        return bool(self.server._rpc.d.save_full_session(self.hash))

    def save_resume(self):
        return bool(self.server._rpc.d.save_resume(self.hash))

    def custom_throw(self, key):
        return self.server._rpc.d.custom_throw(self.hash, key)

    @property
    def name(self):
        return self.server.get_name(self.hash)

    def incomplete(self):
        return bool(self.server._rpc.d.incomplete(self.hash))

    def is_meta(self):
        return bool(self.server._rpc.d.is_meta(self.hash))

    def is_not_partially_done(self):
        return bool(self.server._rpc.d.is_not_partially_done(self.hash))

    def is_partially_done(self):
        return bool(self.server._rpc.d.is_partially_done(self.hash))

    def is_pex_active(self):
        return bool(self.server._rpc.d.is_pex_active(self.hash))

    def load_date(self):
        return self.server._rpc.d.load_date(self.hash)

    def add_peer(self, peer):
        return self.server._rpc.d.add_peer(self.hash, peer)

    def check_hash(self):
        return self.server._rpc.d.check_hash(self.hash)

    def create_link(self, link):
        return self.server._rpc.d.create_link(self.hash, link)

    def delete_link(self):
        return self.server._rpc.d.delete_link(self.hash)

    def delete_tied(self):
        return self.server._rpc.d.delete_tied(self.hash)

    def erase(self):
        self.server._un_cache_hash(self.hash)
        return self.server._rpc.d.erase(self.hash)

    def base_filename(self):
        return self.server._rpc.d.base_filename(self.hash)

    def base_path(self):
        return self.server._rpc.d.base_path(self.hash)

    def bitfield(self):
        return self.server._rpc.d.bitfield(self.hash)

    def bytes_done(self):
        return SizeBytes(self.server._rpc.d.bytes_done(self.hash))

    def chunk_size(self):
        return self.server._rpc.d.chunk_size(self.hash)

    def chunks_hashed(self):
        return self.server._rpc.d.chunks_hashed(self.hash)

    def complete(self):
        return bool(self.server._rpc.d.complete(self.hash))

    def completed_bytes(self):
        return SizeBytes(self.server._rpc.d.completed_bytes(self.hash))

    def completed_chunks(self):
        return self.server._rpc.d.completed_chunks(self.hash)

    def connection_leech(self):
        return self.server._rpc.d.connection_leech(self.hash)

    def connection_seed(self):
        return self.server._rpc.d.connection_seed(self.hash)

    def creation_date(self):
        return self.server._rpc.d.creation_date(self.hash)

    def free_diskspace(self):
        return self.server._rpc.d.free_diskspace(self.hash)

    def hash(self):
        return self.hash

    def hashing(self):
        return self.server._rpc.d.hashing(self.hash)

    def ignore_commands(self):
        return self.server._rpc.d.ignore_commands(self.hash)

    def left_bytes(self):
        return SizeBytes(self.server._rpc.d.left_bytes(self.hash))

    def loaded_file(self):
        return self.server._rpc.d.loaded_file(self.hash)

    def local_id(self):
        return self.server._rpc.d.local_id(self.hash)

    def local_id_html(self):
        return self.server._rpc.d.local_id_html(self.hash)

    def max_file_size(self):
        return SizeBytes(self.server._rpc.d.max_file_size(self.hash))

    def max_size_pex(self):
        return self.server._rpc.d.max_size_pex(self.hash)

    def mode(self, element):
        return self.server._rpc.d.mode(self.hash, element)

    def get_name(self):
        return self.server.name(self.hash)

    def peers_accounted(self):
        return self.server._rpc.d.peers_accounted(self.hash)

    def peers_complete(self):
        return self.server._rpc.d.peers_complete(self.hash)

    def peers_connected(self):
        return self.server._rpc.d.peers_connected(self.hash)

    def peers_not_connected(self):
        return self.server._rpc.d.peers_not_connected(self.hash)

    def priority_str(self):
        return self.server._rpc.d.priority_str(self.hash)

    @property
    def ratio(self):
        return self.server._rpc.d.ratio(self.hash)/1000.0

    def size(self):
        return SizeBytes(self.server._rpc.d.size_bytes(self.hash))

    def size_bytes(self):
        return self.server._rpc.d.size_bytes(self.hash)

    def size_chunks(self):
        return self.server._rpc.d.size_chunks(self.hash)

    def size_files(self):
        return self.server._rpc.d.size_files(self.hash)

    def size_pex(self):
        return self.server._rpc.d.size_pex(self.hash)

    def state(self):
        return self.server._rpc.d.state(self.hash)

    def state_changed(self):
        return self.server._rpc.d.state_changed(self.hash)

    def state_counter(self):
        return self.server._rpc.d.state_counter(self.hash)

    def tied_to_file(self):
        return self.server._rpc.d.tied_to_file(self.hash)

    def tracker_focus(self):
        return self.server._rpc.d.tracker_focus(self.hash)

    def tracker_numwant(self):
        return self.server._rpc.d.tracker_numwant(self.hash)

    def tracker_size(self):
        return self.server._rpc.d.tracker_size(self.hash)

    def up_rate(self):
        return SizeBytes(self.server._rpc.d.up_rate(self.hash))

    def up_total(self):
        return SizeBytes(self.server._rpc.d.up_total(self.hash))

    def uploads_max(self):
        return SizeBytes(self.server._rpc.d.uploads_max(self.hash))

    def initialize_logs(self):
        return self.server._rpc.d.initialize_logs(self.hash)

    def is_active(self):
        return bool(self.server._rpc.d.is_active(self.hash))

    def is_hash_checked(self):
        return bool(self.server._rpc.d.is_hash_checked(self.hash))

    def is_hash_checking(self):
        return bool(self.server._rpc.d.is_hash_checking(self.hash))

    def is_multi_file(self):
        return bool(self.server._rpc.d.is_multi_file(self.hash))

    def is_open(self):
        return bool(self.server._rpc.d.is_open(self.hash))

    def is_pex_active(self):
        return bool(self.server._rpc.d.is_pex_active(self.hash))

    def is_private(self):
        return bool(self.server._rpc.d.is_private(self.hash))

    def open(self):
        return bool(self.server._rpc.d.open(self.hash))

    def pause(self):
        return not bool(self.server._rpc.d.pause(self.hash))

    def resume(self):
        return not bool(self.server._rpc.d.resume(self.hash))

    def set_connection_current(self, value):
        return self.server._rpc.d.connection_current.set(self.hash, value)

    def set_ignore_commands(self, value):
        return self.server._rpc.d.ignore_commands.set(self.hash, value)

    def set_priority(self, priority):
        return self.server._rpc.d.priority.set(self.hash, priority)

    def set_tied_to_file(self):
        return self.server._rpc.d.tied_to_file.set(self.hash)

    def set_tracker_numwant(self, num):
        return self.server._rpc.d.tracker_numwant.set(self.hash, num)

    def set_uploads_max(self, max):
        return self.server._rpc.d.uploads_max.set(self.hash)

    def start(self):
        return not bool(self.server._rpc.d.start(self.hash))

    def stop(self):
        return self.server._rpc.d.stop(self.hash)

    def try_close(self):
        return self.server._rpc.d.try_close(self.hash)

    def try_start(self):
        return self.server._rpc.d.try_start(self.hash)

    def try_stop(self):
        return self.server._rpc.d.try_stop(self.hash)

    def update_priorities(self):
        return self.server._rpc.d.update_priorities(self.hash)

    def views(self, value):
        return self.server._rpc.d.views(self.hash, value)

    def views_has(self, value):
        return self.server._rpc.d.views.has(self.hash, value)

    def views_push_back(self, value):
        return self.server._rpc.d.views.push_back(self.hash, value)

    def views_push_back_unique(self, value):
        return self.server._rpc.d.views.push_back_unique(self.hash, value)

    def views_remove(self, view):
        return self.server._rpc.d.views.remove(self.hash, view)

    def time_left(self):
        if self.complete():
            return TimePeriod(seconds=0)
        return TimePeriod(
            seconds=(self.left_bytes() / self.down_rate()))

    def is_unregistered(self):
        return re.match(r'Tracker: \[Failure reason "Unregistered torrent',
                        self.message(), re.I)

    @property
    def files(self):
        '''memoizes a torrents list of files. this function gets called
        when the "files" attribute is accessed.'''
        if self.__files:
            return self.__files
        returnGroup = FileGroup()
        files = [x[0] for x in self.server._rpc.f.multicall(self.hash,
                                                            0, 'f.path=')]
        for index, path in enumerate(files):
            returnGroup.append(
                File(
                    self.server,
                    path,
                    self.hash,
                    index
                )
            )
        self.__files = returnGroup
        return self.__files

    @property
    def trackers(self):
        if self.hash in self.server._trackerCache:
            return self.server._trackerCache[self.hash]
        ret = []
        tracker_urls =\
            [x[0] for x in self.server._rpc.t.multicall(self.hash, 0,
                                                        't.url=')]
        for i, url in enumerate(tracker_urls):
            ret.append(
                Tracker(self.server, url, self.hash, i)
            )
        self.server._trackerCache[self.hash] = ret
        return ret

    def seed_time(self):
        return TimePeriod(seconds=time.time()-int(self.custom2()))

    def __bonus(self, season=False, modifier=1):
        return modifier * 0.15 * self.size().toGiB() * \
                4 * 24 * [1, self.seed_time().days / 28.0][season]

    def __repr__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)

    def __ne__(self, value):
        return value != self.name


class TorrentGroup(Sequence):

    '''List-like group object for Torrent objects.
    Works with normal list methods.'''

    def __init__(self, *items):
        self.data = list(items)

    def __len__(self):
        return len(self.data)

    def pop(self):
        return self.data.pop()

    def __getitem__(self, value):
        if isinstance(value, slice):
            return TorrentGroup(*self.data[value])
        else:
            return self.data[value]

    class __down:
        def total(self):
            pass

    def remove(self, value):
        self.data.remove(value)

    def append(self, value):
        self.data.append(value)

    def erase_all(self):
        '''removes all Torrents in group from rtorrent'''
        for torrent in self.data[:]:
            if torrent.erase():
                self.data.remove(torrent)

    def stop_all(self):
        '''stops all torrents in group'''
        if not self.data:
            return []
        mc = xmlrpclib.MultiCall(self.data[0].server._rpc)
        for torrent in self.data:
            mc.d.stop(torrent.hash)
        return list(mc())

    def start_all(self):
        '''starts all torrents in group'''
        if not self.data:
            return []
        mc = xmlrpclib.MultiCall(self.data[0].server._rpc)
        for torrent in self.data:
            mc.d.start(torrent.hash)
        return list(mc())

    def pause_all(self):
        '''pauses all torrents in group'''
        if not self.data:
            return []
        mc = xmlrpclib.MultiCall(self.data[0].server._rpc)
        for torrent in self.data:
            mc.d.pause(torrent.hash)
        return list(mc())

    def resume_all(self):
        '''resumes all torrents in group'''
        if not self.data:
            return []
        mc = xmlrpclib.MultiCall(self.data[0].server._rpc)
        for torrent in self.data:
            mc.d.resume(torrent.hash)
        return list(mc())

    def open_all(self):
        '''opens all torrents in group'''
        if not self.data:
            return []
        mc = xmlrpclib.MultiCall(self.data[0].server._rpc)
        for torrent in self.data:
            mc.d.open(torrent.hash)
        return list(mc())

    def close_all(self):
        '''closes all torrents in group'''
        if not self.data:
            return []
        mc = xmlrpclib.MultiCall(self.data[0].server._rpc)
        for torrent in self.data:
            mc.d.close(torrent.hash)
        return list(mc())

    def size(self):
        '''returns a SizeBytes object of the total size of
        all the Torrents in the group in bytes'''
        return SizeBytes(self.size_bytes())

    def size_bytes(self):
        '''returns a SizeBytes object of the total size of
        all the Torrents in the group in bytes'''
        if not self.data:
            return 0
        mc = xmlrpclib.MultiCall(self.data[0].server._rpc)
        for torrent in self.data:
            mc.d.size_bytes(torrent.hash)
        return sum(mc())

    def complete(self):
        '''returns True if all the Torrents in the group
        are complete'''
        if not self.data:
            return True
        mc = xmlrpclib.MultiCall(self.data[0].server._rpc)
        for torrent in self.data:
            mc.d.complete(torrent.hash)
        return all(mc())

    def up_rate(self):
        '''returns SizeByte object containing the current
        total upload rate of all the Torrents in the group'''
        if not self.data:
            return SizeBytes(0)
        mc = xmlrpclib.MultiCall(self.data[0].server._rpc)
        for torrent in self.data:
            mc.d.up_rate(torrent.hash)
        return SizeBytes(sum(mc()))

    def down_rate(self):
        '''returns SizeByte object containing the current
        total download rate of all the Torrents in the group'''
        if not self.data:
            return SizeBytes(0)
        mc = xmlrpclib.MultiCall(self.data[0].server._rpc)
        for torrent in self.data:
            mc.d.down_rate(torrent.hash)
        return SizeBytes(sum(mc()))

    def up_total(self):
        '''returns SizeByte object containing the current
        total bytes uploaded of all the Torrents in the group'''
        if not self.data:
            return SizeBytes(0)
        mc = xmlrpclib.MultiCall(self.data[0].server._rpc)
        for torrent in self.data:
            mc.d.up.total(torrent.hash)
        return SizeBytes(sum(mc()))

    def down_total(self):
        '''returns SizeByte object containing the current
        total bytes downloaded of all the Torrents in the group'''
        if not self.data:
            return SizeBytes(0)
        mc = xmlrpclib.MultiCall(self.data[0].server._rpc)
        for torrent in self.data:
            mc.d.down.total(torrent.hash)
        return SizeBytes(sum(mc()))

    def hashing(self):
        '''returns True if any of the Torrents in the group are hashing'''
        if not self.data:
            return False
        mc = xmlrpclib.MultiCall(self.data[0].server._rpc)
        for torrent in self.data:
            mc.d.hashing(torrent.hash)
        return any(mc())

    @property
    def ratio(self):
        '''returns the total overall ratio of all the Torrents in the group'''
        if not self.data:
            return 0
        mc = xmlrpclib.MultiCall(self.data[0].server._rpc)
        for torrent in self.data:
            mc.d.ratio(torrent.hash)

        g = [x/1000.0 for x in mc()]
        return sum(g) / len(g)

    def each(self, func):
        '''takes a function or a Torrent instance method as an argument and
        applies it to every Torrent in the group. similar to the map function.
        returns a list.'''
        if isinstance(func, type) or isinstance(func, FunctionType):
            ret = list(map(func, self))
            if all([isinstance(t, Torrent) for t in ret]):
                return TorrentGroup(*ret)
            return ret
        ret = [x.__getattribute__(func)() for x in self.data]
        if all([isinstance(t, Torrent) for t in ret]):
            return TorrentGroup(*ret)
        return ret

    def filter(self, func):
        '''takes a function that returns a bool as an argument and filters the
        group by applying the function to each member'''
        if type(func) == str:
            s = func
            func = lambda x: s in x.name.lower()
        ret = list(filter(func, self))
        if all([isinstance(t, Torrent) for t in ret]):
            return TorrentGroup(*ret)
        return ret

    def unregistered(self):
        return self.filter(lambda x: x.is_unregistered())

    def set_throttle_name(self, name):
        '''sets a throttle name for each Torrent in the group.'''
        for torrent in self:
            torrent.pause()
            torrent.throttle_name.set(name)
            torrent.resume()

    def sort(self):
        self.data.sort()

    def multicall(self, arg):
        if not self.data:
            return []
        mc = xmlrpclib.MultiCall(self.data[0].server._rpc)
        for torrent in self:
            mc._MultiCall__call_list.append(
                (arg, (torrent.hash,))
            )
        return list(mc())

    def __repr__(self):
        return pprint.pformat(self.data, width=120)


class Tracker:

    def __init__(self, server, url, hash, index):
        self.server = server
        self.url = url
        self.hash = hash
        self.index = index
        self.idx = 0;

    def group(self):
        return self.server._rpc.t.group(self.hash, self.index)

    def id(self):
        return self.server._rpc.t.id(self.hash, self.index)

    def min_interval(self):
        return self.server._rpc.t.min_interval(self.hash, self.index)

    def normal_interval(self):
        return self.server._rpc.t.normal_interval(self.hash, self.index)

    def scrape_complete(self):
        return self.server._rpc.t.scrape_complete(self.hash, self.index)

    def scrape_downloaded(self):
        return self.server._rpc.t.scrape_downloaded(self.hash, self.index)

    def scrape_incomplete(self):
        return self.server._rpc.t.scrape_incomplete(self.hash, self.index)

    def scrape_time_last(self):
        return self.server._rpc.t.scrape_time_last(self.hash, self.index)

    def type(self):
        return self.server._rpc.t.type(self.hash, self.index)

    def url(self):
        return self.server._rpc.t.url(self.hash, self.index)

    def is_enabled(self):
        return self.server._rpc.t.is_enabled(self.hash, self.index)

    def is_open(self):
        return self.server._rpc.t.is_open(self.hash, self.index)

    def set_enabled(self, value):
        return self.server._rpc.t.enabled.set(self.hash, self.index, value)

    def __iter__(self):
        return self.url

    def __next__(self):
        self.idx += 1
        try:
            return self.url[self.idx-1]
        except IndexError:
            self.idx = 0
            raise StopIteration

    def __repr__(self):
        return str(self.url)

    def __str__(self):
        return str(self.url)

    def __unicode__(self):
        return str(self.url)


class File:

    '''takes a name (path), an info hash, and an index number to initialize.
    all file operations are available as instance methods.'''

    priority = namedtuple('priority', 'off normal high')(
        0, 1, 2
    )

    def __init__(self, server, name, hash, index):
        self.server = server
        self.name = name
        self.hash = hash
        self.index = index

    def completed_chunks(self):
        return self.server._rpc.f.completed_chunks(self.hash, self.index)

    def frozen_path(self):
        return self.server._rpc.f.frozen_path(self.hash, self.index)

    def last_touched(self):
        return self.server._rpc.f.last_touched(self.hash, self.index)

    def match_depth_next(self):
        return self.server._rpc.f.match_depth_next(self.hash, self.index)

    def match_depth_prev(self):
        return self.server._rpc.f.match_depth_prev(self.hash, self.index)

    def offset(self):
        return self.server._rpc.f.offset(self.hash, self.index)

    def path(self):
        return self.server._rpc.f.path(self.hash, self.index)

    def path_components(self):
        return self.server._rpc.f.path_components(self.hash, self.index)

    def path_depth(self):
        return self.server._rpc.f.path_depth(self.hash, self.index)

    def priority(self):
        return self.server._rpc.f.priority(self.hash, self.index)

    def priority_str(self):
        return ['off', 'normal', 'high'][self.server._rpc.f.priority(
            self.hash, self.index)]

    def range_first(self):
        return self.server._rpc.f.range_first(self.hash, self.index)

    def range_second(self):
        return self.server._rpc.f.range_second(self.hash, self.index)

    def size(self):
        return SizeBytes(
            self.server._rpc.f.size_bytes(self.hash, self.index))

    def size_bytes(self):
        return self.server._rpc.f.size_bytes(self.hash, self.index)

    def size_chunks(self):
        return self.server._rpc.f.size_chunks(self.hash, self.index)

    def is_create_queued(self):
        return self.server._rpc.f.is_create_queued(self.hash, self.index)

    def is_created(self):
        return self.server._rpc.f.is_created(self.hash, self.index)

    def is_open(self):
        return self.server._rpc.f.is_open(self.hash, self.index)

    def is_resize_queued(self):
        return self.server._rpc.f.is_resize_queued(self.hash, self.index)

    def set_create_queued(self, value):
        return self.server._rpc.f.create_queued.set(
            self.hash, self.index, value)

    def set_priority(self, value):
        return not bool(
            self.server._rpc.f.priority.set(self.hash, self.index, value)
        )

    def set_resize_queued(self):
        return self.server._rpc.f.resize_queued.set(self.hash, self.index)

    def unset_create_queued(self):
        return self.server._rpc.f.create_queued.unset(self.hash, self.index)

    def unset_resize_queued(self):
        return self.server._rpc.f.resize_queued.set(self.hash, self.index)

    def __repr__(self):
        return repr(self.name)

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)

    def __contains__(self, a):
        return a in self.name


class FileGroup(Sequence):

    '''list group of File objects. Standard list methods work.'''

    #__slots__ = []

    def __init__(self, *items):
        self.__data = list(items)
        for item in list(items):
            if not isinstance(item, File):
                raise TypeError('{0} is not a File object'.format(item))

    def append(self, item):
        if isinstance(item, File):
            self.__data.append(item)
        else:
            raise TypeError('{0} is not a File object'.format(item))

    def setPriority(self, value):
        '''set the priority of all the File objects in the group. accepted
        values a 0 for off, 1 for normal, or 2 for high priority'''
        return list([x.priority.set(value) for x in self])

    def filter(self, value):
        '''returns a FileGroup object for all Files in the group
        matching "value"'''
        returnGroup = FileGroup()
        for file in self.__data:
            if value in file.name:
                returnGroup.append(file)
        return returnGroup

    def sort(self):
        self.__data.sort()

    def pop(self):
        return self.__data.pop()

    def __len__(self):
        return len(self.__data)

    def __getitem__(self, val):
        if isinstance(val, slice):
            return FileGroup(*self.__data[val])
        else:
            return self.__data[val]

    def __repr__(self):
        return pprint.pformat(self.__data, width=120)


class SizeBytes(float):

    '''class for nicer byte values'''

    def __repr__(self):
        return repr(self.sizeof_fmt(self))

    def __str__(self):
        return self.sizeof_fmt(self)

    __unicode__ = __str__

    def sizeof_fmt(self, num):
        for x in ['bytes', 'KB', 'MB', 'GB']:
            if num < 1024.0 and num > -1024.0:
                return "%3.1f%s" % (num, x)
            num /= 1024.0
        return "%3.1f%s" % (num, 'TB')

    def toGiB(self):
        return int(self)/(1024**3)

    def value(self):
        return int(self)

    def __div__(self, a):
        return SizeBytes(float(self)/float(a))

    def __rdiv__(self, a):
        return SizeBytes(float(a)/float(self))

    def __truediv__(self, a):
        return SizeBytes(float(self)/float(a))

    def __mul__(self, a):
        return SizeBytes(float(self)*float(a))

    def __rmul__(self, a):
        return SizeBytes(float(self)*float(a))

    def __add__(self, a):
        return SizeBytes(float(self)+float(a))

    def __sub__(self, a):
        return SizeBytes(float(self)-float(a))

    def __pow__(self, a):
        return SizeBytes(pow(float(self), float(a)))


class TimePeriod(datetime.timedelta):

    @property
    def hours(self):
        return self.seconds / 3600

    @property
    def minutes(self):
        return self.seconds % 3600 / 60

    @property
    def sec(self):
        return self.seconds % 60

    def format(self):
        return (self.days,
                "{0:02d}:{1:02d}:{2:02d}".format(
                    int(self.hours),
                    int(self.minutes),
                    int(self.sec)))

    def __repr__(self):
        return 'TimePeriod' + repr(self.format())
