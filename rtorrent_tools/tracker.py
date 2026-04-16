
class Tracker:

    def __init__(self, server, url, hash, index):
        self.server = server
        self.url = url
        self.hash = hash
        self.index = index
        self.idx = 0

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
        return iter(self.url)

    def __contains__(self, sub):
        return sub in self.url

    def __next__(self):
        self.idx += 1
        try:
            return self.url[self.idx-1]
        except IndexError:
            self.idx = 0
            raise StopIteration from None

    def __repr__(self):
        return str(self.url)

    def __str__(self):
        return str(self.url)

    def __unicode__(self):
        return str(self.url)

