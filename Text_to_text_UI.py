from tkinter import *
from PIL import ImageTk, Image
import BayeModel
import os

root = Tk()
root.title("Image-to-text")

img_path = 'New_image/'
'''
while True:
    img_path = input("Enter image folder>")
    if os.path.isdir(img_path):
        break
    print("Image not found")
'''

image_list, list_of_characters,list_of_str = [],[],[]
for filename in os.listdir(img_path):
    image, character, path, output_str = BayeModel.__main__(img_path+filename)
    image_list.append(ImageTk.PhotoImage(Image.open(path).resize([400,400])))
    list_of_characters.append(character)
    list_of_str.append(output_str)
    
    
# Pictures
number = 1
my_label = Label(image = image_list[0])
my_label.grid(row=0, column=0, columnspan=3)

from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'ACa0a344979d0858c1ac24eede195cc554'
auth_token = '30ad569050b783c42c6922207d4532ee'
client = Client(account_sid, auth_token)

def forward(image_number):
    global my_label
    global button_forward
    global button_back
    global button_sms
    
    my_label.grid_forget()
    my_label = Label(image=image_list[image_number - 1])
    button_forward = Button(root, text=">>", command = lambda:forward(image_number+1))
    button_back = Button(root, text="<<", command = lambda:back(image_number-1))
    button_sms = Button(root, text ="send sms", command=lambda:middle(image_number))
    
    if image_number == len(image_list):
        button_forward = Button(root, text= ">>", state=DISABLED)
    
    my_label.grid(row=0, column=0, columnspan=3)
    button_back.grid(row=1, column=0)
    button_sms.grid(row=1, column=1)
    button_forward.grid(row=1, column=2)
    #print(image_number)
    #client.messages.create(body="This is the " + str(list_of_characters[image_number-2])+ " picture",\
                                     #from_='+16812502153',\
                                     #to='+15148146788')
                                                
    
def middle(image_number):
    global my_label
    global button_forward
    global button_back
    global button_sms
    
    my_label.grid_forget()
    my_label = Label(image=image_list[image_number - 1])
    button_forward = Button(root, text=">>", command = lambda:forward(image_number+1))
    button_back = Button(root, text="<<", command = lambda:back(image_number-1))
    button_sms = Button(root, text ="send sms", command=lambda:middle(image_number))
    
    if image_number == len(image_list):
        button_forward = Button(root, text= ">>", state=DISABLED)
    if image_number == 1:
        button_back = Button(root, text= "<<", state=DISABLED)
    
    my_label.grid(row=0, column=0, columnspan=3)
    button_back.grid(row=1, column=0)
    button_sms.grid(row=1, column=1)
    button_forward.grid(row=1, column=2)
    #print(image_number)
    client.messages.create(body="This is the " + str(list_of_characters[image_number-1]) + " picture\n"+ list_of_str[image_number-1] ,\
                                     from_='+16812502153',\
                                     to='+15148146788')
    
def back(image_number):
    global my_label
    global button_forward
    global button_back
    global button_sms
    
    
    my_label.grid_forget()
    my_label = Label(image=image_list[image_number - 1])
    button_forward = Button(root, text=">>", command = lambda:forward(image_number+1))
    button_back = Button(root, text="<<", command = lambda:back(image_number-1))
    button_sms = Button(root, text ="send sms", command=lambda:middle(image_number))
    
    if image_number == 1:
        button_back = Button(root, text= "<<", state=DISABLED)
    
    my_label.grid(row=0, column=0, columnspan=3)
    button_back.grid(row=1, column=0)
    button_sms.grid(row=1, column=1)
    button_forward.grid(row=1, column=2)
    #print(image_number)
    #client.messages.create(body="This is the " +str(list_of_characters[image_number])+ " picture",\
                                     #from_='+16812502153',\
                                     #to='+15148146788')

button_back = Button(root, text="<<", command = back, state=DISABLED)
button_sms = Button(root, text ="send sms", command=lambda:middle(1))
button_forward = Button(root, text=">>", command= lambda:forward(2))

button_back.grid(row=1, column=0)
button_sms.grid(row=1, column=1)
button_forward.grid(row=1, column=2)

root.mainloop()
