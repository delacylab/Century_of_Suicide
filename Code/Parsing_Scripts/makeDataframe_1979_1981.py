import pandas as pd
import argparse
import StateFIPSTable
import BirthStateTable
from datetime import date
import os
#state_FIPS = StateFIPSTable.lookup_table
birth_state_dict = BirthStateTable.lookup_table
parser = argparse.ArgumentParser()
parser.add_argument('filename',help='file')
args = parser.parse_args()
filename = args.filename
afile = open('../../../Raw_Datasets/CDC/CDC_Original_Text_Files/' + filename)
lines = [line for line in afile]
allrows = []
numLines = 0
for line in lines:
   #print("processing row",numLines)
   currentrow = []
   #NOTE: the "Tape location" in data dictionary is NOT zero based
   #so I have to subtract one from everything in it
   recordtype = line[18] #1 = same res/death location, 2=different
   residentstatus = line[19] #1=same res/death loc,2=same state diff county
   #3 = diff state, 4=foreign citizen in US
   occurenceState = str(line[20:22])  #eg. UT
   occurenceState = birth_state_dict[occurenceState]
   occurenceCountyFIPS = str(line[22:25]) #NO int conversion
#   occurenceNYCcode = str(line[25:27]) #YC = NYC code, we don't care about that
   #occurenceCountyPopSize = line[48] #0 = highest > million, 6= < 25,000
   residenceState = str(line[30:32]) #NOTE ZZ=foreign resident, also could have
   residenceState = birth_state_dict[residenceState]
   #territories here?
#   residenceStateCountry = line[32:34] #recode of above with some countries
   residenceCounty = str(line[32:35]) #county FIPS
   residenceCityNotFIPS = str(line[35:38])
   residenceCityPopSize = line[38] #almost same as county, Z=foreign
   residenceMetroAreaBoolean = line[39] #1=Metro, 2-Not, Z=foreign resident
#   residenceNYCcode = line[44:46] #YC=NYC code
   SMSA = str(line[45:48])
   birthState = str(line[77:79]) #e.g. UT
   birthState = birth_state_dict[birthState]
#   birthStateCountry = line[58:60] #recode of above with some countries
   #next 2 fields are education - annoyingly there are 2 version (1989,2003)
   #one will always be blank
   #edu1989 = line[51:53] #see data dictionary
   deathMonth = line[54:56] #e.g. 07 for July
   
   gender = str(line[58]) # M/F
   if gender == '1':
      gender = 'M'
   if gender == '2':
      gender = 'F'
   #Age - this will be ugly
   ageType = line[63] #1= age in years, 2=months,3=days,4=hours,5=minutes,9=NA
   ageNum = int(line[64:66]) #number with unites given in ageType
   #NOTE we want ageNum as int so we will not cast here
   #ageSub = line[113] #1=age was calculated from birth/death, blank=reported
   ageRecode52 = line[66:68] #this may be useful, uses age groups e.g. 35-39
   ageRecode27 = line[68:70] #different table, same idea as above line
   ageRecode12 = line[70:72] #another different table
   ageRecode22 = line[72:74] #table for infants
   placeOfDeath = line[74] #hospital/home/other, see table
   maritalStatus = str(line[76]) #S/M/W/D/N/U, N and U = unknown
   if maritalStatus == '1':
      maritalStatus = 'S'
   elif maritalStatus == '2':
      maritalStatus = 'M'
   elif maritalStatus == '3':
      maritalStatus = 'W'
   elif maritalStatus == '4':
      maritalStatus = 'D'
   elif maritalStatus == '8':
      maritalStatus = 'N'
   elif maritalStatus == '9':
      maritalStatus = 'U'
   else:
      maritalStatus = 'U'

   deathDate = int(line[56:58]) #01-31, have to do extra work here to get day of week
   dayOfWeek = 9 #
   if deathDate != 99:      
     deathDateClass = date(1988,int(deathMonth),int(deathDate))   
     dayOfWeek = deathDateClass.isoweekday() #line[82] #Coded day of week e.g.3=  Tuesday Suicide Tuesday?
     dayOfWeek += 1
     if dayOfWeek == 8:
        dayOfWeek = 1
   #industry = line[84:87]  
   #if this is same as file
   #workInjury = str(line[135]) #Y/N/U(nknown)
   #if workInjury == '1':
   #   workInjury = 'Y'
   #elif workInjury == '2':
   #   workInjury = 'N'
   #else:
   #   workInjury = 'U'
   #mannerOfDeath = line[138] #See table, important ones we want probably
   #2=Suicide, 4=Pending Investigation, 5=unknown, 6=Self-inflicted
   #Could be blank as well for unknown
   #disposition = line[107] #Burial/Cremation/Other/Unknown
   autopsy = str(line[83]) #Y/N/U
   if autopsy == '1':
      autopsy = 'Y'
   elif autopsy == '2':
      autopsy = 'N'
   else:
      autopsy = 'U'
#   certifier = line[109] #D/P/M/O e.g. Doctor/physician do we care?
#   tobaccoUse = line[141] #Y/N/P/U
#   pregnancy = line[142] #Could be interesting, see table
#   activityCode = line[139] #active at time of death, see table
   placeOfInjury = line[140] #Place of injury where applicable, see table
   #Now for ICD codes which I think are important
   ICD9 = str(line[141:145])
   ICDrecode282 = str(line[145:150])
   ICDrecode72 = str(line[150:153])
   ICDrecode61 = str(line[153:156])
   ICDrecode34 = str(line[156:159])
   #Multiple conditions
#Space has been provided for maximum of 20 conditions.  Each condition takes 7 positions in the record.  The 7th position will be blank.  Records that do not have 20 conditions are blank in the unused area.
   numConditions = line[159:161]
   condition01 = str(line[161:168])
   condition02 = str(line[168:175])
   condition03 = str(line[175:182])
   condition04 = str(line[182:189])
   condition05 = str(line[189:196])
   condition06 = str(line[196:203])
   condition07 = str(line[203:210])
   condition08 = str(line[210:217])
   condition09 = str(line[217:224])
   condition10 = str(line[224:231])
   condition11 = str(line[231:238])
   condition12 = str(line[238:245])
   condition13 = str(line[245:252])
   condition14 = str(line[252:259])
   condition15 = str(line[259:266])
   condition16 = str(line[266:273])
   condition17 = str(line[273:280])
   condition18 = str(line[280:287])
   condition19 = str(line[287:294])
   condition20 = str(line[294:301])
   #RA codes are more amenable to statistical tabulation
   numRAConditions = line[337:339]
   RAcondition01 = str(line[340:345])
   RAcondition02 = str(line[345:350])
   RAcondition03 = str(line[350:355])
   RAcondition04 = str(line[355:360])
   RAcondition05 = str(line[360:365])
   RAcondition06 = str(line[365:370])
   RAcondition07 = str(line[370:375])
   RAcondition08 = str(line[375:380])
   RAcondition09 = str(line[380:385])
   RAcondition10 = str(line[385:390])
   RAcondition11 = str(line[390:395])
   RAcondition12 = str(line[395:400])
   RAcondition13 = str(line[400:405])
   RAcondition14 = str(line[405:410])
   RAcondition15 = str(line[410:415])
   RAcondition16 = str(line[415:420])
   RAcondition17 = str(line[420:425])
   RAcondition18 = str(line[425:430])
   RAcondition19 = str(line[430:435])
   RAcondition20 = str(line[435:440])
#END OF NEW MULTIPLE CONDS
   race = str(line[59:61]) #this will be troublesome, apparently Asian-PI
   #codes have changed over the years. Table is:
   #01 = White, 02=Black, 03=AI-AN, 04=Chinese, 05=Japanese, 06=Hawaiian,
   #07=Filipino, Asian-PI is all codes from 18-78
   #So China/Japan/Hawaiian/Filipino != Asian-PI???
   raceRecode3 = line[61] #1 = White, 3=Black, 2=Neither
   #raceHispanicCode = line[79:81]
   #raceHispanicRecode = line[81] # codes 6-9=Non-Hispanic
   
   #1999 might be only one for this
   #occupation = line[87:90]
   #Now to append all these
   currentrow.append(recordtype)
   currentrow.append(residentstatus)
   currentrow.append(occurenceState) 
   currentrow.append(occurenceCountyFIPS) 
   #currentrow.append(occurenceCountyPopSize) 
   currentrow.append(residenceState) 
   currentrow.append(residenceCounty) 
   currentrow.append(residenceCityNotFIPS)
   currentrow.append(residenceCityPopSize) 
   currentrow.append(residenceMetroAreaBoolean) 
   currentrow.append(SMSA)
   currentrow.append(birthState) 
   #currentrow.append(edu1989) 
   currentrow.append(deathMonth) 
   currentrow.append(gender) 
   currentrow.append(ageType) 
   currentrow.append(ageNum) 
   #currentrow.append(ageSub) 
   currentrow.append(ageRecode52) 
   currentrow.append(ageRecode27) 
   currentrow.append(ageRecode12) 
   currentrow.append(ageRecode22) 
   currentrow.append(placeOfDeath) 
   currentrow.append(maritalStatus) 
   currentrow.append(dayOfWeek) 
   #currentrow.append(industry) 
   #currentrow.append(workInjury)
   #currentrow.append(mannerOfDeath)
   #currentrow.append(disposition)
   currentrow.append(autopsy)
   #currentrow.append(certifier)
   #currentrow.append(tobaccoUse)
   #currentrow.append(pregnancy)
   #currentrow.append(activityCode)
   currentrow.append(placeOfInjury)
   currentrow.append(ICD9)
   currentrow.append(ICDrecode282)
   currentrow.append(ICDrecode72)
   currentrow.append(ICDrecode61)
   currentrow.append(ICDrecode34)
   currentrow.append(race)
   currentrow.append(raceRecode3)
   #currentrow.append(raceRecode5)
   #currentrow.append(raceHispanicCode)
   #currentrow.append(raceHispanicRecode)
   currentrow.append(numConditions)
   currentrow.append(condition01)
   currentrow.append(condition02)
   currentrow.append(condition03)
   currentrow.append(condition04)
   currentrow.append(condition05)
   currentrow.append(condition06)
   currentrow.append(condition07)
   currentrow.append(condition08)
   currentrow.append(condition09)
   currentrow.append(condition10)
   currentrow.append(condition11)
   currentrow.append(condition12)
   currentrow.append(condition13)
   currentrow.append(condition14)
   currentrow.append(condition15)
   currentrow.append(condition16)
   currentrow.append(condition17)
   currentrow.append(condition18)
   currentrow.append(condition19)
   currentrow.append(condition20)
   currentrow.append(numRAConditions)
   currentrow.append(RAcondition01)
   currentrow.append(RAcondition02)
   currentrow.append(RAcondition03)
   currentrow.append(RAcondition04)
   currentrow.append(RAcondition05)
   currentrow.append(RAcondition06)
   currentrow.append(RAcondition07)
   currentrow.append(RAcondition08)
   currentrow.append(RAcondition09)
   currentrow.append(RAcondition10)
   currentrow.append(RAcondition11)
   currentrow.append(RAcondition12)
   currentrow.append(RAcondition13)
   currentrow.append(RAcondition14)
   currentrow.append(RAcondition15)
   currentrow.append(RAcondition16)
   currentrow.append(RAcondition17)
   currentrow.append(RAcondition18)
   currentrow.append(RAcondition19)
   currentrow.append(RAcondition20)
   #1999 might be only one for this
   #currentrow.append(occupation)
   allrows.append(currentrow)
   numLines += 1
colNames = ['Record_type','Resident_Status','Occurence_State','Occurence_County', 'Resident_State','Resident_County_NOT_FIPS', 'Resident_City_NOT_FIPS', 'Resident_City_PopSize','Resident_Metro','SMSA','Birth_State','Death_Month','Gender','Age_Type','Age_Number','Age_Recode_52','Age_Recode_27','Age_Recode_12','Age_Recode_22','Death_Place','Martial_Status','Day_of_week','Autopsy','Place_of_Injury','ICD9','ICD282','ICD72','ICD61','ICD34','Race','Race_Recode_3', 'Num_EA_Conditions', 'EA_Condition_01', 'EA_Condition_02', 'EA_Condition_03','EA_Condition_04','EA_Condition_05','EA_Condition_06','EA_Condition_07','EA_Condition_08', 'EA_Condition_09','EA_Condition_10', 'EA_Condition_11', 'EA_Condition_12','EA_Condition_13','EA_Condition_14','EA_Condition_15','EA_Condition_16','EA_Condition_17','EA_Condition_18','EA_Condition_19','EA_Condition_20', 'Num_RA_Conditions', 'RA_Condition_01', 'RA_Condition_02', 'RA_Condition_03','RA_Condition_04','RA_Condition_05','RA_Condition_06','RA_Condition_07','RA_Condition_08', 'RA_Condition_09','RA_Condition_10', 'RA_Condition_11', 'RA_Condition_12','RA_Condition_13','RA_Condition_14','RA_Condition_15','RA_Condition_16','RA_Condition_17','RA_Condition_18','RA_Condition_19','RA_Condition_20']
df = pd.DataFrame(allrows, columns=colNames)
if numLines != df.shape[0]:
   print("text file had",numLines,"df.shape[0] is", df.shape[0],"they SHOULD be the same. Exiting.")
   exit(1)
df.to_csv('../Cleaned_Data/' + os.path.basename(filename.replace('txt','csv')), index=False)
