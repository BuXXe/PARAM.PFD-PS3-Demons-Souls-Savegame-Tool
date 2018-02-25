# PARAM.PFD-PS3-Demons-Souls-Savegame-Tool
This script can open and decrypt PS3 savegame files protected by a PARAM.PFD. Furthermore it can re-encrypt modified files and integrate the modifications to the PARAM.PFD (signing). It was meant to be used for (Demon's Souls) savegame files but may work for other situations as well.

## Overview
The PARAM_PFD.py has all the things you need to do the decrypt / encrypt / sign stuff.  
The PARAM_SFO.py just parses the .SFO but it is never really used in the rest of the project  
The Main.py just shows the usage of the script.    
  
_<Demon's Souls specific part>:_   
_The savegame structure seems to use ???USER.DAT(??? are numbers) files of 256kb size each. The numbers imply some kind of hierarchy of the files. Each character has one (or more) .DAT file(s) (mostly these have lower numbers). A character file can be identified by looking at the offset 0xD4 - 0xF3 in a hex editor, which should show the character name. The offsets and adresses / structures which have been identified can be seen in the DemonsSouls/SaveGameEditor.py which can parse a ???USER.DAT character file and print the information. I just lost the motivation to really write a GUI for read AND write and due to the fact that nobody will ever use this thing except for me, I just think a hex editor serves this cause well enough. I add a template for the 010 Editor (by Sweetscape Software) which is a commercial hex editor (boohoo) that I experimented with during this project. The templating stuff is cool but I stick to free tools instead. There are some dirty hacks / missing parts in the templates as well so just see them as a nice to have. Big thanks again to the editor by Wulf2k from which I created the DemonSoulsResources.py library._  

## Requirements 
The tool is based on python 2.7 and uses the crypto library pycrypto which can be installed using `pip install pycrypto`
## Limits and TODOS
The tool is able to decrypt / encrypt protected files and resign the PARAM.PFD if files were changed. This is currently only tested for Demon's Souls savegame files. Right now there are these known limitations / TODOS:
* The PARAM.SFO can be parsed using the PARAM_SFO.py but the encryption / decryption is not done yet (reason: it uses some different mechanisms)

## Usage
``` python
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

```

## Documentation
I crawled through many different sources to get a good overview on the structure and mechanisms the PS3 uses to protect its files. In order to make it easier for others to get this insight I created some diagrams. I just wanted to save the knowledge so I did not put a focus on a standardized syntax. The diagrams were created using [Draw.io](http://www.draw.io), even though they don't force any mentioning I just want to put it here cause it is free and a really great toolbox. The draw.io .xml file for al diagrams is in the repo as well.  

#### PARAM.PFD Structure
![PARAM.PFD structure diagram](documentation/daw.io%20diagrams/pfdstructure.svg)  
#### PARAM.PFD decryption / encryption mechanisms
![PARAM.PFD decryption diagram](documentation/daw.io%20diagrams/decryption%20and%20encryption%20mechanisms/decrypt.svg)  
![PARAM.PFD encryption diagram](documentation/daw.io%20diagrams/decryption%20and%20encryption%20mechanisms/encrypt.svg)  
#### PARAM.PFD file modification process
After you have modified a decrypted file using a hex-editor or whatever you encrypt it back. Now you need to do these steps in this order to update the PARAM.PFD:
1. update the file hashes in the protected files table entries
1. update the y table signatures
1. calculate the y table HMACSHA1
1. calculate the tables_header+x table HMACSHA1
1. encrypt the header_table

![PARAM.PFD file hashes diagram](documentation/daw.io%20diagrams/PARAM.PFD%20rebuild%20process/filehashes.svg) 
![PARAM.PFD y table signatures diagram](documentation/daw.io%20diagrams/PARAM.PFD%20rebuild%20process/ytablesigs.svg) 
![PARAM.PFD xy table HMACSHA1 diagram](documentation/daw.io%20diagrams/PARAM.PFD%20rebuild%20process/xytablehmac.svg) 
![PARAM.PFD header table diagram](documentation/daw.io%20diagrams/PARAM.PFD%20rebuild%20process/headertable.svg) 



## Acknowledgments
The knowledge and motivation to build this project was, among others, based on [@Wulf2k](http://www.github.com/Wulf2k) who built a VB Demon's Souls savegame editor. I don't like VB and had some issues using it so i built this one using python. And of course the [PS3DevWiki](http://www.psdevwiki.com/ps3/)
