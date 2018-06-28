from Tkinter import *
from main import chat

window = Tk()

window.wm_title("Flydubai ChatBot Assistant")

messages = Text(window)
messages.pack()

messages.insert(INSERT,'Agent:\n' + 'Welcome to the flydubai chat assistant\n\
    Here you can talk to us about\n\
    * Search flights\n\
    * Book flights\n\
    * Track flights\n')

input_user = StringVar()
input_field = Entry(window, text=input_user)
input_field.pack(side=BOTTOM, fill=X)

print 'pintooo'
bot = chat()
def Enter_pressed(event):
    input_get = input_field.get()
    # print(input_get)
    messages.insert(INSERT, 'You:\n%s\n\n\n' % input_get)
    if(bot.flag==0):
    	response = bot.bolo(input_get)
    	messages.insert(INSERT, 'Agent:\n'+str(response)+'\n\n')
    	if response.startswith("Searching"):
    		bot.flag = 1


    if(bot.flag==1):
    	response = bot.Search(input_get)
    	messages.insert(INSERT, 'Agent:\n'+str(response)+'\n\n')

    # label = Label(window, text=input_get)
    input_user.set('')
    # label.pack()
    return "break"

frame = Frame(window)  # , width=300, height=300)
input_field.bind("<Return>", Enter_pressed)
frame.pack()



window.mainloop()
