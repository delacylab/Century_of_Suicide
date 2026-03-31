import pandas as pd
import argparse
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import numpy as np
import os
parser = argparse.ArgumentParser()
parser.add_argument('filename',help='file')
args = parser.parse_args()
filename = args.filename
afile = open('../../../Raw_Datasets/CDC/CDC_Original_Text_Files/' + filename)
lines = [line for line in afile]
allrows = []
numLines = 0
for line in lines:
   currentrow = []
   #NOTE: the "Tape location" in data dictionary is NOT zero based
   #so I have to subtract one from everything in it
   recordtype = line[18] #1 = same res/death location, 2=different
   residentstatus = line[19] #1=same res/death loc,2=same state diff county
   #3 = diff state, 4=foreign citizen in US
   occurenceState = line[20:22]  #eg. UT
   occurenceCountyFIPS = str(line[22:25]) #NO int conversion
   occurenceNYCcode = str(line[25:27]) #YC = NYC code, we don't care about that
   occurenceCountyPopSize = line[27] #0 = highest > million, 6= < 25,000
   residenceState = line[28:30] #NOTE ZZ=foreign resident, also could have
   #territories here?
   residenceStateCountry = line[32:34] #recode of above with some countries
   residenceCounty = str(line[34:37]) #county FIPS
   residenceCity = str(line[37:42]) #City FIPS, didn't know these existed
   residenceCityPopSize = line[42] #almost same as county, Z=foreign
   residenceMetroAreaBoolean = line[43] #1=Metro, 2-Not, Z=foreign resident
   residenceNYCcode = line[44:46] #YC=NYC code
   birthState = line[54:56] #e.g. UT
   birthStateCountry = line[58:60] #recode of above with some countries
   #next 2 fields are education - annoyingly there are 2 version (1989,2003)
   #one will always be blank
   edu1989 = str(line[60:62]) #see data dictionary
   edu2003 = str(line[62]) #simpler code
   eduCode = int(line[63]) #0 = 1989, 1=2003, 2 = none
   #unfortunately there are blank spaces in at least one of these
   eduHS = 0
   if eduCode == 0: #1989 case
      if int(edu1989) == 99:
         eduHS = np.nan
      elif int(edu1989) >= 12:
         eduHS = 1
      #else 0 but we already set default to 0
   elif eduCode == 1: #2003 case
      if int(edu2003) == 9:
         eduHS = np.nan
      elif int(edu2003) >= 3:
         eduHS = 1
      #else 0 but we already set default to 0
   else: #eduCode not set
      eduHS = np.nan
      
   deathMonth = line[64:66] #e.g. 07 for July
   gender = line[68] # M/F
   #Age - this will be ugly
   ageType = str(line[69]) #1= age in years, 2=months,3=days,4=hours,5=minutes,9=NA
   ageNum = int(line[70:73]) #number with unites given in ageType
   #New part for a unified AGE_YEARS field
   ageYears = 0
   if ageType == '1': #Next three digits are years
      ageYears = ageNum

   #NOTE we want ageNum as int so we will not cast here
   ageSub = line[73] #1=age was calculated from birth/death, blank=reported
   ageRecode52 = line[74:76] #this may be useful, uses age groups e.g. 35-39
   ageRecode27 = line[76:78] #different table, same idea as above line
   ageRecode12 = line[78:80] #another different table
   ageRecode22 = line[80:82] #table for infants
   placeOfDeath = line[82] #hospital/home/other, see table
   maritalStatus = line[83] #S/M/W/D/N/U, N and U = unknown
   dayOfWeek = str(line[84]) #Coded day of week e.g.3=  Tuesday Suicide Tuesday?
   dataYear = line[101:105] # current data year e.g. 2003? May want to check
   #if this is same as file
   workInjury = line[105] #Y/N/U(nknown)
   mannerOfDeath = str(line[106]) #See table, important ones we want probably
   #2=Suicide, 4=Pending Investigation, 5=unknown, 6=Self-inflicted
   #Could be blank as well for unknown
   disposition = line[107] #Burial/Cremation/Other/Unknown
   autopsy = line[108] #Y/N/U
   certifier = line[109] #D/P/M/O e.g. Doctor/physician do we care?
   tobaccoUse = line[141] #Y/N/P/U
   pregnancy = str(line[142]) #Could be interesting, see table
   activityCode = str(line[143]) #active at time of death, see table
   placeOfInjury = str(line[144]) #Place of injury where applicable, see table
   #Now for ICD codes which I think are important
   ICD10 = str(line[145:149])
   ICDrecode358 = str(line[149:152])
   ICDrecode113 = str(line[153:156])
   ICDrecode130 = str(line[156:159])
   ICDrecode39 = str(line[159:161])
   #Multiple conditions
#Space has been provided for maximum of 20 conditions.  Each condition takes 7 positions in the record.  The 7th position will be blank.  Records that do not have 20 conditions are blank in the unused area.
   numConditions = line[162:164]
   condition01 = str(line[164:171])
   condition02 = str(line[171:178])
   condition03 = str(line[178:185])
   condition04 = str(line[185:192])
   condition05 = str(line[192:199])
   condition06 = str(line[199:206])
   condition07 = str(line[206:213])
   condition08 = str(line[213:220])
   condition09 = str(line[220:227])
   condition10 = str(line[227:234])
   condition11 = str(line[234:241])
   condition12 = str(line[241:248])
   condition13 = str(line[248:255])
   condition14 = str(line[255:262])
   condition15 = str(line[262:269])
   condition16 = str(line[269:276])
   condition17 = str(line[276:283])
   condition18 = str(line[283:290])
   condition19 = str(line[290:297])
   condition20 = str(line[297:304])
   #RA codes are more amenable to statistical tabulation
   numRAConditions = line[340:342]
   RAcondition01 = str(line[343:348])
   RAcondition02 = str(line[348:353])
   RAcondition03 = str(line[353:358])
   RAcondition04 = str(line[358:363])
   RAcondition05 = str(line[363:368])
   RAcondition06 = str(line[368:373])
   RAcondition07 = str(line[373:378])
   RAcondition08 = str(line[378:383])
   RAcondition09 = str(line[383:388])
   RAcondition10 = str(line[388:393])
   RAcondition11 = str(line[393:398])
   RAcondition12 = str(line[398:403])
   RAcondition13 = str(line[403:408])
   RAcondition14 = str(line[408:413])
   RAcondition15 = str(line[413:418])
   RAcondition16 = str(line[418:423])
   RAcondition17 = str(line[423:428])
   RAcondition18 = str(line[428:433])
   RAcondition19 = str(line[433:438])
   RAcondition20 = str(line[438:443])
#END OF NEW MULTIPLE CONDS
   race = str(line[444:446]) #this will be troublesome, apparently Asian-PI
   #codes have changed over the years. Table is:
   #01 = White, 02=Black, 03=AI-AN, 04=Chinese, 05=Japanese, 06=Hawaiian,
   #07=Filipino, Asian-PI is all codes from 18-78
   #So China/Japan/Hawaiian/Filipino != Asian-PI???
   bridgedrace = line[446] #1=Bridged, blank=not
   raceImputed = line[447] #1=Imputed, blank=not
   raceRecode3 = line[448] #1 = White, 3=Black, 2=Neither
   raceRecode5 = line[449] #1=White, 2=Black,3=AI-AN,4=Asian,5=PI
   raceHispanicCode = line[483:486]
   raceHispanicRecode = line[487] # codes 6-9=Non-Hispanic
   raceRecode40 = line[488:490] #available after 2012 - race percentages
   
   #Now to append all these
   currentrow.append(recordtype)
   currentrow.append(residentstatus)
   currentrow.append(occurenceState) 
   currentrow.append(occurenceCountyFIPS) 
   currentrow.append(occurenceNYCcode) 
   currentrow.append(occurenceCountyPopSize) 
   currentrow.append(residenceState) 
   currentrow.append(residenceStateCountry) 
   currentrow.append(residenceCounty) 
   currentrow.append(residenceCity) 
   currentrow.append(residenceCityPopSize) 
   currentrow.append(residenceMetroAreaBoolean) 
   currentrow.append(residenceNYCcode) 
   currentrow.append(birthState) 
   currentrow.append(birthStateCountry) 
   currentrow.append(edu1989) 
   currentrow.append(edu2003) 
   currentrow.append(eduCode) 
   currentrow.append(eduHS)
   currentrow.append(deathMonth) 
   currentrow.append(gender) 
   currentrow.append(ageType) 
   currentrow.append(ageNum) 
   currentrow.append(ageYears)
   currentrow.append(ageSub) 
   currentrow.append(ageRecode52) 
   currentrow.append(ageRecode27) 
   currentrow.append(ageRecode12) 
   currentrow.append(ageRecode22) 
   currentrow.append(placeOfDeath) 
   currentrow.append(maritalStatus) 
   currentrow.append(dayOfWeek) 
   currentrow.append(dataYear) 
   currentrow.append(workInjury)
   currentrow.append(mannerOfDeath)
   currentrow.append(disposition)
   currentrow.append(autopsy)
   currentrow.append(certifier)
   currentrow.append(tobaccoUse)
   currentrow.append(pregnancy)
   currentrow.append(activityCode)
   currentrow.append(placeOfInjury)
   currentrow.append(ICD10)
   currentrow.append(ICDrecode358)
   currentrow.append(ICDrecode113)
   currentrow.append(ICDrecode130)
   currentrow.append(ICDrecode39)
   currentrow.append(race)
   currentrow.append(bridgedrace)
   currentrow.append(raceImputed)
   currentrow.append(raceRecode3)
   currentrow.append(raceRecode5)
   currentrow.append(raceHispanicCode)
   currentrow.append(raceHispanicRecode)
   currentrow.append(raceRecode40)
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
   allrows.append(currentrow)
   numLines += 1
colNames = ['Record_type','Resident_Status','Occurence_State','Occurence_County','Occurence_NYC','Occurence_County_PopSize','Resident_State','Resident_State_Country','Resident_County_FIPS','Resident_City','Resident_City_PopSize','Resident_Metro','Resident_NYC','Birth_State','Birth_Country','EDU_1989','EDU_2003','EDU_WHICH','EDU_HS', 'Death_Month','Gender','Age_Type','Age_Number','Age_Years','Age_Calc','Age_Recode_52','Age_Recode_27','Age_Recode_12','Age_Recode_22','Death_Place','Marital_Status','Day_of_week','Data_Year','Work_Injury','Manner_of_Death','Disposition','Autopsy','Certifier','Tobacco_Use','Pregnancy_Status','Activity_Code','Place_of_Injury','ICD10','ICD358','ICD113','ICD130','ICD39','Race','Bridged_Race','Race_Imputed','Race_Recode_3','Race_Recode_5','Race_Hispanic_Code','Race_Hispanic_Recode', 'Race_Recode_40', 'Num_EA_Conditions', 'EA_Condition_01', 'EA_Condition_02', 'EA_Condition_03','EA_Condition_04','EA_Condition_05','EA_Condition_06','EA_Condition_07','EA_Condition_08', 'EA_Condition_09','EA_Condition_10', 'EA_Condition_11', 'EA_Condition_12','EA_Condition_13','EA_Condition_14','EA_Condition_15','EA_Condition_16','EA_Condition_17','EA_Condition_18','EA_Condition_19','EA_Condition_20', 'Num_RA_Conditions', 'RA_Condition_01', 'RA_Condition_02', 'RA_Condition_03','RA_Condition_04','RA_Condition_05','RA_Condition_06','RA_Condition_07','RA_Condition_08', 'RA_Condition_09','RA_Condition_10', 'RA_Condition_11', 'RA_Condition_12','RA_Condition_13','RA_Condition_14','RA_Condition_15','RA_Condition_16','RA_Condition_17','RA_Condition_18','RA_Condition_19','RA_Condition_20']
df = pd.DataFrame(allrows, columns=colNames)
#This is probably the place to do onehotencoding
ohe_dict = {}
ohe_dict['Marital_Status'] = sorted([ ['S'],['M'],['W'],['D'],['N'],['U'] ])
ohe_dict['Day_of_week'] = sorted([ ['1'],['2'],['3'],['4'],['5'],['6'],['7'],['9'] ])
ohe_dict['Death_Place'] = sorted([ ['1'],['2'],['3'],['4'],['5'],['6'],['7'],['9']  ])
ohe_dict['Work_Injury'] = sorted([ ['Y'],['N'],['U'] ])
ohe_dict['Manner_of_Death'] = sorted([ ['1'],['2'],['3'],['4'],['5'],['6'],['7'] ])
ohe_dict['Disposition'] = sorted([ ['B'],['C'],['O'],['U'] ])
ohe_dict['Autopsy'] = sorted([ ['Y'],['N'],['U'] ])
ohe_dict['Certifier'] = sorted([ ['D'],['P'],['M'],['O'] ])
ohe_dict['Tobacco_Use'] = sorted([ ['Y'],['N'],['P'],['U'] ])
ohe_dict['Pregnancy_Status'] = sorted([ ['1'],['2'],['3'],['4'],['7'],['8'],['9'] ])
ohe_dict['Activity_Code'] = sorted([ ['0'],['1'],['2'],['3'],['4'],['8'],['9']  ])
ohe_dict['Place_of_Injury'] = sorted([ ['0'],['1'],['2'],['3'],['4'],['5'],['6'],['7'],['8'],['9']  ])
ohe_dict['ICD39'] = sorted([ ['01'],['02'],['03'],['04'],['05'],['06'],['07'],['08'],['09'],['10'],['11'],['12'],['13'],['14'],['15'],['16'],['17'],['18'],['19'],['20'],['21'],['22'],['23'],['24'],['25'],['26'],['27'],['28'],['29'],['30'],['31'],['32'],['33'],['34'],['35'],['36'],['37'],['38'],['39'],['40'],['41'],['42'] ])
#ohe_dict['Bridged_Race'] = This only has one possible value in a sense (blank or 1) so I am holding off on this for now
ohe_dict['Race_Imputed'] = sorted([ ['1'],['2'] ] )
ohe_dict['Race_Recode_5'] = sorted([ ['1'],['2'],['3'],['4'],['5'] ])
#should have some kind of explanation lookup table for numerical values that are categorical
explanation_dict = {}
#Important - need to have blank entries in array for gaps in possible values for this to work
explanation_dict['Day_of_week'] = ['','Sun','Mon','Tue','Wed','Thu','Fri','Sat','','Unknown']
explanation_dict['Death_Place'] = ['','Inpatient','Outpatient/ER','DOA','Home','Hospice','Nursing_Home','Other','','Unknown']
explanation_dict['Manner_of_Death'] = ['','Accident','Suicide','Homicide','Pending_Investigation','Could_not_determine','Self-Inflicted','Natural']
explanation_dict['Pregnancy_Status'] = ['','Not_within_year','Pregnant','Not_but_within_42days','Not_but_within_43-365','','','Not_On_Cert','NA','Unknown']
explanation_dict['Activity_Code'] = ['Sports','Leisure','Income','Other_Work','Vital_Act','','','','Other','Unknown']
explanation_dict['Place_of_Injury'] = ['Home','Residential_Inst','Public','Sports','Street/Highway','Trade/Service','Industrial','Farm','Other','Unknown']
explanation_dict['ICD39'] = ['','Tuberculosis','Syphilis','HIV','Malignant_Neoplasm','Malignant_Stomach','Malignant_Intestine','Malignant_Pancreas','Malignant_Lung','Malignant_Breast','Malignant_Cervix_Ovary','Malignant_Prostate','Malignant_Urinary','Malignant_NonHodgkin','Malignant_Leukemia','Malignant_Other','Diabetes','Alzheimers','Cardiovascular','Heart_Disease','Hypertensive','Ischemic','Heart_Other','Hypertension','Cerebrovascular','Atherosclerosis','Circulatory_Other','Influenza_Pneumonia','Chronic_Respiratory','Peptic_Ulcer','Liver_Disease/Cirrhosis','Nephritis','Pregnancy','Perinatal','Congenital','SIDS','Abnormal','All_Other_Diseases_Residual','Motor_Vehicle_Accident','Other_Accidents_Effects','Self-Harm/Suicide','Homicide','All_Other_External']
explanation_dict['Race_Imputed'] = ['','Unknown_Imputed','Other_Imputed']
explanation_dict['Race_Recode_5'] = ['','White','Black','Native_American','Asian','PI']
for col in ohe_dict.keys():
   enc = OneHotEncoder(handle_unknown='ignore',sparse=False)
   enc.fit(ohe_dict[col])
   enca = enc.transform(np.array(df[col].tolist()).reshape(-1,1))
   new_col_names = []
   for item in ohe_dict[col]: #this should get to the targets
      suffix = item[0]
      if col in explanation_dict.keys():
         suffix = (explanation_dict[col])[int(suffix)]
      new_col_names.append(col + '_' + suffix)
   dftemp = pd.DataFrame(enca,columns=new_col_names)
   #Now just need to concat it to original dataframe. 
   df = pd.concat([df, dftemp],axis=1)

#end of line
if numLines != df.shape[0]:
   print("text file had",numLines,"df.shape[0] is", df.shape[0],"they SHOULD be the same. Exiting.")
   exit(1)
df.to_csv('../Cleaned_Data/' + os.path.basename(filename.replace('txt','csv')), index=False)
