from genericpath import exists
from statistics import mean
from timeit import repeat
import numpy as np
from enum import Flag, auto


class ClipFlags(Flag):
    Below = auto()
    Above = auto()
    Equal = auto()
    BelowAndAbove = Below | Above


class SplitFlags(Flag):
    OverlapInLoRows = auto()
    OverlapInHiRows = auto()
    OverlapInBothRows = OverlapInLoRows | OverlapInHiRows


class DataProvider:
    def __init__(self, ColumnHeaderKeysOrDict, NumpyArray: np.ndarray):
        if type(ColumnHeaderKeysOrDict) == dict:
            self.ColumnHeader = ColumnHeaderKeysOrDict.copy()
        else:
            if type(ColumnHeaderKeysOrDict) == str:
                ColumnHeaderKeysOrDict = [ColumnHeaderKeysOrDict]
            ColCnt = len(ColumnHeaderKeysOrDict)
            self.ColumnHeader = {ColumnHeaderKeysOrDict[i]: range(ColCnt)[i] for i in range(ColCnt)}
        if not type(NumpyArray) == np.ndarray:
            self.Data = np.array(NumpyArray).transpose()
        else:
            self.Data = np.array(NumpyArray, copy=True)  # Create a true copy
        
        self.__DetermineColumns__()
        if self.Columns == 1: # 1D-Vector to 2D-matrix
            self.Data = self.Data.reshape(-1, 1)

        if not self.Columns == len(ColumnHeaderKeysOrDict):
            raise ValueError("ColumnHeader-count not matching with DataColumns-count.")
        self.__DetermineRows__()

    def ClipData(self, ColumnKeyOrIndex, RemoveAtValue, ClipFlag: ClipFlags):
        clipCol = self.GetColumn(ColumnKeyOrIndex)
        removeIndicies = []
        # for iRow in range(len(clipCol)):
        #     if ClipFlags.Above in ClipFlag and clipCol[iRow] > RemoveAtValue:
        #         removeIndicies.append(iRow)
        #     if ClipFlags.Below in ClipFlag and clipCol[iRow] < RemoveAtValue:
        #         removeIndicies.append(iRow)
        #     if ClipFlags.Equal in ClipFlag and clipCol[iRow] == RemoveAtValue:
                # removeIndicies.append(iRow)

        if ClipFlags.Above in ClipFlag:
            removeIndicies = np.where(clipCol > RemoveAtValue)
        if ClipFlags.Below in ClipFlag:
            removeIndicies = np.where(clipCol < RemoveAtValue)
        if ClipFlags.Equal in ClipFlag:
            removeIndicies = np.where(clipCol == RemoveAtValue)

        self.RemoveRows(removeIndicies)
        return

    def GetData(self):
        return self.Data

    def GetRow(self, RowIndex):
        return self.Data[RowIndex, :]

    def OverrideRow(self, RowIndex, RowValues):
        self.Data[RowIndex, :] = RowValues
    
    def MeanRows(self, Key="Mean"):
        meanVals = [None] * self.Rows
        for row in range(self.Rows):
            meanVals[row] = mean(self.GetRow(row))

        self.AppendColumn(Key, meanVals)
    
    def MeanColumns(self):
        meanVals = [None] * self.Columns
        for iCol in range(self.Columns):
            meanVals[iCol] = mean(self.GetColumn(iCol))
        
        self.AppendRow(meanVals)
    
    def AbsColumn(self, ColumnKeyOrIndex):
        colIndex = self.__GetColumnIndexFromKey__(ColumnKeyOrIndex)
        self.Data[:, colIndex] = np.abs(self.Data[:, colIndex])

    def RemoveRows(self, RowIndicies):
        self.Data = np.delete(self.Data, RowIndicies, axis=0)
        self.__DetermineRows__()
        return

    def KeepRows(self, RowIndicies):
        if not type(RowIndicies) == range:
            RowIndicies = range(RowIndicies[0], RowIndicies[1])

        self.Data = self.Data[RowIndicies, :]
        self.__DetermineRows__()

    def MultiplyColumn(self, ColumnKeyOrIndex, ScalarOrSameSizeNDArray):
        colIndex = self.__GetColumnIndexFromKey__(ColumnKeyOrIndex)
        self.Data[:, colIndex] = np.multiply(self.Data[:, colIndex], ScalarOrSameSizeNDArray)
        return

    def DivideColumn(self, ColumnKeyOrIndex, ScalarOrSameSizeNDArray):
        self.Data[:, self.__GetColumnIndexFromKey__(ColumnKeyOrIndex)] = np.divide(
            self.Data[:, self.__GetColumnIndexFromKey__(ColumnKeyOrIndex)], ScalarOrSameSizeNDArray
        )
        return

    def DivideByColumn(self, ColumnKeyOrIndex, ScalarOrSameSizeNDArray):
        self.Data[:, self.__GetColumnIndexFromKey__(ColumnKeyOrIndex)] = np.divide(
            ScalarOrSameSizeNDArray, self.Data[:, self.__GetColumnIndexFromKey__(ColumnKeyOrIndex)]
        )
        return

    def AddToColumn(self, ColumnKeyOrIndex, ScalarOrSameSizeNDArray):
        self.Data[:, self.__GetColumnIndexFromKey__(ColumnKeyOrIndex)] = np.add(
            self.Data[:, self.__GetColumnIndexFromKey__(ColumnKeyOrIndex)], ScalarOrSameSizeNDArray
        )
        return

    def SubtractFromColumn(self, ColumnKeyOrIndex, ScalarOrSameSizeNDArray):
        self.Data[:, self.__GetColumnIndexFromKey__(ColumnKeyOrIndex)] = np.subtract(
            self.Data[:, self.__GetColumnIndexFromKey__(ColumnKeyOrIndex)], ScalarOrSameSizeNDArray
        )
        return

    def SubtractColumnFrom(self, ColumnKeyOrIndex, ScalarOrSameSizeNDArray):
        self.Data[:, self.__GetColumnIndexFromKey__(ColumnKeyOrIndex)] = np.subtract(
            ScalarOrSameSizeNDArray, self.Data[:, self.__GetColumnIndexFromKey__(ColumnKeyOrIndex)]
        )
        return

    def SplitDataAtRow(self, Index: int, SplitFlag: SplitFlags = SplitFlags.OverlapInBothRows):
        cRows = self.Rows
        Index = int(Index)
        # The short ifs define where the overlapping index is stored (loRows, hiRows or both!)
        loRows = self.Data[0 : Index + (1 if SplitFlags.OverlapInLoRows in SplitFlag else 0)]
        hiRows = self.Data[Index + (0 if SplitFlags.OverlapInHiRows in SplitFlag else 1) : cRows]

        return loRows, np.flip(hiRows, axis=0)

    def SeparateLineRepeats(self, RepeatsPerLine):
        # Check if RptsPerLine has a fractional part
        if not (RepeatsPerLine % 1) == 0:
            raise "Error: RepeatsPerLine not an integer value (float with fractional part)"
        RepeatsPerLine = int(RepeatsPerLine)
        # Check if Rows is a multiple of RepeatsPerLine!
        if not (self.Rows % RepeatsPerLine) == 0:
            raise "Error: Datarows not a multiple of given RepeatsPerLine."

        # Preparation
        tarRows = int(self.Rows / RepeatsPerLine)
        headerCells = [None] * self.Columns
        dataCells = [None] * self.Columns

        # Data manupulation
        for col in range(self.Columns):
            newData = np.reshape(self.GetColumn(col), (tarRows, RepeatsPerLine))
            newMean = np.zeros((tarRows, 1))
            for i in range(tarRows):
                newMean[i] = mean(newData[i, :])

            dataHeader = [None] * (RepeatsPerLine + 1)  # Single Points + 1xMean
            currHeadName = self.__GetKeyFromColumnIndex__(col)
            for i in range(RepeatsPerLine):
                dataHeader[i] = currHeadName + "-Pnt" + str(i)
            dataHeader[i + 1] = currHeadName + "-Mean"

            headerCells[col] = dataHeader
            dataCells[col] = np.column_stack((newData, newMean))

        # Create new combined data
        header = [None]
        dataShape = np.shape(dataCells[0])
        dataMatrix = np.zeros((dataShape[0], 1))
        for col in range(self.Columns):
            header = np.append(header, headerCells[col])
            dataMatrix = np.column_stack((dataMatrix, dataCells[col]))

        header = np.delete(header, 0).tolist()  # Remove [None] column and convert back to list
        dataMatrix = np.delete(dataMatrix, 0, axis=1)  # Remove [None] column
        dataBuilder = DataProvider(header, dataMatrix)

        # Use another DataProvider to build the new data and grab it from there
        self.ColumnHeader = dataBuilder.ColumnHeader
        self.Data = dataBuilder.Data
        self.__DetermineColumns__()
        self.__DetermineRows__()
        return

    def __RemoveRowsFromNumpyarray__(nparray: np.ndarray, Indicies):
        return np.delete(nparray, Indicies, axis=0)

    def __DetermineRows__(self):
        self.Rows = np.size(self.Data, axis=0)

    def __DetermineColumns__(self):
        if self.Data.shape.__len__() == 1:
            self.Columns = 1
        else:
            self.Columns = np.size(self.Data, axis=1)

    def GetColumn(self, ColumnKeyOrIndex):
        return self.Data[:, self.__GetColumnIndexFromKey__(ColumnKeyOrIndex)]
    
    def OverrideColumn(self, ColumnKeyOrIndex, ColumnValues):
        self.Data[:, self.__GetColumnIndexFromKey__(ColumnKeyOrIndex)] = ColumnValues
        return

    def AppendColumn(self, NewColumnKey, ColumnValues):
        if not type(NewColumnKey) == str:
            raise "Error: ColumnKey needs to be a string."
        if not self.Rows == len(ColumnValues):
            raise "Error: Given column not matching in rows"

        for key in self.ColumnHeader.keys():
            if key == NewColumnKey:
                raise Exception("Error: Key already existing")

        self.ColumnHeader[NewColumnKey] = self.Columns
        self.Data = np.column_stack((self.Data, ColumnValues))
        self.__DetermineColumns__()
        return

    def AppendRow(self, RowValues):
        self.Data = np.row_stack((self.Data, RowValues))
        self.__DetermineRows__()
        return

    def RemoveColumns(self, ColumnKeysOrIndicies):

        colKeys = self.__GetKeysFromColumnIndicies__(ColumnKeysOrIndicies)
        colIndicies = self.__GetColumnIndiciesFromKeys__(ColumnKeysOrIndicies)

        self.Data = np.delete(self.Data, colIndicies, axis=1)  # Remove data-column
        for key in colKeys:
            self.ColumnHeader.pop(key)  # Remove corresponding HeaderColumn-Entries
        self.__DetermineColumns__()  # Update self.Columns

        # Update the dictionary to match the new data-column-order
        kCnt = 0
        for key in self.ColumnHeader.keys():
            self.ColumnHeader[key] = kCnt
            kCnt += 1
        return

    def __GetColumnIndiciesFromKeys__(self, ColumnKeysOrIndicies):
        if type(ColumnKeysOrIndicies) == int or type(ColumnKeysOrIndicies) == str:
            ColumnKeysOrIndicies = [ColumnKeysOrIndicies]
        iCnt = len(ColumnKeysOrIndicies)
        indicies = [None] * iCnt
        for i in range(iCnt):
            indicies[i] = self.__GetColumnIndexFromKey__(ColumnKeysOrIndicies[i])
        return indicies

    def __GetColumnIndexFromKey__(self, ColumnKeyOrIndex):
        if type(ColumnKeyOrIndex) == str:
            return self.ColumnHeader[ColumnKeyOrIndex]
        else:
            return ColumnKeyOrIndex

    def __GetKeysFromColumnIndicies__(self, ColumnKeysOrIndicies):
        if type(ColumnKeysOrIndicies) == int or type(ColumnKeysOrIndicies) == str:
            ColumnKeysOrIndicies = [ColumnKeysOrIndicies]
        kCnt = len(ColumnKeysOrIndicies)
        keys = [None] * kCnt
        for i in range(kCnt):
            keys[i] = self.__GetKeyFromColumnIndex__(ColumnKeysOrIndicies[i])
        return keys

    def __GetKeyFromColumnIndex__(self, ColumnKeyOrIndex):
        if type(ColumnKeyOrIndex) == int:
            for key, value in self.ColumnHeader.items():
                if ColumnKeyOrIndex == value:
                    return key
        else:
            return ColumnKeyOrIndex


    ### Native operators
    def __getitem__(self, key):
        return self.GetColumn(key)

    def __setitem__(self, key, data):
        try: # to get the key: Success = Key already exists -> Override
            _i = self.__GetColumnIndexFromKey__(key)
            _key = self.__GetKeyFromColumnIndex__(_i)
            self.OverrideColumn(_key, data)

        except: # Failed = Key doesn't exist -> AppendColumn
            self.AppendColumn(key, data)

        return
