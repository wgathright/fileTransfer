import argparse
import subprocess
import os
import threading
import hashlib
import time


# Array of File objects
files = []
islands = []

# Create File class
class File(object):
    def __init__(self,fileName):
        self.fileName = fileName # file path to original
        self.si = ""             # storage island to copy to
        self.copyFullPath = ""   # file path to copy (si + /file)
        self.originalMD5 = ""
        self.copyMD5 = ""
        
        
    def moveFile(self):
        if isDebug:
            print('Copying ', file.fileName,' to ', file.si)
        
        if isVerbose:
            subprocess.call(['rsync','-avrz', self.fileName, self.si])
        else:
            subprocess.call(['rsync','-arz', self.fileName, self.si])
        
        
    def generateHash(self,fileToCheck):
        with open(fileToCheck,'rb') as openedFile:
            fileContents = openedFile.read()
            md5Returned = hashlib.md5(fileContents).hexdigest()
            return md5Returned
        
    def makeCopyPath(self):
        headTail = os.path.split(self.fileName)
        tail = headTail[1]
        self.copyFullPath = self.si + '/' + tail
        
# End of File class 
         

# Build array of file objects from source
def buildList(sourceInput):
    if os.path.isdir(sourceInput):
        for entry in os.scandir(sourceInput):
            files.append(File(entry.path))
    elif os.path.isfile(sourceInput):
        with open(sourceInput) as fin:
            for line in fin:
                files.append(File(line.strip()))
    else:
        print("Source Input Error")
        
        
# Build array of Storage Islands from destination       
def buildIslands(destinationInput):
    if os.path.isdir(destinationInput):
        for entry in os.scandir(destinationInput):
            islands.append(entry.path)
    elif os.path.isfile(destinationInput):
        with open(destinationInput) as fin:
            for line in fin:
                islands.append(line.strip())
    else:
        print("Destination Input Error")
        


if __name__ == '__main__':

    
    # Initialize the argument parser
    parser = argparse.ArgumentParser(
        description="File Transfer Script"
        )
    
    # Add parameters positional/optional(--)
    parser.add_argument('-s','--source', help="Source")
    parser.add_argument('-d','--destination', help="Destination")
    parser.add_argument('-v','--verbose',help="Verbose",action='store_true')
    parser.add_argument('--debug',help="Debug",action='store_true')
    parser.add_argument('--disablethread',help="Disable Threading",action='store_true')
    
    
    
    
    # Parse the arguments
    args = parser.parse_args()
    mySource = args.source
    myDestination = args.destination
    isVerbose = args.verbose
    isDebug = args.debug
    threadingDisabled = args.disablethread
    
    if isDebug:
        print(args)
        start = time.perf_counter()
    
    
    buildList(mySource)
     
    buildIslands(myDestination)
        
    
    print("Number of files to be transferred: ", len(files))
    print("Number of storage islands available: ",len(islands))
    
    currentIsland = 0   

    for file in files:
        
        if currentIsland < len(islands):
            file.si = islands[currentIsland]
            currentIsland += 1
        else:
            currentIsland = 0
            file.si = islands[currentIsland]
        
    
    if threadingDisabled:
        print("Threading Disabled")
        for file in files:
            file.moveFile()
    else:
        threads = []
        # create threaded moveFile() 
        for file in files:
            t = threading.Thread(target=file.moveFile)
            t.start()
            threads.append(t)
        
        for thread in threads:
            thread.join()
        
    
    print('\n')
   
    # Generate md5 for original and copy
    for file in files:
        file.originalMD5 = file.generateHash(file.fileName)
        file.makeCopyPath()
        file.copyMD5 = file.generateHash(file.copyFullPath)
        
        # Compare md5 of orginal to copy
        if file.originalMD5 == file.copyMD5:
            print("MD5 checksum Matches")
            print("Original: ",file.fileName,"MD5 -- ", file.originalMD5)
            print("Copy: ",file.copyFullPath ,"MD5 -- ",file.copyMD5, '\n')
        else:
            print("ERROR: MD5 checksum does NOT match")
            print("Original: ",file.fileName,"MD5 -- ", file.originalMD5)
            print("Copy: ",file.copyFullPath ,"MD5 -- ",file.copyMD5)
            
            
    
    if isDebug:
        finish = time.perf_counter()
        print(f'Finished in {round(finish-start, 2)} second(s)')
        
        
    
   
    
    
    
    