import re
import datetime

def getdate(uinput):
    daypattern='([0-9]+)'
    datepattern = '(([0-9]+((r)(d)|(t)(h)|(n)(d)))?)'

    monthpattern='((\s+)(?:(Jan)|(jan)|(Feb)|(feb)|(Mar)|(mar)|(Apr)|(apr)|(May)|(may)|(Jun)|(jun)|(Jul)|(jul)|(Aug)|(aug)|(Sep)|(sep)|(Oct)|(oct)|(Nov)|(nov)|(Dec)|(dec)))'
    nexttodate_pattern = '((r)(d)|(t)(h)|(n)(d))?'
    of_pattern = '((\s+)(o)(f))?'
    pattern3 = '((\s+)(?:(next week)|(next month)))'
    textpattern3 = re.compile(datepattern+of_pattern+pattern3)
    match = re.search(textpattern3,uinput)

    if(match!=None):
        print match.group()
        day = re.search(daypattern,match.group())
        if(day.group()!=None):
            day = day.group()
            print day

        month = re.search(re.compile(pattern3),match.group())
        if(month.group()!=None):
            if(month.group().strip()=="next week"):
                month = datetime.date.today().month
                print month
            else:
                month = datetime.date.today().month + 1
                print month

        year = datetime.date.today().year





    # textpattern='((\s+)(?:(Tomorrow)|(nextday)|(next month)|(Day after tomorrow)|(end of the month)))'
    # textpattern1 = re.compile("(?!<\\s|^)\\s+(?!\\s|$)")
    # futurepattern='((\s+)(?:(after)))'
    # pattern3=re.compile(textpattern1)
    # date=re.search(pattern3,uinput)
    # if(textpattern1.group()=="Tomorrow"|textpattern1.group()=="nextday"):
    #     date=datetime.datetime.now()+datetime.timedelta(days=1)#getting the Exact time :(
    #     print date
    # if(textpattern1.group()=="dayaftertomorrow"):
    #     date=datetime.datetime.now()+datetime.timedelta(days=2)
    #     print date
    # # I wanna fly from A to B after n days
    # pattern5=re.comile(futurepattern+datepattern)
    # date=re.search(pattern5,uinput)
    # i=datepattern;
    # if(i=='[(0-9])'):
    #     date=datetime.datetime.now()+datetime.timedelta(days=i)
    # print date

    # pattern5=re.compile(textpattern1)
    # date=re.search(pattern5,uinput)
    # date=datetime.datetime.now()
    # dates = [date + datetime.timedelta(days=i) for i in range(-4 - date.weekday(), 4 - date.weekday())]
    # print dates


while True:
    user_input = raw_input('>>')
    getdate(user_input)
    if(user_input=="exit"):
        break;
