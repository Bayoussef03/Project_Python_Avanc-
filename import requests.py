import tkinter 
from tkinter import filedialog
from PIL import Image, ImageTk
import requests
import json 
import sqlite3



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


def importer():
    ouvrir_fichier= filedialog.askopenfilenames(title="ouvrir un ou des fichiers", defaultextension=".json" 
                                                , filetypes=[("Fichier json", ".json"),("Fichier PDF",".pdf"),
                                                             ("Fichier CSV", ".csv"),("Fichier Texte", ".txt" ), ("tout les Fichiers",".*")], 
                                                initialdir=r'C:\Users\MSI\Desktop\Ynov matiere\python avancé\projet python avancé')
    
  
# Fonction pour effacer le contenu de la table dans la base de données SQLite

def effacer():
    try:
        # Établir une connexion à la base de données
        connexion = sqlite3.connect(nom_base_de_donnees)

        # Créer un objet curseur pour exécuter des requêtes SQL
        curseur = connexion.cursor()

        # Nom de la table que vous souhaitez effacer (remplacez 'votre_table' par le nom réel de votre table)
        nom_table = 'votre_table'

        # Exécuter la requête SQL pour effacer le contenu de la table
        curseur.execute(f'DELETE FROM {nom_table};')

        # Valider la transaction
        connexion.commit()

        # Fermer le curseur et la connexion
        curseur.close()
        connexion.close()

        # Afficher un message de succès (vous pouvez ajuster cela selon vos besoins)
        print("Contenu de la table effacé avec succès.")

    except Exception as e:
        # En cas d'erreur, afficher un message d'erreur (vous pouvez ajuster cela selon vos besoins)
        print(f"Erreur lors de l'effacement de la table : {str(e)}")

# Créer une fenêtre Tkinter
app = tkinter.Tk()

bouton_effacer = tkinter.Button(app, text="Effacer la dataset", command=effacer)

bouton_effacer.pack()
     


#creation de la fenetre 

app = tkinter.Tk()

label1 = tkinter.Label(app)


label1.grid(pady=15)

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







bouton_importer = tkinter.Button(app, text='importer un fichier', command=importer)
bouton_tele = tkinter.Button(app, text="telecharger des données", command=cliquer )
bouton_effacer = tkinter.Button(app, text="effacer la dataset", command=effacer)






app.attributes("-alpha", 0.95)
app.iconbitmap(r"C:\Users\MSI\Desktop\Ynov matiere\python avancé\projet python avancé\music.ico")

left_frame = tkinter.Frame(app, width=200, height=400, bg='grey')
left_frame.grid(row=0, column=0, padx=10, pady=5)

right_frame = tkinter.Frame(app, width=650, height=400, bg='grey')
right_frame.grid(row=0, column=1, padx=10, pady=5)

# Create frames and labels in left_frame
tkinter.Label(left_frame, text="Original Image").grid(row=0, column=0, padx=5, pady=5)

# Create tool bar frame
tool_bar = tkinter.Frame(left_frame, width=180, height=185)
tool_bar.grid(row=2, column=0, padx=5, pady=5)

# Example labels that serve as placeholders for other widgets
tkinter.Label(tool_bar, text="Tools", relief=tkinter.RAISED).grid(row=0, column=0, padx=5, pady=3, ipadx=10)  # ipadx is padding inside the Label widget
tkinter.Label(tool_bar, text="Filters", relief=tkinter.RAISED).grid(row=0, column=1, padx=5, pady=3, ipadx=10)

# Example labels that could be displayed under the "Tool" menu
tkinter.Label(tool_bar, text="Select").grid(row=1, column=0, padx=5, pady=5)
tkinter.Label(tool_bar, text="Crop").grid(row=2, column=0, padx=5, pady=5)
tkinter.Label(tool_bar, text="Rotate & Flip").grid(row=3, column=0, padx=5, pady=5)
tkinter.Label(tool_bar, text="Resize").grid(row=4, column=0, padx=5, pady=5)
tkinter.Label(tool_bar, text="Exposure").grid(row=5, column=0, padx=5, pady=5)

#placement des widget 
label1.grid(row=0, column=0, pady=15, padx=10)
bouton_importer.grid(row=3, column=1, pady=15, padx=10)
bouton_tele.grid(row=1, column=1, pady=15, padx=10)
bouton_effacer.grid(row=2, column=1, padx=10, pady=15)

app.mainloop() 























