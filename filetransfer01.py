import argparse
import subprocess
import os
import threading
import hashlib


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
        print('Copying ', file.fileName,' to ', file.si)
        subprocess.call(['rsync','-r', self.fileName, self.si])
        
        
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
        print("Source Input Read Error")
        
        
# Build array of Storage Islands from destination       
def buildIslands(destinationInput):
    if os.path.isdir(destinationInput):
        for entry in os.scandir(destinationInput):
            islands.append(entry.path)
    elif os.path.isfile(destinationInput):
        with open(destinationInput) as fin:
            for line in fin:
                islands.append(line.strip())
        


if __name__ == '__main__':
    
    # Initialize the argument parser
    parser = argparse.ArgumentParser(
        description="File Transfer Script"
        )
    
    # Add parameters positional/optional(--)
    parser.add_argument('source', help="Source")
    parser.add_argument('destination', help="Destination")
    #TODO: add rsync options (-avrz) -v verbose, -a archive, -z compress
    
    
    
    # Parse the arguments
    args = parser.parse_args()
    mySource = args.source
    myDestination = args.destination
    print(args)
    
    
    buildList(mySource)
     
    buildIslands(myDestination)
        
    
    print("Number of files to be transferred: ", len(files))
    print("Number of storage islands available: ",len(islands))
    
    currentIsland = 0   
    #TODO: if ('df -h' < 75%) ->  assign; else pass
    for file in files:
        
        if currentIsland < len(islands):
            file.si = islands[currentIsland]
            currentIsland += 1
        else:
            currentIsland = 0
            file.si = islands[currentIsland]
        
    
    
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

        
        
    
   
    
    
    
    