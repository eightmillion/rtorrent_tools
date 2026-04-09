from .fileutils import SizeBytes

class Peer:

    def __init__(self, server, infohash, pid):
        self.server = server
        self.id = pid
        self.banned = self.__banned(server)
        self.snubbed = self.__snubbed(server)
        self.infohash = infohash

    def id_html(self):
        return self.server._rpc.p.id_html()
    
    def address(self):
        return self.server._rpc.p.address(f'{self.infohash}:p{self.id}')

    def client_version(self):
        return self.server._rpc.p.client_version(f'{self.infohash}:p{self.id}')

    def completed_percent(self):
        return self.server._rpc.p.completed_percent(f'{self.infohash}:p{self.id}')

    def options_str(self):
        return self.server._rpc.p.options_str(f'{self.infohash}:p{self.id}')

    def down_rate(self):
        return SizeBytes(self.server._rpc.p.down_rate(f'{self.infohash}:p{self.id}'))

    def down_total(self):
        return SizeBytes(self.server._rpc.p.down_total(f'{self.infohash}:p{self.id}'))

    def up_rate(self):
        return SizeBytes(self.server._rpc.p.up_rate(f'{self.infohash}:p{self.id}'))

    def up_total(self):
        return SizeBytes(self.server._rpc.p.up_total(f'{self.infohash}:p{self.id}'))

    def peer_rate(self):
        return SizeBytes(self.server._rpc.p.peer_rate(f'{self.infohash}:p{self.id}'))

    def peer_total(self):
        return SizeBytes(self.server._rpc.p.peer_total(f'{self.infohash}:p{self.id}'))

    def port(self):
        return self.server._rpc.p.port(f'{self.infohash}:p{self.id}')

    def is_encrypted(self):
        return bool(self.server._rpc.p.is_encrypted(f'{self.infohash}:p{self.id}'))

    def is_incoming(self):
        return bool(self.server._rpc.p.is_incoming(f'{self.infohash}:p{self.id}'))

    def is_obfuscated(self):
        return bool(self.server._rpc.p.is_obfuscated(f'{self.infohash}:p{self.id}'))

    def is_preferred(self):
        return bool(self.server._rpc.p.is_preferred(f'{self.infohash}:p{self.id}'))

    def is_snubbed(self):
        return bool(self.server._rpc.p.is_snubbed(f'{self.infohash}:p{self.id}'))

    def is_unwanted(self):
        return bool(self.server._rpc.p.is_unwanted(f'{self.infohash}:p{self.id}'))

    def call_target(self):
        return self.server._rpc.p.call_target(f'{self.infohash}:p{self.id}')

    def disconnect(self):
        return self.server._rpc.p.disconnect(f'{self.infohash}:p{self.id}')

    def disconnect_delayed(self):
        return self.server._rpc.p.disconnect_delayed(f'{self.infohash}:p{self.id}')

    def __repr__(self):
        addr = f'{self.address()}:{self.port()}'
        return  f'{addr:22s} - {self.completed_percent():03d}% - {self.client_version():24s} - DR:{self.down_rate()} DT:{self.down_total()} UR:{self.up_rate()} UT:{self.up_total()}'

    class __banned:
        
        def __init__(self, server):
            self.server = server

        def __call__(self):
            return bool(self.server._rpc.p.banned(f'{self.infohash}:p{self.id}'))

        def set(self):
            return self.server._rpc.p.banned.set(self, value)

    class __snubbed:
        
        def __init__(self, server):
            self.server = server

        def __call__(self):
            return bool(self.server._rpc.p.snubbed(f'{self.infohash}:p{self.id}'))

        def set(self):
            return self.server._rpc.p.snubbed.set(self, value)
