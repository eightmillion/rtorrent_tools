from collections.abc import Sequence
from collections import namedtuple
import pprint
import datetime
import time

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

    def set_create_queued(self, value=''):
        return self.server._rpc.f.set_create_queued(
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
            print(type(item))
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
        return float(self)/float(a)

    def __rdiv__(self, a):
        return float(a)/float(self)

    def __truediv__(self, a):
        return float(self)/float(a)

    def __mul__(self, a):
        return float(self)*float(a)

    def __rmul__(self, a):
        return float(self)*float(a)

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

chunk = lambda hashes, l=100: [hashes[x:x+l] for x in range(0, len(hashes), l)]
