import tkinter 
from tkinter import filedialog 
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import json 
import sqlite3
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



def cliquer():
   
   site = "https://pixees.fr/informatiquelycee/donnees_a2.html#:~:text=Avec%20une%20simple%20url%2C%20le,sous%20forme%20de%20donn%C3%A9es%20JSON."
   reponse = requests.get(site)
   if reponse.status_code == 200:
        donnees = reponse.json()
        print("Données téléchargées avec succès:", donnees)
        label1.config(text="Données téléchargées avec succès!")
   else:
       
        print("Échec du téléchargement des données. Code d'état:", reponse.status_code)
        label1.config(text="Échec du téléchargement des données. Code d'état:" + str(reponse.status_code))

def retourner(frame):
    frame.grid_forget()
    fenetre_principale.grid()
    

###############bouton qui affiche le nombre des paragraphe 
class paragraphe(tkinter.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, text="af", command=self.afficher_informations, **kwargs)

        self.var_numero = tkinter.StringVar()
        self.var_numero.set("1")

        self.menu_deroulant = tkinter.OptionMenu(master, self.var_numero, *range(1, 21))
        self.menu_deroulant.bind("<Button-1>", self.on_dropdown_click)
        
        self.label_choix = tkinter.Label(master, text="Choisissez le numéro du paragraphe:")
        self.label_choix.grid(row=0, column=0, padx=10, pady=10)
        self.menu_deroulant.grid(row=0, column=1, padx=10, pady=10)


    def compter_mots(self, paragraphe):
        mots = paragraphe.split()
        return len(mots)

    def arrondir_a_dizaine(self, nombre):
        return round(nombre, -1)

    def afficher_informations(self):
        selected_numero = self.var_numero.get()
        paragraphe = f"Contenu du paragraphe {selected_numero} ici..."  # Remplacez cela par le vrai contenu du paragraphe
        nombre_mots = self.compter_mots(paragraphe)
        nombre_mots_arrondi = self.arrondir_a_dizaine(nombre_mots)

        # Affichage des informations
        message = f"Paragraphe {selected_numero} :\nNombre de mots : {nombre_mots}\nNombre de mots arrondi à la dizaine : {nombre_mots_arrondi}"
        messagebox.showinfo("Informations", message)

    def on_dropdown_click(self, event):
        self.menu_deroulant["menu"].post(event.x_root, event.y_root)

class graphique(tkinter.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, text="Générer Graphique", command=self.generer_graphique, **kwargs)

        self.var_choix = tkinter.StringVar()
        self.var_choix.set("selon les mots")

        # Libellé avant le bouton
        self.label_avant_bouton = tkinter.Label(master, text="Cliquez sur le bouton pour générer des graphique:")
        self.label_avant_bouton.grid(row=3, column=0, padx=10, pady=10)

        # Menu déroulant pour choisir entre "selon les mots" et "selon les caractères"
        self.menu_deroulant_choix = tkinter.OptionMenu(master, self.var_choix, "selon les mots", "selon les caractères")
        self.menu_deroulant_choix.grid(row=3, column=1, padx=10, pady=10)
    def generer_graphique(self):
        choix = self.var_choix.get()
        # Ajoutez votre code de génération de graphiques ici
        # Par exemple, un simple message pour montrer que la méthode est appelée
        print(f"Génération de graphique selon : {choix}")

class photo1(tkinter.Button):
    def __init__(self,master=None, image_path=None, **kwargs):
        super().__init__(master, text="Télécharger la photo numéro 1", command=self.affichier_photo, **kwargs)
    
        self.label_image = tkinter.Label(master)
        self.label_image.grid(row=3, column=0, pady=20)
        self.image_path = image_path

           
    def affichier_photo(self):
        try:
            # Ouvrir l'image avec Pillow
            image = Image.open(self.image_path)

            # Redimensionner l'image
            nouvelle_taille = (100, 100)
            image_modifié= image.resize(nouvelle_taille)

            # Convertir l'image pour Tkinter
            photo = ImageTk.PhotoImage(image_modifié)

            # Mettre à jour l'étiquette avec la nouvelle image
            self.label_image.configure(image=photo)
            self.label_image.image = photo  # Gardez une référence pour éviter la suppression par le ramasse-miettes
            self.label_image.place(relx=0.9, rely=0.9, anchor="center")
        except Exception as e:
            print(f"Erreur lors de l'affichage de l'image : {e}")
        
    #def recadrer l'image : 1) automatiquement 2) manuellement 
        
                
    
        
#def afficher_graphique():
#def effacer():
#def agregation():


    




#creation de la fenetre 

app = tkinter.Tk()

label1 = tkinter.Label(app)



largeur_fenetre = 900
hauteur_fenetre = 700

largeur_app= app.winfo_screenwidth()
hauteur_app = app.winfo_screenheight()

x = (largeur_app- 900) // 2
y = (hauteur_app - 750) // 2
app.geometry("900x700+300+50")

app.resizable(width=True,height=True)
app.title('My World Be Like')
app.configure(background='#2C3E50')
app.attributes("-alpha", 0.95)
app.iconbitmap(r"C:\Users\MSI\Desktop\projet python avancé\music.ico")
chemin_image = (r"C:\Users\MSI\Desktop\nexus.jpg")








#création des bouttons
fenetre_principale= tkinter.Frame(app, bg="#2C3E50")

#partie 1
fenetre_partie1 = tkinter.Frame(app, bg='#2C3E50')

bouton_tele = tkinter.Button(fenetre_partie1, text="telecharger des données", command=cliquer )
bouton_partie1 = tkinter.Button(fenetre_principale, text='PARTIE 1', command=lambda: fenetre_partie1.grid())
bouton_retour1 = tkinter.Button(fenetre_partie1, text='retourner a la fenetre principale', command=lambda: retourner(fenetre_partie1))
#bouton_afficher_graphique = tkinter.Button(fenetre_partie1, text="Afficher Graphique", command=afficher_graphique)
#bouton_effacer = tkinter.Button(fenetre_partie1, text="Supprimer les données", command=effacer)
#bouton avec down menu : bouton_agregation = tkinter.Button(fenetre_partie1, text="", command=agregation)





#partie 2 
fenetre_partie2 = tkinter.Frame(app , bg='#2C3E50')
bouton_partie2 = tkinter.Button(fenetre_principale, text='PARTIE 2', command=lambda: fenetre_partie2.grid())
bouton_retour2 = tkinter.Button(fenetre_partie2, text='retourner a la fenetre principale', command=lambda: retourner(fenetre_partie2))
bouton_paragraphe = paragraphe(fenetre_partie2)
bouton_graphique = graphique(fenetre_partie2)
bouton_photo = photo1(fenetre_partie2, image_path=chemin_image)
#bouton world









#placement des widget 





#les boutons du partie 1
bouton_partie1.grid(row=1, column=0, pady=15, padx=10)
bouton_tele.grid(row=0, column=0, pady=15, padx=10)
bouton_retour1.grid(row=1, column=0, pady=15, padx=10)
#bouton_afficher_graphique.grid(row=2, column=0, pady=15, padx=10)
#bouton_effacer.grid(row=3, column=0, pady=15, padx=10)
#bouton_agregation.grid(row=4, column=0, pady=15, padx=10)






#les boutons du partie 2


bouton_paragraphe.grid(row=1, column=0, padx=10, pady=10)
bouton_partie2.grid(row=2, column=0, pady=15, padx=10)
bouton_graphique.grid(row=4, column=0, padx=10, pady=10)
bouton_photo.grid(row=5, column=0, pady=20)
bouton_retour2.grid(row=6, column=0, pady=20)



fenetre_principale.grid()



app.mainloop() 























