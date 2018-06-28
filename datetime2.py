import re
import datetime
from datetime import timedelta
import pandas

def getdate(input):
	future_pattern='((\s+)(?:(tomorrow|next day|nextday)))'
	dat_pattern='((\s+)(?:(day after tomorrow)))'
	pattern=re.compile(future_pattern)
	pattern1=re.compile(dat_pattern)
	date=re.search(pattern,input)
	date2=re.search(pattern1,input)
    
    # TOMORROW | NEXT DAY | NEXTDAY
	date=datetime.datetime.now()+datetime.timedelta(days=1)
	date1=pandas.to_datetime(date)
	print date1
	print date1.day,date1.month,date1.year

	# DAY AFTER TOMORROW
	date2=datetime.datetime.now()+datetime.timedelta(days=2)
	date2=pandas.to_datetime(date2)
	print date2.day,date2.month,date2.year
      

   


	


    

while True:
    uinput = raw_input('>>')
    getdate(uinput)
    if(uinput=="exit"):
        break;
