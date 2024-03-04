import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import types

class ImageEdit2:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Éditeur d'image 2")
        self.image_modifiee = None
        self.original = None
        self.abs_dir = os.path.dirname(os.path.abspath(__file__))
        self.tk_image = None
        self.nb_image_path = f"{self.abs_dir}/resources/nfl_logo.jpg"
        self.nb_image = Image.open(self.nb_image_path)
        self.enregisrement_path = f"{self.abs_dir}/resultat/photon1.jpg"
        self.create_widgets()

    def create_widgets(self):
        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(padx=10, pady=10)
        
        tk.Label(self.controls_frame, text="Angle:").grid(row=0, column=0)
        apply_button = tk.Button(self.controls_frame, text="Appliquer", command=self.apply_changes)
        apply_button.grid(row=0, column=2, pady=10)
        self.angle_entry = tk.Entry(self.controls_frame)
        self.angle_entry.grid(row=0, column=1, pady=5)

        charger_button = tk.Button(self.controls_frame, text="Charger l'image local", command=self.load_image)
        self.enregistrer_button = tk.Button(self.controls_frame, text="Enregistrer l'image", command=self.download_image, state=tk.DISABLED)
        charger_button.grid(row=3, column=0)
        self.enregistrer_button.grid(row=3, column=2)


        self.image_frame = tk.Frame(self.root, width=50, height=50)
        self.image_frame.pack(padx=10, pady=10)
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(fill="both", expand=True)

        self.image_frame.bind("<Configure>", self.on_image_frame_resize)

    def on_image_frame_resize(self, event):
        
        if event.width > 400:
            self.image_frame.config(width=200)
        if event.height > 400:
            self.image_frame.config(height=200)

    def load_image(self):
        try:
            self.original = self.nb_image.copy().resize((200, 200))
            self.display_image(self.original)
        except Exception as e:
            tk.messagebox.showerror("Erreur", f"Problème lors du chargement de l'image: {str(e)}")

    def display_image(self, image):
        self.tk_image = ImageTk.PhotoImage(image=image, master=self.root)
        self.image_label.config(image=self.tk_image)
        self.image_modifiee = image

    def apply_changes(self):
        try:
            angle = float(self.angle_entry.get())
            image_transformee = self.image_modifiee.rotate(angle, expand=True)
            self.display_image(image_transformee)
            self.enregistrer_button.config(state=tk.NORMAL)
        except Exception as e:
            if type(e) == AttributeError and "NoneType" in str(e):
                tk.messagebox.showerror("Erreur", "Il faut charger l'image pour pouvoir la modifier")
            elif type(e) == ValueError:
                tk.messagebox.showerror("Erreur", "Valeur non conforme. Merci de donner une valeur numérique l'angle.")
            else:
                tk.messagebox.showerror("Erreur", f"Exception lors de la rotation: {str(e)}")
                
    def download_image(self):
        if self.image_modifiee:
            try:
                self.image_modifiee.save(self.enregisrement_path)
                tk.messagebox.showinfo("Succès", f"Image enregistrée avec succès sous {self.enregisrement_path}")
            except Exception as e:
                tk.messagebox.showerror("Erreur", f"Erreur lors de l'enregistrement de l'image : {str(e)}")

    def run(self):
        self.root.mainloop()