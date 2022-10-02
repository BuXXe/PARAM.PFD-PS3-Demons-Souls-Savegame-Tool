import UI

cfg =   ""
save =  ""
sfid =  ""

#cfg = 'games.conf'
#save = 'BLES00932DEMONSS005'
#sfid = 'READFROMCFG'

import sys; 
if len(sys.argv) == 2:
    save = sys.argv[1]

UI.main(save,sfid,cfg)

# todo: 
# +/- store save_path
# new class: ui / save manager: self.pfd, sfo
# bool for getsfid == 32
# gcf class ?