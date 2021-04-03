import tkinter as t
import Menu_Demineur as MD #partie qui gere le bandeau d'options
import Grille as G #autre partie du programme du jeu (interface grille + gestion de la grille)

demineur=t.Tk()
MD.barre_de_menu(demineur)
G.nom_fenetre=demineur
G.dessiner(demineur)
demineur.title("Demineur")
demineur.resizable(width=False,height=False)
demineur.mainloop()