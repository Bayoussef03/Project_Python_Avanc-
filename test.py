import tkinter as tk
from tkinter import PhotoImage

def main():
    root = tk.Tk()
    root.title("Application avec Background Photo")

    # Charger l'image depuis le chemin spécifié
    image_path = "C:/Users/MSI/Desktop/eff.jpg"
    photo = PhotoImage(file=image_path)

    # Créer un Canvas pour afficher l'image en arrière-plan
    canvas = tk.Canvas(root, width=photo.width(), height=photo.height())
    canvas.pack(fill=tk.BOTH, expand=True)

    # Afficher l'image en arrière-plan
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)

    # Ajouter d'autres éléments à votre interface utilisateur ici...

    root.mainloop()

if __name__ == "__main__":
    main()
