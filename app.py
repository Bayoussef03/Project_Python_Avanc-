import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import requests

from image_edit1 import ImageEdit1
from image_edit2 import ImageEdit2
from donnees import ExtDonnees
from word import Gen_word
from sqllite_handler import SQLiteHandler

class NFLApp:
    
    def __init__(self, root):
        # design de l'app
        self.app_height= 1100
        self.app_width = 900
        self.abs_dir = os.path.dirname(os.path.abspath(__file__))
        home_img = Image.open(f"{self.abs_dir}/resources/home-icon.png")
        home_img = home_img.resize((20, 20))
        self.home_icon = ImageTk.PhotoImage(home_img)
        self.app_logo = ImageTk.PhotoImage(Image.open(f"{self.abs_dir}/resources/app_logo.ico"))
        root.iconphoto(True, self.app_logo)
        
        self.path_livre = f"{self.abs_dir}/resultat/livre.txt"

        mm_img_path = os.path.join(self.abs_dir, "resources/main_menu_background.png")  
        mm_background_img = Image.open(mm_img_path)
        mm_background_img = mm_background_img.resize((self.app_height, self.app_width))
        self.mm_background_photo = ImageTk.PhotoImage(mm_background_img)
        self.background_canvas = tk.Canvas(root, width=self.app_width, height=self.app_height)
        self.background_canvas.pack(fill="both", expand=True)
        self.background_canvas.create_image(0, 0, anchor=tk.NW, image=self.mm_background_photo)
        self.background_canvas.bind("<Configure>", self.update_canvas_size)


        # config de base
        self.root = root
        self.root.title("NFL par Youssef Barred")
        self.root.geometry(f"{self.app_height}x{self.app_width}")
        
        # la partie historisation
        self.messages = []
        self.message_label = tk.Label(self.background_canvas, text='', bd=1, relief=tk.SUNKEN, anchor=tk.W, background="#FFBA00")
        self.message_label.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        self.message_label.lift()
        
        # burger
        self.burger_button = tk.Button(self.background_canvas, text="☰", command=self.toggle_main_menu, background="white", highlightthickness=0)
        self.burger_button.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=10)

        self.main_menu_frame = tk.Frame(self.background_canvas, width=200, height=400, background="white", highlightthickness=0, padx=10, pady=10)
        self.button_main_menu = tk.Button(self.main_menu_frame, text="Menu principal", command=self.main_menu, background="white", height=2, width=10, relief=tk.RAISED)
        self.button_part1 = tk.Button(self.main_menu_frame, text="Partie 1", command=self.part1_menu, background="white", height=2, width=10, relief=tk.RAISED)
        self.button_part2 = tk.Button(self.main_menu_frame, text="Partie 2", command=self.part2_menu, background="white", height=2, width=10, relief=tk.RAISED)


        self.button_main_menu.pack(side=tk.TOP)
        self.button_part1.pack(side=tk.TOP)
        self.button_part2.pack(side=tk.TOP)
        
        self.sql_handler=SQLiteHandler(f"{self.abs_dir}/resultat/ma_base.db")

       
    def update_canvas_size(self, event):

        new_width = event.width
        new_height = event.height
        self.app_width = new_width
        self.app_height = new_height
        mm_background_img = Image.open(os.path.join(self.abs_dir, "resources/main_menu_background.png"))
        mm_background_img = mm_background_img.resize((new_width, new_height))
        self.mm_background_photo = ImageTk.PhotoImage(mm_background_img)
        self.background_canvas.config(width=new_width, height=new_height)
        self.background_canvas.itemconfig(1, image=self.mm_background_photo)

    def toggle_main_menu(self):
        if self.main_menu_frame.winfo_ismapped():
            self.main_menu_frame.pack_forget()
        else:
            self.main_menu_frame.pack(side=tk.LEFT, anchor=tk.NW)
            
    def main_menu(self):
        self.clear_widgets()  
        self.main_menu_frame.pack_forget()  
        self.ajouter_message("Menu prinicpal")

    def part1_menu(self):
        self.clear_widgets()
        self.main_menu_frame.pack_forget()
        self.ajouter_message("Accès à la partie 1")
        
        part1 = tk.Frame(self.root, width=900, height=600)
        part1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
                
        button_telecharger_db = tk.Button(part1, text="Télécharger et crééer la BD", command=self.telecharger_db, background="white", height=2, width=20, relief=tk.RAISED)
        button_delete_data = tk.Button(part1, text="Supprimer les données", command=self.delete_data, background="white", height=2, width=20, relief=tk.RAISED)
        button_chart_salaire = tk.Button(part1, text="Graphique salaire des joueurs", command=self.chart_salaire, background="white", height=2, width=20, relief=tk.RAISED)
        button_graphique_taille = tk.Button(part1, text="Graphique tailles des joueurs", command=self.graphique_taille, background="white", height=2, width=20, relief=tk.RAISED)
        button_aggreagation_donnees = tk.Button(part1, text="Aggrégation des données", command=self.aggregation_des_donnees, background="white", height=2, width=20, relief=tk.RAISED)

        button_telecharger_db.pack(side=tk.TOP)
        button_delete_data.pack(side=tk.TOP)
        button_chart_salaire.pack(side=tk.TOP)
        button_graphique_taille.pack(side=tk.TOP)
        button_aggreagation_donnees.pack(side=tk.TOP)

    def part2_menu(self):
        self.clear_widgets()
        self.main_menu_frame.pack_forget()
        self.ajouter_message("Accès à la partie 2")
        
        # creation et population menu partie 2
        part2 = tk.Frame(self.root, background="white", width=1000, height=600)
        part2.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        button_telecharger_livre = tk.Button(part2, text="Télécharger le livre", command=self.telecharger_livre, background="white", height=2, width=20, relief=tk.RAISED)
        button_extraire_donnees = tk.Button(part2, text="Information du livre (calcul)", command=self.extraire_donnees, background="white", height=2, width=20, relief=tk.RAISED)
        button_telecharger_image = tk.Button(part2, text="Télécharger et éditer une image", command=self.telecharger_image, background="white", height=2, width=20, relief=tk.RAISED)
        button_edit_image = tk.Button(part2, text="Charger et editer l'image locale", command=self.edit_image, background="white", height=2, width=20, relief=tk.RAISED)
        button_generer_word = tk.Button(part2, text="Création du fichier Word", command=self.generer_word, background="white", height=2, width=20, relief=tk.RAISED)

        # Pack buttons horizontally and center them
        button_telecharger_livre.pack(side=tk.TOP)
        button_extraire_donnees.pack(side=tk.TOP)
        button_telecharger_image.pack(side=tk.TOP)
        button_edit_image.pack(side=tk.TOP)
        button_generer_word.pack(side=tk.TOP)

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            if widget not in [self.message_label, self.background_canvas, self.burger_button]:
                widget.destroy()

    def ajouter_message(self, message):
        self.messages.append(message)
        self.afficher_messages()
        
    def afficher_messages(self):
        displayed_message = "\n".join(self.messages[-5:])
        self.message_label.config(text=displayed_message)
        
    def telecharger_livre(self):
        livre_lien = 'https://www.gutenberg.org/cache/epub/39743/pg39743.txt'
        livre_request = requests.get(livre_lien)
        if os.path.exists(self.path_livre):
            response = messagebox.askyesno("fichier existant", f"Le livre est déjà téléchargé, voulez vous l'écrasser ?")
        
            if response:
                os.remove(self.path_livre)
                with open(self.path_livre, 'wb') as file:
                    file.write(livre_request.content)    
                self.ajouter_message("Livre téléchargé.")
            else:
                self.ajouter_message("Livre existant convervé.")
        else:
            with open(self.path_livre, 'wb') as file:
                    file.write(livre_request.content)    
                    self.ajouter_message("Livre téléchargé.")
            
    def extraire_donnees(self):
        self.ajouter_message("Extraction et affichage des infos de l'auteur...")
        ExtDonnees(self.path_livre).extraire_donnees()

    def telecharger_image(self):
        self.ajouter_message("Téléchargement de l'image...")
        ImageEdit1()

    def edit_image(self):
        self.ajouter_message("Menu édition de l'image ouvert")
        ImageEdit2()

    def generer_word(self):
        self.ajouter_message("Création du document Word...")
        try:
            word = Gen_word()
            word.generate()
            tk.messagebox.showinfo("Succès", f"Fichier Word généré avec succès et enregistré sous sous {word.path_rapport}")
        except Exception as e:
            tk.messagebox.showerror("Erreur", f"Problème lors de la génération du fichier Word: {str(e)}")

    def telecharger_db(self):
        self.ajouter_message("Téléchargement des données et enregistrement de la BD...")
        message = self.sql_handler.create_and_save_database()
        if message == "La base de données existe déjà!":
            response = messagebox.askyesno("BD existante", f"La base de données existe déjà, voulez vous l'écrasser ?")

            if response:
                self.sql_handler.delete_database()
                message = self.sql_handler.create_and_save_database()
                tk.messagebox.showinfo("Info", message)
            else:
                tk.messagebox.showinfo("Info", "BD existante conservée")


    def delete_data(self):
        self.ajouter_message("Suppression des données...")
        message = self.sql_handler.delete_database()
        tk.messagebox.showinfo("Info", message)
        
    def chart_salaire(self):
        self.ajouter_message("Calcul et affichage chart position...")
        try:
            self.sql_handler.display_salary_chart()
        except Exception as e:
            tk.messagebox.showerror("Erreur", f"Problème lors de la génération du graph position: {str(e)}")
            
    def graphique_taille(self):
        self.ajouter_message("Calcul et affichage graphique des tailles...")
        try:
            self.sql_handler.player_by_height_chat()
        except Exception as e:
            tk.messagebox.showerror("Erreur", f"Problème lors de la génération du graph taille: {str(e)}")
        
    def aggregation_des_donnees(self):
        self.ajouter_message("Calcul et affichage d'aggrégation des données...")
        try:
            text = self.sql_handler.minmax_players_by_position() + "\n\n" + self.sql_handler.display_player_by_height() + "\n\n" + self.sql_handler.minmax_players_by_position() + "\n\n" + self.sql_handler.display_salary_stats()
            tk.messagebox.showinfo("Infomation générales", text)
        except Exception as e:
            tk.messagebox.showerror("Erreur", f"Problème lors de l'aggrégation des données: {str(e)}")
        
        

if __name__ == "__main__":
    root = tk.Tk()
    app = NFLApp(root)
    root.mainloop()