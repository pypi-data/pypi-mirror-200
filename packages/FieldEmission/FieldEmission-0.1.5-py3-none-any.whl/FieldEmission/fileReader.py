import numpy as np
import re


def ReadDataFile(Filename):
    f = open(Filename)
    lines = f.readlines()
    f.close()
    # Search for header column and create a dictionary for
    cCommentLines = 0
    for iLine in range(0, len(lines)):
        currLine = lines[iLine]
        if currLine.startswith("#"):  # Check for possible header-line
            # Remove distrubing characters
            currLine = re.sub("\t|\#|\ |\n", "", currLine)
            splitLine = currLine.split(",")
            if len(splitLine) > 1:  # Has it at least 2 entries?
                ColumnCount = len(splitLine)  # Get amount of columns
                # Make dictionary and basic numpy-structure
                HeaderColumn = {splitLine[i]: range(ColumnCount)[i] for i in range(ColumnCount)}
                break
    del f

    # Parse data and insert to numpy-array
    data = []
    for iLine in range(0, len(lines)):
        currLine = lines[iLine]
        if currLine.startswith("#"):  # Check if line is a comment
            continue
        currLine = re.sub("\t|\#|\ |\n", "", currLine)
        if currLine == "":  # or empty
            continue

        # Dataline found -> Parse and enter to numpy-array
        split = currLine.split(",")
        if len(split) == ColumnCount:
            for iSplit in range(len(split)):
                split[iSplit] = float(split[iSplit].strip("\t "))
            data.append(split)
    Data = np.array(data)  # Convert list to numpy-array
    return HeaderColumn, Data


def ReadSweepFile(Filename, ExpandRpts=True):
    f = open(Filename)
    lines = f.readlines()
    f.close()
    # Search for header column and create a dictionary for
    cCommentLines = 0
    for iLine in range(0, len(lines)):
        currLine = lines[iLine]
        currLine = re.sub("\t|\#|\ |\n", "", currLine) # Remove distrubing characters
        if currLine.startswith("Rpts"):  # Check for possible header-line
            splitLine = currLine.split(",")
            if len(splitLine) > 1:  # Has it at least 2 entries?
                ColumnCount = len(splitLine)  # Get amount of columns
                # Make dictionary and basic numpy-structure
                HeaderColumn = {splitLine[i]: range(ColumnCount)[i] for i in range(ColumnCount)}
                break
    del f

    # Parse data and insert to numpy-array
    data = []
    OriginalRpts = []
    for iLine in range(0, len(lines)):
        currLine = lines[iLine]
        currLine = re.sub("\t|\#|\ |\n", "", currLine)
        if currLine.startswith("Rpts"):  # Check if line is a comment
            continue
        if currLine == "":  # or empty
            continue

        # Dataline found -> Parse and enter to numpy-array
        split = currLine.split(",")
        if len(split) == ColumnCount:
            for iSplit in range(len(split)):
                split[iSplit] = float(split[iSplit].strip("\t "))

            if ExpandRpts == True:              # Expand repeats into "Rpts=1" lines?
                OriginalRpts.append(int(split[0]))   # Get amound of repeats
                split[0] = 1                    # Replace origin Rpts with 1
                for rpt in range(OriginalRpts[-1]):
                    data.append(split)          # Add rpts lines with "Rpts=1" lines
            else:
                data.append(split)              # Otherwise append original line

    Data = np.array(data)  # Convert list to numpy-array
    return HeaderColumn, Data, OriginalRpts