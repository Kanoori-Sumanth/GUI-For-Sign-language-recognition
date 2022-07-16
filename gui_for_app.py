from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image
import cv2
from gtts import gTTS
from playsound import playsound
import http.client as httplib
import numpy as np

def play():
	internet_status = checkInternetHttplib("www.google.com", 3)
	file_name = ""
	sentence_val = sent_val.get()
	if(internet_status == True):
		gtts_obj = gTTS(sentence_val,lang="en",slow=True)
		file_name = "sentence.mp3"
		gtts_obj.save(file_name)
		playsound(file_name)
	else:
		messagebox.showwarning("Alert","No internet")

# function to check internet connectivity
def checkInternetHttplib(url="www.geeksforgeeks.org", timeout=3):
    connection = httplib.HTTPConnection(url, timeout=timeout)
    try:
        # only header requested for fast operation
        connection.request("HEAD", "/")
        connection.close() # connection closed
        # print("Internet On")
        return True
    except Exception as exep:
        # print(exep)
        return False



# Define function to show frame
cap = cv2.VideoCapture(0)

def show_frames(img_label,transformed_roi):
	global cap

	# Get the latest frame and convert into Image
	cv2image = cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
	m,n = cv2image.shape[:2]
	cv2image = cv2.resize(cv2image,(n-50,m-50))

	trans_cv2img = cv2.resize(cv2image[120:370,40:290],(200,200)) # taking roi from cam input as an image
	
	# F1 = np.array([[-10,0,10],[0,0,0],[-10,0,10]])
	F1 = np.array([[0,0,0],[-15,0,15],[0,0,0]])
	trans_cv2img = cv2.cvtColor(trans_cv2img,cv2.COLOR_BGR2GRAY)
	trans_cv2img=cv2.filter2D(src=trans_cv2img,kernel=F1,ddepth=-1) # apply filter
	# trans_cv2img = np.where(trans_cv2img[:,0]<150,0,200)
	# print(trans_cv2img[0,0])

	# trans_cv2img = cv2.flip(trans_cv2img,1)
	img = Image.fromarray(cv2image)
	trans_img = Image.fromarray(trans_cv2img)

	imgtk = ImageTk.PhotoImage(image = img) # converting image to PhotoImage
	trans_imgtk = ImageTk.PhotoImage(image = trans_img)

	img_label.imgtk = imgtk
	img_label.configure(image=imgtk)

	transformed_roi.imgtk = trans_imgtk
	transformed_roi.configure(image=trans_imgtk)

	# Repeat after an interval to capture continiously
	img_label.after(10, show_frames,img_label,transformed_roi)

if __name__ == "__main__":

	win = Tk()
	win.title("Sign recogntion")
	win_width,win_height = 1280,700

	left_width = win_width*60//100
	right_width = win_width*40//100
	win.geometry(str(win_width) + "x" + str(win_height))

	# ------------- left panel containing camera and predictions ------------- 
	left = Frame(win,width=left_width,highlightbackground="black", highlightthickness=2)
	left.grid(row=0,column=0)

	head = Label(left,text="Sign Language to Text",font=("Arial 30"),highlightbackground="black", highlightthickness=2)
	head.width = 600
	head.height = 100
	head.grid(row=0,column=0,padx=50,pady=15,columnspan=2)

	# ------------- frame to show camera input and ROI ------------- 
	cam_frame = Frame(left,width=left_width,height=win_height-300,highlightbackground="black",highlightthickness=2)
	cam_frame.grid(row=1,column=0,columnspan=2)

	cam_inp = Label(cam_frame)
	cam_inp.grid(row=0,column=0)

	transformed_roi = Label(cam_frame)
	transformed_roi.grid(row=0,column=1)

	show_frames(cam_inp,transformed_roi)


	# ------------- predictions panel at the bottom ------------- 
	pred = Frame(left,width=left_width,highlightbackground="red",highlightthickness=2)
	pred.grid(row=2,column=0,pady=10)

	pred_font = ("Arial 20")
	charac = Label(pred,text="Character: ",font=pred_font)
	charac.grid(row=0,column=0,padx=20,pady=5)

	charac_val = StringVar()
	charac_val.set("A")
	charac_entry = Label(pred,textvariable=charac_val,font=pred_font)
	charac_entry.grid(row=0,column=1,padx=20,pady=5)

	word = Label(pred,text="Word: ",font=pred_font)
	word.grid(row=1,column=0,padx=20,pady=5)

	word_val = StringVar()
	word_val.set("APPLE")
	word_entry = Label(pred,textvariable=word_val,font=pred_font)
	word_entry.grid(row=1,column=1,padx=20,pady=5)

	sent = Label(pred,text="Sentence: ",font=pred_font)
	sent.grid(row=2,column=0,padx=20,pady=5)

	sent_val = StringVar()
	sent_val.set("A FOR APPLE")
	sent_entry = Label(pred,textvariable=sent_val,font=pred_font)
	sent_entry.grid(row=2,column=1,padx=20,pady=5)


	# button to play generated sentence

	sentence_val = sent_val.get()
	# internet_status = checkInternetHttplib("www.google.com", 3)
	# file_name = ""
	# if(internet_status == True):
	# 	gtts_obj = gTTS(sentence_val,lang="en",slow=True)
	# 	file_name = "sentence.mp3"
	# 	gtts_obj.save(file_name)
	

	play_btn = Button(left,text="Play",font=pred_font,command=lambda:play())
	play_btn.grid(row=2,column=1)

	print(sentence_val)



	# ------------- right panel containing image with signs ------------- 
	right = Frame(win,width=right_width,height=win_height,highlightbackground="black",highlightthickness=2)
	right.grid(row=0,column=1,pady=0)


	img = ImageTk.PhotoImage(Image.open("/home/user/Documents/programming/Py/Projects/Sign-detection/Ours/signs_resized.png"))
	img_label = Label(right,image=img)
	img_label.grid(row=0,column=0,padx=2,pady=30,rowspan=2)

	caption = Label(right,text="Signs in American sign language",font=("Arial 20"))
	caption.grid(row=2,column=0)


	win.mainloop()