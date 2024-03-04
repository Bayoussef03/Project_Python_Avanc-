from tkinter import Tk, Text, Scrollbar, Button, messagebox, Frame, Label, Toplevel
from tkinter import PhotoImage
import re
import os
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class ExtDonnees:
    def __init__(self, path_livre):
        self.root = Tk()
        self.path_livre = path_livre
        self.abs_path = os.path.dirname(os.path.abspath(__file__))

    def extraire_donnees(self):
        try:
            with open(self.path_livre, "r", encoding="utf-8") as fichier_livre:
                content = fichier_livre.read()

                debut_titre_livre = content.find("Title:") + len("Title:")
                fin_titre_livre = content.find("Author:")
                titre_livre = content[debut_titre_livre:fin_titre_livre].strip()

                debut_auteur = content.find("Author:") + len("Author:")
                fin_auteur = content.find("Release date:")
                nom_auteur = content[debut_auteur:fin_auteur].strip()

                debut_chapitre_1 = 'R. M. APPLETON, H                "        168'
                fin_chapitre_1 = "and the referee for the ball."

                debut_chapitre = content.find(debut_chapitre_1) + len(debut_chapitre_1)
                fin_chapitre = content.find(fin_chapitre_1)
                chapitre_1 = content[
                    debut_chapitre : fin_chapitre + len(fin_chapitre_1)
                ].strip()

                chapitre_1_nettoyé = re.sub(r"\[Illustration:[^\]]*\]", "", chapitre_1)

                self.root.title("Informations du Livre")

                titre_frame = Frame(self.root)
                titre_frame.pack(pady=10)

                titre_label = Label(
                    titre_frame,
                    text=f"Titre du livre: {titre_livre}",
                    font=("Helvetica", 14, "bold"),
                    bg="blue",
                )
                titre_label.pack()

                auteur_frame = Frame(self.root)
                auteur_frame.pack(pady=10)

                auteur_label = Label(
                    auteur_frame,
                    text=f"Nom de l'auteur: {nom_auteur}",
                    font=("Helvetica", 12),
                    fg="blue",
                )
                auteur_label.pack()

                chapitre1_frame = Frame(self.root)
                chapitre1_frame.pack(pady=20)

                voir_texte = Scrollbar(chapitre1_frame, orient="vertical")
                voir_texte.pack(side="right", fill="y")

                texte_aff = Text(
                    chapitre1_frame,
                    wrap="word",
                    yscrollcommand=voir_texte.set,
                    font=("Helvetica", 12),
                    bg="grey",
                )
                texte_aff.pack(expand=True, fill="both")

                lignes_hors_analyse = [
                    "ENGLISH AND AMERICAN RUGBY",
                    "AMERICAN FOOTBALL.",
                ]
                for line in lignes_hors_analyse:
                    texte_aff.insert("end", f"{line}\n")

                paragraphe = self.paragraphe_nettoyé(
                    chapitre_1_nettoyé, lignes_hors_analyse
                )

                paragraphe_gr_mots = defaultdict(list)
                paragraphe_par_mots = defaultdict(int)

                for i, paragraphe_xxx in enumerate(paragraphe, start=1):

                    if paragraphe_xxx.strip() not in lignes_hors_analyse:

                        nombres_mots, mots_arrondis = self.comptage_mots(paragraphe_xxx)

                        paragraphe_gr_mots[nombres_mots].append(f"Paragraphe {i}")
                        paragraphe_par_mots[mots_arrondis] += 1

                        texte_aff.insert(
                            "end",
                            f"Paragraphe {i} ({nombres_mots} mots --> {mots_arrondis} mots):\n{paragraphe_xxx}\n\n",
                        )

                voir_texte.config(command=texte_aff.yview)

                bouton_comptage = Button(
                    self.root,
                    text="Compter les paragraphes",
                    command=lambda: self.comptage_aff(
                        chapitre_1_nettoyé, lignes_hors_analyse
                    ),
                )
                bouton_comptage.pack(pady=10)

                bouton_nb_mots = Button(
                    self.root,
                    text="Compter les mots par paragraphe",
                    command=lambda: self.fe_comptage_mots(
                        lignes_hors_analyse, paragraphe
                    ),
                )
                bouton_nb_mots.pack(pady=10)

                bouton_tri_pg = Button(
                    self.root,
                    text="Trier les paragraphes par longueur",
                    command=lambda: self.tri_aff(paragraphe_gr_mots),
                )
                bouton_tri_pg.pack(pady=10)

                graph_button = Button(
                    self.root,
                    text="Afficher le graphique de distribution",
                    command=lambda: self.aff_graph_pt2(paragraphe_par_mots),
                )
                graph_button.pack(pady=10)

                self.root.mainloop()

        except FileNotFoundError:
            messagebox.showerror("Erreur", "Le fichier n'a pas été trouvé.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")

    def comptage_aff(self, text, lignes_hors_analyse):
        numero_paragraphe = self.comptage_paragraphes(text, lignes_hors_analyse)
        messagebox.showinfo(
            "Comptage des paragraphes",
            f"Nombre de paragraphes dans le chapitre : {numero_paragraphe}",
        )

    def comptage_paragraphes(self, text, lignes_hors_analyse):
        paragraphe = self.paragraphe_nettoyé(text, lignes_hors_analyse)
        paragraphe = [
            paragraphe_xxx.strip()
            for paragraphe_xxx in paragraphe
            if paragraphe_xxx.strip()
        ]
        return len(paragraphe)

    def comptage_mots(self, paragraphe_xxx):
        mots = re.findall(r"\b[^\W\d_,-]+(?:-[^\W\d_,-]+)*\b", paragraphe_xxx)
        nombres_mots = len(mots)

        mots_arrondis = (nombres_mots // 10) * 10

        return nombres_mots, mots_arrondis

    def paragraphe_nettoyé(self, text, lignes_hors_analyse):
        paragraphe = re.split(r"\n{2,}", text)
        paragraphe = [
            paragraphe_xxx.strip()
            for paragraphe_xxx in paragraphe
            if paragraphe_xxx.strip() not in lignes_hors_analyse
        ]
        return paragraphe

    def fe_comptage_mots(self, lignes_hors_analyse, paragraphe):
        fenetre_ducomptage_mots = Toplevel(self.root)
        fenetre_ducomptage_mots.title("Comptage des mots par paragraphe")

        paragraphe_gr_mots = defaultdict(list)

        for i, paragraphe_xxx in enumerate(paragraphe, start=1):
            if paragraphe_xxx.strip() not in lignes_hors_analyse:
                nombres_mots, mots_arrondis = self.comptage_mots(paragraphe_xxx)
                paragraphe_gr_mots[mots_arrondis].append(f"Paragraphe {i}")

        for mots_arrondis, paragraphe in paragraphe_gr_mots.items():
            message = f"Paragraphes avec {mots_arrondis} mots : {', '.join(paragraphe)}"
            Label(fenetre_ducomptage_mots, text=message, font=("Helvetica", 12)).pack()

    def tri_aff(self, paragraphe_gr_mots):
        paragraphe_nb_arrondis_longeur = sorted(
            paragraphe_gr_mots.items(), key=lambda x: x[0]
        )

        fenetre_tri_pg = Toplevel(self.root)
        fenetre_tri_pg.title("Tri des paragraphes par longueur")

        for mots_arrondis, paragraphe in paragraphe_nb_arrondis_longeur:
            message = (
                f"Paragraphes avec {mots_arrondis} mots  : {', '.join(paragraphe)}"
            )
            Label(fenetre_tri_pg, text=message, font=("Helvetica", 12)).pack()

    def aff_graph_pt2(self, paragraphe_par_mots):

        plt.bar(paragraphe_par_mots.keys(), paragraphe_par_mots.values(), color="blue")
        plt.xlabel("Nombre de mots par paragraphe ")
        plt.ylabel("Nombre de paragraphes")
        plt.title("Distribution des longueurs des paragraphes")

        graph_filename = f"{self.abs_path}/resultat/distribution_graph.png"
        plt.savefig(graph_filename)

        fenetre_graph_partie2 = Toplevel(self.root)
        fenetre_graph_partie2.title("Distribution des longueurs des paragraphes")

        graph_label = Label(fenetre_graph_partie2)
        graph_label.pack()

        graph_image_pt2 = PhotoImage(file=graph_filename, master=self.root)
        graph_label.config(image=graph_image_pt2)
        graph_label.image = graph_image_pt2

        fig, ax = plt.subplots()
        ax.bar(paragraphe_par_mots.keys(), paragraphe_par_mots.values(), color="blue")
        ax.set_xlabel("Nombre de mots par paragraphe")
        ax.set_ylabel("Nombre de paragraphes")
        ax.set_title("Distribution des longueurs des paragraphes")

        canvas = FigureCanvasTkAgg(fig, master=fenetre_graph_partie2)
        canvas.draw()
        canvas.get_tk_widget().pack()

        toolbar = NavigationToolbar2Tk(canvas, fenetre_graph_partie2)
        toolbar.update()
        canvas.get_tk_widget().pack()

        fenetre_graph_partie2.mainloop()
