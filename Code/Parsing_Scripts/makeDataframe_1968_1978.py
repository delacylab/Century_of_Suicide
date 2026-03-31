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
   recordtype = line[10] #1 = same res/death location, 2=different
   residentstatus = line[11] #1=same res/death loc,2=same state diff county
   #3 = diff state, 4=foreign citizen in US
   occurenceState = str(line[25:27])  #eg. UT
   occurenceState = birth_state_dict[occurenceState]
   occurenceCountyFIPS = str(line[27:30]) #NO int conversion
#   occurenceNYCcode = str(line[25:27]) #YC = NYC code, we don't care about that
   #occurenceCountyPopSize = line[48] #0 = highest > million, 6= < 25,000
   residenceState = str(line[12:14]) #NOTE ZZ=foreign resident, also could have
   residenceState = birth_state_dict[residenceState]
   #territories here?
#   residenceStateCountry = line[32:34] #recode of above with some countries
   residenceCounty = str(line[14:17]) #county FIPS
   residenceCityNotFIPS = str(line[17:20])
   residenceCityPopSize = line[20] #almost same as county, Z=foreign
   SMSA = str(line[21:24])
   residenceMetroAreaBoolean = line[24] #1=Metro, 2-Not, Z=foreign resident

   deathMonth = line[30:32] #e.g. 07 for July   
   gender = str(line[34]) # M/F
   if gender == '1':
      gender = 'M'
   if gender == '2':
      gender = 'F'
   #Age - this will be ugly
   ageType = line[38] #1= age in years, 2=months,3=days,4=hours,5=minutes,9=NA
   ageNum = int(line[39:41]) #number with unites given in ageType
   #NOTE we want ageNum as int so we will not cast here
   #ageSub = line[113] #1=age was calculated from birth/death, blank=reported
   ageRecode27 = line[43:45] #different table, same idea as above line
   ageRecode12 = line[41:43] #another different table
   ageRecode22 = line[45:47] #table for infants
   deathDate = int(line[32:34]) #01-31, have to do extra work here to get day of week
   dayOfWeek = 9 #
   if deathDate != 99:      
     deathDateClass = date(1988,int(deathMonth),int(deathDate))   
     dayOfWeek = deathDateClass.isoweekday() #line[82] #Coded day of week e.g.3=  Tuesday Suicide Tuesday?
     dayOfWeek += 1
     if dayOfWeek == 8:
        dayOfWeek = 1
   autopsy = str(line[51]) #Y/N/U
   if autopsy == '1':
      autopsy = 'Y'
   elif autopsy == '2':
      autopsy = 'N'
   else:
      autopsy = 'U'
   placeOfInjury = line[90] #Place of injury where applicable, see table
   #Now for ICD codes which I think are important
   ICD8 = str(line[59:63])
   ICDrecode281 = str(line[63:68])
   ICDrecode69 = str(line[68:71])
   ICDrecode65 = str(line[71:74])
   ICDrecode34 = str(line[74:77])
   #Multiple conditions
#Space has been provided for maximum of 20 conditions.  Each condition takes 7 positions in the record.  The 7th position will be blank.  Records that do not have 20 conditions are blank in the unused area.
   numConditions = line[98:100]
   condition01 = str(line[100:108])
   condition02 = str(line[108:116])
   condition03 = str(line[116:124])
   condition04 = str(line[124:132])
   condition05 = str(line[132:140])
   condition06 = str(line[140:148])
   condition07 = str(line[148:156])
   condition08 = str(line[156:164])
   condition09 = str(line[164:172])
   condition10 = str(line[172:180])
   condition11 = str(line[180:188])
   condition12 = str(line[188:196])
   condition13 = str(line[196:204])
   condition14 = str(line[204:212])
   #RA codes are more amenable to statistical tabulation
   numRAConditions = line[212:214]
   RAcondition01 = str(line[214:219])
   RAcondition02 = str(line[219:224])
   RAcondition03 = str(line[224:229])
   RAcondition04 = str(line[229:234])
   RAcondition05 = str(line[234:239])
   RAcondition06 = str(line[239:244])
   RAcondition07 = str(line[244:249])
   RAcondition08 = str(line[249:254])
   RAcondition09 = str(line[254:259])
   RAcondition10 = str(line[259:264])
   RAcondition11 = str(line[264:269])
   RAcondition12 = str(line[269:274])
   RAcondition13 = str(line[274:279])
   RAcondition14 = str(line[279:284])
#END OF NEW MULTIPLE CONDS
   race = str(line[35]) #this will be troublesome, apparently Asian-PI
   #codes have changed over the years. Table is:
   #01 = White, 02=Black, 03=AI-AN, 04=Chinese, 05=Japanese, 06=Hawaiian,
   #07=Filipino, Asian-PI is all codes from 18-78
   #So China/Japan/Hawaiian/Filipino != Asian-PI???
   raceRecode3 = str(line[37]) #1 = White, 3=Black, 2=Neither
   #ARGH so for no apparent reason they switched 2 and 3 here and I want it to
   #line up with others.
   if raceRecode3 == '2':
      raceRecode3 = '3'
   elif raceRecode3 == '3':
      raceRecode3 = '2'
   #Now to append all these
   currentrow.append(recordtype)
   currentrow.append(residentstatus)
   currentrow.append(occurenceState) 
   currentrow.append(occurenceCountyFIPS) 
   currentrow.append(residenceState) 
   currentrow.append(residenceCounty) 
   currentrow.append(residenceCityNotFIPS)
   currentrow.append(residenceCityPopSize) 
   currentrow.append(SMSA)
   currentrow.append(residenceMetroAreaBoolean) 
   currentrow.append(deathMonth) 
   currentrow.append(gender) 
   currentrow.append(ageType) 
   currentrow.append(ageNum) 
   currentrow.append(ageRecode27) 
   currentrow.append(ageRecode12) 
   currentrow.append(ageRecode22) 
   currentrow.append(dayOfWeek) 
   currentrow.append(autopsy)
   currentrow.append(placeOfInjury)
   currentrow.append(ICD8)
   currentrow.append(ICDrecode281)
   currentrow.append(ICDrecode69)
   currentrow.append(ICDrecode65)
   currentrow.append(ICDrecode34)
   currentrow.append(race)
   currentrow.append(raceRecode3)
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
   allrows.append(currentrow)
   numLines += 1
colNames = ['Record_type','Resident_Status','Occurence_State','Occurence_County', 'Resident_State','Resident_County_NOT_FIPS', 'Resident_City_NOT_FIPS', 'Resident_City_PopSize','SMSA', 'Resident_Metro','Death_Month','Gender','Age_Type','Age_Number','Age_Recode_27','Age_Recode_12','Age_Recode_22','Day_of_week','Autopsy','Place_of_Injury','ICD8','ICD281','ICD69','ICD65','ICD34','Race','Race_Recode_3', 'Num_EA_Conditions', 'EA_Condition_01', 'EA_Condition_02', 'EA_Condition_03','EA_Condition_04','EA_Condition_05','EA_Condition_06','EA_Condition_07','EA_Condition_08', 'EA_Condition_09','EA_Condition_10', 'EA_Condition_11', 'EA_Condition_12','EA_Condition_13','EA_Condition_14', 'Num_RA_Conditions', 'RA_Condition_01', 'RA_Condition_02', 'RA_Condition_03','RA_Condition_04','RA_Condition_05','RA_Condition_06','RA_Condition_07','RA_Condition_08', 'RA_Condition_09','RA_Condition_10', 'RA_Condition_11', 'RA_Condition_12','RA_Condition_13','RA_Condition_14']
df = pd.DataFrame(allrows, columns=colNames)
if numLines != df.shape[0]:
   print("text file had",numLines,"df.shape[0] is", df.shape[0],"they SHOULD be the same. Exiting.")
   exit(1)
df.to_csv('../Cleaned_Data/' + os.path.basename(filename.replace('txt','csv')), index=False)
