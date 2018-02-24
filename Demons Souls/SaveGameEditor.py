from binascii import hexlify,unhexlify
from DemonSoulsResources import ResourceLibrary
import struct

# holds known information for a Demon Souls Savegame
# unknown blocks are not yet interpreted
class DemonsSoulsSaveGame:
    Library = ResourceLibrary()    
    GameInfo = {}
    PlayerStatus = {}
    PlayerEquipment = {}
    Inventory = {}
    SpellsandMiracles = {}
    Deposit = {}
    
    def readGameInfo(self, f):
        f.seek(0x4)
        self.GameInfo["World_Index"]=f.read(1)
        self.GameInfo["Block_Index"]=f.read(1)

        f.seek(0x1EBF8)
        self.GameInfo["Nexus_Tendency"]=f.read(4)
        self.GameInfo["_Nexus_Tendency_Copy?"]=f.read(4)
        
        self.GameInfo["World1_Tendency"]=f.read(4)
        self.GameInfo["_World1_Tendency_Copy?"]=f.read(4)
        
        self.GameInfo["World4_Tendency"]=f.read(4)
        self.GameInfo["_World4_Tendency_Copy?"]=f.read(4)

        self.GameInfo["World3_Tendency"]=f.read(4)
        self.GameInfo["_World3_Tendency_Copy?"]=f.read(4)

        self.GameInfo["World5_Tendency"]=f.read(4)
        self.GameInfo["_World5_Tendency_Copy?"]=f.read(4)

        self.GameInfo["World2_Tendency"]=f.read(4)
        self.GameInfo["_World2_Tendency_Copy?"]=f.read(4)
        
    def ShowGameInfo(self):
        tendencies = [struct.unpack(">f", self.GameInfo[u])[0] for u in ["Nexus_Tendency","World1_Tendency","World2_Tendency","World3_Tendency","World4_Tendency","World5_Tendency"]]
        print "Game Info:"
        print u"\u2554" + u"\u2550" * 15 + (u"\u2566" * 1 + u"\u2550" * 16)  + u"\u2557"
        print u"\u2551World Index: %2i\u2551 Block Index: %2i\u2551" % (ord(self.GameInfo["World_Index"]),ord(self.GameInfo["Block_Index"]))

        print u"\u2560" + u"\u2550" * 15 + u"\u2569" + u"\u2566" * 1 + u"\u2550" * 8 + u"\u2566" * 1 + u"\u2550" * 6 +u"\u2569" +u"\u2550"+(u"\u2566" * 1 + u"\u2550" * 8) * 4 + u"\u2557"
        
        print (u"\u2551%16s" + (u"\u2551%8s")*6 + u"\u2551") % ("","Nexus","World1","World2","World3","World4","World5")
        print (u"\u2551%16s" + (u"\u2551%8i")*6 + u"\u2551") % tuple(["World Tendencies"]+tendencies)

        print u"\u255A" + u"\u2550" * 16 + (u"\u2569" * 1 + u"\u2550" * 8) * 6 + u"\u255D"

    def readPlayerStatus(self, f):
        f.seek(0x50)
        self.PlayerStatus["Current_HP"]=f.read(4)
        self.PlayerStatus["_Current_HP_Copy?"]=f.read(4)
        self.PlayerStatus["Maximum_HP"]=f.read(4)
        
        self.PlayerStatus["Current_MP"]=f.read(4)
        self.PlayerStatus["_Current_MP_Copy?"]=f.read(4)
        self.PlayerStatus["Maximum_MP"]=f.read(4)
        
        self.PlayerStatus["Current_Stamina"]=f.read(4)
        self.PlayerStatus["_Current_Stamina_Copy?"]=f.read(4)
        self.PlayerStatus["Maximum_Stamina"]=f.read(4)
        
        self.PlayerStatus["Vitality"]=f.read(4)
        self.PlayerStatus["_Vitality_Copy?"]=f.read(4)
        
        self.PlayerStatus["Intelligence"]=f.read(4)
        self.PlayerStatus["_Intelligence_Copy?"]=f.read(4)
        
        self.PlayerStatus["Endurance"]=f.read(4)
        self.PlayerStatus["_Endurance_Copy?"]=f.read(4)
        
        self.PlayerStatus["Strength"]=f.read(4)
        self.PlayerStatus["_Strength_Copy?"]=f.read(4)
        
        self.PlayerStatus["Dexterity"]=f.read(4)
        self.PlayerStatus["_Dexterity_Copy?"]=f.read(4)
        
        self.PlayerStatus["Magic"]=f.read(4)
        self.PlayerStatus["_Magic_Copy?"]=f.read(4)
        
        self.PlayerStatus["Faith"]=f.read(4)
        self.PlayerStatus["_Faith_Copy?"]=f.read(4)
        
        self.PlayerStatus["Luck"]=f.read(4)
        self.PlayerStatus["_Luck_Copy?"]=f.read(4)

        f.seek(0xBC)
        self.PlayerStatus["Current_Souls"]=f.read(4)

        f.seek(0xC8)
        self.PlayerStatus["Soul_Memory"]=f.read(4)
        self.PlayerStatus["Levels_Purchased"]=f.read(4)

        f.seek(0xD4)
        # Unicode Name (bytes are: 00 charbyte 00 charbyte ...) with 16 Chars Max
        self.PlayerStatus["Character_Name"]=f.read(32)

        # 0 is female
        f.seek(0xF6)
        self.PlayerStatus["Gender"]=f.read(1)

        f.seek(0xFB)
        self.PlayerStatus["Starting_Class"]=f.read(1)

        f.seek(0x2B4)
        self.PlayerStatus["Hairstyle"]=f.read(4)

        f.seek(0x14368)
        self.PlayerStatus["Hair_Color_R"]=f.read(4)
        self.PlayerStatus["Hair_Color_G"]=f.read(4)
        self.PlayerStatus["Hair_Color_B"]=f.read(4)

        f.seek(0x1EBF0)
        self.PlayerStatus["Character_Tendency"]=f.read(4)
        self.PlayerStatus["_Character_Tendency_Copy?"]=f.read(4)

    def ShowPlayerStatus(self):
        print "Player Status:"

        R,G,B = [struct.unpack(">f", self.PlayerStatus[u])[0] for u in ["Hair_Color_R","Hair_Color_G","Hair_Color_B"]]
        Gender = ["Female","Male"][ord(self.PlayerStatus["Gender"])]
        Hair = self.Library.getTextforHairstyleID(struct.unpack(">i", self.PlayerStatus["Hairstyle"])[0])[1] 
        Start = self.Library.getTextforClassID(ord(self.PlayerStatus["Starting_Class"]))[1] 

        print "Name: %s Gender: %s"%(self.PlayerStatus["Character_Name"].replace("\x00",""),Gender)
        print "Hairstyle: %s (ColorRGB: %f;%f;%f)"%( Hair, R, G, B)
        print "Starting Class: %s"%(Start)
        print "Character Tendency: %i"%struct.unpack(">f", self.PlayerStatus["Character_Tendency"])[0]
        
        columWidth=22
        print u"\u2554" + u"\u2550" * columWidth + u"\u2566" * 1 + u"\u2550" * columWidth  + u"\u2557"
        print (u"\u2551%21s " + u"\u2551%21s " + u"\u2551") % ("HP / MaxHP","%i / %i"%tuple([struct.unpack(">i", self.PlayerStatus[u])[0] for u in ["Current_HP","Maximum_HP"]]))
        print u"\u2560" + u"\u2550" * columWidth + u"\u256C" * 1 + u"\u2550" * columWidth  + u"\u2563"
        print (u"\u2551%21s " + u"\u2551%21s " + u"\u2551") % ("MP / MaxMP","%i / %i"%tuple([struct.unpack(">i", self.PlayerStatus[u])[0] for u in ["Current_MP","Maximum_MP"]]))
        print u"\u2560" + u"\u2550" * columWidth + u"\u256C" * 1 + u"\u2550" * columWidth  + u"\u2563"
        print (u"\u2551%21s " + u"\u2551%21s " + u"\u2551") % ("Stamina / MaxStamina","%i / %i"%tuple([struct.unpack(">i", self.PlayerStatus[u])[0] for u in ["Current_Stamina","Maximum_Stamina"]]))
        print u"\u2560" + u"\u2550" * columWidth + u"\u256C" * 1 + u"\u2550" * columWidth  + u"\u2563"
 
        print (u"\u2551%21s " + u"\u2551%21s " + u"\u2551") % ("Souls","%i"%tuple([struct.unpack(">i", self.PlayerStatus[u])[0] for u in ["Current_Souls"]]))
        print u"\u2560" + u"\u2550" * columWidth + u"\u256C" * 1 + u"\u2550" * columWidth  + u"\u2563"
        print (u"\u2551%21s " + u"\u2551%21s " + u"\u2551") % ("Soul Memory","%i"%tuple([struct.unpack(">i", self.PlayerStatus[u])[0] for u in ["Soul_Memory"]]))
        print u"\u2560" + u"\u2550" * columWidth + u"\u256C" * 1 + u"\u2550" * columWidth  + u"\u2563"
        print (u"\u2551%21s " + u"\u2551%21s " + u"\u2551") % ("Levels Purchased","%i"%tuple([struct.unpack(">i", self.PlayerStatus[u])[0] for u in ["Levels_Purchased"]]))
        print u"\u2560" + u"\u2550" * columWidth + u"\u256C" * 1 + u"\u2550" * columWidth  + u"\u2563"

        print (u"\u2551%21s " + u"\u2551%21s " + u"\u2551") % ("Vitality","%i"%tuple([struct.unpack(">i", self.PlayerStatus[u])[0] for u in ["Vitality"]]))
        print u"\u2560" + u"\u2550" * columWidth + u"\u256C" * 1 + u"\u2550" * columWidth  + u"\u2563"
        print (u"\u2551%21s " + u"\u2551%21s " + u"\u2551") % ("Intelligence","%i"%tuple([struct.unpack(">i", self.PlayerStatus[u])[0] for u in ["Intelligence"]]))
        print u"\u2560" + u"\u2550" * columWidth + u"\u256C" * 1 + u"\u2550" * columWidth  + u"\u2563"
        print (u"\u2551%21s " + u"\u2551%21s " + u"\u2551") % ("Endurance","%i"%tuple([struct.unpack(">i", self.PlayerStatus[u])[0] for u in ["Endurance"]]))
        print u"\u2560" + u"\u2550" * columWidth + u"\u256C" * 1 + u"\u2550" * columWidth  + u"\u2563"
        print (u"\u2551%21s " + u"\u2551%21s " + u"\u2551") % ("Strength","%i"%tuple([struct.unpack(">i", self.PlayerStatus[u])[0] for u in ["Strength"]]))
        print u"\u2560" + u"\u2550" * columWidth + u"\u256C" * 1 + u"\u2550" * columWidth  + u"\u2563"
        print (u"\u2551%21s " + u"\u2551%21s " + u"\u2551") % ("Dexterity","%i"%tuple([struct.unpack(">i", self.PlayerStatus[u])[0] for u in ["Dexterity"]]))
        print u"\u2560" + u"\u2550" * columWidth + u"\u256C" * 1 + u"\u2550" * columWidth  + u"\u2563"
        print (u"\u2551%21s " + u"\u2551%21s " + u"\u2551") % ("Magic","%i"%tuple([struct.unpack(">i", self.PlayerStatus[u])[0] for u in ["Magic"]]))
        print u"\u2560" + u"\u2550" * columWidth + u"\u256C" * 1 + u"\u2550" * columWidth  + u"\u2563"
        print (u"\u2551%21s " + u"\u2551%21s " + u"\u2551") % ("Faith","%i"%tuple([struct.unpack(">i", self.PlayerStatus[u])[0] for u in ["Faith"]]))
        print u"\u2560" + u"\u2550" * columWidth + u"\u256C" * 1 + u"\u2550" * columWidth  + u"\u2563"
        print (u"\u2551%21s " + u"\u2551%21s " + u"\u2551") % ("Luck","%i"%tuple([struct.unpack(">i", self.PlayerStatus[u])[0] for u in ["Luck"]]))
        print u"\u255A" + u"\u2550" * columWidth + u"\u2569" * 1 + u"\u2550" * columWidth  + u"\u255D"


    def readEquipment(self, f):
        f.seek(0x28C)
        self.PlayerEquipment["Left_Mainarm"]=f.read(4)
        self.PlayerEquipment["Right_Mainarm"]=f.read(4)
        self.PlayerEquipment["Left_Sidearm"]=f.read(4)
        self.PlayerEquipment["Right_Sidearm"]=f.read(4)

        self.PlayerEquipment["Arrow_Type"]=f.read(4)
        self.PlayerEquipment["Bolt_Type"]=f.read(4)

        self.PlayerEquipment["Helmet"]=f.read(4)
        self.PlayerEquipment["Chest"]=f.read(4)
        self.PlayerEquipment["Gauntlets"]=f.read(4)
        self.PlayerEquipment["Leggings"]=f.read(4)
    
        # drop 4 byte hairstyle instead of seeking over these 4 bytes
        f.read(4)
        self.PlayerEquipment["Ring1"]=f.read(4)
        self.PlayerEquipment["Ring2"]=f.read(4)
        
        self.PlayerEquipment["Quickslot1"]=f.read(4)
        self.PlayerEquipment["Quickslot2"]=f.read(4)
        self.PlayerEquipment["Quickslot3"]=f.read(4)
        self.PlayerEquipment["Quickslot4"]=f.read(4)
        self.PlayerEquipment["Quickslot5"]=f.read(4)

    def ShowEquipment(self):
        print "Equipment"
        columWidth=22

        lm,rm = [self.Library.getTextforWeaponID(x)[1] for x in [struct.unpack(">L", self.PlayerEquipment[u])[0] for u in ["Left_Mainarm","Right_Mainarm"]]]
        ls,rs = [self.Library.getTextforWeaponID(x)[1] for x in [struct.unpack(">L", self.PlayerEquipment[u])[0] for u in ["Left_Sidearm","Right_Sidearm"]]]
        r1,r2 = [self.Library.getTextforRingID(x)[1] for x in [struct.unpack(">L", self.PlayerEquipment[u])[0] for u in ["Ring1","Ring2"]]]
        am,bm = [self.Library.getTextforItemID(x)[1] for x in [struct.unpack(">L", self.PlayerEquipment[u])[0] for u in ["Arrow_Type","Bolt_Type"]]]
        l,g,c,h = [self.Library.getTextforArmorID(x)[1] for x in [struct.unpack(">L", self.PlayerEquipment[u])[0] for u in ["Leggings","Gauntlets","Chest","Helmet"]]]
        quickslots = [self.Library.getTextforItemID(x)[1] for x in [struct.unpack(">L", self.PlayerEquipment[u])[0] for u in ["Quickslot1","Quickslot2","Quickslot3","Quickslot4","Quickslot5"]]]
        
        print u"\u2554" + u"\u2550" * columWidth + u"\u2566" * 1 + u"\u2550" * (columWidth+15)  + u"\u2557"
        print (u"\u2551%21s " + u"\u2551%36s " + u"\u2551") % ("Left / Right Mainarm","%s / %s"%(lm,rm))
        print u"\u2560" + u"\u2550" * columWidth + u"\u256C" * 1 + u"\u2550" * (columWidth+15)  + u"\u2563"
        print (u"\u2551%21s " + u"\u2551%36s " + u"\u2551") % ("Left / Right Sidearm","%s / %s"%(ls,rs))
        print u"\u2560" + u"\u2550" * columWidth + u"\u256C" * 1 + u"\u2550" * (columWidth+15)  + u"\u2563"
        print (u"\u2551%21s " + u"\u2551%36s " + u"\u2551") % ("Ring1 / Ring2","%s / %s"%(r1,r2))
        print u"\u2560" + u"\u2550" * columWidth + u"\u256C" * 1 + u"\u2550" * (columWidth+15)  + u"\u2563"
        print (u"\u2551%21s " + u"\u2551%36s " + u"\u2551") % ("Arrows / Bolts","%s / %s"%(am,bm))
        print u"\u2560" + u"\u2550" * columWidth + u"\u256C" * 1 + u"\u2550" * (columWidth+15)  + u"\u2563"

        print (u"\u2551%21s " + u"\u2551%36s " + u"\u2551") % ("Helmet","%s"%(h))
        print u"\u2560" + u"\u2550" * columWidth + u"\u256C" * 1 + u"\u2550" * (columWidth+15)  + u"\u2563"
        print (u"\u2551%21s " + u"\u2551%36s " + u"\u2551") % ("Chest","%s"%(c))
        print u"\u2560" + u"\u2550" * columWidth + u"\u256C" * 1 + u"\u2550" * (columWidth+15)  + u"\u2563"
        print (u"\u2551%21s " + u"\u2551%36s " + u"\u2551") % ("Gauntlets","%s"%(g))
        print u"\u2560" + u"\u2550" * columWidth + u"\u256C" * 1 + u"\u2550" * (columWidth+15)  + u"\u2563"
        print (u"\u2551%21s " + u"\u2551%36s " + u"\u2551") % ("Leggings","%s"%(l))
        print u"\u2560" + u"\u2550" * columWidth + u"\u256C" * 1 + u"\u2550" * (columWidth+15)  + u"\u2563"

        for q in ["Quickslot1","Quickslot2","Quickslot3","Quickslot4","Quickslot5"]:
            t=self.Library.getTextforItemID(struct.unpack(">L", self.PlayerEquipment[q])[0])[1]
            print (u"\u2551%21s " + u"\u2551%36s " + u"\u2551") % (q,"%s"%(t))
            if q is "Quickslot5":
                print u"\u255A" + u"\u2550" * columWidth + u"\u2569" * 1 + u"\u2550" * (columWidth+15)  + u"\u255D"
            else:   
                print u"\u2560" + u"\u2550" * columWidth + u"\u256C" * 1 + u"\u2550" * (columWidth+15)  + u"\u2563"
        
    def readInventory(self, f):
        f.seek(0x2D4)
        self.Inventory["Used_Entries"]=f.read(4)
        self.Inventory["Max_Entries"]=f.read(4)

        self.Inventory["Entries"]=[{"Item_Type":f.read(1),"Padding":f.read(3), "Item_ID":f.read(4), "Item_Count":f.read(4),"Misc":f.read(20)} for u in range(int(hexlify(self.Inventory["Max_Entries"]),16))]

    def ShowInventory(self):
        # 32 max length text
        # 99 max count value
        print "Inventory:"
        print "Used Entries: %i"%struct.unpack(">L", self.Inventory["Used_Entries"])[0]
        weapons,armor,items,rings="","","",""
        for x in range(struct.unpack(">L", self.Inventory["Max_Entries"])[0]):
            if self.Inventory["Entries"][x]["Item_Type"]=="\xff":
                continue
            if self.Inventory["Entries"][x]["Item_Type"]=="\x00":
                weapons += self.Library.getTextforWeaponID(struct.unpack(">L", self.Inventory["Entries"][x]["Item_ID"])[0])[1]+" : "+ "%i"%struct.unpack(">L", self.Inventory["Entries"][x]["Item_Count"])[0] + "\n"
            if self.Inventory["Entries"][x]["Item_Type"]=="\x10":
                armor += self.Library.getTextforArmorID(struct.unpack(">L", self.Inventory["Entries"][x]["Item_ID"])[0])[1]+" : "+ "%i"%struct.unpack(">L", self.Inventory["Entries"][x]["Item_Count"])[0] + "\n"
            if self.Inventory["Entries"][x]["Item_Type"]=="\x20":
                rings += self.Library.getTextforRingID(struct.unpack(">L", self.Inventory["Entries"][x]["Item_ID"])[0])[1]+" : "+ "%i"%struct.unpack(">L", self.Inventory["Entries"][x]["Item_Count"])[0] + "\n"
            if self.Inventory["Entries"][x]["Item_Type"]=="\x40":
                items += self.Library.getTextforItemID(struct.unpack(">L", self.Inventory["Entries"][x]["Item_ID"])[0])[1]+" : "+ "%i"%struct.unpack(">L", self.Inventory["Entries"][x]["Item_Count"])[0] + "\n"
             
        print "Weapons:\n=============\n"+weapons+"Armor:\n=============\n"+armor+"Rings:\n=============\n"+rings+"Items:\n=============\n"+items
        
    def readSpellsandMiracles(self, f):
        f.seek(0x102E0)
        self.SpellsandMiracles["Spell_Slots"]=f.read(4)
        f.seek(0x1030C)
        self.SpellsandMiracles["Miracle_Slots"]=f.read(4)

        f.seek(0x143E8)
        self.SpellsandMiracles["Spell_Count"]=f.read(4)
        
        self.SpellsandMiracles["Entries"]=[{"Spell_Status":f.read(4), "Spell_ID":f.read(4), "Misc1":f.read(4),"Misc2":f.read(4)} for u in range(int(hexlify(self.SpellsandMiracles["Spell_Count"]),16))]

    def ShowSpellsandMiracles(self):
        print "Spells and Miracles:"
        print "Spell Slots: %i  Miracle Slots: %i"%tuple([struct.unpack(">L", self.SpellsandMiracles[u])[0] for u in ["Spell_Slots","Miracle_Slots"]])
        spells=""
        Spell_Status=["Unavailable","Unknown","Known","Memorized"]
        for x in range(struct.unpack(">L", self.SpellsandMiracles["Spell_Count"])[0]):
            a = struct.unpack(">L", self.SpellsandMiracles["Entries"][x]["Spell_Status"])[0]
            
            st = Spell_Status[a]
            name = self.Library.getTextforSpellID(struct.unpack(">L", self.SpellsandMiracles["Entries"][x]["Spell_ID"])[0])[1]

            spells += name + " : " + st +"\n"
             
        print spells       

    def readDeposit(self, f):
        f.seek(0x14BE8)
        # fixed length of 2048 entries? perhaps also stored somewhere
        self.Deposit["Entries"]=[{"Unknown":f.read(4), "Item_Type":f.read(1), "Item_ID":f.read(3),"Unknown2":f.read(4),"Item_Count":f.read(1),"Unknown3":f.read(7)} for u in range(2048)]

    def ShowDeposit(self):
        # 32 max length text
        # 99 max count value
        print "Deposit:"
        print len(self.Deposit["Entries"])
        weapons,armor,items,rings="","","",""
        for x in range(2048):
            if self.Deposit["Entries"][x]["Item_Type"]=="\xff":
                continue
            if self.Deposit["Entries"][x]["Item_Type"]=="\x00":
                weapons += self.Library.getTextforWeaponID(struct.unpack(">L", "\x00"+self.Deposit["Entries"][x]["Item_ID"])[0])[1]+" : "+ "%i"%ord(self.Deposit["Entries"][x]["Item_Count"]) + "\n"
            if self.Deposit["Entries"][x]["Item_Type"]=="\x10":
                armor += self.Library.getTextforArmorID(struct.unpack(">L", "\x00"+self.Deposit["Entries"][x]["Item_ID"])[0])[1]+" : "+ "%i"%ord(self.Deposit["Entries"][x]["Item_Count"]) + "\n"
            if self.Deposit["Entries"][x]["Item_Type"]=="\x20":
                rings += self.Library.getTextforRingID(struct.unpack(">L", "\x00"+self.Deposit["Entries"][x]["Item_ID"])[0])[1]+" : "+ "%i"%ord(self.Deposit["Entries"][x]["Item_Count"]) + "\n"
            if self.Deposit["Entries"][x]["Item_Type"]=="\x40":
                items += self.Library.getTextforItemID(struct.unpack(">L", "\x00"+self.Deposit["Entries"][x]["Item_ID"])[0])[1]+" : "+ "%i"%ord(self.Deposit["Entries"][x]["Item_Count"]) + "\n"
             
        print "Weapons:\n=============\n"+weapons+"Armor:\n=============\n"+armor+"Rings:\n=============\n"+rings+"Items:\n=============\n"+items

        
    def __init__(self,filepath):
        # opens the .DAT in filepath and tries to interpret it
        # no real checks if a real userfile is read
        # if it crashes, either the structure is wrong in this
        # parser or the file is no demon souls user file
        self.filepath = filepath
        
        with open(filepath,"rb") as w:
            self.readGameInfo(w)
            self.readPlayerStatus(w)
            self.readEquipment(w)
            self.readInventory(w)
            self.readSpellsandMiracles(w)
            self.readDeposit(w)

        self.ShowGameInfo()
        self.ShowPlayerStatus()
        self.ShowEquipment()
        self.ShowInventory()
        self.ShowSpellsandMiracles()
        self.ShowDeposit()

DemonsSoulsSaveGame("Decrypted/1USER.DAT")
