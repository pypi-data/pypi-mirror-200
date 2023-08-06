from logging import exception
import random
from FieldEmission.dataProvider import *
import numpy as np
import math
from scipy.optimize import curve_fit
import scipy.constants as sciConst


def __1dPoly__(x, a, b):
    y = np.add(np.multiply(a, x), b)
    return y


def GetLinearFitParam(x, y):
    popt, pcov = curve_fit(__1dPoly__, x, y)
    yGrad = popt[0]
    yOff = popt[1]
    return __1dPoly__, yGrad, yOff


def FowlerNordheimParameters(DatMgr: DataProvider, ColumnFnX="FNx", ColumnFnY="FNx", xFitRegion=[0, 0.5], distance_µm=50, phiMaterial=4.8, interpolate=[0.025, 2], nInterpolPnts=100):
    # Theory from Lagotzy
    A = 154  # [A eV V^-2]
    B = 6830 # [eV**(-1,5) V m**(-1)]

    fnx = DatMgr.GetColumn(ColumnFnX)
    fny = DatMgr.GetColumn(ColumnFnY)
    _iRegion = np.where((fnx >= xFitRegion[0]) & (fnx <= xFitRegion[1]))
    fnx = fnx[_iRegion]
    fny = fny[_iRegion]

    _iMaxSplit = (np.where(fnx == max(fnx))[-1][-1] + 1)  // 2
    # vec1 = fnx[:_iMaxSplit]
    # vec2 = fnx[_iMaxSplit:]
    # fnx = np.mean((vec1, vec2), axis=0)
    # vec1 = fny[:_iMaxSplit]
    # vec2 = fny[_iMaxSplit:]
    # fny = np.mean((vec1, vec2), axis=0)

    fitFunc, fnGrad, fnYOff = GetLinearFitParam(fnx, fny)

    fitX = np.linspace(interpolate[0], interpolate[1], nInterpolPnts)
    fitY = fitFunc(fitX, fnGrad, fnYOff)

    aFN = np.exp(fnYOff)
    bFN = -fnGrad

    betaF = (B * phiMaterial**1.5) / bFN
    gamma = betaF / distance_µm
    areaS = (aFN * phiMaterial) / (A * betaF**2)

    fnProvider = DataProvider(["fnx", "fny"], [fitX, fitY])

    uiX = np.divide(distance_μm, fitX)
    uiProvider = CreateIdealFowlerNordheimUI(uVector_V=uiX, betaF=betaF, distance_µm=distance_μm, phiMaterial=phiMaterial, areaS_cm2=areaS, noiseLevel=1e-12)

    params = {
        "beta": betaF,
        "gamma": gamma,
        "areaS": areaS,
        "fitFunc1D": fitFunc,
        "interpolatedFN": fnProvider,
        "interpolatedUI": uiProvider
    }
    return params


def FowlerNordheim(DatMgr: DataProvider, ColumnU, ColumnI, distance_µm, Keys=["FNx", "FNy"], AppendToGiven=True):
    # Create copys of U and I (also for predefining correct array-size)
    fnX = abs(DatMgr.GetColumn(ColumnU))  # Here still U!
    fnY = abs(DatMgr.GetColumn(ColumnI))  # Here still I!

    fnX = np.divide(distance_µm, fnX)
    fnY = np.log(np.multiply(fnY, np.power(fnX, 2))) # Multiply, because fnX already 1/E!
    # for iRow in range(len(fnX)):
    #     fnX[iRow] = distance_m / fnX[iRow]  # Convert d/U = 1/E
    #     fnY[iRow] = math.log(fnY[iRow] * math.pow(fnX[iRow], 2))  # Convert I -> fnY

    fn = DataProvider(Keys, np.transpose([fnX, fnY]))
    if AppendToGiven == True:
        # DatMgr = DatMgr.AppendColumn(Keys[0], fnX)
        # DatMgr = DatMgr.AppendColumn(Keys[1], fnY)
        DatMgr.AppendColumn(Keys[0], fnX)
        DatMgr.AppendColumn(Keys[1], fnY)
    return fn


def CreateIdealFowlerNordheimUI(uVector_V, betaF=np.double, distance_µm=50, phiMaterial=4.8, areaS_cm2=1e-12, noiseLevel=1e-12):
    vType = type(uVector_V)
    if not vType == range and not vType == list and not vType == np.ndarray:
        raise ('Error: voltagesU is not type "range", "list" or "numpy.ndarray"')

    if vType == range:
        vList = list(uVector_V)
    else:
        vList = uVector_V

    if vType == list or vType == range:
        U = np.array(vList)
    else:
        U = uVector_V

    # Constants for getting I [A]: E [MV/m], S [cm²], phi [eV]
    _A = 154  # A * e * V * V^-2 | Combines all constants together
    _B = 6830  # eV^3/2 * V / m | Combines all power-constants together

    # "Map" parameters
    _beta = betaF
    _d_µm = distance_µm
    _phi = phiMaterial
    _S = areaS_cm2
    _nL = noiseLevel
    _n = 0.5e-12

    # Build E-Field-Vector in MegaVolt/Meter
    E = U / _d_μm  # Build MV/m (== V/µm)
    ETip = E * _beta  # Build enhanced field

    const = (_A * _S) / (_phi)
    expConst = -_B * (_phi**1.5)

    numVals = const * (ETip**2)
    expVals = expConst / ETip
    expMul = np.exp(expVals)
    fnI = np.multiply(numVals, expMul)

    for index in range(U.__len__()):
        if abs(fnI[index]) < _nL:
            rVal = random.random() - 0.5
            fnI[index] = _nL * rVal

    data = np.array([U, fnI])
    rProvider = DataProvider(["U", "I"], np.transpose(data))
    return rProvider
