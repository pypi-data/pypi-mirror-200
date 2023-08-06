import gc, socket, ssl, struct, os, zlib, io, binascii, hashlib, json, collections, time, sys

if not hasattr(gc, 'mem_free'):
  class FakeGC:
    def __init__(self):
      pass
    def mem_free(self):
      return 0
    def collect(self):
      pass
  gc = FakeGC()

try:
  from zlib import DecompIO as _DecompIO
  import cryptolib
  import machine
except ImportError:
  def _DecompIO(f):
    bytes = f.read()
    dco = zlib.decompressobj()
    dec = dco.decompress(bytes)
    f.seek(f.tell()-len(dco.unused_data))
    return io.BytesIO(dec)

print('Preallocating 32k buffer required for zlib decompression. Hold onto your butts...')
#print('mem_free before _master_decompio', gc.mem_free())
_master_decompio = _DecompIO(io.BytesIO(b'x\x9c\x03\x00\x00\x00\x00\x01'))
print('...done! mem_free:', gc.mem_free())

class DecompIO:

  def __init__(self, f):
    self._orig_f_pos = f.tell()
    self._orig_f = f
    self._pos = 0
    self._phoenix()
      
  def _phoenix(self):
    global _master_decompio
    before = gc.mem_free()
    self._orig_f.seek(self._orig_f_pos)
    gc.collect() # wtf - commenting out this line will cause OOM
    os.listdir()
    del _master_decompio
    gc.collect()
    _master_decompio = _DecompIO(self._orig_f)
    self._id = id(_master_decompio)
    self._pos = 0

  def read(self, nbytes):
    global _master_decompio
    assert self._id == id(_master_decompio)
    data = _master_decompio.read(nbytes)
    self._pos += len(data)
    return data
    
  def readline(self):
    global _master_decompio
    assert self._id == id(_master_decompio)
    data = _master_decompio.readline()
    self._pos += len(data)
    return data

  def seek(self, pos):
    global _master_decompio
    if pos < self._pos:
      #reset
      self._phoenix()
    while self._pos < pos:
      toss = _master_decompio.read(min(512,pos-self._pos))
      self._pos += len(toss)
    assert self._pos == pos
    

try:
  from btree import open as btree
except ImportError:
  import pickle

try: FileNotFoundError
except NameError:
  FileNotFoundError = OSError

Commit = collections.namedtuple("Commit", ("tree", "author"))

class DB:
  def __init__(self, fn):
    self._fn = fn
    self._f = None

  def __enter__(self):
    try:
      btree
      try:
        self._f = open(self._fn, "r+b")
      except OSError:
        self._f = open(self._fn, "w+b")
      self._db = btree(self._f, pagesize=512)
    except NameError:
      try:
        with open(self._fn,'rb') as f:
          self._db = pickle.load(f)
      except FileNotFoundError:
        self._db = {}
    return self
    
  def __exit__(self, type, value, traceback):
    if hasattr(self._db, 'close'):
      self._db.close()
    else:
      with open(self._fn,'wb') as f:
        pickle.dump(self._db, f)
    if self._f: self._f.close()

  def __setitem__(self, key, item):
    self._db[key] = item

  def __getitem__(self, key):
    return self._db[key]

  def get(self, key, default=None):
    return self._db.get(key, default)

  def __delitem__(self, key):
    del self._db[key]

  def keys(self):
    return self._db.keys()

  def values(self):
    return self._db.values()

  def items(self):
    return self._db.items()

  def __contains__(self, item):
    return item in self._db

  def __iter__(self):
    return iter(self._db)

  def flush(self):
    if hasattr(self._db, 'flush'):
      self._db.flush()
     

def _read_headers(x):
  while line:=x.readline():
    #print('resp header', line)
    if line.startswith(b'HTTP/1.0') and not line.startswith(b'HTTP/1.0 200'):
      raise Exception(line.decode().strip())
    if not line.strip(): break

def _read_kind_size(f):
  byt = struct.unpack("B", f.read(1))[0]
  kind = (byt & 0x70) >> 4
  size = byt & 0x0F
  offset = 4
  while byt & 0x80:
    byt = struct.unpack("B", f.read(1))[0]
    size += (byt & 0x7F) << offset
    offset += 7
  return kind, size

def _read_little_size(f):
  size = bshift = 0
  while True:
    byt = f.read(1)[0]
    size |= (byt & 0x7f) << bshift
    if byt & 0x80 == 0:
      break
    bshift += 7
  return size

def _read_offset(f):
  offset = 0
  while True:
    byt = f.read(1)[0]
    offset = (offset << 7) | (byt & 0x7f)
    if byt & 0x80 == 0:
      break
    offset += 1
  return offset
  
  
_ODSDeltaCmd = collections.namedtuple("_ODSDeltaCmd", ('start','append','base_start','nbytes'))

class _ObjReader:

  def __init__(self, f):
    self.f = f
    self.start = f.tell()
    self.kind, self.size = _read_kind_size(f)
  
  # https://git-scm.com/docs/pack-format#_deltified_representation
  def _parse_ods_delta(self):
    if hasattr(self, 'cmds'): return
    offset = _read_offset(self.f)
    self.base_object_offset = self.start - offset
    dec_stream = DecompIO(self.f)
    self.cmds = []
    pos = 0
    base_size = _read_little_size(dec_stream)
    self.size = obj_size = _read_little_size(dec_stream)
    while ch := dec_stream.read(1):
      byt = ch[0]
      if byt == 0x00: continue
      if (byt & 0x80) != 0: # copy command
        vals = io.BytesIO()
        for i in range(7):
          bmask = 1 << i
          if (byt & bmask) != 0:
            vals.write(dec_stream.read(1))
          else:
            vals.write(b'\x00')
        start = int.from_bytes(vals.getvalue()[0:4], 'little')
        nbytes = int.from_bytes(vals.getvalue()[4:6], 'little')
        if nbytes == 0:
          nbytes = 0x10000
        self.cmds.append(_ODSDeltaCmd(pos, None, start, nbytes))
        pos += nbytes
      else: # append command
        nbytes = byt & 0x7f
        to_append = dec_stream.read(nbytes)
        assert nbytes==len(to_append)
        self.cmds.append(_ODSDeltaCmd(pos, to_append, None, nbytes))
        pos += nbytes

  def __enter__(self):
    if self.kind==6: # ofs-delta
      self._parse_ods_delta()
      self.return_to_pos = self.f.tell()
      self.pos = 0
      self.f.seek(self.base_object_offset)
      self.base_obj_reader = _ObjReader(self.f)
      self.base_obj_pos = None
      return self
    else:
      self.decompressed_stream = DecompIO(self.f)
      return self.decompressed_stream
  
  def __exit__(self, type, value, traceback):
    if self.kind==6:
      del self.base_obj_pos
      self.base_obj_reader.__exit__(None, None, None)
      del self.base_obj_reader
      if hasattr(self, 'decompressed_stream'):
        del self.decompressed_stream
      self.f.seek(self.return_to_pos)
    else:
      pass
    
  def read(self, nbytes):
    if not nbytes: return b''
    ret = io.BytesIO()
#    print('===============read', nbytes, 'from position',self.pos)
    for cmd in self.cmds:
      if cmd.start+cmd.nbytes < self.pos: continue
#      print('cmd',cmd, 'self.pos', self.pos, 'nbytes',nbytes)
      if cmd.append:
        to_append = cmd.append[self.pos-cmd.start:min(nbytes,cmd.nbytes)]
      else:
        if self.base_obj_pos is None:
#          print('base_obj_reader.__enter__()')
          self.base_obj_reader.__enter__()
          self.base_obj_pos = 0
#        print('cmd.base_start+self.pos-cmd.start', cmd.base_start, self.pos, cmd.start)
        self.base_obj_reader.decompressed_stream.seek(cmd.base_start+self.pos-cmd.start)
        to_append = self.base_obj_reader.decompressed_stream.read(min(nbytes,cmd.nbytes-(self.pos-cmd.start)))
      ret.write(to_append)
      nbytes -= len(to_append)
      self.pos += len(to_append)
#      print('>',to_append)
      os.listdir()
      if nbytes < 1: break
    ret = ret.getvalue()
    return ret

  def digest(self):
    print('#',end='')
    kind = self.kind
    with self as f:
      if kind==6:
        kind = self.base_obj_reader.kind
      h = hashlib.sha1()
      if kind==1: h.update(b'commit ')
      elif kind==2: h.update(b'tree ')
      elif kind==3: h.update(b'blob ')
      else: raise Exception('unknown kind', kind)
      h.update(str(self.size).encode())
      h.update(b'\x00')
      while data := f.read(512):
        h.update(data)
    digest = h.digest()
    return digest
    
  
def _read_until(f, stop_byte):
  buf = io.BytesIO()
  while byt:=f.read(1):
    buf.write(byt)
    if byt==stop_byte: break
  return buf.getvalue()

    
def _parse_pkt_file(git_dir, fn, pkt_id, db):
#  pkt_id = int(fn.split('.')[0])
  with open(fn,'rb') as f:
    assert f.read(4)==b'PACK'
    version = struct.unpack('!I', f.read(4))[0]
    del version
    cnt = struct.unpack('!I', f.read(4))[0]
    #print('reading', cnt, 'objs from', fn)
    for i in range(cnt):
      fpos = f.tell()
      o = _ObjReader(f)
      kind = o.kind
      size = o.size
      assert kind!=0
      idx = struct.pack('QBQQQ', pkt_id, kind, f.tell(), size, fpos)
      sig = o.digest()
      db[sig] = idx
    print()
    #TODO parse tail, which is hash of packet
    #print('done at', f.tell(), 'remaining', len(f.read()))


def _iter_pkt_lines(x, f=None):
  ticks = False
  while pkt_bytes := x.read(4):
    pkt_bytes = int(pkt_bytes,16)
    pkt_bytes -= 4
    if pkt_bytes>0:
      buf = io.BytesIO()
      channel = x.read(1)
      pkt_bytes -= 1
      if channel==b'\x01':
        while pkt_bytes>0:
          data = x.read(min(512,pkt_bytes))
          pkt_bytes -= len(data)
          if f: f.write(data)
#        print('>',end='')
        if ticks:
          sys.stdout.write('>')
        else:
          ticks = True
          # skip the first tick
      else:
        buf.write(channel)
        while pkt_bytes>0:
          bits = x.read(min(512,pkt_bytes))
          if not bits: break
          pkt_bytes -= len(bits)
          buf.write(bits)
        data = buf.getvalue()
        if ticks:
          sys.stdout.write('\n')
          ticks = False
        yield data


def _isdir(fn):
  try:
    return (os.stat(fn)[0] & 0x4000) != 0
  except OSError:
    return False


def _rmrf(directory):
  git_dir = f'{directory}/.ygit'
  if _isdir(git_dir):
    print('removing ygit repo at', git_dir)
    for fn in os.listdir(git_dir):
      os.remove(f'{directory}/.ygit/{fn}')
    os.rmdir(git_dir)


def clone(url, directory='.', *, username=None, password=None, ref='HEAD', shallow=True, cone=None, quiet=False):
  if isinstance(ref,str):
    ref = ref.encode()
  print(f'cloning {url} into {directory} @ {ref.decode()}')
  repo = Repo(directory)
  repo._init(url, cone=cone, username=username, password=password)
  repo.pull(quiet=quiet, shallow=shallow, ref=ref)
  return repo


class Repo:


  def __init__(self, directory='.'):
    self._dir = directory

    
  @property
  def _git_dir(self):
    return f'{self._dir}/.ygit'
    
    
  def update_authentication(self, username, password, url=None):
    with DB(f'{self._git_dir}/config') as db:
      self._save_auth(db, username, password, url=url)
    
    
  def _save_auth(self, db, username, password, url=None):
    if isinstance(url, str):
      url = url.encode()
    c = cryptolib.aes(b'ygit'+binascii.hexlify(machine.unique_id()).decode(),1)
    s = f'{username}:{password}'.encode()
    b64 = b'Basic '+binascii.b2a_base64(s)[:-1]
    if len(b64)%16:
      b64 += b' '*(16-len(b64)%16) # right pad to %16 bytes long
    encrypted = c.encrypt(b64)
    if not url:
      url = db[b'repo']
    db[b'Basic HTTP auth for '+url] = encrypted
    

    
  def _git_upload_pack(self, url, data=None):
    gc.collect()
    proto, _, host, path = url.split("/", 3)
    port = 443 if proto=='https:' else 80
    if ':' in host:
      host, port = host.split(':',1)
      port = int(port)
    method = 'POST' if data else 'GET'
    endpoint = 'git-upload-pack' if method=='POST' else 'info/refs?service=git-upload-pack'
    s = socket.socket()
    s.connect((host, port))
    if proto=='https:':
      s = ssl.wrap_socket(s)
    x = s.makefile("rb") if hasattr(s,'makefile') else s
    send = s.send if hasattr(s,'send') else s.write
    req = f'{method} /{path}/{endpoint} HTTP/1.0\r\n'
    send(req.encode())
    headers = {
      'Host': host,
      'User-Agent': 'ygit/0.0.1',
      'Accept': '*/*',
    }
    with DB(f'{self._git_dir}/config') as db:
      if b'Basic HTTP auth for '+url.encode() in db:
        auth = db[b'Basic HTTP auth for '+url.encode()]
        c = cryptolib.aes(b'ygit'+binascii.hexlify(machine.unique_id()).decode(),1)
        headers['Authorization'] = c.decrypt(auth).decode().strip()
    if data:
      headers['Content-Type'] = 'application/x-git-upload-pack-request'
      headers['Accept'] = 'application/x-git-upload-pack-result'
      headers['Accept-Encoding'] = 'deflate, gzip, br, zstd'
      headers['Git-Protocol'] = 'version=2'
      headers['Content-Length'] = str(len(data))
    for k,v in headers.items():
      send(f'{k}: {v}\r\n'.encode())
      #print('k,v', k,v)
    send(b'\r\n')
    if data:
      send(data)
    return s,x


  def _init(self, repo, cone=None, username=None, password=None):
    git_dir = self._git_dir
    if _isdir(git_dir):
      raise Exception(f'fatal: ygit repo already exists at {git_dir}')
    if not _isdir(self._dir):
      os.mkdir(self._dir)
    os.mkdir(git_dir)
    with DB(f'{git_dir}/config') as db:
      db[b'repo'] = repo.encode()
      if cone:
        db[b'cone'] = cone.encode()
      if username and password:
        self._save_auth(db, username, password)


  def checkout(self, ref='HEAD'):
    git_dir = self._git_dir
    commit = self._ref_to_commit(git_dir, ref)
    if not commit:
      raise Exception(f'unknown ref: {ref}')
    with DB(f'{git_dir}/idx') as db:
      print('checking out', commit.decode())
      commit = self._get_commit(git_dir, db, commit)
      for mode, fn, digest in self._walk_tree(git_dir, db, self._dir, commit.tree):
        #print('entry', repr(mode), int(mode), fn, binascii.hexlify(digest) if digest else None)
        if int(mode)==40000:
          if not _isdir(fn):
            os.mkdir(fn)
        elif int(mode)==160000:
          print('ignoring submodule:', fn)
        else:
          self._checkout_file(git_dir, db, fn, digest)


  def status(self, out=sys.stdout, ref='HEAD'):
    changes = False
    git_dir = self._git_dir
    commit = self._ref_to_commit(git_dir, ref)
    if not commit:
      raise Exception(f'unknown ref: {ref}')
    with DB(f'{git_dir}/idx') as db:
      print('status of', commit.decode())
      commit = self._get_commit(git_dir, db, commit)
      for mode, fn, digest in self._walk_tree(git_dir, db, self._dir, commit.tree):
        if int(mode)==40000:
          if not _isdir(fn):
            out.write(f'A {fn}\n')
            changes = True
        else:
          status = self._checkout_file(git_dir, db, fn, digest, write=False)
          if status:
            out.write(f'{status} {fn[len(self._dir):]}\n')
            changes = True
    return changes


  def _checkout_file(self, git_dir, db, fn, ref, write=True):
    if ref not in db:
      raise Exception(f'unknown ref for file:{fn} sig:{binascii.hexlify(ref)}')
    ref_data = db[ref]
    pkt_id, kind, pos, size, ostart = struct.unpack('QBQQQ', ref_data)
    assert kind in (3,6)
    h = hashlib.sha1()
    h.update(b'blob ')
    h.update(str(size).encode())
    h.update(b'\x00')
    try:
      with open(fn,'rb') as f:
        while data:=f.read(1024):
          h.update(data)
      status = 'M' if h.digest()!=ref else None
    except FileNotFoundError:
      status = 'D'
    if status and write:
      if kind==3: kind = 'BLOB'
      if kind==6: kind = 'OFS_DELTA'
      print('writing:', fn, f'({kind})')
      pkt_fn = f'{git_dir}/{pkt_id}.pack'
      with open(pkt_fn, 'rb') as pkt_f:
        pkt_f.seek(ostart)
        with _ObjReader(pkt_f) as fin:
          with open(fn, 'wb') as fout:
            while data:=fin.read(512):
              fout.write(data)
          del fin
    return status


  def _get_commit(self, git_dir, db, commit):
    if binascii.unhexlify(commit) not in db:
      self._fetch(git_dir, db, True, False, commit)
    idx = db[binascii.unhexlify(commit)]
    pkt_id, kind, pos, size, ostart = struct.unpack('QBQQQ', idx)
    assert kind==1
    fn = f'{git_dir}/{pkt_id}.pack'
    with open(fn, 'rb') as f:
      f.seek(pos)
      s1 = DecompIO(f)
      tree, author = None, None
      while line:=s1.readline():
        if line==b'\n': break
        k,v = line.split(b' ',1)
        if k==b'tree': tree = v.strip().decode()
        if k==b'author': author = v.strip().decode()
      del s1
    return Commit(tree, author)

  
  def _walk_tree(self, git_dir, db, directory, ref):
    if isinstance(ref, str):
      ref = binascii.unhexlify(ref)
    data = db[ref]
    pkt_id, kind, pos, size, ostart = struct.unpack('QBQQQ', data)
    assert kind==2
    fn = f'{git_dir}/{pkt_id}.pack'
    with open(fn, 'rb') as f:
      f.seek(pos)
      next = []
      s2 = DecompIO(f)
      to_yield = []
      while line:=_read_until(s2, b'\x00'):
        digest = s2.read(20)
        mode, fn = line[:-1].decode().split(' ',1)
        fn = f'{directory}/{fn}'
        if mode=='40000':
          to_yield.append((mode, fn, None))
          next.append((fn, digest))
        if mode=='160000':
          print('ignoring submodule', fn,'(unsupported)')
        else:
          to_yield.append((mode, fn, digest))
      yield from to_yield
      for fn, digest in next:
        yield from self._walk_tree(git_dir, db, fn, digest)


  def pull(self, shallow=True, quiet=False, ref='HEAD'):
    if self.fetch(quiet=quiet, shallow=shallow, ref=ref):
      self.checkout(ref=ref)


  def branches(self):
    git_dir = self._git_dir
    with DB(f'{git_dir}/refs') as db:
      return [k[len(b'refs/heads/'):].decode() for k in db if k.startswith(b'refs/heads/')]
  

  def tags(self):
    git_dir = self._git_dir
    with DB(f'{git_dir}/refs') as db:
      return [k[len(b'refs/tags/'):].decode() for k in db if k.startswith(b'refs/tags/')]

    
  def pulls(self):
    git_dir = self._git_dir
    with DB(f'{git_dir}/refs') as db:
      return [k[len(b'refs/pull/'):].decode() for k in db if k.startswith(b'refs/pull/')]
  

  def _ref_to_commit(self, git_dir, ref):
    if isinstance(ref,str):
      ref = ref.encode()
    if len(ref)==40:
      return ref
    with DB(f'{git_dir}/refs') as db:
      for possible_ref in [ref, b'refs/heads/'+ref, b'refs/tags/'+ref, b'refs/pull/'+ref]:
        if possible_ref in db:
         return binascii.hexlify(db[possible_ref])
    return None

  
  def fetch(self, shallow=True, quiet=False, ref='HEAD'):
    directory = self._dir
    if isinstance(ref,str):
      ref = ref.encode()
    git_dir = f'{directory}/.ygit'
    with DB(f'{git_dir}/config') as db:
      repo = db[b'repo'].decode()
    print(f'fetching: {repo} @ {ref.decode()}')

    s,x = self._git_upload_pack(repo)
    _read_headers(x)
    capabilities = None
    with DB(f'{git_dir}/refs') as db:
      for packline in _iter_pkt_lines(x):
        if packline.startswith(b'#'): continue
        if b'\x00' in packline:
          packline, capabilities = packline.split(b'\x00', 1)
        arev, aref = packline.split(b' ', 1)
        aref = aref.strip()
        db[aref] =binascii.unhexlify(arev)
      HEAD = binascii.hexlify(db[b'HEAD']) if b'HEAD' in db else None # empty repo
    s.close()
    
    commit = self._ref_to_commit(git_dir, ref)

  #  if requested_rev==b'HEAD':
  #    s,x = _request(repo, data=b'0014command=ls-refs\n0014agent=git/2.37.20016object-format=sha100010009peel\n000csymrefs\n000bunborn\n0014ref-prefix HEAD\n001bref-prefix refs/heads/\n0000')
  #    _read_headers(x)
  #    ORIG_HEAD = _read_pkt_lines(x, git_dir)[0]
  #    s.close()
  #    print('ORIG_HEAD', ORIG_HEAD, requested_rev, rev)

    with DB(f'{git_dir}/idx') as db:
      return self._fetch(git_dir, db, shallow, quiet, commit)


  def _fetch(self, git_dir, db, shallow, quiet, commit):
    assert commit is None or isinstance(commit, bytes) and len(commit)==40 # only full hashes here

    with DB(f'{git_dir}/config') as config_db:
      repo = config_db[b'repo'].decode()

    if commit:
      print(f'fetching commit: {commit.decode()}')
    else:
      print('fetched an empty repo')
      return False

    if binascii.unhexlify(commit) in db:
      print('up to date!')
      return False

    cmd = io.BytesIO()
    cmd.write(b'0011command=fetch0014agent=git/2.37.20016object-format=sha10001000dofs-delta')
    if quiet: cmd.write(b'000fno-progress')
    if quiet: cmd.write(b'000finclude-tag')
    if shallow: cmd.write(b'000cdeepen 1')
    if False: cmd.write(b'0014filter blob:none') # blobless clone
    cmd.write(f'0032want {commit.decode()}\n'.encode())
    for k in db.keys():
      if k==b'HEAD': continue
      have = f'0032have {binascii.hexlify(k).decode()}\n'
      print(repr(have))
      cmd.write(have.encode())
    cmd.write(b'0009done\n0000')
    s,x = self._git_upload_pack(repo, data=cmd.getvalue())
    _read_headers(x)
    db.flush()

    i = len([s for s in os.listdir(git_dir) if s.endswith('.pack')])+1
    fn = f'{git_dir}/{i}.pack'
    with open(fn,'wb') as f:
      for packline in _iter_pkt_lines(x, f=f):
        if packline.startswith(b'\x02'):
          print(packline[1:].decode().strip())
        if packline.startswith(b'\x03'):
          raise Exception(packline[1:].decode().strip())
    _parse_pkt_file(git_dir, fn, i, db)

    s.close()
    return True



