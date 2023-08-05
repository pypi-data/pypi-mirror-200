#!/usr/bin/python
import argparse
import os
import datetime
import time

def Gen_CDF_PPA(inFileName, outFileName, ITkStripSub, HybridType, HybridRefNum, Institute, Operator, Instrument, ProgramName, RunNumber):
# 2022.08 Edited by Kaili, Fix Issue from Zhan for mislining.
  Date = ""
  TimeStamp = ""
#所有Line数字对应原脚本行号+1的行。[5,8]对应第[6,9]两个Centroid. （其高度在5,8)两行。
#始终使用Point读取Z, 在Centroid上一行。Centroid读取XY.
#ABC FM1,2指ABC芯片角上用作定位的两个,左右shining pad. HCC FM为X hybrid的下方，更靠近ABC的一侧。
#to see which line is what
  refline=[180,178]
  #整体偏离11
  # ABCFM1line = [115,123, 131,139, 147,155, 163,171, 179,187]
  # ABCFM2line = [117,125, 133,141, 149,157, 165,173, 181,189]
  ABCFM1line = [118, 124, 130, 136, 142, 148, 154, 160, 166, 172] #ABC X_0_1
  ABCFM2line = [120, 126, 132, 138, 144, 150, 156, 162, 168 ,174] #ABC_X_0_2
  #ABCFM2line = [126,128,130,132, 134,136,138,140,
  #142,144,146,148, 150,152,154,156,
  #158,160,162,164, 166,168,170,172,
  #174,176,178,180, 182,184,186,188,
  #190,192,194,196, 198,200,202,204]
  HCCFM1line = [37]
  HCCFM2line = [35]
  #HCCFM2line = [32,34,36,38]
  # onchipsABCHeightline=[125,127,131,129, 133,135,139,137,
  #  141,143,147,145, 149,151,155,153, 
  #  157,159,163,161, 165,167,171,169, 
  #  173,175,179,177, 181,183,187,185,
  #  189,191,195,193, 197,199,203,201]
  onchipsHCCHeightline=[30,32,34,36]#
  # onhybridABCHeightline=[4,46,4,48, 46,49,48,51, 
  # 49,52,51,53, 52,55,53,57, 
  # 55,58,57,59, 58,61,59,63,
  # 61,64,63,65, 64,67,65,69, 
  # 67,70,69,71, 70,7,71,7]
  # #onhybridABCHeightline=[4,46,4,48, 46,49,48,51, 
  # #49,52,51,53, 52,55,53,57, 
  # #55,58,57,59, 58,61,59,63,
  # #61,64,63,65, 64,67,65,69, 
  # #67,70,69,71, 70,7,71,7]
  onhybridHCCHeightline=[40,41,42,43] #对应行号41-44
  # #onjigHeightline=[73:124]
  # #ABCHeightline=onhybridABCHeightline+onchipsABCHeightline
  ABCHeightline=[
               38,39,45,46, 117,119,121,122, 45,46,47,48, 123,125,127,128,
               47,48,49,50, 129,131,133,134, 49,50,51,52, 135,137,139,140,
               51,52,53,54, 141,143,145,146, 53,54,55,56, 147,149,151,152,
               55,56,57,58, 153,155,157,158, 57,58,59,60, 159,161,163,164,
               59,60,61,62, 165,167,169,170, 61,62,63,64, 171,173,175,176]
                #39,40， 45,46-65为hybrid表面
               #行号118-123 为 ABCX_9.
  # ABCHeightline=[x-1 for x in ABCHeightline ]

  HCCHeightline=onhybridHCCHeightline+onchipsHCCHeightline
  # JIGline=range(65,116)
  JIGline=range(182,254)
  # in data file
  inFile = open(inFileName, "r")

  if not inFile:
    print("No inFile!!!!!")
    return
  lines = inFile.readlines()

  iPosition = 0
  line = lines[0]
  # if not line.startswith("NAME"):
    # print("No Program Name")
    #exit(0)
  
  # get date and time
  iPosition = iPosition + 1
  line = lines[iPosition]
  # if not line.startswith("DATE"): 
    # print("No Date.....")
    #exit(0)
  #line = line.strip("\r\n")
  #Date = line.split(",")[1].split(":")[2]+"-"+line.split(",")[1].split(":")[0]+"-"+line.split(",")[1].split(":")[1]
  iPosition = iPosition + 1
  line = lines[iPosition]
  if not line.startswith("TIME"): 
    print("No Time......")
    #exit(0)
  timestruct1=os.path.getctime(inFileName)
  timestruct2=time.localtime(timestruct1)
  TimeStamp=time.strftime("%Y-%m-%dT%H:%M:%S",timestruct2)
  # TimeStamp =timestruct.astimezone().isformat(timespec='milliseconds')

  # get postion of two referece points
  iPosition = iPosition+1
  ref = [[], []] #[0]: ref1[x, y], [1]: ref2[x,y]
  for index in range(len(ref)):
    iPosition = iPosition+1
    line = lines[refline[index]]
    line = line.strip("\r\n")

    print(line.split()[2])
    # print(line.split()[3])
    ref[index].append(round(float(line.split()[2]),5))
    ref[index].append(round(float(line.split()[3]),5))
    # if 1==index:
    #   ref[index].append(round(float("+000.000"),5))
   #ref[0].append(float(0))
   #ref[0].append(float(0))

  # ref[0][1]=0
  # ref[1][1]=0

  # Get ABC FM Positions
  ABCFM1 = [] 
  ABCFM2 = []
  HCCFM1 = []
  HCCFM2 = []
  for index in range(10):
    ABCFM1.append([])
    ABCFM2.append([])
  for index in range(len(ABCFM1)):
    iPosition = iPosition+1
    line = lines[ABCFM1line[index]]
    line = line.strip("\r\n")
    ABCFM1[index].append(round(float(line.split()[2]),5))
    ABCFM1[index].append(round(float(line.split()[3]),5))
    iPosition = iPosition+1
    line = lines[ABCFM2line[index]]
    line = line.strip("\r\n")
    ABCFM2[index].append(round(float(line.split()[2]),5))
    ABCFM2[index].append(round(float(line.split()[3]),5))
  # Get HCC FM Positions
  iPosition = iPosition+1
  line = lines[HCCFM1line[0]]
  line = line.strip("\r\n")
  HCCFM1.append(round(float(line.split()[2]),5))
  HCCFM1.append(round(float(line.split()[3]),5))
  iPosition = iPosition+1
  line = lines[HCCFM2line[0]]
  line = line.strip("\r\n")
  HCCFM2.append(round(float(line.split()[2]),5))
  HCCFM2.append(round(float(line.split()[3]),5))

  outFile = open(outFileName, "w")
  #----Header
  outFile.write("#---Header: \n")
  outFile.write("EC or Barrel:              {0}\n".format(ITkStripSub))
  outFile.write("Hybrid Type:               {0}\n".format(HybridType))
  outFile.write("Hybrid Ref Number:         {0}\n".format(HybridRefNum))
  outFile.write("Measurement Date/Time:     {0}\n".format(TimeStamp+"+08:00"))
  outFile.write("Institute:                 {0}\n".format(Institute))
  outFile.write("Operator:                  {0}\n".format(Operator))
  outFile.write("Instrument Used:           {0}\n".format(Instrument))
  outFile.write("Test Run Number:           {0}\n".format(RunNumber))
  outFile.write("Measurement Program Name:  {0}\n".format(ProgramName))

  #---Position scan
  outFile.write("#---Position Scan: \n")
  outFile.write("#Location          X [mm]    Y [mm]\n")
  if HybridType=="HX":
    outFile.write("H_X_P1        {:>10}{:>10}\n".format(ref[0][0], -ref[0][1]))
    outFile.write("H_X_P2        {:>10}{:>10}\n".format(ref[1][0], -ref[1][1]))
  else:  
    outFile.write("H_Y_P1        {:>10}{:>10}\n".format(ref[0][0], -ref[0][1]))
    outFile.write("H_Y_P2        {:>10}{:>10}\n".format(ref[1][0], -ref[1][1]))
  for index in range(len(ABCFM1)):
    if HybridType=="HX":
      outFile.write("ABC_X_{:}_P1    {:>10}{:>10}\n".format(9-index, ABCFM1[index][0], ABCFM1[index][1]))
      outFile.write("ABC_X_{:}_P2    {:>10}{:>10}\n".format(9-index, ABCFM2[index][0], ABCFM2[index][1]))
    else:
      outFile.write("ABC_Y_{:}_P1    {:>10}{:>10}\n".format(index, ABCFM1[index][0], -ABCFM1[index][1]))
      outFile.write("ABC_Y_{:}_P2    {:>10}{:>10}\n".format(index, ABCFM2[index][0], -ABCFM2[index][1]))
  if HybridType=="HX":
    outFile.write("HCC_X_{:}_P1    {:>10}{:>10}\n".format(0,HCCFM1[0], HCCFM1[1]))
    outFile.write("HCC_X_{:}_P2    {:>10}{:>10}\n".format(0,HCCFM2[0], HCCFM2[1]))
  else:
    outFile.write("HCC_Y_{:}_P1    {:>10}{:>10}\n".format(0,HCCFM1[0], -HCCFM1[1]))
    outFile.write("HCC_Y_{:}_P2    {:>10}{:>10}\n".format(0,HCCFM2[0], -HCCFM2[1]))

  #---Height scan
  indexheight = -1
  ABCHeightPosition = [[], [], [], [], [], [], [], []]
  HCCHeightPosition = [[], [], [], [], [], [], [], []]
  iABC = 0
  indexheight = indexheight
  while iABC<10:
    index = 0
    while index<8:
      indexheight = indexheight+1
      line = lines[ABCHeightline[indexheight]]
      line = line.strip("\r\n")
      ABCHeightPosition[index].append(round(float(line.split()[2]), 5))
      ABCHeightPosition[index].append(round(float(line.split()[3]), 5))
      line = lines[ABCHeightline[indexheight]]
      line = line.strip("\r\n")    
      ABCHeightPosition[index].append(round(float(line.split()[4]), 5))
      index = index+1
    iABC = iABC+1
  index = 0
  indexheight = -1
  while index<8:
    indexheight = indexheight+1
    line = lines[HCCHeightline[indexheight]]
    line = line.strip("\r\n")
    HCCHeightPosition[index].append(round(float(line.split()[2]), 5))
    HCCHeightPosition[index].append(round(float(line.split()[3]), 5))
    line = lines[HCCHeightline[indexheight]]
    line = line.strip("\r\n")  
    HCCHeightPosition[index].append(round(float(line.split()[4]), 5))
    index = index+1
  # Get Jig Surface Positions
  JigSurfN = 254-182
  JIG = []
  indexheight=-1
  for index in range(JigSurfN):
    JIG.append([])
  for index in range(len(JIG)):
    indexheight = indexheight+1
    line = lines[JIGline[indexheight]]
    line = line.strip("\r\n")
    JIG[index].append(round(float(line.split()[2]),5))
    JIG[index].append(round(float(line.split()[3]),5))
    JIG[index].append(round(float(line.split()[4]),5))

  outFile.write("#---Height Scan:\n")
  outFile.write("#Location      Type     X [mm]     Y [mm]    Z [mm]\n")
  iABC = 0
  while iABC<10:
    if HybridType=="HX":
      outFile.write("ABC_X_{:<5}     1   {:>10}{:>10}{:>10}\n".format(9-iABC, ABCHeightPosition[0][3*iABC], ABCHeightPosition[0][3*iABC+1], ABCHeightPosition[0][3*iABC+2]))
      outFile.write("ABC_X_{:<5}     1   {:>10}{:>10}{:>10}\n".format(9-iABC, ABCHeightPosition[1][3*iABC], ABCHeightPosition[1][3*iABC+1], ABCHeightPosition[1][3*iABC+2]))
      outFile.write("ABC_X_{:<5}     1   {:>10}{:>10}{:>10}\n".format(9-iABC, ABCHeightPosition[2][3*iABC], ABCHeightPosition[2][3*iABC+1], ABCHeightPosition[2][3*iABC+2]))
      outFile.write("ABC_X_{:<5}     1   {:>10}{:>10}{:>10}\n".format(9-iABC, ABCHeightPosition[3][3*iABC], ABCHeightPosition[3][3*iABC+1], ABCHeightPosition[3][3*iABC+2]))
      outFile.write("ABC_X_{:<5}     2   {:>10}{:>10}{:>10}\n".format(9-iABC, ABCHeightPosition[4][3*iABC], ABCHeightPosition[4][3*iABC+1], ABCHeightPosition[4][3*iABC+2]))
      outFile.write("ABC_X_{:<5}     2   {:>10}{:>10}{:>10}\n".format(9-iABC, ABCHeightPosition[5][3*iABC], ABCHeightPosition[5][3*iABC+1], ABCHeightPosition[5][3*iABC+2]))
      outFile.write("ABC_X_{:<5}     2   {:>10}{:>10}{:>10}\n".format(9-iABC, ABCHeightPosition[6][3*iABC], ABCHeightPosition[6][3*iABC+1], ABCHeightPosition[6][3*iABC+2]))
      outFile.write("ABC_X_{:<5}     2   {:>10}{:>10}{:>10}\n".format(9-iABC, ABCHeightPosition[7][3*iABC], ABCHeightPosition[7][3*iABC+1], ABCHeightPosition[7][3*iABC+2]))
    else:
      outFile.write("ABC_Y_{:<5}     1   {:>10}{:>10}{:>10}\n".format(iABC, ABCHeightPosition[0][3*iABC], -ABCHeightPosition[0][3*iABC+1], ABCHeightPosition[0][3*iABC+2]))
      outFile.write("ABC_Y_{:<5}     1   {:>10}{:>10}{:>10}\n".format(iABC, ABCHeightPosition[1][3*iABC], -ABCHeightPosition[1][3*iABC+1], ABCHeightPosition[1][3*iABC+2]))
      outFile.write("ABC_Y_{:<5}     1   {:>10}{:>10}{:>10}\n".format(iABC, ABCHeightPosition[2][3*iABC], -ABCHeightPosition[2][3*iABC+1], ABCHeightPosition[2][3*iABC+2]))
      outFile.write("ABC_Y_{:<5}     1   {:>10}{:>10}{:>10}\n".format(iABC, ABCHeightPosition[3][3*iABC], -ABCHeightPosition[3][3*iABC+1], ABCHeightPosition[3][3*iABC+2]))
      outFile.write("ABC_Y_{:<5}     2   {:>10}{:>10}{:>10}\n".format(iABC, ABCHeightPosition[4][3*iABC], -ABCHeightPosition[4][3*iABC+1], ABCHeightPosition[4][3*iABC+2]))
      outFile.write("ABC_Y_{:<5}     2   {:>10}{:>10}{:>10}\n".format(iABC, ABCHeightPosition[5][3*iABC], -ABCHeightPosition[5][3*iABC+1], ABCHeightPosition[5][3*iABC+2]))
      outFile.write("ABC_Y_{:<5}     2   {:>10}{:>10}{:>10}\n".format(iABC, ABCHeightPosition[6][3*iABC], -ABCHeightPosition[6][3*iABC+1], ABCHeightPosition[6][3*iABC+2]))
      outFile.write("ABC_Y_{:<5}     2   {:>10}{:>10}{:>10}\n".format(iABC, ABCHeightPosition[7][3*iABC], -ABCHeightPosition[7][3*iABC+1], ABCHeightPosition[7][3*iABC+2]))
    iABC = iABC+1

  if HybridType=="HX":
    outFile.write("HCC_X_{:<5}     1   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[0][0], HCCHeightPosition[0][1], HCCHeightPosition[0][2]))
    outFile.write("HCC_X_{:<5}     1   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[1][0], HCCHeightPosition[1][1], HCCHeightPosition[1][2]))
    outFile.write("HCC_X_{:<5}     1   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[2][0], HCCHeightPosition[2][1], HCCHeightPosition[2][2]))
    outFile.write("HCC_X_{:<5}     1   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[3][0], HCCHeightPosition[3][1], HCCHeightPosition[3][2]))
    outFile.write("HCC_X_{:<5}     2   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[4][0], HCCHeightPosition[4][1], HCCHeightPosition[4][2]))
    outFile.write("HCC_X_{:<5}     2   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[5][0], HCCHeightPosition[5][1], HCCHeightPosition[5][2]))
    outFile.write("HCC_X_{:<5}     2   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[6][0], HCCHeightPosition[6][1], HCCHeightPosition[6][2]))
    outFile.write("HCC_X_{:<5}     2   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[7][0], HCCHeightPosition[7][1], HCCHeightPosition[7][2]))
  else:
    outFile.write("HCC_Y_{:<5}     1   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[0][0], -HCCHeightPosition[0][1], HCCHeightPosition[0][2]))
    outFile.write("HCC_Y_{:<5}     1   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[1][0], -HCCHeightPosition[1][1], HCCHeightPosition[1][2]))
    outFile.write("HCC_Y_{:<5}     1   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[2][0], -HCCHeightPosition[2][1], HCCHeightPosition[2][2]))
    outFile.write("HCC_Y_{:<5}     1   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[3][0], -HCCHeightPosition[3][1], HCCHeightPosition[3][2]))
    outFile.write("HCC_Y_{:<5}     2   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[4][0], -HCCHeightPosition[4][1], HCCHeightPosition[4][2]))
    outFile.write("HCC_Y_{:<5}     2   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[5][0], -HCCHeightPosition[5][1], HCCHeightPosition[5][2]))
    outFile.write("HCC_Y_{:<5}     2   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[6][0], -HCCHeightPosition[6][1], HCCHeightPosition[6][2]))
    outFile.write("HCC_Y_{:<5}     2   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[7][0], -HCCHeightPosition[7][1], HCCHeightPosition[7][2]))

  for index in range(JigSurfN):
    outFile.write("JIG{:<5}        0   {:>10}{:>10}{:>10}\n".format("", JIG[index][0], JIG[index][1], JIG[index][2]))


###########PPB Function#############


def Gen_CDF_PPB(inFileName, outFileName, ITkStripSub, HybridType, HybridRefNum, Institute, Operator, Instrument, ProgramName, RunNumber):
# 2022.08 Edited by Kaili, Fix Issue from Zhan for mislining.
# 2023.02 For PPB
  Date = ""
  TimeStamp = ""
#所有Line数字对应原脚本行号+1的行。[5,8]对应第[6,9]两个Centroid. （其高度在5,8)两行。
#始终使用Point读取Z, 在Centroid上一行。Centroid读取XY.
#ABC FM1,2指ABC芯片角上用作定位的两个,左右shining pad. HCC FM为X hybrid的下方，更靠近ABC的一侧。
#to see which line is what
  refline=[128,126]
  #整体偏离11
  # ABCFM1line = [115,123, 131,139, 147,155, 163,171, 179,187]
  # ABCFM2line = [117,125, 133,141, 149,157, 165,173, 181,189]
  ABCFM1line = [66, 72, 78, 84, 90, 96, 102, 108, 114, 120] #ABC X_0_1
  ABCFM2line = [68, 74, 80, 86, 92, 98, 104, 110, 116, 122] #ABC_X_0_2

  #ABCFM2line = [126,128,130,132, 134,136,138,140,
  #142,144,146,148, 150,152,154,156,
  #158,160,162,164, 166,168,170,172,
  #174,176,178,180, 182,184,186,188,
  #190,192,194,196, 198,200,202,204]
  HCCFM1line = [37]
  HCCFM2line = [35]
  #HCCFM2line = [32,34,36,38]
  # onchipsABCHeightline=[125,127,131,129, 133,135,139,137,
  #  141,143,147,145, 149,151,155,153, 
  #  157,159,163,161, 165,167,171,169, 
  #  173,175,179,177, 181,183,187,185,
  #  189,191,195,193, 197,199,203,201]
  onchipsHCCHeightline=[30,32,34,36]#
  # onhybridABCHeightline=[4,46,4,48, 46,49,48,51, 
  # 49,52,51,53, 52,55,53,57, 
  # 55,58,57,59, 58,61,59,63,
  # 61,64,63,65, 64,67,65,69, 
  # 67,70,69,71, 70,7,71,7]
  # #onhybridABCHeightline=[4,46,4,48, 46,49,48,51, 
  # #49,52,51,53, 52,55,53,57, 
  # #55,58,57,59, 58,61,59,63,
  # #61,64,63,65, 64,67,65,69, 
  # #67,70,69,71, 70,7,71,7]
  onhybridHCCHeightline=[40,41,42,43] #对应行号41-44
  # #onjigHeightline=[73:124]
  # #ABCHeightline=onhybridABCHeightline+onchipsABCHeightline
  ABCHeightline=[
               38,39,45,46, 65, 67, 69, 70,     45,46,47,48,  71, 73, 75, 76, 
               47,48,49,50, 77, 79, 81, 82,     49,50,51,52,  83, 85, 87, 88, 
               51,52,53,54, 89, 91, 93, 94,     53,54,55,56,  95, 97, 99, 100, 
               55,56,57,58, 101, 103, 105, 106, 57,58,59,60, 107, 109, 111, 112,
               59,60,61,62, 113, 115, 117, 118, 61,62,63,64, 119, 121, 123, 124]
                #39,40， 45,46-65为hybrid表面
               #行号118-123 为 ABCX_9.
  # ABCHeightline=[x-1 for x in ABCHeightline ]
  HCCHeightline=onhybridHCCHeightline+onchipsHCCHeightline

  JIGline=range(130,202)
  #-52
  # in data file
  inFile = open(inFileName, "r")

  if not inFile:
    print("No inFile!!!!!")
    return
  lines = inFile.readlines()

  iPosition = 0
  line = lines[0]
  
  # get date and time
  iPosition = iPosition + 1
  line = lines[iPosition]
  # if not line.startswith("DATE"): 
    # print("No Date.....")
    #exit(0)
  #line = line.strip("\r\n")
  #Date = line.split(",")[1].split(":")[2]+"-"+line.split(",")[1].split(":")[0]+"-"+line.split(",")[1].split(":")[1]
  iPosition = iPosition + 1
  line = lines[iPosition]
  if not line.startswith("TIME"): 
    print("No Time......")
    #exit(0)

  timestruct1=os.path.getctime(inFileName)
  timestruct2=time.localtime(timestruct1)
  TimeStamp=time.strftime("%Y-%m-%dT%H:%M:%S",timestruct2)
  # TimeStamp =timestruct.astimezone().isformat(timespec='milliseconds')

  # get postion of two referece points
  iPosition = iPosition+1
  ref = [[], []] #[0]: ref1[x, y], [1]: ref2[x,y]
  for index in range(len(ref)):
    iPosition = iPosition+1
    line = lines[refline[index]]
    line = line.strip("\r\n")

    print(line.split()[2])
    # print(line.split()[3])
    ref[index].append(round(float(line.split()[2]),5))
    ref[index].append(round(float(line.split()[3]),5))
    # if 1==index:
    #   ref[index].append(round(float("+000.000"),5))
   #ref[0].append(float(0))
   #ref[0].append(float(0))

  # ref[0][1]=0
  # ref[1][1]=0

  # Get ABC FM Positions
  ABCFM1 = [] 
  ABCFM2 = []
  HCCFM1 = []
  HCCFM2 = []
  for index in range(10):
    ABCFM1.append([])
    ABCFM2.append([])
  for index in range(len(ABCFM1)):
    iPosition = iPosition+1
    line = lines[ABCFM1line[index]]
    line = line.strip("\r\n")
    ABCFM1[index].append(round(float(line.split()[2]),5))
    ABCFM1[index].append(round(float(line.split()[3]),5))
    iPosition = iPosition+1
    line = lines[ABCFM2line[index]]
    line = line.strip("\r\n")
    ABCFM2[index].append(round(float(line.split()[2]),5))
    ABCFM2[index].append(round(float(line.split()[3]),5))
  # Get HCC FM Positions
  iPosition = iPosition+1
  line = lines[HCCFM1line[0]]
  line = line.strip("\r\n")
  HCCFM1.append(round(float(line.split()[2]),5))
  HCCFM1.append(round(float(line.split()[3]),5))
  iPosition = iPosition+1
  line = lines[HCCFM2line[0]]
  line = line.strip("\r\n")
  HCCFM2.append(round(float(line.split()[2]),5))
  HCCFM2.append(round(float(line.split()[3]),5))

  outFile = open(outFileName, "w")
  #----Header
  outFile.write("#---Header: \n")
  outFile.write("EC or Barrel:              {0}\n".format(ITkStripSub))
  outFile.write("Hybrid Type:               {0}\n".format(HybridType))
  outFile.write("Hybrid Ref Number:         {0}\n".format(HybridRefNum))
  outFile.write("Measurement Date/Time:     {0}\n".format(TimeStamp+"+08:00"))
  outFile.write("Institute:                 {0}\n".format(Institute))
  outFile.write("Operator:                  {0}\n".format(Operator))
  outFile.write("Instrument Used:           {0}\n".format(Instrument))
  outFile.write("Test Run Number:           {0}\n".format(RunNumber))
  outFile.write("Measurement Program Name:  {0}\n".format(ProgramName))

  #---Position scan
  outFile.write("#---Position Scan: \n")
  outFile.write("#Location          X [mm]    Y [mm]\n")
  if HybridType=="HX":
    outFile.write("H_X_P1        {:>10}{:>10}\n".format(ref[0][0], -ref[0][1]))
    outFile.write("H_X_P2        {:>10}{:>10}\n".format(ref[1][0], -ref[1][1]))
  else:  
    outFile.write("H_Y_P1        {:>10}{:>10}\n".format(ref[0][0], -ref[0][1]))
    outFile.write("H_Y_P2        {:>10}{:>10}\n".format(ref[1][0], -ref[1][1]))
  for index in range(len(ABCFM1)):
    if HybridType=="HX":
      outFile.write("ABC_X_{:}_P1    {:>10}{:>10}\n".format(9-index, ABCFM1[index][0], ABCFM1[index][1]))
      outFile.write("ABC_X_{:}_P2    {:>10}{:>10}\n".format(9-index, ABCFM2[index][0], ABCFM2[index][1]))
    else:
      outFile.write("ABC_Y_{:}_P1    {:>10}{:>10}\n".format(index, ABCFM1[index][0], -ABCFM1[index][1]))
      outFile.write("ABC_Y_{:}_P2    {:>10}{:>10}\n".format(index, ABCFM2[index][0], -ABCFM2[index][1]))
  if HybridType=="HX":
    outFile.write("HCC_X_{:}_P1    {:>10}{:>10}\n".format(0,HCCFM1[0], HCCFM1[1]))
    outFile.write("HCC_X_{:}_P2    {:>10}{:>10}\n".format(0,HCCFM2[0], HCCFM2[1]))
  else:
    outFile.write("HCC_Y_{:}_P1    {:>10}{:>10}\n".format(0,HCCFM1[0], -HCCFM1[1]))
    outFile.write("HCC_Y_{:}_P2    {:>10}{:>10}\n".format(0,HCCFM2[0], -HCCFM2[1]))

  #---Height scan
  indexheight = -1
  ABCHeightPosition = [[], [], [], [], [], [], [], []]
  HCCHeightPosition = [[], [], [], [], [], [], [], []]
  iABC = 0
  indexheight = indexheight
  while iABC<10:
    index = 0
    while index<8:
      indexheight = indexheight+1
      line = lines[ABCHeightline[indexheight]]
      line = line.strip("\r\n")
      ABCHeightPosition[index].append(round(float(line.split()[2]), 5))
      ABCHeightPosition[index].append(round(float(line.split()[3]), 5))
      line = lines[ABCHeightline[indexheight]]
      line = line.strip("\r\n")    
      ABCHeightPosition[index].append(round(float(line.split()[4]), 5))
      index = index+1
    iABC = iABC+1
  index = 0
  indexheight = -1
  while index<8:
    indexheight = indexheight+1
    line = lines[HCCHeightline[indexheight]]
    line = line.strip("\r\n")
    HCCHeightPosition[index].append(round(float(line.split()[2]), 5))
    HCCHeightPosition[index].append(round(float(line.split()[3]), 5))
    line = lines[HCCHeightline[indexheight]]
    line = line.strip("\r\n")  
    HCCHeightPosition[index].append(round(float(line.split()[4]), 5))
    index = index+1
  # Get Jig Surface Positions
  JigSurfN = 72
  JIG = []
  indexheight=-1
  for index in range(JigSurfN):
    JIG.append([])
  for index in range(len(JIG)):
    indexheight = indexheight+1
    line = lines[JIGline[indexheight]]
    line = line.strip("\r\n")
    JIG[index].append(round(float(line.split()[2]),5))
    JIG[index].append(round(float(line.split()[3]),5))
    JIG[index].append(round(float(line.split()[4]),5))

  outFile.write("#---Height Scan:\n")
  outFile.write("#Location      Type     X [mm]     Y [mm]    Z [mm]\n")
  iABC = 0
  while iABC<10:
    if HybridType=="HX":
      outFile.write("ABC_X_{:<5}     1   {:>10}{:>10}{:>10}\n".format(9-iABC, ABCHeightPosition[0][3*iABC], ABCHeightPosition[0][3*iABC+1], ABCHeightPosition[0][3*iABC+2]))
      outFile.write("ABC_X_{:<5}     1   {:>10}{:>10}{:>10}\n".format(9-iABC, ABCHeightPosition[1][3*iABC], ABCHeightPosition[1][3*iABC+1], ABCHeightPosition[1][3*iABC+2]))
      outFile.write("ABC_X_{:<5}     1   {:>10}{:>10}{:>10}\n".format(9-iABC, ABCHeightPosition[2][3*iABC], ABCHeightPosition[2][3*iABC+1], ABCHeightPosition[2][3*iABC+2]))
      outFile.write("ABC_X_{:<5}     1   {:>10}{:>10}{:>10}\n".format(9-iABC, ABCHeightPosition[3][3*iABC], ABCHeightPosition[3][3*iABC+1], ABCHeightPosition[3][3*iABC+2]))
      outFile.write("ABC_X_{:<5}     2   {:>10}{:>10}{:>10}\n".format(9-iABC, ABCHeightPosition[4][3*iABC], ABCHeightPosition[4][3*iABC+1], ABCHeightPosition[4][3*iABC+2]))
      outFile.write("ABC_X_{:<5}     2   {:>10}{:>10}{:>10}\n".format(9-iABC, ABCHeightPosition[5][3*iABC], ABCHeightPosition[5][3*iABC+1], ABCHeightPosition[5][3*iABC+2]))
      outFile.write("ABC_X_{:<5}     2   {:>10}{:>10}{:>10}\n".format(9-iABC, ABCHeightPosition[6][3*iABC], ABCHeightPosition[6][3*iABC+1], ABCHeightPosition[6][3*iABC+2]))
      outFile.write("ABC_X_{:<5}     2   {:>10}{:>10}{:>10}\n".format(9-iABC, ABCHeightPosition[7][3*iABC], ABCHeightPosition[7][3*iABC+1], ABCHeightPosition[7][3*iABC+2]))
    else:
      outFile.write("ABC_Y_{:<5}     1   {:>10}{:>10}{:>10}\n".format(iABC, ABCHeightPosition[0][3*iABC], -ABCHeightPosition[0][3*iABC+1], ABCHeightPosition[0][3*iABC+2]))
      outFile.write("ABC_Y_{:<5}     1   {:>10}{:>10}{:>10}\n".format(iABC, ABCHeightPosition[1][3*iABC], -ABCHeightPosition[1][3*iABC+1], ABCHeightPosition[1][3*iABC+2]))
      outFile.write("ABC_Y_{:<5}     1   {:>10}{:>10}{:>10}\n".format(iABC, ABCHeightPosition[2][3*iABC], -ABCHeightPosition[2][3*iABC+1], ABCHeightPosition[2][3*iABC+2]))
      outFile.write("ABC_Y_{:<5}     1   {:>10}{:>10}{:>10}\n".format(iABC, ABCHeightPosition[3][3*iABC], -ABCHeightPosition[3][3*iABC+1], ABCHeightPosition[3][3*iABC+2]))
      outFile.write("ABC_Y_{:<5}     2   {:>10}{:>10}{:>10}\n".format(iABC, ABCHeightPosition[4][3*iABC], -ABCHeightPosition[4][3*iABC+1], ABCHeightPosition[4][3*iABC+2]))
      outFile.write("ABC_Y_{:<5}     2   {:>10}{:>10}{:>10}\n".format(iABC, ABCHeightPosition[5][3*iABC], -ABCHeightPosition[5][3*iABC+1], ABCHeightPosition[5][3*iABC+2]))
      outFile.write("ABC_Y_{:<5}     2   {:>10}{:>10}{:>10}\n".format(iABC, ABCHeightPosition[6][3*iABC], -ABCHeightPosition[6][3*iABC+1], ABCHeightPosition[6][3*iABC+2]))
      outFile.write("ABC_Y_{:<5}     2   {:>10}{:>10}{:>10}\n".format(iABC, ABCHeightPosition[7][3*iABC], -ABCHeightPosition[7][3*iABC+1], ABCHeightPosition[7][3*iABC+2]))
    iABC = iABC+1

  if HybridType=="HX":
    outFile.write("HCC_X_{:<5}     1   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[0][0], HCCHeightPosition[0][1], HCCHeightPosition[0][2]))
    outFile.write("HCC_X_{:<5}     1   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[1][0], HCCHeightPosition[1][1], HCCHeightPosition[1][2]))
    outFile.write("HCC_X_{:<5}     1   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[2][0], HCCHeightPosition[2][1], HCCHeightPosition[2][2]))
    outFile.write("HCC_X_{:<5}     1   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[3][0], HCCHeightPosition[3][1], HCCHeightPosition[3][2]))
    outFile.write("HCC_X_{:<5}     2   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[4][0], HCCHeightPosition[4][1], HCCHeightPosition[4][2]))
    outFile.write("HCC_X_{:<5}     2   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[5][0], HCCHeightPosition[5][1], HCCHeightPosition[5][2]))
    outFile.write("HCC_X_{:<5}     2   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[6][0], HCCHeightPosition[6][1], HCCHeightPosition[6][2]))
    outFile.write("HCC_X_{:<5}     2   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[7][0], HCCHeightPosition[7][1], HCCHeightPosition[7][2]))
  else:
    outFile.write("HCC_Y_{:<5}     1   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[0][0], -HCCHeightPosition[0][1], HCCHeightPosition[0][2]))
    outFile.write("HCC_Y_{:<5}     1   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[1][0], -HCCHeightPosition[1][1], HCCHeightPosition[1][2]))
    outFile.write("HCC_Y_{:<5}     1   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[2][0], -HCCHeightPosition[2][1], HCCHeightPosition[2][2]))
    outFile.write("HCC_Y_{:<5}     1   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[3][0], -HCCHeightPosition[3][1], HCCHeightPosition[3][2]))
    outFile.write("HCC_Y_{:<5}     2   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[4][0], -HCCHeightPosition[4][1], HCCHeightPosition[4][2]))
    outFile.write("HCC_Y_{:<5}     2   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[5][0], -HCCHeightPosition[5][1], HCCHeightPosition[5][2]))
    outFile.write("HCC_Y_{:<5}     2   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[6][0], -HCCHeightPosition[6][1], HCCHeightPosition[6][2]))
    outFile.write("HCC_Y_{:<5}     2   {:>10}{:>10}{:>10}\n".format(0, HCCHeightPosition[7][0], -HCCHeightPosition[7][1], HCCHeightPosition[7][2]))

  for index in range(JigSurfN):
    outFile.write("JIG{:<5}        0   {:>10}{:>10}{:>10}\n".format("", JIG[index][0], JIG[index][1], JIG[index][2]))
