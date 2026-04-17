from .fileutils import *
from .tracker import Tracker
from urllib.parse import urlsplit
from .peer import Peer
import os
import time

class Torrent:

    '''must be initialized with a server, and an info hash.
    provides all of the torrent methods available through
    XMLRPC/JSONRPC as instance methods.'''

    def __init__(self, server, hash):
#        if not isinstance(server, Server):
#            raise TypeError(f'{server} must be type Server')
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
        def set(self, value):
            return self.__server._rpc.d.peers_min.set(self.__hash)

    class __peers_max:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash
        def __call__(self): return self.__server._rpc.d.peers_max(self.__hash)
        def set(self, value):
            return self.__server._rpc.d.peers_max.set(self.__hash)

    class __ignore_commands:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash
        def __call__(self):
            return self.__server._rpc.d.ignore_commands(self.__hash)
        def set(self, value):
            return self.__server._rpc.d.ignore_commands.set(self.__hash)

    class __peer_exchange:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash
        def __call__(self):
            return self.__server._rpc.d.peer_exchange(self.__hash)
        def set(self, value):
            return self.__server._rpc.d.peer_exchange(self.__hash)

    class __hashing_failed:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash
        def __call__(self):
            return self.__server._rpc.d.hashing_failed(self.__hash)
        def set(self, value):
            return self.__server._rpc.d.hashing_failed.set(self.__hash, value)

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

        def __call__(self):
            return bool(self.__server._rpc.d.accepting_seeders(self.__hash))
        def disable(self):
            return bool(self.__server._rpc.d.accepting_seeders.disable(self.__hash))
        def enable(self):
            return bool(self.__server._rpc.d.accepting_seeders.enable(self.__hash))

    class __custom:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash

        def if_z(self, key, default):
            return self.__server._rpc.d.custom.if_z(self.__hash, key, default)

        def __call__(self, key):
            return self.__server._rpc.d.custom(self.__hash, key)
        def set(self, key, value):
            return self.__server._rpc.d.custom.set(self.__hash, key, value)
        def keys(self): return self.__server._rpc.d.custom.keys(self.__hash)

    class __custom1:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash

        def __call__(self):
            return self.__server._rpc.d.custom1(self.__hash)
        def set(self, value):
            return self.__server._rpc.d.custom1.set(self.__hash, value)

    class __custom2:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash

        def __call__(self):
            return self.__server._rpc.d.custom2(self.__hash)
        def set(self, value):
            return self.__server._rpc.d.custom2.set(self.__hash, value)

    class __custom3:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash

        def __call__(self): return self.__server._rpc.d.custom3(self.__hash)
        def set(self, value):
            return self.__server._rpc.d.custom3.set(self.__hash, value)

    class __custom4:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash

        def __call__(self): return self.__server._rpc.d.custom4(self.__hash)
        def set(self, value):
            return self.__server._rpc.d.custom4.set(self.__hash, value)

    class __custom5:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash

        def __call__(self): return self.__server._rpc.d.custom5(self.__hash)
        def set(self, value):
            return self.__server._rpc.d.custom5.set(self.__hash, value)

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

        def rate(self):
            return SizeBytes(self.__server._rpc.d.down.rate(self.hash))
        def total(self):
            return SizeBytes(self.__server._rpc.d.down.total(self.hash))

        class __choke_heuristics:

            def __init__(self, server, hash):
                self.__server = server
                self.hash = hash

            def __call__(self):
                return self.__server._rpc.d.down.choke_heuristics(self.hash)
            def leech(self):
                return self.__server._rpc.d.down.choke_heuristics.leech(self.hash)
            def seed(self):
                return self.__server._rpc.d.down.choke_heuristics.seed(self.hash)
            def set(self, value):
                return self.__server._rpc.d.down.choke_heuristics.set(self.hash, value)

    class __disconnect:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash

        def seeders(self): self.__server._rpc.d.disconnect.seeders(self.__hash)

    class __connection_current:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash

        def __call__(self):
            return self.__server._rpc.connection_current(self.__hash)
        def set(self, value):
            return self.__server._rpc.connection_current(self.__hash, value)

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
        def set(self, message):
            return self.__server._rpc.d.message.set(self.__hash, message)

    class __priority:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash
        def __call__(self): return self.__server._rpc.d.priority(self.__hash)
        def set(self, priority):
            return self.__server._rpc.d.priority.set(self.__hash, priority)

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
        def set(self, name):
            return self.__server._rpc.d.throttle_name.set(self.__hash, name)

    class __tied_to_file:

        def __init__(self, server, hash):
            self.__server = server
            self.__hash = hash
        def __call__(self): return self.__server._rpc.d.tied_to_file(self.__hash)
        def set(self, file):
            return self.__server._rpc.d.tied_to_file.set(self.__hash, file)

    def save_full_session(self):
        return bool(self.server._rpc.d.save_full_session(self.hash))

    def save_resume(self):
        return bool(self.server._rpc.d.save_resume(self.hash))

    def custom_throw(self, key):
        return self.server._rpc.d.custom_throw(self.hash, key)

    @property
    def name(self):
        return self.server._rpc.d.name(self.hash)

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

    def create_link(self):
        return self.server._rpc.d.create_link(self.hash)

    def delete_link(self):
        return self.server._rpc.d.delete_link(self.hash)

    def delete_tied(self):
        return self.server._rpc.d.delete_tied(self.hash)

    def erase(self):
        return self.server._rpc.d.erase(self.hash)

    def erase_with_files(self):
        files = self.get_files()
        list(map(os.remove, files))
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

    def set_create_resize(self):
        self.server._rpc.f.multicall(
            self.hash,
            "",
            "f.set_create_queued=0"
        )
        self.server._rpc.f.multicall(
            self.hash,
            "",
            "f.set_resize_queued=0"
        )


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

    def get_files(self):
        return list(map(lambda x:os.path.join(self.directory_base(),
                                              str(x)), self.files))

    def peers(self):
        return [ Peer(self.server, self.hash, p[3])
                for p in self.server._rpc.p.multicall(self.hash,
                                                      "",
                                                      "p.address=",
                                                      "p.port=",
                                                      "p.client_version=",
                                                      "p.id=") ]

    def trackers(self, num=0):
        ret = []
        tracker_urls =\
            [x[0] for x in self.server._rpc.t.multicall(self.hash, num,
                                                        't.url=')]
        for i, url in enumerate(tracker_urls):
            ret.append(
                Tracker(self.server, url, self.hash, i)
            )
        return ret

    def seed_time(self):
        return TimePeriod(seconds=time.time()-int(self.custom("addtime")))

    def __repr__(self):
        return self.name

    def __info__(self):
        calls = [
		    {'methodName': 'd.name', 'params': [self.hash]},
		    {'methodName': 'd.size_bytes', 'params': [self.hash]},
		    {'methodName': 'd.completed_bytes', 'params': [self.hash]},
		    {'methodName': 'd.directory', 'params': [self.hash]},
			{'methodName': 't.multicall', 'params': [self.hash, "", "t.url="]}
		]

        results = self.server._rpc.system.multicall(calls)

        try:
            return ( f'{results[0][0]} | {urlsplit(results[4][0][0][0]).netloc}'
                  f' | {results[2][0]/results[1][0]*100:.2f}% | {results[3][0]}'
                    )
        except Exception:
            return results

    def __str__(self):
        return str(self.name)

    def __contains__(self, sub):
        return sub in self.name

    def __unicode__(self):
        return str(self.name)

    def __ne__(self, value):
        return value != self.name
