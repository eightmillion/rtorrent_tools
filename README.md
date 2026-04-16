# rtorrent_tools
-----
This is my rtorrent python XMLRPC/JSONRPC library. I've used it for years for managing a large (15000+) rtorrent instance. Most operations return a `TorrentGroup` object. This object can perform operations on that group of torrents.

-----
### Typical Usage
```python
In [1]: import rtorrent_tools
In [2]: rt = rtorrent_tools.Server('http://localhost/RPC2', jsonrpc=True)
In [3]: g = rt.matching_names('single.female.lawyer')
In [4]: g
Out [4]:
['Single.Female.Lawyer.S12E00.1080p.AMZN.WEB-DL.DDP2.0.H.264-NTb.mkv',
 'Single.Female.Lawyer.S12E01.1080p.AMZN.WEB-DL.DDP2.0.H.264-NTb.mkv',
 'Single.Female.Lawyer.S12E02.1080p.AMZN.WEB-DL.DDP2.0.H.264-NTb.mkv',
 'Single.Female.Lawyer.S12E03.1080p.AMZN.WEB-DL.DDP2.0.H.264-NTb.mkv',
 'Single.Female.Lawyer.S12E04.1080p.AMZN.WEB-DL.DDP2.0.H.264-NTb.mkv',
 'Single.Female.Lawyer.S12E05.1080p.AMZN.WEB-DL.DDP2.0.H.264-NTb.mkv',
 'Single.Female.Lawyer.S12E06.1080p.AMZN.WEB-DL.DDP2.0.H.264-NTb.mkv',
 'Single.Female.Lawyer.S12E07.1080p.AMZN.WEB-DL.DDP2.0.H.264-NTb.mkv',
 'Single.Female.Lawyer.S12E08.1080p.AMZN.WEB-DL.DDP2.0.H.264-NTb.mkv',
 'Single.Female.Lawyer.S12E09.1080p.AMZN.WEB-DL.DDP2.0.H.264-NTb.mkv',
 'Single.Female.Lawyer.S12E10.1080p.AMZN.WEB-DL.DDP2.0.H.264-NTb.mkv',
 'Single.Female.Lawyer.S12E11.1080p.AMZN.WEB-DL.DDP2.0.H.264-NTb.mkv']

In [5]: g.directory.set('/mnt/tv/single.female.lawyer/s01')
In [6]: g.set_create_resize()
In [7]: g.start_all()
