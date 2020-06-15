## /***********************************************************
# * Name of program: 
# * Authors: 
# * Description: Starter code for Project 4
# **********************************************************/
import struct
import sys
import math

# Seeking to an aribitrary position and reading in a set number of bytes.
# This function unpacks bytes according to little endian disk format and
# host order of running computer.
# https://docs.python.org/3/library/struct.html
def get_bytes(f, pos, numBytes):
        f.seek(pos)
        byte = f.read(numBytes)
        if (numBytes == 2):
                formatString = "H"
        elif (numBytes == 1):
                formatString = "B"
        elif (numBytes == 4):
                formatString = "i"
        else:
                raise Exception("Not implemented")

        return struct.unpack(ENDIAN_FORMAT+formatString, byte)[0]

def get_Sector(N):
    FirstSectorofCluster = ((N - 2) * BPB_SecPerClus) + FirstDataSector

    return FirstSectorofCluster

def rootDirSectors():
    RootDirSectors = ((BPB_RootEntCnt * 32) + (BPB_BytesPerSec - 1)) / BPB_BytesPerSec
    RootDirSectors = round(RootDirSectors)

    return RootDirSectors

def firstDataSector():
        
        FirstDataSector = BPB_RsvdSecCnt + (BPB_NumFATs * BPB_FATSz32) + RootDirSectors

        return FirstDataSector

def dataSec(TotSec, BPB_ResvdSecCnt, BPB_NumFATs, FATSz, RootDirSectors):
    DataSec = TotSec - (BPB_ResvdSecCnt + (BPB_NumFATs * FATSz) + RootDirSectors)

    return DataSec

def countOfClusters(DataSec, BPB_SecPerClus):
    CountOfClusters = DataSec / BPB_SecPerClus
    return CountOfClusters

def fatOffset(N):
    FATOffset = N * 4
    return FATOffSet

def thisFatSecNum(BPB_ResvdSecCnt, FATOffset, BPB_BytsPerSec):
    ThisFatSecNum = BPB_ResvdSecCnt + (FATOffset / BPB_BytsPerSec)
    #Round this number down need to figure out how to do this
    return ThisFatSecNum

def thisFATEntOffset(FATOffset, BOB_BytsPerSec):
    ThisFATEntOffset = REM(FATOffset / BOB_BytsPerSec)

    return thisFATEntOffset

def rootLocation():
        f = open("fat32.img", 'rb')
        RootDirSectors = rootDirSectors()
        RootDirSectors = 0
        return RootDirSectors

def rootLocation1():
        
        FirstDataSector = BPB_RsvdSecCnt + (BPB_NumFATs * BPB_FATSz32) + RootDirSectors
        return FirstDataSector

def rootLocation2():       
        N = BPB_RootClus

        sector = ((N - 2) * BPB_SecPerClus) + FirstDataSector

        return sector

def rootLocation3():
        rootByteAddress = sector * BPB_BytesPerSec
        return rootByteAddress



        f.seek(rootByteAddress)

        byte = f.read(11)


        dir_attr = rootByteAddress + 11

        newByte = get_bytes(f, dir_attr, 1)


        dir_attr += 32
        return dir_attr

def main():
        # BPB Constants
        global BPB_BytesPerSec
        global BPB_SecPerClus
        global BPB_RsvdSecCnt
        global BPB_NumFATs
        global BPB_FATSz32
        global FirstDataSector
        global RootDirSectors
        global BPB_RootEntCnt
        global ENDIAN_FORMAT
        global pieceOfShit
        global BPB_RootClus
        global dir_attr
        global sector

        rootCount = 0
        
        f = open("fat32.img", 'rb')

        if sys.byteorder == 'little':
                ENDIAN_FORMAT = "<"
        else:
                ENDIAN_FORMAT = ">"


        BPB_BytesPerSec = get_bytes(f, 11, 2)
        BPB_SecPerClus = get_bytes(f, 13, 1)
        BPB_RsvdSecCnt = get_bytes(f, 14, 2)
        BPB_NumFATs = get_bytes(f, 16, 1)
        BPB_FATSz32 = get_bytes(f, 36, 4)

        BPB_RootClus = get_bytes(f, 44, 4)
        BPB_RootEntCnt = get_bytes(f, 17, 2)


        if rootCount == 0:
                RootDirSectors = rootLocation()
                FirstDataSector = rootLocation1()
                sector = rootLocation2()
                rootByteAddress = rootLocation3()
                f.seek(rootByteAddress)

                byte = f.read(11)


                dir_attr = rootByteAddress + 11

                newByte = get_bytes(f, dir_attr, 1)


                dir_attr += 32
                
        rootCount += 1



        #TODO: Get and seek to the root directory

        # Begin taking arguments
        while True:
            
                user_input = input("] ")
                user_input_list = user_input.split()
                command = user_input_list[0].strip()

                args = user_input_list[1:]
                

                #Start processing the commands

                if command == "info":
                        info(rootByteAddress) #TODO: Finish this function
                        
                elif command == "stat":
                        dirEntries(f, dir_attr, command, args)

                elif command == "cd":
                        dirEntries(f, dir_attr, command, args)

                elif command == "ls":
                        dirEntries(f, dir_attr, command, args)

                elif command == "read":
                        RootDirSectors = 0
                        dirEntries(f, dir_attr, command, args)

                elif command == "volume":
                        volume(byte)

                elif command == "deleted":
                        dirEntries(f, dir_attr, command, args)

                elif command == "quit":
                        print("Quitting.\n")
                        f.close()
                        quit()

                else:
                        print("Unrecognized command\n")

def stat(f, myByte, fileSize, something, result_num):
        print("The file ", myByte, " has a file size of ", fileSize)
        if get_bytes(f, something, 1) == 32:
                fileAttr = "ATTR_ARCHIVE"
                print("and the file has an attribute of ", fileAttr)
        elif get_bytes(f, something, 1) == 16:
                fileAttr = "ATTR_DIRECTORY"
                print("and the file has an attribute of ", fileAttr)
        elif get_bytes(f, something, 1) == 8:
                fileAttr = "ATTR_VOLUME_ID"
                print("and the file has an attribute of ", fileAttr)
        elif get_bytes(f, something, 1) == 4:
                fileAttr = "ATTR_SYSTEM"
                print("and the file has an attribute of ", fileAttr)
        elif get_bytes(f, something, 1) == 2:
                fileAttr = "ATTR_HIDDEN"
                print("and the file has an attribute of ", fileAttr)
        elif get_bytes(f, something, 1) == 1:
                fileAttr = "ATTR_READ_ONLY"
                print("and the file has an attribute of ", fileAttr)

        print("first cluster number is ", result_num)

def read(f, args, result_num):
        fileName = args[0]
        
        startPos = args[1]
        numBytes = args[2]
        sector = get_Sector(result_num)
        firstSector = firstDataSector()
        firstSectorofFileCluster = (((result_num - 2) * BPB_SecPerClus) + firstSector) * BPB_BytesPerSec

        startPos = int(startPos) + int(firstSectorofFileCluster)

        f.seek(startPos)
        myString = f.read(int(numBytes))
        myString = myString.decode('ascii')

        print(myString)
        

def deleted(f,thing):
        thing = thing + 1
        f.seek(thing)
        myByte = f.read(11)
        myByte = myByte.decode('ascii')
        myByte = myByte.replace(" ", "")
        myByte = myByte.replace("TXT", ".TXT")
        myByte = "_" + myByte
        print(myByte)
                                

def volume(byte):
        myByte = byte.decode('ascii')
        myByte = myByte.replace(" ", "")
        myByte = myByte.replace("TXT", ".TXT")
        print(myByte)

def info(rootByteAddress):

        print("BPB_BytesPerSec is ", hex(BPB_BytesPerSec), BPB_BytesPerSec)

        print("BPB_SecPerClus is ", hex(BPB_SecPerClus), BPB_SecPerClus)

        print("BPB_RsvdSecCnt is ", hex(BPB_RsvdSecCnt), BPB_RsvdSecCnt)

        print("BPB_NumFATs is ", hex(BPB_NumFATs), BPB_NumFATs)

        print("BPB_FATSz32 is ", hex(BPB_FATSz32), BPB_FATSz32)

        print("rootByteAddress is ", hex(rootByteAddress), rootByteAddress)
        return True

def cd(f, dir_attr, myByte, result_num, args, command):
        
        lsList = []
        sectorList = []
       
        if get_bytes(f, dir_attr, 1) == 16:
                dirPosition = f.seek(dir_attr - 11)
                
                sector = get_Sector(result_num)

            

                firstSector = firstDataSector()

                firstSectorofFileCluster = (((result_num - 2) * BPB_SecPerClus) + firstSector) * BPB_BytesPerSec

                firstSectorOfCD = firstSectorofFileCluster

                f.seek(firstSectorofFileCluster)
                

                dirFileAttr = int(firstSectorofFileCluster) + 11
              

                if get_bytes(f, dirFileAttr, 1) == 15:
                        skip = 0
                else:
                        dirContents = f.read(11)
                        
                        count = 0

                        moreEntries = True
                        while moreEntries:
                                while count < 18:

                                        dirFileAttr = int(firstSectorofFileCluster) + 11
                                        if get_bytes(f, dirFileAttr, 1) == 15:
                                                count = count + 1
                                        elif get_bytes(f, dirFileAttr, 1) == 00:
                                                break
                                        elif count < 16:
                                                f.seek(firstSectorofFileCluster)
                                                        
                                                myBytes = f.read(11)

                                                

                                                if 229 == get_bytes(f, firstSectorofFileCluster, 1):
                                                        count = count + 1
                                                        continue

                                                if 0 == get_bytes(f, firstSectorofFileCluster, 1) :
                                                        moreEnties = False
                                                        break
                                                
                                                
                                                myBytes = myBytes.decode('ascii')
                                                myBytes = myBytes.replace(" ", "")
                                                lsList.append(myBytes)
                                                sectorList.append(firstSectorofFileCluster)
                                              
                                                count = count + 1

                                        firstSectorofFileCluster = firstSectorofFileCluster + 32
                                count = 0
                                FATOffset = result_num * 4

                                ThisFATSecNum = BPB_RsvdSecCnt + (FATOffset // BPB_BytesPerSec)
                                ThisFATEntOffset = (FATOffset % BPB_BytesPerSec)

                                nextClusterPos = ThisFATSecNum * BPB_BytesPerSec + ThisFATEntOffset
                                                                                  
                                nextCluster = get_bytes(f, nextClusterPos, 4)

                                result_num = nextCluster

                                if result_num > 268435448:
                                        break



                                firstSectorofFileCluster = (((result_num - 2) * BPB_SecPerClus) + firstSector) * BPB_BytesPerSec

                        positionCounter = 0
                        i = -1
                        previousPrompt = args[0] + "]"
                        oldLsList = lsList
                        
                        while True:
                                oldLsList = lsList
                                if command != "ls":
                                        prompt = args[0] + "]"
                                        
                                user_input = input(previousPrompt)
                                user_input_list = user_input.split()
                                command = user_input_list[0].strip()
                                args = user_input_list[1:]
                                
                                if command != "ls":
                                        if args[0] not in lsList or args[0] not in oldLsList:
                                                
                                                print("that is not in the directory")
                                                args[0] = "DIR"

                                countblack = []

                                if command == "ls":
                                        
                                        for item in lsList:
                                                print(item)

                                elif command == "cd" and args[0] == "..":
                                        
                                        previousPrompt = "DIR]"
                                       
                                        args[0] = prompt
                                        postitionCounter = 0
                                        i = -1
                                        
                                        

                                        break
                                        
                                        
                                        
                                elif command == "cd":
                                        if args[0] in lsList:
                                                for item in lsList:
                                                       
                                                        if item == args[0]:
                                                               
                                                                while i != positionCounter:
                                                                        i += 1
                                                                        
                                                                        if i == positionCounter:
                                                                                
                                                                                dirPos = sectorList[i]
                                                                           
                                                                                dir_attr = dirPos - 21
                                                                                if command == "ls":
                                                                                      
                                                                                        dirEntries(f, dir_attr, "ls", args)
                                                                                elif command == "cd":
                                                                                     
                                                                                        if args[0] == "..":
                                                                                                args[0] = "DIR"
                                                                                        else:
                                                                                                dirEntries(f, dir_attr, "cd", args)
                                                                                
                                                                           
                                                                                
                                                        positionCounter += 1

                                                        
                        

                if command == "cd":
                        dirEntries(f, dir_attr, "cd", args)
                if command == "ls":
                        dirEntries(f, dir_attr, "ls", args)



def dirEntries(f, dir_attr, command, args):
        while True:
           
                dir_attr = dir_attr + 32
                if get_bytes(f, dir_attr, 1) == 15:
                        counter = 0
                elif get_bytes(f, dir_attr, 1) == 00:
                        return 0
                
                else:
                        
                        start_addr = dir_attr - 11
                        f.seek(start_addr)
                        leadInt = get_bytes(f, start_addr, 1)
                      
                        

                        if leadInt == 0xe5:
                            if command == "deleted":
                                    deleted(f,start_addr)
                                
                        else:
                            
                                if command == "deleted":
                                        counter = 0
                                        
                                else:
                                        f.seek(start_addr)
                                        byte = f.read(11)
                                       
                                        myByte = byte.decode('ascii')

                                        myByte = myByte.replace(" ", "")
                                        myByte = myByte.replace("TXT", ".TXT")
                        
                                        if command == "stat" or command == "read" or command == "cd":
                                        
                                                if args[0] == myByte:
                                                        new_addr = start_addr + 28
                                                        fstClusHi = start_addr + 20
                                                        fstClusLow = start_addr + 26
                                                        clusHiNum = get_bytes(f, fstClusHi, 2)
                                                        clusLowNum = get_bytes(f, fstClusLow, 2)
                                                        result_num = str(clusHiNum) + str(clusLowNum)
                                                        result_num = int(result_num)

                                                        
                                                        fileSize = get_bytes(f, new_addr, 4)

                                                        if command == "read":
                                                                read(f, args, result_num)
                                                                
                                                        elif command == "cd":
                                                                cd(f, dir_attr, myByte, result_num, args, command)
                                                                
                                                                
                                                        else:
                                                                stat(f, myByte, fileSize, dir_attr, result_num)


                                        else:
                                                print(myByte)
                                                                         

                



                                
main()
