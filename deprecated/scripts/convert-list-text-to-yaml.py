import os
import sys
import ruamel.yaml as yaml
import codecs
import pdb
import glob

if (len(sys.argv) is not 3):
    print ("Error: Need <input folder> followed by <output folder>")
    exit()

inputFolder = sys.argv[1] # first argument: input folder
outputFolder = sys.argv[2] # second argument: output folder

def readFile(filePath):
    f = open(filePath)
    contents = f.readlines()
    f.close()
    return contents

def formatIdentifier(id):
    # Split at '_', then format each portion and then join the 2 numbers together
    return '_'.join(['{:03d}'.format(int(num)) for num in id.split("_")])

# Get list of .txt files from the input folder
listInputFiles = glob.glob(os.path.join(os.getcwd(), inputFolder, "*.txt"))
print (str(len(listInputFiles)) + " input files found..")

for inputFilename in listInputFiles:

    currentFilename = os.path.basename(inputFilename)
    print ("Processing file: " + currentFilename)

    # Read input file
    data = readFile(inputFilename)

    total_lines = len(data)

    if total_lines == 1:
        print ("Warning: Fcile: " + currentFilename + " is empty")
    elif total_lines % 3 is not 0:
        print ('Error: total lines must be multiple of 3')

    total_records = int(total_lines / 3)

    sections = []
    poems = []
    for i in range(total_records):
        identifier, urdu, english = data[(i * 3) : (i * 3) + 3]
        identifier, urdu, english = identifier.strip(), urdu.strip(), english.strip()

        # Is Section
        if '#' in identifier:
            if len(poems) > 0:
                sections.append({'poems' : poems})
                poems = []
            sections.append({'sectionName': [{'lang': 'ur', 'text': urdu}, {'lang': 'en', 'text': english}]})

        else:
            identifier = formatIdentifier(identifier)
            poems.append({'id' : identifier, 'poemName': [{'lang': 'ur', 'text': urdu}, {'lang': 'en', 'text': english}]})

    # Add poems of the last section to the object
    if len(poems) > 0:
        sections.append({'poems' : poems})

    listPoem = {'sections' : sections}

    # Get name of output file
    outputFilename = currentFilename[:-4] + '.yaml'
    outputFilePath = os.path.join(os.getcwd(), outputFolder, outputFilename)

    # Create output folder if it does not exist
    if not os.path.exists(os.path.dirname(outputFilePath)):
        os.makedirs(os.path.dirname(outputFilePath))

    with codecs.open(outputFilePath, "w", "utf-8") as outputFile:
        yaml.dump(listPoem,
                  outputFile,
                  Dumper = yaml.RoundTripDumper,
                  encoding = "utf-8",
                  allow_unicode = True,
                  explicit_start = True,
                  width = 10000
                  )
print ("Done")
