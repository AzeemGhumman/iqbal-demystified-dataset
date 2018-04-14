import os
import sys
from collections import OrderedDict
import glob
import ntpath
import ruamel.yaml as yaml
import codecs
import pdb

if len(sys.argv) < 3:
    print ("Error: Need <input folder> followed by <output folder>")
    exit()

inputFolders = sys.argv[1:-1] # every argument except last: input folder
outputFolder = sys.argv[-1] # last argument: output folder


listInputFiles = []
for inputFolder in inputFolders:
    listInputFiles.extend(glob.glob(os.path.join(os.getcwd(), inputFolder, "**", "*.yaml"), recursive = True))

print (str(len(listInputFiles)) + " input files found..")

urduOutputContents = []
romanOutputContents = []
englishOutputContents = []

for inputFilename in listInputFiles:
    with open(inputFilename, 'r') as inputFile:
      fileContents = inputFile.read()

      print ("Processing file: " + ntpath.basename(inputFilename))

      yamlObject = yaml.load(fileContents, Loader=yaml.Loader)
      shers = yamlObject['sher']
      for sher in shers:
          urduSher = [i['text'] for i in sher['sherContent'] if i['lang'] == 'ur'][0]
          urduLines = [line.strip() for line in urduSher.split("|")]

          romanSher = [i['text'] for i in sher['sherContent'] if i['lang'] == 'ro'][0]
          romanLines = [line.strip() for line in romanSher.split("|")]

          englishSher = [i['text'] for i in sher['sherContent'] if i['lang'] == 'en'][0]
          englishLines = [line.strip() for line in englishSher.split("|")]

          if len(urduLines) is not len(romanLines):
            print ("Error: Roman Lines mismatch")

          if len(urduLines) is not len(englishLines):
            print ("Error: English lines mismatch")

          urduOutputContents.extend(urduLines)
          romanOutputContents.extend(romanLines)
          englishOutputContents.extend(englishLines)

# Create output folder if it does not exist
absOutputFolderPath = os.path.join(os.path.join(os.getcwd(), outputFolder))
if not os.path.exists(absOutputFolderPath):
    os.makedirs(absOutputFolderPath)

# Dump urdu and roman data in 2 different files in the output folder given by user

outputFileName = os.path.basename(os.path.dirname(outputFolder))
urduOutputFilePath = os.path.join(absOutputFolderPath, outputFileName + ".ur")
romanOutputFilePath = os.path.join(absOutputFolderPath, outputFileName + ".ro")
englishOutputFilePath = os.path.join(absOutputFolderPath, outputFileName + ".en")

with open(urduOutputFilePath, 'w') as outputFile:
    outputFile.write("\n".join(urduOutputContents))

with open(romanOutputFilePath, 'w') as outputFile:
    outputFile.write("\n".join(romanOutputContents))

with open(englishOutputFilePath, 'w') as outputFile:
    outputFile.write("\n".join(englishOutputContents))
