import os
import math
import argparse
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
# from scipy import optimize
import seaborn as sns
from PIL import Image
# this script corresponding to v2 metrology drawing.

def getMinMax(inList):
  min = 10000
  max = -10000
  for element in inList:
    if element<min:
      min = element
    if element>max:
      max = element
  return [min, max]

def getAvg(inList):
  sum = 0
  for element in inList:
    sum = sum+element
  return sum/len(inList)

def process_data(inFile, outPath, run_num_str):
  outPath = outPath + '/'

  passMetrology = True
  ## FM Refreence Position
  XABCFM1X_Ref = [0.899,10.563,20.227,29.891,39.555,49.219,58.883,68.547,78.211,87.875]
  XABCFM2X_Ref = [8.501,18.165,27.829,37.493,47.157,56.821,66.485,76.149,85.813,95.477]
  XABCFMY_Ref = 1.198
  XHCCFM1_Ref = [6.721, 7.319]
  XHCCFM2_Ref = [11.653, 7.319]

  YABCFM1X_Ref = [0.875,10.539,20.203,29.867,39.531,49.195,58.859,68.523,78.187,87.851]
  YABCFM2X_Ref = [8.478,18.142,27.806,37.47,47.134,56.798,66.492,76.126,85.79,95.454]
  YABCFMY_Ref = 1.193
  YHCCFM1_Ref = [6.698, 7.315]
  YHCCFM2_Ref = [11.629, 7.315]
  ##------------------

  lines = inFile.readlines()

  # extract Hybrid ID
  HybridID = ""
  for line in lines:
    if line.startswith("Hybrid Ref Number"):
      HybridID = line.strip("\n").split(":",1)[-1].strip()
      break
  # extract Hybrid Type
  HybridType = ""
  for line in lines:
    if line.startswith("Hybrid Type"):
      HybridType = line.strip("\n").split(":",1)[-1].strip()
      break
  # extract Date
  Date = ""
  for line in lines:
    if line.startswith("Measurement Date/Time"):
      Date = line.strip("\n").split(":",1)[-1].strip()
      break
  # extract Institute
  Institute = ""
  for line in lines:
    if line.startswith("Institute"):
      Institute = line.strip("\n").split(":",1)[-1].strip()
      break
  # extract Instrument
  Instrument = ""
  for line in lines:
    if line.startswith("Instrument Used"):
      Instrument = line.strip("\n").split(":",1)[-1].strip()
      break
  # extract Operator
  Operator = ""
  for line in lines:
    if line.startswith("Operator"):
      Operator = line.strip("\n").split(":",1)[-1].strip()
      break
  # extract RunNumber
  RunNumber = ""
  for line in lines:
    if line.startswith("Test Run Number"):
      RunNumber = line.strip("\n").split(":",1)[-1].strip()
      break


  #extract ABC Position
  iPosition = 0
  for line in lines:
    line = line.strip('\n')
    if line.startswith("#---Position Scan"):
      break
    iPosition = iPosition+1
  iPosition = iPosition+4

  ABCFM1 = []
  ABCFM2 = []
  ABCFMDistance = []
  ABCFM1Diff = []
  ABCFM2Diff = []
  for index in range(10):
    ABCFM1.append([])
    ABCFM2.append([])
    ABCFM1Diff.append([])
    ABCFM2Diff.append([])
  for index in range(10):
    line = lines[iPosition]
    list = line.strip('\n').split(" ")
    while "" in list:
      list.remove("")
    ABCFM1[index].append(float(list[1]))
    ABCFM1[index].append(float(list[2]))
    iPosition = iPosition+1
    line = lines[iPosition]
    list = line.strip('\n').split(" ")
    while "" in list:
      list.remove("")
    ABCFM2[index].append(float(list[1]))
    ABCFM2[index].append(float(list[2]))
    iPosition = iPosition+1

    #calculate the distance between two FMs
    distance = math.sqrt(pow(ABCFM1[index][0]-ABCFM2[index][0], 2)+pow(ABCFM1[index][1]-ABCFM2[index][1], 2))
    ABCFMDistance.append(distance)

    #Calculate the Difference of FM position with the reference values
    if HybridType=="HX":
      ABCFM1Diff[index].append(ABCFM1[index][0]-XABCFM1X_Ref[index])
      ABCFM1Diff[index].append(ABCFM1[index][1]-XABCFMY_Ref)
      ABCFM2Diff[index].append(ABCFM2[index][0]-XABCFM2X_Ref[index])
      ABCFM2Diff[index].append(ABCFM2[index][1]-XABCFMY_Ref)
    else:
      ABCFM1Diff[index].append(ABCFM1[index][0]-YABCFM1X_Ref[index])
      ABCFM1Diff[index].append(ABCFM1[index][1]-YABCFMY_Ref)
      ABCFM2Diff[index].append(ABCFM2[index][0]-YABCFM2X_Ref[index])
      ABCFM2Diff[index].append(ABCFM2[index][1]-YABCFMY_Ref)

  ## FM Position within 0.1 mm of the reference positions
  for index in range(0, 10):
    if abs(ABCFM1Diff[index][0])>0.1 or abs(ABCFM1Diff[index][1])>0.1:
      passMetrology = False
      if HybridType=="HX":
        st.write("ABC_{0} FM1 Position Failed!!!!".format(9-index))
      else:
        st.write("ABC_{0} FM1 Position Failed!!!!".format(index))
    if abs(ABCFM2Diff[index][0])>0.1 or abs(ABCFM2Diff[index][1])>0.1:
      passMetrology = False
      if HybridType=="HX":
        st.write("ABC_{0} FM2 Position Failed!!!!".format(9-index))
      else:
        st.write("ABC_{0} FM2 Position Failed!!!!".format(index))

  # FM distance within 7.602 +- 0.01 mm
  for distance in ABCFMDistance:
    if distance<(7.602-0.01) or distance>(7.602+0.01):
      passMetrology = False
      #st.write("ABC FM Distance Failed!!!!")

  HCCFM1 = []
  HCCFM2 = []
  line = lines[iPosition]
  list = line.strip('\n').split(" ")
  while "" in list:
    list.remove("")
  HCCFM1.append(float(list[1]))
  HCCFM1.append(float(list[2]))
  iPosition = iPosition+1

  line = lines[iPosition]
  list = line.strip('\n').split(" ")
  while "" in list:
    list.remove("")
  HCCFM2.append(float(list[1]))
  HCCFM2.append(float(list[2]))

  HCCFM1Diff = []
  HCCFM2Diff = []
  if HybridType=="HX":
    HCCFM1Diff.append(HCCFM1[0]-XHCCFM1_Ref[0])
    HCCFM1Diff.append(HCCFM1[1]-XHCCFM1_Ref[1])
    HCCFM2Diff.append(HCCFM2[0]-XHCCFM2_Ref[0])
    HCCFM2Diff.append(HCCFM2[1]-XHCCFM2_Ref[1])
  else:
    HCCFM1Diff.append(HCCFM1[0]-YHCCFM1_Ref[0])
    HCCFM1Diff.append(HCCFM1[1]-YHCCFM1_Ref[1])
    HCCFM2Diff.append(HCCFM2[0]-YHCCFM2_Ref[0])
    HCCFM2Diff.append(HCCFM2[1]-YHCCFM2_Ref[1])
  if abs(HCCFM1Diff[0])>0.1 or abs(HCCFM1Diff[1])>0.1:
    passMetrology = False
    st.write("HCC FM1 Position Failed!!!!")
  if abs(HCCFM2Diff[0])>0.1 or abs(HCCFM2Diff[1])>0.1:
    passMetrology = False
    st.write("HCC FM2 Position Failed!!!!")

  HCCFMDistance = math.sqrt(pow(HCCFM1[0]-HCCFM2[0], 2)+pow(HCCFM1[1]-HCCFM2[1], 2))
  if HCCFMDistance<(4.932-0.01) or HCCFMDistance>(4.932+0.01):
    passMetrology = False
    #st.write("HCC FM Distance Failed!!!!!!")

  #extract Glue Height
  iPosition = iPosition+3
  HybridPositions = []
  ABCPositions = []
  for index1 in range(4):
    HybridPositions.append([])
    ABCPositions.append([])
    for index2 in range(10):
      HybridPositions[index1].append([])
      ABCPositions[index1].append([])
  for index2 in range(10):
    for index1 in range(4):
      line = lines[iPosition]
      list = line.strip('\n').split(" ")
      while "" in list:
        list.remove("")
      HybridPositions[index1][index2].append(float(list[2]))
      HybridPositions[index1][index2].append(float(list[3]))
      HybridPositions[index1][index2].append(float(list[4]))
      iPosition = iPosition+1
    for index1 in range(4):
      line = lines[iPosition]
      list = line.strip('\n').split(" ")
      while "" in list:
        list.remove("")
      ABCPositions[index1][index2].append(float(list[2]))
      ABCPositions[index1][index2].append(float(list[3]))
      ABCPositions[index1][index2].append(float(list[4]))
      iPosition = iPosition+1

  # calculate glue height and ABC tilt
  ABCGlueHeight = []
  Tilt_BE = []
  Tilt_FE = []
  Height_tune1 = [ 0.015, 0.01, 0.011, 0.005, 0.005, 0.005, 0.005, 0.005, 0.0, 0.005]
  for index in range(10):
    Height1 = (ABCPositions[0][index][2] - HybridPositions[0][index][2] - 0.3) * 1000
    Height2 = (ABCPositions[1][index][2] - HybridPositions[1][index][2] - 0.3) * 1000
    Height3 = (ABCPositions[2][index][2] - HybridPositions[2][index][2] - 0.3) * 1000
    Height4 = (ABCPositions[3][index][2] - HybridPositions[3][index][2] - 0.3) * 1000
    # Height = (Height1+Height2+Height3+Height4)/4 - Height_tune1[9-index]*1000
    Height = (Height1+Height2+Height3+Height4)/4 
    ABCGlueHeight.append(Height)


    Tilt_BE.append(abs(ABCPositions[0][index][2]-ABCPositions[1][index][2])/(math.sqrt(pow(ABCPositions[0][index][0]-ABCPositions[1][index][0], 2)+pow(ABCPositions[0][index][1]-ABCPositions[1][index][1], 2))))
    Tilt_FE.append(abs(ABCPositions[2][index][2]-ABCPositions[3][index][2])/(math.sqrt(pow(ABCPositions[2][index][0]-ABCPositions[3][index][0], 2)+pow(ABCPositions[2][index][1]-ABCPositions[3][index][1], 2))))


    if Height>160:
      passMetrology = False
      if HybridType=="HX":
        st.write("ABC_{0} Glue Height Failed!!!!".format(9-index))
      else:
        st.write("ABC_{0} Glue Height Failed!!!!".format(index))
    if Height<80:
      if HybridType=="HX":
        st.write("ABC_{0} Glue Height < 80 microns!!!!".format(9-index))
      else:
        st.write("ABC_{0} Glue Height < 80 microns!!!!".format(index))

  HybridHCCPositions = [[], [], [], []]
  HCCPositions = [[], [], [], []]
  for index in range(4):
    line = lines[iPosition]
    list = line.strip('\n').split(" ")
    while "" in list:
      list.remove("")
    HybridHCCPositions[index].append(float(list[2]))
    HybridHCCPositions[index].append(float(list[3]))
    HybridHCCPositions[index].append(float(list[4]))
    iPosition = iPosition+1
  for index in range(4):
    line = lines[iPosition]
    list = line.strip('\n').split(" ")
    while "" in list:
      list.remove("")
    HCCPositions[index].append(float(list[2]))
    HCCPositions[index].append(float(list[3]))
    HCCPositions[index].append(float(list[4]))
    iPosition = iPosition+1

  Height1 = (HCCPositions[0][2] - HybridHCCPositions[0][2] - 0.3) * 1000
  Height2 = (HCCPositions[1][2] - HybridHCCPositions[1][2] - 0.3) * 1000
  Height3 = (HCCPositions[2][2] - HybridHCCPositions[2][2] - 0.3) * 1000
  Height4 = (HCCPositions[3][2] - HybridHCCPositions[3][2] - 0.3) * 1000
  HCCGlueHeight = (Height1+Height2+Height3+Height4)/4.
  if HCCGlueHeight<80 or HCCGlueHeight>160:
    passMetrology = False
    st.write("HCC Glue Height Failed!!!!")
  
  # HCC Tilt
  # should be TiltX: 23; Y: 03;
  HCCTiltX = abs(HCCPositions[2][2]-HCCPositions[3][2])/(math.sqrt(pow(HCCPositions[2][0]-HCCPositions[3][0], 2)+pow(HCCPositions[2][1]-HCCPositions[3][1], 2)))
  HCCTiltY = abs(HCCPositions[0][2]-HCCPositions[3][2])/(math.sqrt(pow(HCCPositions[0][0]-HCCPositions[3][0], 2)+pow(HCCPositions[0][1]-HCCPositions[3][1], 2)))
  
  for index in range(10):
    if Tilt_FE[index]>0.025:
      if HybridType=="HX":
        st.write("ABC_{0} Frontend Tilt Failed!!!!".format(9-index))
      else:
        st.write("ABC_{0} Frontend Tilt Failed!!!!".format(index))
  for index in range(10):
    if Tilt_BE[index]>0.025:
      if HybridType=="HX":
        st.write("ABC_{0} Backend Tilt Failed!!!!".format(9-index))
      else:
        st.write("ABC_{0} Backend Tilt Failed!!!!".format(index))
 
  # HCC Tilt
  if HCCTiltX>0.025:
    passMetrology = False
    st.write("HCC X-Tilt Failed!!!!")
  if HCCTiltY>0.025:
    passMetrology = False
    st.write("HCC Y-Tilt Failed!!!!")

  #extract Package Height
  JIGPositions = []
  JIGSurfN = 4
  for index in range(JIGSurfN):
    JIGPositions.append([])
    line = lines[iPosition]
    list = line.strip('\n').split(" ")
    while "" in list:
      list.remove("")
    JIGPositions[index].append(float(list[2]))
    JIGPositions[index].append(float(list[3]))
    JIGPositions[index].append(float(list[4]))
    iPosition = iPosition+1
  
  Height0 = 0
  for index in range(JIGSurfN):
    Height0 = Height0+JIGPositions[index][2]
  
  Height0 = Height0 / JIGSurfN
  # calculate ABC package height
  ABCPackageHeight = []
  x0 = []
  y0 = []
  z0 = []
  Height_tune2 = [ 0.010, 0.005, 0.005, 0.010, 0.0, 0.0, 0.0, -0.01, -0.003, -0.005]
  for index in range(10):
    # Height0 = (JIGPositions[0][2]+JIGPositions[1][2]+JIGPositions[2][2]+JIGPositions[3][2]+JIGPositions[4][2]+JIGPositions[5][2]+JIGPositions[6][2])/7.
    Height1 = (ABCPositions[0][index][2]+ABCPositions[1][index][2]+ABCPositions[2][index][2]+ABCPositions[3][index][2])/4.
    # Height = (Height1 - Height0 -0.030 + Height_tune2[9-index])*1000
    Height = (Height1 - Height0)*1000
    ABCPackageHeight.append(Height)
    if Height<760 or Height>840:
      passMetrology = False
      if HybridType=="HX":
        st.write("ABC_{0} Package Height Failed!!!!".format(9-index))
      else:
        st.write("ABC_{0} Package Height Failed!!!!".format(index))
  # Height0 = (JIGPositions[0][2]+JIGPositions[1][2]+JIGPositions[2][2]+JIGPositions[3][2]+JIGPositions[4][2]+JIGPositions[5][2]+JIGPositions[6][2])/7.
  Height1 = (HCCPositions[0][2]+HCCPositions[1][2]+HCCPositions[2][2]+HCCPositions[3][2])/4.
  HCCPackageHeight = (Height1 - Height0)*1000
  if HCCPackageHeight<760 or HCCPackageHeight>840:
    passMetrology = False
    st.write("HCC Package Height Failed!!!!")

  ##----------------Print Result-------------
  st.write('###### Writing results to files')
  outFileName = outPath+"HybridMetrologyResults_"+HybridID+"_"+run_num_str+".txt"
  st.write("Output file: {0}.txt".format("HybridMetrologyResults_"+HybridID+"_"+run_num_str))
  outFile = open(outFileName, "w")
  outFile.write("Hybrid: "+HybridID+"\n")
  
  if passMetrology:
    outFile.write("\n Pass Metrology \n")
  else:
    outFile.write("\n Fail Metrology \n")

  # print FM Positions Difference
  outFile.write("\n")
  if HybridType=="HY":
    outFile.write("ABC[0-9] FM Position Difference w.r.t Reference Position [-0.1, 0.1] [mm]:\n")
  else:
    outFile.write("ABC[9-0] FM Position Difference w.r.t Reference Position [-0.1, 0.1] [mm]:\n")
  outFile.write("FM1-X: ")
  for index in range(0, 10):
    outFile.write(str(round(ABCFM1Diff[index][0],3))+" ")
  outFile.write("\n")
  outFile.write("FM1-Y: ")
  for index in range(0, 10):
    outFile.write(str(round(ABCFM1Diff[index][1],3))+" ")
  outFile.write("\n")
  outFile.write("FM2-X: ")
  for index in range(0, 10):
    outFile.write(str(round(ABCFM2Diff[index][0],3))+" ")
  outFile.write("\n")
  outFile.write("FM2-Y: ")
  for index in range(0, 10):
    outFile.write(str(round(ABCFM2Diff[index][1],3))+" ")
  outFile.write("\n")

  outFile.write("HCC FM1 Position Difference (X-Y) [-0.1, 0.1] [mm]: {}, {} \n".format(round(HCCFM1Diff[0], 3), round(HCCFM1Diff[1], 3)))
  outFile.write("HCC FM2 Position Difference (X-Y) [-0.1, 0.1] [mm]: {}, {} \n".format(round(HCCFM2Diff[0], 3), round(HCCFM2Diff[1], 3)))

  # print Glue Height
  outFile.write("\n")
  if HybridType=="HY":
    outFile.write("Glue Height ABC[0-9] [80, 160][um]:\n")
  else:
    outFile.write("Glue Height ABC[9-0] [80, 160][um]:\n")
  for index in range(0, 10):
    outFile.write(str(round(ABCGlueHeight[index], 3))+" ")
  outFile.write("\n")
  outFile.write("Glue Height HCC [80, 160][um]: ")
  outFile.write(str(round(HCCGlueHeight, 3))+"\n")

  # print ASIC Tilt
  outFile.write("\n")
  if HybridType=="HY":
    outFile.write("Backend Tilt ABC[0-9] [<0.025]:\n")
  else:
    outFile.write("Backend Tilt ABC[9-0] [<0.025]:\n")
  for index in range(0, 10):
    outFile.write(str(round(Tilt_BE[index], 5))+" ")
  outFile.write("\n")
  if HybridType=="HY":
    outFile.write("Frontend Tilt ABC[0-9] [<0.025]:\n")
  else:
    outFile.write("Frontend Tilt ABC[9-0] [<0.025]:\n")
  for index in range(0, 10):
    outFile.write(str(round(Tilt_FE[index], 5))+" ")
  outFile.write("\n")

  outFile.write("HCC Tilt[<0.025]: "+str(round(HCCTiltX, 5))+", "+str(round(HCCTiltY, 5))+"\n")
  
  # print Package Height
  outFile.write("\n")
  if HybridType=="HY":
    outFile.write("Package Height ABC[0-9] [760, 840][um]:\n")
  else:
    outFile.write("Package Height ABC[9-0] [760, 840][um]:\n")
  for index in range(0, 10):
    outFile.write(str(round(ABCPackageHeight[index], 3))+" ")
  outFile.write("\n")
  outFile.write("Package Height HCC [760, 840][um]: ")
  outFile.write(str(round(HCCPackageHeight, 3))+"\n")
  
  outFile.close()


  ##----------------Arrange Result-----------
  pGlueHeight = []
  pPackageHeight = []
  pPositionX = []
  pPositionY = []
  pABCFETilt = []
  pABCBETilt = []
  pHCCTilt = [] 

  for index in range(10):
    if HybridType=="HX":
      pGlueHeight.append(ABCGlueHeight[9-index])
      pPackageHeight.append(ABCPackageHeight[9-index])
      pPositionX.append(ABCFM1Diff[9-index][0])
      pPositionX.append(ABCFM2Diff[9-index][0])
      pPositionY.append(ABCFM1Diff[9-index][1])
      pPositionY.append(ABCFM2Diff[9-index][1])
      pABCFETilt.append(Tilt_FE[9-index])
      pABCBETilt.append(Tilt_BE[9-index])
    else:
      pGlueHeight.append(ABCGlueHeight[index])
      pPackageHeight.append(ABCPackageHeight[index])
      pPositionX.append(ABCFM1Diff[index][0])
      pPositionX.append(ABCFM2Diff[index][0])
      pPositionY.append(ABCFM1Diff[index][1])
      pPositionY.append(ABCFM2Diff[index][1])
      pABCFETilt.append(Tilt_FE[index])
      pABCBETilt.append(Tilt_BE[index])
  pGlueHeight.append(HCCGlueHeight)
  pPackageHeight.append(HCCPackageHeight)
  pPositionX.append(HCCFM1Diff[0])
  pPositionX.append(HCCFM2Diff[0])
  pPositionY.append(HCCFM1Diff[1])
  pPositionY.append(HCCFM2Diff[1])
  pHCCTilt.append(HCCTiltX)
  pHCCTilt.append(HCCTiltY)

    
  ##--------------output json file-------------------
  JsonFileName = outPath+"HybridMetrologyResults_"+HybridID+"_"+run_num_str+".json"
  st.write("Output file: {0}.json".format("HybridMetrologyResults_"+HybridID+"_"+run_num_str))
  outJson = open(JsonFileName, "w")
  outJson.write('{                            \n')
  outJson.write('  "component": "{0}",        \n'.format(HybridID))
  outJson.write('  "date": "{0}",             \n'.format(Date))
  outJson.write('  "institution": "{0}",      \n'.format(Institute))
  if passMetrology == True:
    outJson.write('  "passed": "{0}",         \n'.format("true"))
  else:
    outJson.write('  "passed": "{0}",         \n'.format("false"))
  #outJson.write('  "problems": "{0}",         \n'.format("true"))
  outJson.write('  "problems": "{0}",         \n'.format("false"))
  outJson.write('  "properties": {            \n')
  outJson.write('    "USER": "{0}"            \n'.format(Operator))
  outJson.write('    "SETUP": "{0}",          \n'.format(Instrument))
  outJson.write('    "SCRIPT_VERSION": "{0}", \n'.format("itkdataflow master"))
  outJson.write('  },                         \n')
  outJson.write('  "results": {               \n')
  # outJson.write('    "FILE": "",              \n')
  outJson.write('    "HEIGHT": {              \n')
  if HybridType=="HX":
    hybridtype = "X"
  else:
    hybridtype = "Y"
  for i in range(10):
    outJson.write('      "ABC_{0}_{1}": {2},  \n'.format(hybridtype,i,round(pGlueHeight[i],2)))
  outJson.write('      "HCC_{0}_{1}": {2}     \n'.format(hybridtype,0,round(pGlueHeight[10],2)))
  outJson.write('    },                       \n')
  outJson.write('    "POSITION": {            \n')
  for i in range(10):
    outJson.write('      "ABC_{0}_{1}": [     \n'.format(hybridtype,i))
    outJson.write('        [                  \n')
    outJson.write('          {0},             \n'.format(round(pPositionX[2*i]*1000,2)))
    outJson.write('          {0}              \n'.format(round(pPositionY[2*i]*1000,2)))
    outJson.write('        ],                 \n')
    outJson.write('        [                  \n')
    outJson.write('          {0},             \n'.format(round(pPositionX[2*i+1]*1000,2)))
    outJson.write('          {0}              \n'.format(round(pPositionY[2*i+1]*1000,2)))
    outJson.write('        ]                  \n')
    outJson.write('      ],                   \n')
  outJson.write('      "HCC_{0}_{1}": [       \n'.format(hybridtype,0))
  outJson.write('        [                    \n')
  outJson.write('          {0},               \n'.format(round(pPositionX[20]*1000,2)))
  outJson.write('          {0}                \n'.format(round(pPositionY[20]*1000,2)))
  outJson.write('        ],                   \n')
  outJson.write('        [                    \n')
  outJson.write('          {0},               \n'.format(round(pPositionX[21]*1000,2)))
  outJson.write('          {0}                \n'.format(round(pPositionY[21]*1000,2)))
  outJson.write('        ]                    \n')
  outJson.write('      ]                      \n')
  outJson.write('    },                       \n')
  outJson.write('    "TILT": {                \n')
  for i in range(10):
    outJson.write('      "ABC_{0}_{1}": [     \n'.format(hybridtype,i))
    outJson.write('        {0},               \n'.format(round(pABCBETilt[i],6)))
    outJson.write('        {0}                \n'.format(round(pABCFETilt[i],6)))
    outJson.write('      ],                   \n')
  outJson.write('      "HCC_{0}_{1}": [       \n'.format(hybridtype,0))
  outJson.write('        {0},                 \n'.format(round(pHCCTilt[0],6)))
  outJson.write('        {0}                  \n'.format(round(pHCCTilt[1],6)))
  outJson.write('      ]                      \n')
  outJson.write('    },                       \n')
  outJson.write('    "TOTAL_HEIGHT": {        \n')
  for i in range(10):
    outJson.write('      "ABC_{0}_{1}": {2},  \n'.format(hybridtype,i,round(pPackageHeight[i],2)))
  outJson.write('      "HCC_{0}_{1}": {2}     \n'.format(hybridtype,0,round(pPackageHeight[10],2)))
  outJson.write('    }                        \n')
  outJson.write('  },                         \n')
  outJson.write('  "runNumber": "{0}",        \n'.format(RunNumber))
  outJson.write('  "testType": "{0}"          \n'.format("ASIC_METROLOGY"))
  outJson.write('}                            \n')
  outJson.close()


  ##----------------make graphs-----------------
   
  plt.rcParams.update({'axes.labelsize': 6, 'axes.titlesize':10, 'xtick.labelsize':8, 'ytick.labelsize':8})
  
  plot_plotly = False
  
  axis_labels = ["ABCX0", "ABCX1", "ABCX2", "ABCX3", "ABCX4", "ABCX5", "ABCX6", "ABCX7", "ABCX8", "ABCX9", "HCCX"]
  axis_labels2 = ["ABCX0_1", "ABCX0_2",
                  "ABCX1_1", "ABCX1_2",
                  "ABCX2_1", "ABCX2_2",
                  "ABCX3_1", "ABCX3_2",
                  "ABCX4_1", "ABCX4_2",
                  "ABCX5_1", "ABCX5_2",
                  "ABCX6_1", "ABCX6_2",
                  "ABCX7_1", "ABCX7_2",
                  "ABCX8_1", "ABCX8_2",
                  "ABCX9_1", "ABCX9_2",
                  "HCCX_1","HCCX_2"]
  

  #Plot Glue thickness 
  spec_max_glue = 160
  spec_min_glue = 80
  
  background = 'white'
  ymin = spec_min_glue - 20
  ymax = spec_max_glue + 20
  
  Hybrid_DZ=sns.scatterplot(x=axis_labels, y=pGlueHeight,   marker='D', color='blue')
  Hybrid_DZ.set(ylabel='Glue Thickness [\u03BCm]', ylim=(ymin,ymax), title = 'Glue Thickness', facecolor = background)
  Hybrid_DZ.set_xticklabels(axis_labels, rotation = 45)
  Hybrid_DZ.axes.axhline(y = 80, color='black', linewidth=1, linestyle='--')
  Hybrid_DZ.axes.axhline(y = 160, color='black', linewidth=1, linestyle='--')

  plt.plot()
  plt.savefig("{0}GlueHeight_{1}.pdf".format(outPath,run_num_str))
  plt.savefig("{0}GlueHeight_{1}.png".format(outPath,run_num_str))
  plt.clf() 
  
  #Plot Package Height
  spec_max_p = 840
  spec_min_p = 760
  
  background = 'white'
  ymin = spec_min_p - 20
  ymax = spec_max_p + 20
  
  Hybrid_DZ_p=sns.scatterplot(x=axis_labels, y=pPackageHeight,   marker='D', color='blue')
  Hybrid_DZ_p.set(ylabel='Total Package Height [\u03BCm]', ylim=(ymin, ymax), title = 'Package Height', facecolor = background)
  Hybrid_DZ_p.axes.axhline(y = 760, color='black', linewidth=1, linestyle='--')
  Hybrid_DZ_p.axes.axhline(y = 840, color='black', linewidth=1, linestyle='--')
  Hybrid_DZ_p.set_xticklabels(axis_labels,rotation=45)
  
  plt.plot()
  plt.savefig("{0}PackageHeight_{1}.pdf".format(outPath,run_num_str))
  plt.savefig("{0}PackageHeight_{1}.png".format(outPath,run_num_str))
  plt.clf() 
  
  #Plot ASIC positions X
  spec_max_x = 0.1
  spec_min_x = -0.1
  
  background = 'white'
  ymin = spec_min_x - 0.05
  ymax = spec_max_x + 0.05
  
  Asic_x = sns.scatterplot(x = np.arange(0,22,1), y = pPositionX , marker = 'D', color = 'blue')
  Asic_x.set( ylabel='Difference from reference X coordinate [mm]', ylim=(ymin, ymax), title = 'Asic Positions X', facecolor = background)
  Asic_x.axes.axhline(y = -0.1, color='black', linewidth=1, linestyle='--')
  Asic_x.axes.axhline(y = 0.1, color='black', linewidth=1, linestyle='--')
  Asic_x.set_xticks(np.arange(0,22,1))
  Asic_x.set_xticklabels(axis_labels2, fontsize=6, rotation=45)

  plt.plot()
  plt.savefig("{0}PositionX_{1}.pdf".format(outPath,run_num_str))
  plt.savefig("{0}PositionX_{1}.png".format(outPath,run_num_str))
  plt.clf() 
  
  #Plot ASIC positions Y
  spec_max_y = 0.1
  spec_min_y = -0.1
  
  background = 'white'
  ymin = spec_min_y - 0.05
  ymax = spec_max_y + 0.05
  
  

                  # "ABCX1", "ABCX2", "ABCX3", "ABCX4", "ABCX5", "ABCX6", "ABCX7", "ABCX8", "ABCX9"]

  Asic_y = sns.scatterplot(x = np.arange(0,22,1), y = pPositionY, marker = 'D', color = 'blue')
  Asic_y.set( ylim = (ymin, ymax), ylabel='Difference from reference Y coordinate [mm]', title = 'Asic Positions Y', facecolor = background)
  Asic_y.axes.axhline(y = -0.1, color='black', linewidth=1, linestyle='--')
  Asic_y.axes.axhline(y = 0.1, color='black', linewidth=1, linestyle='--')
  Asic_y.set_xticks(np.arange(0,22,1))
  Asic_y.set_xticklabels(axis_labels2, fontsize = 6, rotation=45)
  # Asic_y
  # np.arange(1,23,1)
  
  plt.plot()
  plt.savefig("{0}PositionY_{1}.pdf".format(outPath,run_num_str))
  plt.savefig("{0}PositionY_{1}.png".format(outPath,run_num_str))
  plt.clf() 
  
  #Plot Front-End Tilt for ASICs
  axis_labels = ["ABCX0", "ABCX1", "ABCX2", "ABCX3", "ABCX4", "ABCX5", "ABCX6", "ABCX7", "ABCX8", "ABCX9"]
  
  spec_max_tilt = 0.025
  
  background = 'white'
  ymax = 0.025
  
  ax_ftilt = sns.scatterplot(x=axis_labels, y=pABCFETilt, marker = 'D', color = 'blue')
  ax_ftilt.set(xlabel = None, ylabel = 'Tilt', ylim=(0, ymax), title = 'Front-End Tilt', facecolor = background)
  ax_ftilt.set_xticklabels(axis_labels, rotation = 45)
  
  plt.plot()
  plt.savefig("{0}ABCFETilt_{1}.pdf".format(outPath,run_num_str))
  plt.savefig("{0}ABCFETilt_{1}.png".format(outPath,run_num_str))
  plt.clf() 
  
  
  #Plot Back-End Tilt for ASICS
  background = 'white'
  ymax = 0.025
  
  ax_btilt = sns.scatterplot(x=axis_labels, y=pABCBETilt, marker = 'D', color = 'blue')
  ax_btilt.set(xlabel = None, ylabel = 'Tilt', ylim=(0, ymax), title = 'Back-End Tilt', facecolor = background)
  ax_btilt.set_xticklabels(axis_labels, rotation = 45)
  
  plt.plot()
  plt.savefig("{0}ABCBETilt_{1}.pdf".format(outPath,run_num_str))
  plt.savefig("{0}ABCBETilt_{1}.png".format(outPath,run_num_str))
  plt.clf() 
  
  background = 'white'
  ymax = 0.025
  
  ax_HCCtilt = sns.scatterplot(x=['x', 'y'], y=pHCCTilt, marker = 'D', color = 'blue')
  ax_HCCtilt.margins(1,1)
  ax_HCCtilt.set(xlabel = None, ylabel = 'Tilt', ylim=(0, ymax), title = 'HCC Tilt',  facecolor = background)
  
  plt.plot()
  plt.savefig("{0}HCCTilt_{1}.pdf".format(outPath,run_num_str))
  plt.savefig("{0}HCCTilt_{1}.png".format(outPath,run_num_str))
  plt.clf() 
  
  ### Below will be shown on webpage
  #download results
  btxt_metrology_results = open(outFileName,'rb')
  bjson_metrology_results = open(JsonFileName,'rb')

  st.write('##### Download metrology results below')
  st.download_button(label='Dowload metrology results in TXT format',data = btxt_metrology_results, file_name="{0}.txt".format("HybridMetrologyResults_"+HybridID+"_"+run_num_str), mime = "text/plain")
  st.download_button(label='Dowload metrology results in JSON format',data = bjson_metrology_results, file_name="{0}.json".format("HybridMetrologyResults_"+HybridID+"_"+run_num_str), mime = "application/json")


  #To display figures in different columns
  image_glue_thickness = Image.open("{0}GlueHeight_{1}.png".format(outPath,run_num_str))
  image_package_height = Image.open("{0}PackageHeight_{1}.png".format(outPath,run_num_str))
  image_position_X = Image.open("{0}PositionX_{1}.png".format(outPath,run_num_str))
  image_position_Y = Image.open("{0}PositionY_{1}.png".format(outPath,run_num_str))
  image_ABCFETilt = Image.open("{0}ABCFETilt_{1}.png".format(outPath,run_num_str))
  image_ABCBETilt = Image.open("{0}ABCBETilt_{1}.png".format(outPath,run_num_str))
  image_HCCTilt = Image.open("{0}HCCTilt_{1}.png".format(outPath,run_num_str))

  bpng_glue_thickness = open("{0}GlueHeight_{1}.png".format(outPath,run_num_str),'rb')
  bpng_package_height = open("{0}PackageHeight_{1}.png".format(outPath,run_num_str),'rb')
  bpng_position_X = open("{0}PositionX_{1}.png".format(outPath,run_num_str),'rb')
  bpng_position_Y = open("{0}PositionY_{1}.png".format(outPath,run_num_str),'rb')
  bpng_ABCFETilt = open("{0}ABCFETilt_{1}.png".format(outPath,run_num_str),'rb')
  bpng_ABCBETilt = open("{0}ABCBETilt_{1}.png".format(outPath,run_num_str),'rb')
  bpng_HCCTilt = open("{0}HCCTilt_{1}.png".format(outPath,run_num_str),'rb')

  bpdf_glue_thickness = open("{0}GlueHeight_{1}.pdf".format(outPath,run_num_str),'rb')
  bpdf_package_height = open("{0}PackageHeight_{1}.pdf".format(outPath,run_num_str),'rb')
  bpdf_position_X = open("{0}PositionX_{1}.pdf".format(outPath,run_num_str),'rb')
  bpdf_position_Y = open("{0}PositionY_{1}.pdf".format(outPath,run_num_str),'rb')
  bpdf_ABCFETilt = open("{0}ABCFETilt_{1}.pdf".format(outPath,run_num_str),'rb')
  bpdf_ABCBETilt = open("{0}ABCBETilt_{1}.pdf".format(outPath,run_num_str),'rb')
  bpdf_HCCTilt = open("{0}HCCTilt_{1}.pdf".format(outPath,run_num_str),'rb')

  ###TODO: enable function "download all"
  st.write('##### Figures')
  col1, col2 = st.columns(2)
  with col1:
    st.image(image_glue_thickness)
    st.download_button(label='Download this figure in PNG format', data = bpng_glue_thickness, mime="image/png")
    st.download_button(label='Download this figure in PDF format', data = bpdf_glue_thickness, mime="application/pdf")

  with col2:
    st.image(image_package_height)
    st.download_button(label='Download this figure in PNG format', data = bpng_package_height, mime="image/png")
    st.download_button(label='Download this figure in PDF format', data = bpdf_package_height, mime="application/pdf")

  col3, col4 = st.columns(2)
  with col3:
    st.image(image_position_X)
    st.download_button(label='Download this figure in PNG format', data = bpng_position_X, mime="image/png")
    st.download_button(label='Download this figure in PDF format', data = bpdf_position_X, mime="application/pdf")

  with col4:
    st.image(image_position_Y)
    st.download_button(label='Download this figure in PNG format', data = bpng_position_Y, mime="image/png")
    st.download_button(label='Download this figure in PDF format', data = bpdf_position_Y, mime="application/pdf")

  col5, col6 = st.columns(2)
  with col5:
    st.image(image_ABCFETilt)
    st.download_button(label='Download this figure in PNG format', data = bpng_ABCFETilt, mime="image/png")
    st.download_button(label='Download this figure in PDF format', data = bpdf_ABCFETilt, mime="application/pdf")

  with col6:
    st.image(image_ABCBETilt)
    st.download_button(label='Download this figure in PNG format', data = bpng_ABCBETilt, mime="image/png")
    st.download_button(label='Download this figure in PDF format', data = bpdf_ABCBETilt, mime="application/pdf")

  col7, col8 = st.columns(2)

  with col7:
    st.image(image_HCCTilt)
    st.download_button(label='Download this figure in PNG format', data = bpng_HCCTilt, mime="image/png")
    st.download_button(label='Download this figure in PDF format', data = bpdf_HCCTilt, mime="application/pdf")

  return outFileName, JsonFileName
  ###----------------------------