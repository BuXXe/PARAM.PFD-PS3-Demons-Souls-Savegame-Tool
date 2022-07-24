# PARAM_SFO (System File Object) Class
# PARAM_SFO Structure 
# see PARAM.SFO.html for documentation (Source: http://www.psdevwiki.com/ps3/PARAM.SFO)
import os
class PARAM_SFO:
    def parse(self):

        # header (each entry is uint32_t = 4 Byte per entry)
        sfo_header = ["magic","version","key_table_start","data_table_start","tables_entries"]
        # index_table (first 2 uint16_t entries, 3 uint32_t entries)
        sfo_index_table_entry = ["key_offset","data_fmt","data_len","data_max_len","data_offset"]

        # data_fmt datatypes are
        # 0004 = utf8-Special (NOT 0x00 terminated)
        # 0204 = utf8 character string (0x00 terminated)
        # 0404 = uint32_t
        with open(self.path, "rb") as f:
            header = {field:f.read(4)[::-1] for field in sfo_header}
            index_table = []

            for k in sfo_header:    
                print k,header[k].encode("hex")

            print "get the index table entries",sum([ord(k) for k in header["tables_entries"]])
            sumdata=0
            for i in range(sum([ord(k) for k in header["tables_entries"]])):
                entry={}
                entry["key_offset"] = f.read(2)[::-1].encode("hex")
                entry["data_fmt"] = f.read(2)[::-1].encode("hex")
                entry["data_len"] = f.read(4)[::-1].encode("hex")
                entry["data_max_len"] = f.read(4)[::-1].encode("hex")
                sumdata+=int(entry["data_max_len"],16)
                entry["data_offset"] = f.read(4)[::-1].encode("hex")
                index_table.append(entry)

            for e in index_table:
                print e
            print sumdata
            key_table=[]
    
            # build key_table
            bytes_read=0
            for x in range(len(index_table)):
                entry=f.read(1)
                bytes_read+=1
                while entry[-1]!=chr(0):
                    bytes_read+=1
                    entry+=f.read(1)
                # cut off the 0x00 byte 
                key_table.append(entry[:-1])

            print key_table
    
            #IMPORTANT! We have a padding here so that the key_table is a multiple of 32bits (4 bytes)
            #If there are padding bits we will just read them here and ignore them
            padding = f.read(4-bytes_read%4)

            # Read the data_table 
            # INFO: Some data entries can be filled with zeroes and are marked with len=0 in the assocaited entry
            # We try to consider this with the following approach
            # read the "len" bytes and the read max_len - len bytes (drop those)
            data_table=[]
            for u in index_table:
        
                value=f.read(int(u["data_len"],16))
                #drop
                f.read(int(u["data_max_len"],16)-int(u["data_len"],16))
                data_table.append(value)


            print data_table
            # ACCOUNT_ID is the id for the PSN account NOT the ps3 profile
            # Attribute has a flag for copy protection of the savegame
            return

    def getIDnTitle(self):

        f1 = open(self.path,'rb')

        f1.seek(0x968)

        self.ID = f1.read(9)

        f1.seek(0xa30)

        self.Title = f1.read(30).rstrip('\x00')

        f1.close()

        return self.ID, self.Title

    def __init__(self,path):
        fn = 'PARAM.SFO'
        if not path.count(fn): path+='/'+fn
        #if not os.path
        self.path = path
        self.getIDnTitle()
        return

        
        
    
