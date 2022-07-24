import os.path

def Prepare(save):
    while 1:
        for ext in 'PFD','SFO':
            path1 = save+'/PARAM.'+ext
            b0 = os.path.isfile(path1)
            if not b0:
                print "File not found: %s" % path1
                save = raw_input("Enter valid save directory or X to eXit:\n")
                break
        if b0: break

    return save

# unused
def des_dec_chk():
    if "Demon's Souls" in param_sfo.Title: # can't access
        for u in param_pfd.protected_files_table:
            fn = u["file_name"].rstrip('\x00')
            if "USER.DAT" in fn:
                f1 = open(save+'/'+fn,'rb')
                b1 = f1.read(1)
                dec1 = (b1 == 0)
                if dec1: print "Looks like decrypted data."
                f1.close()
                break

def Crypt(save, sfid):

    from PARAM_PFD import PARAM_PFD

    # open the param_pfd in the given folder
    param_pfd = PARAM_PFD(save,sfid)

    x1 = save + '/~decrypted.txt'

    dec = os.path.isfile(x1)
    if dec: print "Files were decrypted earlier ... "
    todec = not dec
    
    ri1 = 'a'

    while 1:
        a0 = 'R'
        if todec: a0 = 'D'
        for i in (' '+"Enter C to "+a0+"eCrypt. F to change Folder. X to eXit").split('.'):
            print i[1:]+'.'
        ri1 = raw_input();
        if ri1 == 'C': 1
        elif ri1 in 'FX': break
        else: continue
        print a0+"ecrypting\n{" 
        param_pfd.cryptAllDatFiles_wrap(dec)
        print "}"
        if not todec: 
            print "Rebuilding PFD {"
            # updates the PFD to fit for the contents of the outputfolder
            # where the encrypted DAT Files are 
            param_pfd.rebuildPFD_wrap()
            print "} "
        if todec:
            open(x1,'w').close()
        else:
            os.remove(x1)
        todec = not todec
    return ri1

def GetSFID(cfg, save):
    if cfg == '': cfg = 'games.conf'
    from PARAM_SFO import PARAM_SFO
    global title0, sfid0
    param_sfo = PARAM_SFO(save) 

    print "Title: "+param_sfo.Title
    print "ID: "+param_sfo.ID

    if title0 == param_sfo.Title:
        print 'same sfid ' + sfid0
        return sfid0
    
    title0 = param_sfo.Title

    import games_conf 
    if games_conf.prepare(cfg) == 'X': return 'X'
    print "Reading "+cfg
    sfid = games_conf.scan(cfg, param_sfo)        
    
    sfid0 = sfid

    if sfid:
        print "sfid: '%s'" % sfid
    
    l1 = [
        ['NOTFOUND','game is not found in '+cfg],
        ['','null sfid'],
        ['UNPROTECTED','game is not protected']
        ]

    for i in l1:
        if sfid == l1[0]:
            raw_input(l1[1])
            return

    return sfid

sfid0 = ''
title0 = ''

def main(save, sfid, cfg):    
    while 1:
        while not os.path.isdir(save):
            save = raw_input('Enter save dir or X to eXit:\n')
            if save == 'X': return
        save = Prepare(save)
        if save == 'X': return
        for i in 1,2:
            if len(sfid) == 32: 
                if Crypt(save,sfid) == 'X': return
                break
            if i == 1: sfid = GetSFID(cfg, save)
            else: print "len(sfid) != 32"
            if sfid == 'X': return
        save = ''
        sfid = 'READFROMCFG'