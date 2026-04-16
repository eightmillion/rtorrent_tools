# rtorrent_tools
-----
This is my rtorrent python XMLRPC/JSONRPC library. I've used it for years for managing a large (15000+) rtorrent instance. Most operations return a `TorrentGroup` object. This object can perform operations on that group of torrents.

-----
### Typical Usage
```python
In [1]: import rtorrent_tools
In [2]: rt = rtorrent_tools.Server('http://localhost/RPC2', jsonrpc=True)
In [3]: g = rt.matching_names('single.female.lawyer')
In [4]: g.directory.set('/mnt/tv/single.female.lawyer/s01')
In [5]: g.set_create_resize()
In [6]: g.start_all()
