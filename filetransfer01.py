import argparse
import subprocess
import os


# Array of File objects
files = []
islands = []

# Create File class
class File(object):
    def __init__(self,fileName):
        self.fileName = fileName # file path
        self.si = ""             # storage island to copy to
        
        
    def moveFile(self):
        subprocess.call(['rsync','-r', self.fileName, self.si])
        

# Build array of file objects from source 
def buildList(sourceDirectory):
    for entry in os.scandir(sourceDirectory):
        files.append(File(entry.path))


if __name__ == '__main__':
    
    # Initialize the argument parser
    parser = argparse.ArgumentParser(
        description="File Transfer Script"
        )
    
    # Add parameters positional/optional(--)
    parser.add_argument('source', help="Source")
    #parser.add_argument('destination', help="Destination")
    
    
    
    # Parse the arguments
    args = parser.parse_args()
    mySource = args.source
    print(args)
    
    buildList(mySource)
        
     
    for entry in os.scandir('/home/pi/TestStorage'):
        islands.append(entry.path)
        
    print(len(islands))
    
    currentIsland = 0   
    # TODO: for storageIslands in /TestStorage assign a si to each file in files array
    # if ('df -h' < 75%) ->  assign; else pass
    for file in files:
        
        if currentIsland < len(islands):
            file.si = islands[currentIsland]
            currentIsland += 1
        else:
            currentIsland = 0
            file.si = islands[currentIsland]
        
    
    
    # TODO: Implement threaded rsync -- https://github.com/jbd/msrsync
    
    # create subprocess to run rsync
    for file in files:
        #subprocess.call(['rsync','-r', file.fileName, file.si])
        #subprocess.call(['msrsync', '-p','4', file.fileName, file.si])
        file.moveFile()
        print('Transferring ', file.fileName,' to ', file.si)
    
    
   
    # TODO: Implement checksum after rsync complete -- hashlib?   
    
    
    
    