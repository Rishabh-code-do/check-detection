
import datetime
 
s=int(12112022)
t=str(s)
yyyy=t[4:]
mm=t[2:4]
dd=t[0:2]
date = datetime.date(int(yyyy), int(mm), int(dd))
print(date)