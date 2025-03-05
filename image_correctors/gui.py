from tkinter import Tk, Button, Label, filedialog, Scale, HORIZONTAL
import cv2
from PIL import Image, ImageTk
import intensities_transformation

#Global Variables
original_img = None  
img = None  
img_label = None  

def load_image():
    global original_img, img, img_label
    file_path = filedialog.askopenfilename()
    if file_path:
        img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)  # Convert to grayscale
        original_img = img.copy()  
        update_display()

#Refresh the image display capire che fa
def update_display():
    global img_label
    img_tk = convert_to_tk(img) 
    img_label.config(image=img_tk) 
    img_label.image = img_tk  

def convert_to_tk(img):
    img_pil = Image.fromarray(img)
    return ImageTk.PhotoImage(img_pil)

#Apply an image transformation with an optional parameter
def apply_transformation(transformation, value=None):
    global img
    if img is not None:
        img = transformation(img, value) if value is not None else transformation(img)
        update_display()

#Reset the image to its original state.
def reset_image():
    global img
    img = original_img.copy()
    update_display()

#Save the modified image
def save_image():
    if img is not None:
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if file_path:
            img_pil = Image.fromarray(img)
            img_pil.save(file_path)

def start_gui():
    global img_label

    root = Tk()
    root.title("Image Processing Tool")

    #Load, Reset, Save Buttons
    btn_load = Button(root, text="Load Image", command=load_image)
    btn_reset = Button(root, text="Reset", command=reset_image)
    btn_save = Button(root, text="Save Image", command=save_image)

    #Transformation Buttons
    btn_log = Button(root, text="Log Transform", command=lambda: apply_transformation(intensities_transformation.bijective_log_transform))
    btn_exp = Button(root, text="Exponential Transform", command=lambda: apply_transformation(intensities_transformation.bijective_exp_transform))
    btn_gamma = Button(root, text="Gamma Correction", command=lambda: apply_transformation(intensities_transformation.gamma_correction, 0.5))
    btn_bijective_contrast = Button(root, text="Bijective Contrast", command=lambda: apply_transformation(intensities_transformation.bijective_contrast_stretching, 3))
    btn_nonbijective_contrast = Button(root, text="Non-Bijective Contrast", command=lambda: apply_transformation(intensities_transformation.non_bijective_contrast_stretching, 3))

    #Sliders for gamma and contrast adjustments
    slider_gamma = Scale(root, from_=0.0, to=25.0, resolution=0.01, orient=HORIZONTAL, label="Gamma Correction",
                         command=lambda value: apply_transformation(intensities_transformation.gamma_correction, float(value)))

    slider_contrast = Scale(root, from_=0.0, to=1, resolution=0.01, orient=HORIZONTAL, label="Contrast Stretching",
                            command=lambda value: apply_transformation(intensities_transformation.bijective_contrast_stretching, int(value)))

    #Image display label
    img_label = Label(root)

    #UI Layout
    btn_load.pack()
    btn_reset.pack()
    btn_save.pack()
    btn_log.pack()
    btn_exp.pack()
    btn_gamma.pack()
    btn_bijective_contrast.pack()
    btn_nonbijective_contrast.pack()
    slider_gamma.pack()
    slider_contrast.pack()
    img_label.pack()

    root.mainloop()
