import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO

class ImageEdit1:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Éditeur d'image 1")
        self.modified_image = None
        self.original = None
        self.tk_image = None
        self.lien_image = "https://images.unsplash.com/photo-1490323522928-9bfab6309902?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        self.create_widgets()

    def create_widgets(self):
        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(padx=10, pady=10)

        tk.Label(self.controls_frame, text="Longeur:").grid(row=0, column=0)
        tk.Label(self.controls_frame, text="Largeur:").grid(row=0, column=1)
        tk.Label(self.controls_frame, text="Haut:").grid(row=2, column=0)
        tk.Label(self.controls_frame, text="Bas:").grid(row=2, column=1)
        tk.Label(self.controls_frame, text="Gauche:").grid(row=2, column=2)
        tk.Label(self.controls_frame, text="Droite:").grid(row=2, column=3)
        
        redimensionner_button = tk.Button(self.controls_frame, text="Redimensionner", command=self.redimensionner)
        recadrer_button = tk.Button(self.controls_frame, text="Recadrer", command=self.recadrer)

        self.height_entry = tk.Entry(self.controls_frame)
        self.length_entry = tk.Entry(self.controls_frame)
        self.height_entry.grid(row=1, column=0, pady=5)
        self.length_entry.grid(row=1, column=1, pady=5)
        redimensionner_button.grid(row=1, column=2, pady=5)
        
        self.haut_entry = tk.Entry(self.controls_frame)
        self.bas_entry = tk.Entry(self.controls_frame)
        self.gauche_entry = tk.Entry(self.controls_frame)
        self.droite_entry = tk.Entry(self.controls_frame)
        self.haut_entry.grid(row=3, column=0, pady=5)
        self.bas_entry.grid(row=3, column=1, pady=5)
        self.gauche_entry.grid(row=3, column=2, pady=5)
        self.droite_entry.grid(row=3, column=3, pady=5)
        recadrer_button.grid(row=3, column=4, pady=5)
        
        telecharger_button = tk.Button(self.controls_frame, text="Télécharger et afficher l'image", command=self.telecharger_image)
        telecharger_button.grid(row=4, column=0)


        self.image_frame = tk.Frame(self.root, width=50, height=50)
        self.image_frame.pack(padx=10, pady=10)
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(fill="both", expand=True)

    def telecharger_image(self):
        try:
            response = requests.get(self.lien_image, allow_redirects=True)
            if response.status_code != 200:
                tk.messagebox.showerror("Erreur", f"Problème lors du téléchargement de l'image: {response.status_code} - {response.content}")
            self.image_telechargee = Image.open(BytesIO(response.content))
            self.original = self.image_telechargee.copy().resize((600, 400))
            self.display_image(self.original)
        except Exception as e:
            tk.messagebox.showerror("Erreur", f"Problème lors du chargement de l'image: {str(e)}")

    def display_image(self, image):
        self.tk_image = ImageTk.PhotoImage(image=image, master=self.root)
        self.image_label.config(image=self.tk_image)
        self.modified_image = image

    def redimensionner(self):
        try:
            height = int(self.height_entry.get())
            length = int(self.length_entry.get())
            image_transformee = self.modified_image.resize((height, length))
            self.display_image(image_transformee)
        except Exception as e:
            if type(e) == AttributeError and "NoneType" in str(e):
                tk.messagebox.showerror("Erreur", "Il faut télécharger l'image pour pouvoir la modifier")
            elif type(e) == ValueError:
                tk.messagebox.showerror("Erreur", "Valeurs non conformes. Merci de donner des valeur numériques pour redimensionner.")
            else:
                tk.messagebox.showerror("Erreur", f"Exception lors du redimensionnement: {str(e)}")
    
    def recadrer(self):
        try:
            haut = int(self.haut_entry.get())
            bas = int(self.bas_entry.get())
            gauche = int(self.gauche_entry.get())
            droite = int(self.droite_entry.get())
            if bas < haut or droite < gauche:
                raise ValueError
            box = (gauche, haut, droite, bas)
            image_transformee = self.modified_image.crop(box)
            self.display_image(image_transformee)
            
        except Exception as e:
            if type(e) == AttributeError and "NoneType" in str(e):
                tk.messagebox.showerror("Erreur", "Il faut télécharger l'image pour pouvoir la modifier")
            elif type(e) == ValueError:
                tk.messagebox.showerror("Erreur", f"Valeurs non conformes. Merci de donner des valeur numériques pour rogner avec bas > haut et droite > gauche.")
            else:
                tk.messagebox.showerror("Erreur", f"Exception lors du recadrage: {str(e)}")


    def run(self):
        self.root.mainloop()