import sys
def OptSearchPDB(pdbfile):
    Options = {
        "names":[],
        "res_names":[],
        "chain_id":[],
        "Res_seq_num":{
            "min":sys.maxsize-1,
            "max":0
        },
        "insert_code":[],
        "alt_loc":[]
    }
    with open(pdbfile,"r") as file:
        for line in file:
            if line.startswith(("ATOM","HETATM")):
                name = line[12:16].strip()
                res_name = line[17:20].strip()
                alt_loc=line[16]
                res_seq_str=line[22:26].strip()
                chain_id=line[21]
                insert_code=line[26]
                if name not in Options["names"]:
                    Options["names"].append(name)
                if res_name not in Options["res_names"]:
                    Options["res_names"].append(res_name)
                if alt_loc!=" " and not (alt_loc in Options["alt_loc"]):
                    Options["alt_loc"].append(alt_loc)
                if res_seq_str.isdigit():
                    res_seq_num = int(res_seq_str)
                    Options["Res_seq_num"]["min"]=min(Options["Res_seq_num"]["min"],res_seq_num)
                    Options["Res_seq_num"]["max"]=max(Options["Res_seq_num"]["max"],res_seq_num)
                if chain_id!=" " and not (chain_id in Options["chain_id"]):
                    Options["chain_id"].append(chain_id)
                if insert_code!=" " and not (insert_code in Options["insert_code"]):
                    Options["insert_code"].append(insert_code)
                
                

                     
    return Options

