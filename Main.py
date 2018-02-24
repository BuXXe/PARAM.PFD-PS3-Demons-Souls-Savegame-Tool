from PARAM_PFD import PARAM_PFD

# open the param_pfd in the given folder
param_pfd = PARAM_PFD("BLES00932DEMONSS005")

# decrypt the DAT Files from sourcefolder to targetfolder
param_pfd.decryptAllDatFiles("BLES00932DEMONSS005","Decrypted")

# encrypt the DAT Files from sourcefolder to targetfolder
param_pfd.encryptAllDatFiles("Decrypted","Recrypt")

# updates the PFD to fit for the contents of the outputfolder
# where the encrypted DAT Files are 
param_pfd.rebuildPFD("Recrypt")
