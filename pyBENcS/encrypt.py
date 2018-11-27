#!/usr/bin/python3.6

import os, secrets

HEX = "0123456789ABCDEF"
ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
abc = "abcdefghijklmnopqrstuvwxyz"
NL = bytes("""
""","UTF-8")
NOT_USEABLE_CHARS = """
'"|<>,?*="""

def error(X):
    print(X)
    exit()

def inc(X,A=1):
    return (X+A)%256

def fn_proc(FILE):
    for c in FILE:
        if c in NOT_USEABLE_CHARS:
            error("Unusable character in file name: "+c+'\nstring="'+FILE+'"')
    return FILE

def MAPENC(GAP,SKIP):
    X = GAP
    MAP = []
    for i in range(256):
        if X in MAP:
            while X in MAP: X = inc(X)
        MAP.append(X)
        X = inc(X,SKIP)
    return MAP

def enc(data,MAP):
    datain = data[:]
    datout = []
    for i in datain:
        datout.append(MAP.index(i))

    hdat = ""
    a = 0
    for i in datout:
        hdat+=HEX[i//16]+HEX[i%16]
        a+=1
        if a==32:
            hdat+="""
"""
            a = 0

    return bytes(hdat,"UTF-8")

def dec(data,MAP):
    i = 0
    dataout = []
    while i<len(data):
        if chr(data[i]) not in HEX:
            i+=1
            continue
        if i+1<len(data):
            dataout.append(HEX.find(chr(data[i]))*16+HEX.find(chr(data[i+1])))
        i+=2

    for i in range(len(dataout)):
        dataout[i] = MAP[dataout[i]]

    return bytes(dataout)

ARGS = input("""enc/dec Infile Outfile Key
auto enc/dec makefile
Args?""").split()
if len(ARGS)==0:
    error("No arguments specified!")

AUTO = 0
if ARGS[0]=="auto":
    AUTO = 1
    del ARGS[0]


if (AUTO==0 and len(ARGS)<3) or (AUTO==1 and len(ARGS)<2):
    error("Not enough arguments!")

ENC_FOLDER = ""
DEC_FOLDER = ""

if AUTO:
    try:
        f = open(ARGS[1],"r")
        makedata = str(f.read()).split("\n")
        f.close()
    except:
        error("makefile does not exist!")

    for FILE in makedata:
        if FILE.startswith("<?>"):
            if FILE[3]=="#":
                continue
            if FILE[3:].startswith("ENC_FOLDER=="):
                n = FILE.find("==")+2
                ENC_FOLDER = fn_proc(FILE[n:])+"/"
                try:
                    os.makedirs(ENC_FOLDER)
                except:
                    pass
            elif FILE[3:].startswith("DEC_FOLDER=="):
                n = FILE.find("==")+2
                DEC_FOLDER = fn_proc(FILE[n:])+"/"
                try:
                    os.makedirs(ENC_FOLDER)
                except:
                    pass
    
    OFILE = []
    KFILE = []
    if ARGS[0]=="enc":
        for FILE in makedata:
            if FILE.startswith("<?>") or not len(FILE):
                continue
            IFILE = DEC_FOLDER+FILE
            OFILE.append(ENC_FOLDER+FILE+".enc.txt")
            KFILE.append(ENC_FOLDER+FILE+".key.txt")
            key = secrets.randbelow(16384)
            MAP = MAPENC(key//64,key%64)
            try:
                f = open(IFILE,"rb")
                o = open(OFILE[-1],"wb")
                o.write(enc(f.read(),MAP))
                o.close()
                f.close()
            except FileNotFoundError:
                print("Input file",IFILE,"does not exist!")
                continue
            except:
                print("Something went wrong processing",IFILE,"!")
            f = open(KFILE[-1],"w")
            f.write(str(key))
            f.close()
    elif ARGS[0]=="dec":
        for FILE in makedata:
            if FILE.startswith("<?>") or not len(FILE):
                continue
            IFILE = ENC_FOLDER+FILE+".enc.txt"
            OFILE.append(DEC_FOLDER+FILE)
            KFILE.append(ENC_FOLDER+FILE+".key.txt")
            try:
                f = open(KFILE[-1],"r")
                key = int(f.read())
                f.close()
            except FileNotFoundError:
                print("Key file",KFILE[-1],"does not exist!")
                continue
            except ValueError:
                print("Key file",KFILE[-1],"is not a valid key!")
                continue
            except:
                print("Something went wrong while processing key file",KFILE[-1],"!")
                continue
            MAP = MAPENC(key//64,key%64)
            try:
                f = open(IFILE,"rb")
                outf = open(OFILE[-1],"wb")
                outf.write(dec(f.read(),MAP))
                outf.close()
                f.close()
            except FileNotFoundError:
                print("Input file",IFILE,"does not exist!")
            except BaseException as err:
                print("Something went wrong processing",IFILE,"!\n",err)
    else:
        error("Invalid operation!")

else:
    if ARGS[0]=="enc":
        if len(ARGS)>3:
            try:
                key = int(ARGS[-1])
            except:
                error("Key must be an integer!")
        else:
            key = secrets.randbelow(16384)
        MAP = MAPENC(key//64,key%64)
        f = open(ARGS[1],"rb")
        o = open(ARGS[2],"wb")
        o.write(enc(f.read(),MAP))
        o.close()
        f.close()
        print("Key=",key,"\nDon't lose it, else you will not \
be able to decrypt the file!")
    elif ARGS[0]=="dec":
        if len(ARGS)<3:
            error("Not enough arguments!")
        try:
            key = int(ARGS[-1])
        except:
            error("Key must be an integer!")
        MAP = MAPENC(key//64,key%64)
        f = open(ARGS[1],"rb")
        o = open(ARGS[2],"wb")
        o.write(dec(f.read(),MAP))
        o.close()
        f.close()
    else:
        error("Invalid operation!")

input("Press any key to exit...")
