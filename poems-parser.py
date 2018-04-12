import os
import sys
from enum import IntEnum
from collections import OrderedDict
import glob
import ntpath
import ruamel.yaml as yaml
import codecs
import pdb

if (len(sys.argv) is not 3):
    print ("Error: Need <input folder> followed by <output folder>")
    exit()

inputFolder = sys.argv[1] # first argument: input folder
outputFolder = sys.argv[2] # second argument: output folder

TOTAL_PORTIONS = 8
class PortionEnum(IntEnum):
    UrduHeading = 0
    UrduText = 1
    EnglishHeading = 2
    EnglishIntro = 3
    EnglishText = 4
    EnglishNotes = 5
    AudioUrl = 6
    RomanText = 7

def getPortions(contents):
    allPortions = []
    portion = []
    for line in contents:
        line = line.strip()
        if (line.strip() == "*"):
            allPortions.append(portion)
            portion = []
        elif (len(line) == 0):
            pass
        else:
            portion.append(line)

    if (len(allPortions) is not TOTAL_PORTIONS):
        print ("Error: total portions not what was expected")
    return allPortions

def readFile(filename):
    f = open(filename)
    contents = f.readlines()
    f.close()
    return contents

def getUrduHeading(portionUrduHeading):
    if (len(portionUrduHeading) is 0):
        print ("Error: parsing urdu heading")
    return ' | '.join(portionUrduHeading)

def getEnglishHeading(portionEnglishHeading):
    if (len(portionEnglishHeading) is 0):
        print ("Error: parsing english heading")
    return ' | '.join(portionEnglishHeading)

def getEnglighIntroduction(portionEnglishIntroduction):
    if portionEnglishIntroduction == []: # optional parameter
        return ""
    return ' | '.join(portionEnglishIntroduction)

def getAudioUrl(portionAudioUrl):
    if portionAudioUrl == []: # optional parameter
        return ""
    if portionAudioUrl[0].strip() == 'no audio':
        return ""
    if len(portionAudioUrl) > 1:
        print ("Error: audio url cannot be more than 1 line")
    return portionAudioUrl[0]

def getListShers(poemText):
    shers = []
    buffer = ""
    for line in poemText:
        if line.startswith('@'):
            metaText = line[1:].strip()
            shers.append([metaText, True])
        elif buffer == "":
            buffer += line
        else:
            line = buffer + " | " + line
            shers.append([line, False])
            buffer = ""
    return shers

def areLanguagesSynced(urdu, english, roman):
    totalUrduShers = len(urdu)
    totalEnglishShers = len(english)
    totalRomanShers = len(roman)

    # Compare length of different languages
    if totalEnglishShers > 0 and totalEnglishShers is not totalUrduShers:
        return False
    if totalRomanShers > 0 and totalRomanShers is not totalUrduShers:
        return False

    # Check types of sher for each sher for all lanaguges
    if totalEnglishShers > 0:
        for index in range(0, totalUrduShers):
            if urdu[index][1] is not english[index][1]:
                return False

    if totalRomanShers > 0:
        for index in range(0, totalUrduShers):
            if urdu[index][1] is not roman[index][1]:
                return False

    # Passed all the tests: Must be fine
    return True

def getEnglishNotes(notes):
    # Strip off the number in the start
    updatedNotes = [note[note.find(" ") + 1:] for note in notes]
    return updatedNotes

def generateNotes(sher, notes):
    # Find all the notes in this sher
    words = sher.split(' ')
    phraseIndices = [index - 1 for index, word in enumerate(words) if word.startswith('$')]

    notesList = []
    for phraseIndex in phraseIndices:
        notesObject = OrderedDict()
        notesObject['phrase'] = words[phraseIndex]

        noteString = ''.join(filter(lambda x: x.isdigit(), words[phraseIndex + 1]))
        notesObject['meaning'] = notes[int(noteString) - 1]

        notesObject['occurrence'] = 1
        notesList.append(dict(notesObject))
    return notesList

def removeNoteMarkers(sher):
    return ' '.join([i for i in sher.split(" ") if not i.startswith('$')])


# Get list of .txt files from the input folder
listInputFiles = glob.glob(os.path.join(os.getcwd(), inputFolder, "**", "*.txt"), recursive = True)
print (str(len(listInputFiles)) + " input files found..")

for inputFilename in listInputFiles:

    poemId = ntpath.basename(inputFilename)[:-4]
    print ("Processing file: " + str(poemId))

    # Read file
    contents = readFile(inputFilename)

    # Get file portions
    portions = getPortions(contents)

    # Get urdu heading
    UrduHeading = getUrduHeading(portions[PortionEnum.UrduHeading])

    # Get english heading
    EnglishHeading = getEnglishHeading(portions[PortionEnum.EnglishHeading])

    # Get english introduction
    EnglishIntroduction = getEnglighIntroduction(portions[PortionEnum.EnglishIntro])

    # Get audio url
    AudioUrl = getAudioUrl(portions[PortionEnum.AudioUrl])

    # Get urdu shers
    UrduShers = getListShers(portions[PortionEnum.UrduText])

    # get english shers
    EnglishShers = getListShers(portions[PortionEnum.EnglishText])

    # get roman shers
    RomanShers = getListShers(portions[PortionEnum.RomanText])

    # Sanity check - all languages content must match in size (length of shers) and type (meta)
    # English or Roman or both can be missing

    # Get english notes
    EnglishNotes = getEnglishNotes(portions[PortionEnum.EnglishNotes])

    isValidText = areLanguagesSynced(UrduShers, EnglishShers, RomanShers)

    # Poem object that will hold the whole yaml data
    poemObject = OrderedDict()

    # Add PoemId
    poemObject['id'] = poemId

    # Add AudioUrl
    # TODO: no audio vs empty audio
    poemObject['audioUrl'] = AudioUrl

    # Add headings
    headingList = []
    if (UrduHeading is not ""):
        headingObject = OrderedDict()
        headingObject['lang'] = 'ur'
        headingObject['text'] = UrduHeading
        headingList.append(dict(headingObject))

    if (EnglishHeading is not ""):
        headingObject = OrderedDict()
        headingObject['lang'] = 'en'
        headingObject['text'] = EnglishHeading
        headingList.append(dict(headingObject))

    poemObject['heading'] = headingList

    # Add Introduction
    introList = []
    if (EnglishIntroduction is not ""):
        introObject = OrderedDict()
        introObject['lang'] = 'en'
        introObject['text'] = EnglishIntroduction
        introList.append(dict(introObject))
    poemObject['description'] = introList

    # Add Shers
    sherList = []
    for sherIndex in range(len(UrduShers)):
        sherObject = OrderedDict()
        sherObject["id"] = poemId + "_" + '{:03d}'.format(sherIndex + 1)
        sherObject["meta"] = UrduShers[sherIndex][1]

        sherContent = []

        # Add urdu sher to sherContent
        urduSherContent = OrderedDict()
        urduSherContent["lang"] = "ur"
        urduSherContent["text"] = UrduShers[sherIndex][0]
        sherContent.append(dict(urduSherContent))

        if len(EnglishShers) is not 0:
            # Add notes
            notesList = generateNotes(EnglishShers[sherIndex][0], EnglishNotes)
            EnglishShers[sherIndex][0] = removeNoteMarkers(EnglishShers[sherIndex][0])

            englishSherContent = OrderedDict()
            englishSherContent["lang"] = "en"
            englishSherContent["text"] = EnglishShers[sherIndex][0]
            if (len(notesList) > 0):
                englishSherContent["notes"] = notesList
            sherContent.append(dict(englishSherContent))

        if len(RomanShers) is not 0:
            romanSherContent = OrderedDict()
            romanSherContent["lang"] = "ro"
            romanSherContent["text"] = RomanShers[sherIndex][0]
            sherContent.append(dict(romanSherContent))

        sherObject["sherContent"] = sherContent
        sherList.append(dict(sherObject))

    poemObject['sher'] = sherList

    poemObject = dict(poemObject)

    # TODO: Not proud of this. Doing this because there are sub-folders in input directory
    # Issue: If the input folder name comes somewhere else in the path, it will get replaced too
    outputFilename = inputFilename.replace(inputFolder, outputFolder)
    outputFilename = outputFilename.replace(".txt", ".yaml")

    if not os.path.exists(os.path.dirname(outputFilename)):
        os.makedirs(os.path.dirname(outputFilename))

    with codecs.open(outputFilename, "w", "utf-8") as outputFile:
        yaml.dump(poemObject,
                  outputFile,
                  Dumper = yaml.RoundTripDumper,
                  encoding = "utf-8",
                  allow_unicode = True,
                  explicit_start = True,
                  width = 10000,
                  default_style="'"
                  )
print ("Done")
