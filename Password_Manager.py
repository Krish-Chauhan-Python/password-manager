from tkinter import *
from tkinter import messagebox	
import sqlite3
import random
import pyperclip

root = Tk()
root.title("Password Manager")
root.configure(background = "#333333")
root.geometry("450x500")
global key
key = 0

def filter(a , b , c):
	d = []
	for i in a:
		if b in i[c]:
			d.append(i)
	return d

def search(x , y):
	connection = sqlite3.connect('Passwords.db')

	cur = connection.cursor()

	cur.execute("SELECT *  FROM  Passwords ")	

	a = cur.fetchall()

	connection.commit()

	connection.close()

	b = []

	for i in a:
		if x.lower() in i[0].lower() and y.lower() in i[2].lower():
			b.append(i)

	msg_window = Toplevel()
	msg_window.title("Filtered Passwords")
	msg_window.configure(background = "#333333")
	Label(msg_window , text = "Emails:" , width = 30, relief = "ridge").grid(row = 0 , column = 0 , sticky = W )
	Label(msg_window , text = "Websites:" , width = 19, relief = "ridge").grid(row = 0 , sticky = EW , column = 1 )
	Label(msg_window , text = "Pass Buttons:" , relief = "ridge").grid(row = 0 , column = 2 , sticky = EW)
	for i in b:
		Label(msg_window , text = i[0] , width = 30, relief = "ridge").grid(row = b.index(i) +1 , column = 0 , sticky = W )
		Button(msg_window, bg = "#4185c2" , text = "Show Password" , relief = "groove" , command = lambda: new_window(decode(i[1]))).grid(row = b.index(i)+1 , column = 2 , sticky = E )
		Label(msg_window , text = i[2] , width = 19, relief = "ridge").grid(row = b.index(i)+1 , sticky = EW , column = 1 )

def str_to_binary(c):
    binary = ""
    for i in c:
        b = ""
        a = ord(i)
        while a != 0:
            b += str(a % 2)
            a = a // 2
        b = b[::-1]
        if len(b) < 7:
            b = ("0" *( 7 - len(b))) + b
        
        binary += b
    return binary

def copy(a):
	pyperclip.copy(a)

def new_window(a):
	msg_window = Toplevel()
	msg_window.title("Password")
	msg_window.geometry("145x25")
	msg_window.configure(background = "#333333")
	msgLabel = Label(msg_window , text = a  , bg = "#4185c2", relief = "groove").grid(row = 0 , column = 0 , sticky = EW)
	copy_pass = Button(msg_window,  text = "Copy" , command = lambda: copy(a)  ,  width = 7 , bg = "#4185c2", relief = "groove").grid(row = 0 , column = 1 , sticky = EW)

def show():

	global Email_List
	global Website_List
	global Password_List

	connection = sqlite3.connect('Passwords.db')

	cur = connection.cursor()

	cur.execute("SELECT *  FROM  Passwords ")	

	output = cur.fetchall()

	connection.commit()

	connection.close()

	Label(Email_List , text = "Emails:" , width = 30, relief = "ridge").grid(row = 0 , column = 0 , sticky = W )
	Label(Email_List , text = "Websites:" , width = 19, relief = "ridge").grid(row = 0 , sticky = EW , column = 1 )
	Label(Email_List , text = "Pass Buttons:" , relief = "ridge").grid(row = 0 , column = 2 , sticky = EW)
	for i in output:
		Label(Email_List , text = i[0] , width = 30, relief = "ridge").grid(row = output.index(i) +1 , column = 0 , sticky = W )
		Button(Email_List, bg = "#4185c2" , text = "Show Password" , relief = "groove" , command = lambda: new_window(decode(i[1]))).grid(row = output.index(i)+1 , column = 2 , sticky = E )
		Label(Email_List , text = i[2] , width = 19, relief = "ridge").grid(row = output.index(i)+1 , sticky = EW , column = 1 )

def BinaryToDecimal(binary):
    binary = str(binary)
    decimal = 0
    for i in range(0,len(binary),1):
        decimal += int(binary[len(binary) - 1 - i]) * (2 ** i)
    return (decimal)

def DecimalToBinary(Decimal):
    a = bin(Decimal).replace("0b", "")
    if len(a) % 7 != 0:
        a = "0" * (len(a) // 7) + a
    return a

def binary_to_str(a):
    c = ""
    a = str(a)
    for i in range(0 , len(a) , 7):

        b = int(a[i:i+7])
        b = BinaryToDecimal(b)
        c += chr(b)

    return(c)

def decode(ini_string):
	global key
	ini_string = int(int(ini_string) // key)
	ini_string = DecimalToBinary(ini_string)
	ini_string = binary_to_str(ini_string)
	return ini_string

def encrypt(Password):
	c = str_to_binary(Password)
	c = BinaryToDecimal(c)
	c = c * key
	return c

def add_password():
	global Email
	global Password
	global Website

	connection = sqlite3.connect('Passwords.db')
	
	cur = connection.cursor()

	cur.execute("INSERT INTO Passwords VALUES (:email , :passwords , :website)", 
		{
		"email" :  Email.get(),
		"passwords" : str(encrypt(Password.get())),
		"website" : Website.get()
		})

	connection.commit()

	connection.close()

	show()

def generate():
	global Password

	a = ""
	b = ["0" ,"9" ,"8" ,"7" ,"6" ,"5" ,"4" ,"3" ,"2" ,"1" ,"z" ,"y" ,"x" ,"w" ,"v" ,"u" ,"t" ,"s" ,"r" ,"q" ,"p" ,"o" ,"n" ,"m" ,"l" ,"k" ,"j" ,"i" ,"h" ,"g" ,"f" ,"e" ,"d" ,"c" ,"b" ,"a" , "!" ,"@" ,"#" ,"$" ,"%" ,"^" ,"&" ,"*" ,"(" ,")" , "Z" ,"Y" ,"X" ,"W" ,"V" ,"U" ,"T" ,"S" ,"R" ,"Q" ,"P" ,"O" ,"N" ,"M" ,"L" ,"K" ,"J" ,"I" ,"H" ,"G" ,"F" ,"E" ,"D" ,"C" ,"B" ,"A"]
	for i in range(12):
		a += b[random.randint(0,len(b)-1)]
	a = str(a)
	Password.delete(0,END)
	Password.insert(0,a)	

def show_pass():
	global Password
	global Email
	global Website
	global Email_List
	global Website_List
	global Password_List


	Search_frame = LabelFrame(root, text = "Search")
	Search_frame.grid(row = 0 , column = 0 , columnspan = 3)

	Search_Email_label = Label(Search_frame , text = "Email : " , bg = "#4185c2", relief = "ridge", width = 19	)
	Search_Email_label.grid(row = 0 , column = 0)

	Search_Email = Entry(Search_frame , width = 50 , bg= "#4185c2" , relief = "groove")
	Search_Email.grid(row = 0, column = 1 , sticky = E)

	Search_Website_label = Label(Search_frame , text = "Website : " , bg = "#4185c2", relief = "ridge", width = 19	)
	Search_Website_label.grid(row = 1, column = 0)

	Search_Website = Entry(Search_frame , width = 50 , bg= "#4185c2" , relief = "groove")
	Search_Website.grid(row = 1, column = 1 , sticky = E)

	Search_Button = Button(Search_frame , text = "Enter" , command = lambda : search(Search_Email.get() , Search_Website.get()) , bg = "#4185c2", relief = "groove")
	Search_Button.grid(row = 2 , column = 0 , sticky = EW , columnspan = 2)

	Add_frame = LabelFrame(root, text = "Add Email")
	Add_frame.grid(row = 1 , column = 0 , columnspan = 3)

	Email_label = Label(Add_frame , text = "Email : " , bg = "#4185c2", relief = "ridge", width = 19)
	Email_label.grid(row = 0 , column = 0)

	Email = Entry(Add_frame , width = 50 , bg= "#4185c2" , relief = "groove")
	Email.grid(row = 0, column = 1 , sticky = E , columnspan = 2)

	Password_label = Label(Add_frame , text = "Password : " , bg = "#4185c2", relief = "ridge", width = 19	)
	Password_label.grid(row = 1 , column = 0)

	Password = Entry(Add_frame , width = 40 , bg= "#4185c2" , relief = "groove")
	Password.grid(row = 1, column = 1 , sticky = W)

	Pass_Button = Button(Add_frame , text = "Generate" , command = generate  ,  width = 7 , bg = "#4185c2", relief = "groove")
	Pass_Button.grid(row = 1 , column = 2 , sticky = E)

	Website_label = Label(Add_frame , text = "Website : " , bg = "#4185c2", relief = "ridge", width = 19	)
	Website_label.grid(row = 2 , column = 0)

	Website = Entry(Add_frame , width =50 , bg= "#4185c2" , relief = "groove")
	Website.grid(row = 2, column = 1 , columnspan = 2)

	Add_Button = Button(Add_frame , text = "Add +" , command = add_password ,  width = 50 , bg = "#4185c2", relief = "groove")
	Add_Button.grid(row = 3 , column = 0 , sticky = EW , columnspan = 3)

	Email_List = LabelFrame(root, text = "Information" , bg= "#F2BE6F" , relief = "groove")
	Email_List.grid(row = 2 , column = 0 , columnspan = 3 , sticky = EW)


	show()

def convert(Master_Password):
	global key
	for i in range(len(Master_Password)):
		Master_Password[i] = ord(Master_Password[i])
	key =  ( ( ( (Master_Password[1]) - (Master_Password[2]) ) * ( (Master_Password[3]) + (Master_Password[4]) ) ) - ( ( (Master_Password[5]) + (Master_Password[6]) ) * ( (Master_Password[7]) - (Master_Password[8]) ) ) ) * ( ( (Master_Password[9]) * (Master_Password[10]) ) - ( (Master_Password[11]) * (Master_Password[0]) ) )
	show_pass()

def Get_Master_Pass():

	global Master_Pass
	global Master_Pass_Label
	global Master_Pass_Button

	Master_Password = Master_Pass.get()
	Master_Password = list(Master_Password)
	Master_Pass.destroy()
	Master_Pass_Label.destroy()
	Master_Pass_Button.destroy()
	convert(Master_Password)


def Start():

	global Master_Pass
	global Master_Pass_Label
	global Master_Pass_Button

	Master_Pass_Label =  Label(root , text = "Master Password : " , bg = "#4185c2", relief = "ridge")
	Master_Pass_Label.grid(row = 0, column = 0 , sticky = W)

	Master_Pass = Entry(root , width = 49 , bg= "#4185c2" , relief = "groove")
	Master_Pass.grid(row = 0, column = 1 , sticky = W)

	Master_Pass_Button = Button(root , text = "Enter" , command = Get_Master_Pass  ,  width = 5 , bg = "#4185c2", relief = "groove")
	Master_Pass_Button.grid(row = 0 , column = 2 , sticky = EW)


Start()
root.mainloop()