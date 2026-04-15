#!/usr/bin/env python

from types import FunctionType
import pprint
from collections.abc import Sequence
from collections import namedtuple
from .torrent import Torrent
from .fileutils import SizeBytes
from .jsonrpcproxy import *
import re
import datetime
import sys
import time
import xmlrpc

class TorrentGroup(Sequence):

    '''List-like group object for Torrent objects.
    Works with normal list methods.'''

    def __init__(self, *items):
        self.data = list(items)
        self.down = self.__down(self)
        self.up = self.__up(self)

    def __len__(self):
        return len(self.data)

    def pop(self, value=False):
        if value:
            return self.data.pop(value)
        return self.data.pop()

    def __getitem__(self, value):
        if isinstance(value, slice):
            return TorrentGroup(*self.data[value])
        else:
            return self.data[value]

    class __down:

        def __init__(self, group):
            self.group = group

        def total(self):
            if not self.group.data:
                return SizeBytes(0)
            mc = self.group.data[0].server.get_mc_proxy()
            for torrent in self.group.data:
                mc.d.down.total(torrent.hash)
            return SizeBytes(sum(mc()))

        def rate(self):
            '''returns SizeByte object containing the current
            total download rate of all the Torrents in the group'''
            if not self.group.data:
                return SizeBytes(0)
            mc = self.group.data[0].server.get_mc_proxy()
            for torrent in self.group.data:
                mc.d.down.rate(torrent.hash)
            return SizeBytes(sum(mc()))

    class __up:

        def __init__(self, group):
            self.group = group

        def total(self):
            if not self.group.data:
                return SizeBytes(0)
            mc = self.group.data[0].server.get_mc_proxy()
            for torrent in self.group.data:
                mc.d.up.total(torrent.hash)
            return SizeBytes(sum(mc()))

        def rate(self):
            if not self.group.data:
                return SizeBytes(0)
            mc = self.group.data[0].server.get_mc_proxy()
            for torrent in self.group.data:
                mc.d.up.rate(torrent.hash)
            return SizeBytes(sum(mc()))

    def remove(self, value):
        self.data.remove(value)

    def append(self, value):
        self.data.append(value)

    def erase_all(self):
        '''removes all Torrents in group from rtorrent'''
        for torrent in self.data[:]:
            if torrent.erase():
                self.data.remove(torrent)

    def erase_all_with_files(self):
        '''removes all Torrents in group from rtorrent
        and deletes data from disk. use with caution'''
        for torrent in self.data[:]:
            if torrent.erase_with_files():
                self.data.remove(torrent)

    def stop_all(self):
        '''stops all torrents in group'''
        if not self.data:
            return []
        mc = self.group.data[0].server.get_mc_proxy()
        for torrent in self.data:
            mc.d.stop(torrent.hash)
        return list(mc())

    def start_all(self):
        '''starts all torrents in group'''
        if not self.data:
            return []
        mc = self.group.data[0].server.get_mc_proxy()
        for torrent in self.data:
            mc.d.start(torrent.hash)
        return list(mc())

    def pause_all(self):
        '''pauses all torrents in group'''
        if not self.data:
            return []
        mc = self.group.data[0].server.get_mc_proxy()
        for torrent in self.data:
            mc.d.pause(torrent.hash)
        return list(mc())

    def resume_all(self):
        '''resumes all torrents in group'''
        if not self.data:
            return []
        mc = self.group.data[0].server.get_mc_proxy()
        for torrent in self.data:
            mc.d.resume(torrent.hash)
        return list(mc())

    def open_all(self):
        '''opens all torrents in group'''
        if not self.data:
            return []
        mc = self.group.data[0].server.get_mc_proxy()
        for torrent in self.data:
            mc.d.open(torrent.hash)
        return list(mc())

    def close_all(self):
        '''closes all torrents in group'''
        if not self.data:
            return []
        mc = self.group.data[0].server.get_mc_proxy()
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
        mc = self.group.data[0].server.get_mc_proxy()
        for torrent in self.data:
            mc.d.size_bytes(torrent.hash)
        return sum(mc())

    def complete(self):
        '''returns True if all the Torrents in the group
        are complete'''
        if not self.data:
            return True
        mc = self.group.data[0].server.get_mc_proxy()
        for torrent in self.data:
            mc.d.complete(torrent.hash)
        return all(mc())

    def hashing(self):
        '''returns True if any of the Torrents in the group are hashing'''
        if not self.data:
            return False
        mc = self.group.data[0].server.get_mc_proxy()
        for torrent in self.data:
            mc.d.hashing(torrent.hash)
        return any(mc())

    @property
    def ratio(self):
        '''returns the total overall ratio of all the Torrents in the group'''
        if not self.data:
            return 0
        mc = self.group.data[0].server.get_mc_proxy()
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
        try:
            return TorrentGroup(*ret)
        except:
            return ret

    def unregistered(self):
        return self.filter(lambda x: x.is_unregistered())

    def set_throttle_name(self, name):
        '''sets a throttle name for each Torrent in the group.'''
        self.pause_all()
        mc = self.data[0].server.get_mc_proxy()
        for torrent in self:
            mc.d.throttle_name.set(torrent.hash, name)
        mc()
        self.resume_all()

    def sort(self):
        self.data.sort()

    def multicall(self, arg):
        if not self.data:
            return []
        mc = self.data[0].server.get_mc_proxy()
        for torrent in self:
            mc._MultiCall__call_list.append(
                (arg, (torrent.hash,))
            )
        return list(mc())

    def __repr__(self):
        return pprint.pformat(self.data, width=120)

