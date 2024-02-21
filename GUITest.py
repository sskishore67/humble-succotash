import os

from customtkinter import *
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

from Detect import CheckGlaucoma, PreprocessImage

app = CTk()
app.geometry("1000x500")


def removeAll():
    for items in app.winfo_children():
        items.destroy()


def reset():
    removeAll()
    openBtn = CTkButton(app, text="Open", command=opeimgmg)
    openBtn.place(relx=0.5, rely=0.5, anchor=CENTER)
    app.grid_columnconfigure(1, weight=0)


photo_img = None
photo_ni = None


def opeimgmg():
    global photo_img
    inputImgPath = filedialog.askopenfilename(
        filetypes=[("JPEG Images", "*.jpg")])
    if inputImgPath:
        removeAll()
        image = Image.open(inputImgPath)
        canvas_width = 500
        canvas_height = 500
        image_width, image_height = image.size
        aspect_ratio = min(canvas_width / image_width,
                           canvas_height / image_height)
        new_width = int(image_width * aspect_ratio)
        new_height = int(image_height * aspect_ratio)
        resized_image = image.resize((new_width, new_height))
        photo_img = ImageTk.PhotoImage(image=resized_image)

        frame_l1 = CTkFrame(app, height=30)
        frame_l1.grid(column=0, row=0, sticky=NSEW)
        l1 = CTkLabel(frame_l1, text=os.path.basename(
            image.filename))  # type: ignore
        l1.place(relx=0.5, rely=0.5, anchor=CENTER)

        frame_img = CTkFrame(app)
        frame_img.grid(column=0, row=1, sticky=NSEW)

        canvas_img = Canvas(frame_img, width=canvas_width, height=new_height)
        canvas_img.place(relx=0.5, rely=0.5, anchor=CENTER)
        img_id_img = canvas_img.create_image(
            canvas_width/2, canvas_height/2, image=photo_img, anchor=CENTER)

        # Scale the image to fit the canvas
        canvas_img.config(scrollregion=canvas_img.bbox(ALL))

        app.grid_columnconfigure(0, weight=1)
        app.grid_rowconfigure(0, weight=0)
        app.grid_rowconfigure(1, weight=1)

        btnCTkFrame = CTkFrame(app, height=150)
        btnCTkFrame.grid(column=0, columnspan=2, row=2, sticky=NSEW)
        processBtn = CTkButton(btnCTkFrame, text="Check",
                               command=lambda: process(inputImgPath, processBtn))
        processBtn.place(relx=0.5, rely=0.5, anchor=CENTER)


def process(inputImgPath, processBtn):
    processBtn.configure(text="normalizeing image",state=DISABLED)

    # Preprocess the image
    image = PreprocessImage(inputImgPath,64)
    addProcessedImg(image)


    processBtn.configure(text="Checking",state=DISABLED)
    result,color= CheckGlaucoma(image).split(' ') # type: ignore



    processBtn.configure(text="check again",state= NORMAL)

    resultFrame=CTkFrame(app,width=300,fg_color="black")
    resultFrame.grid(row=2, column=1, sticky='nse')
    

    resultLable=CTkButton(resultFrame,text=str(result),state=DISABLED,fg_color=color)
    resultLable.place(relx=0.5,rely=.4, anchor=CENTER)

    newButton=CTkButton(resultFrame,text="New",command=reset)
    newButton.place(relx=0.5, rely=0.6, anchor=CENTER)


def addProcessedImg(image):
    global photo_ni

    canvas_width = 500
    canvas_height = 500
    image_width, image_height = image.size
    aspect_ratio = min(canvas_width / image_width,
                       canvas_height / image_height)
    new_width = int(image_width * aspect_ratio)
    new_height = int(image_height * aspect_ratio)
    resized_image = image.resize((new_width, new_height))

    photo_ni = ImageTk.PhotoImage(image=resized_image)

    frame_l2 = CTkFrame(app, height=30)
    frame_l2.grid(column=1, row=0, sticky=NSEW)
    l2 = CTkLabel(frame_l2, text="normalized image")  # type: ignore
    l2.place(relx=0.5, rely=0.5, anchor=CENTER)

    frame_ni = CTkFrame(app)
    frame_ni.grid(column=1, row=1, sticky=NSEW)

    canvas_ni = Canvas(frame_ni, width=canvas_width, height=new_height)
    canvas_ni.place(relx=0.5, rely=0.5, anchor=CENTER)

    img_id_ni = canvas_ni.create_image(
        canvas_width/2, canvas_height/2, image=photo_ni, anchor=CENTER)

    # Scale the image to fit the canvas
    canvas_ni.config(scrollregion=canvas_ni.bbox(ALL))

    app.grid_columnconfigure(1, weight=1)


reset()
app.mainloop()
