import os.path, os

URL = 'https://github.com/Nicba1010/PS-Tools/raw/master/format/pfd/games.conf'

def download(cfg, URL):
    
    import urllib

    for i in ('Downloading',cfg,'from',URL): print i

    return urllib.urlretrieve(URL, cfg)

def prepare(cfg):
    # if os.path.isfile(cfg): os.remove(cfg) # dbg
    global URL
    while not os.path.isfile(cfg):
        for i in ("File not found: " + cfg, \
            "Enter G to download file from github.", \
            "Any key to check for file again.", \
            "X to eXit."):
            print i
        s1 = raw_input()
        if s1 == 'G': 
            if download(cfg, URL): print "Complete\n"
            else: print "Failed"
        if s1 == 'X': return s1
    return

def scan(cfg, param_sfo):    
    
    f1 = open(cfg)

    s1 = 1

    while f1.readline() != "; -- UNPROTECTED GAMES --\n": 1

    while s1 <> '\n':
        s1 = f1.readline()
        if s1.count(param_sfo.Title):
            f1.close()
            return 'UNPROTECTED'

    d1 = dict(Title = '; "',
            ID = '[',
            # dhk = ';disc_hash_key=', # we don't need it
            sfid = 'secure_file_id:*=')

    # dict is unsorted (actually reversed), 
    # thus unoptimized, but handy to use

    d2 = dict.fromkeys(d1)

    while s1 <> '':
        s1 = f1.readline()
        for i in d1:
            if not s1.startswith(d1[i]): continue
            if d1[i].count('='): s1 = s1.split('=')[1]
            d2[i] = s1[:-1]
            if i == 'sfid': 
                if d2['Title'].count(param_sfo.Title) \
                    or d2['ID'].count(param_sfo.ID):
                    f1.close()
                    return d2[i]
                else:
                    d2 = dict.fromkeys(d1)
            break
    
    f1.close()
    return 'NOTFOUND'
