import tkinter as t
import Grille as G #autre partie du programme du jeu (interface grille + gestion de la grille)
import Open_Write_Fichier as OW #bibliotheque personnel qui permet d'ouvrir un fichier et d'ecrire dedans
import tkinter.messagebox as tf #c'est le plugin qui fait la pop up pour la demande de fermeture du programme
nb_fenetre_aide=0 #nombre de fenetre aide ouverte
nb_fenetre_stats=0 #nombre de fenetre stats ouverte
nb_fenetre_option=0 #nombre de fenetre option ouverte

def barre_de_menu(nom_fenetre) :
    def afficher_aide() :
        def detruire_fenetre_aide() :
            global nb_fenetre_aide
            nb_fenetre_aide=0
            fenetre_aide.destroy()
        global nb_fenetre_aide
        if nb_fenetre_aide==0 :
            nb_fenetre_aide=1
            fenetre_aide=t.Tk()
            fenetre_aide.title("Aide")
            fenetre_aide.bind("<Escape>",lambda event: detruire_fenetre_aide())
            texte=t.Label(fenetre_aide,text="Le Démineur est un jeu de mémoire et de raisonnement qui n’est pas aussi simple qu’il en a l’air.\nLe but du jeu est de découvrir tous les carrés vides en évitant ceux qui cachent des mines.\nSi vous cliquez sur une mine, vous avez perdu.\nPour faire le meilleur score, vous devez découvrir tous les carrés vides le plus vite possible.\n\nCliquez sur l’un des carrés du champ de mines pour démarrer le chronomètre.\nPour afficher le contenu d’un carré, cliquez dessus.\nSi un chiffre apparaît dans un carré, il indique le nombre de mines dissimulées\ndans les huit carrés qui l’entourent.\nVous pouvez vous servir de ce chiffre pour déterminer si un carré risque ou non de cacher une mine.\n\nPour marquer un carré qui, selon vous, contient une mine, cliquez dessus avec le bouton droit.\nUn drapeau apparaît alors sur le carré suspect.\nEn cas de doute, cliquez une deuxième fois avec le bouton droit \nsur le carré suspect pour changer le drapeau en point d’interrogation.\n\n")
            texte.pack()
            boutonQuitter=t.Button(fenetre_aide,text="Fermer",command=detruire_fenetre_aide)
            boutonQuitter.pack()
            fenetre_aide.mainloop()

    def message_quitter() : # le but est de creer une pop up qui dit que si on a commencer une partie il ne faut pas partir
        choix=tf.askquestion("Quitter","Êtes-vous sur de vouloir quitter ?")
        if choix=="yes" : #t.askquestion est soit egale a no soit yes
            nom_fenetre.destroy()

    def afficher_stats() :
        def detruire_fenetre_stats() :
            global nb_fenetre_stats
            nb_fenetre_stats=0
            fenetre_stats.destroy()
        def selection_choix() :
            texte.config(text="\n".join((OW.ouvrir_fichier("Statistiques.txt",(choix_difficulte.curselection()[0])*2+1)).split(","))[:-1])
            fenetre_stats.update() #on rafraichit la fenetre car sinon on ne verra rien
        global nb_fenetre_stats
        if nb_fenetre_stats==0 :
            nb_fenetre_stats=1
            fenetre_stats=t.Tk()
            fenetre_stats.focus_set()
            fenetre_stats.title("Statistiques")
            fenetre_stats.bind("<Escape>",lambda event: detruire_fenetre_stats())
            choix_difficulte=t.Listbox(fenetre_stats,width="13",height=3,selectmode="single") # width est en pixels / height est en ligne / selectmode fait que l'on ne peut cliquer que sur 1 element
            choix_difficulte.insert(1,"Debutant") # on insert 1 element qui sera
            choix_difficulte.insert(3,"Intermediaire")
            choix_difficulte.insert(5,"Avancée")
            choix_difficulte.grid(padx=10,pady=10,row=0) #permet de placer dans la fenetre le widget
            fenetre_stats.bind("<<ListboxSelect>>",lambda event:selection_choix()) #si un element de la liste est selectionnée alors on appelle la fonction selection_choix
            best_time=t.LabelFrame(fenetre_stats,text="Meilleur Temps : ") #on creer la zone de texte pour les meilleurs temps
            texte=t.Label(best_time,text='\n\n')
            best_time.grid(padx=10,pady=10,column=1,row=0) #permet de placer dans la fenetre le widget
            texte.pack() #permet de placer dans la fenetre le widget
            boutonQuitter=t.Button(fenetre_stats,text="Fermer",command=detruire_fenetre_stats)
            boutonQuitter.grid(column=1,padx=10,pady=10,row=1) #permet de placer dans la fenetre le widget

    def afficher_options() :
        def detruire_fenetre_option() :
            global nb_fenetre_option
            nb_fenetre_option=0
            fenetre_option.destroy()

        def changer_options(temp) :
            if temp=="d" :
                OW.modifier_fichier("Options.txt","9",1)
                OW.modifier_fichier("Options.txt","9",3)
                OW.modifier_fichier("Options.txt","10",5)
                OW.modifier_fichier("Options.txt","1",9)
                G.dessiner(nom_fenetre,True)
            elif temp=="i" :
                OW.modifier_fichier("Options.txt","16",1)
                OW.modifier_fichier("Options.txt","16",3)
                OW.modifier_fichier("Options.txt","40",5)
                OW.modifier_fichier("Options.txt","3",9)
                G.dessiner(nom_fenetre,True)
            elif temp=="a" :
                OW.modifier_fichier("Options.txt","30",1)
                OW.modifier_fichier("Options.txt","16",3)
                OW.modifier_fichier("Options.txt","99",5)
                OW.modifier_fichier("Options.txt","5",9)
                G.dessiner(nom_fenetre,True)

        global nb_fenetre_option
        if nb_fenetre_option==0 : #si il y a deja 1 fenetre alors ne rien faire
            nb_fenetre_option=1
            fenetre_option=t.Tk()
            fenetre_option.focus_set() #permet de faire que si fenetre principal est supr alors elle aussi
            fenetre_option.title("Options") # on renomme le titre de la fenetre
            fenetre_option.bind("<Escape>",lambda event: detruire_fenetre_option())
            cadre_difficulte=t.LabelFrame(fenetre_option,text="Difficulté ")
            cadre_difficulte.grid(row=0)
            choix_difficulte=t.StringVar()
            choix_difficulte.set("d")
            button_debutant=t.Radiobutton(cadre_difficulte,text="Debutant\n10 mines\ngrilles 9 x 9",variable=choix_difficulte,value="d",command=lambda : changer_options("d"))
            button_debutant.grid(row=1,column=0)
            button_intermediaire=t.Radiobutton(cadre_difficulte,text="Intermediaire\n40 mines\ngrilles 16 x 16",variable=choix_difficulte,value="i",command=lambda : changer_options("i"))
            button_intermediaire.grid(row=1,column=1)
            button_avancee=t.Radiobutton(cadre_difficulte,text="Avancé\n99 mines\ngrilles 16 x 30",variable=choix_difficulte,value="a",command=lambda : changer_options("a"))
            button_avancee.grid(row=1,column=2)
            button_debutant.select()
            bouton_ok=t.Button(fenetre_option,text="Ok",command=lambda : detruire_fenetre_option()).grid(row=2)
            fenetre_option.mainloop()

    barre_menu=t.Menu(nom_fenetre) # !!! barre_menu est un widget esclave mais en meme temps maitre (creation) et tearoff = 0 sinon il y a des pointilles moche

    menu_partie=t.Menu(barre_menu,tearoff=0) #on cree une categorie menu_partie dans le widget maitre barre_menu
    menu_partie.add_command(label="Nouvelle Partie",command=lambda : G.dessiner(nom_fenetre,True)) # on ajoute une sous categorie a menu_partie
    menu_partie.add_separator() #on ahoute un separateur
    menu_partie.add_command(label="Statistiques     F4",command=afficher_stats)
    nom_fenetre.bind("<F4>",lambda event: afficher_stats())
    menu_partie.add_command(label="Options      F5",command=afficher_options)
    nom_fenetre.bind("<F5>",lambda event: afficher_options())
    menu_partie.add_separator()
    menu_partie.add_command(label="Quitter      Echap",command=message_quitter) #on cree un sous categorie de menu_partie en dessous du separateur
    nom_fenetre.bind("<Escape>",lambda event: message_quitter()) # on utilise lamba car il parait que c'est plus propre et event parce que la fonction lambda prend forcement un parametre
    barre_menu.add_cascade(label="Partie",menu=menu_partie) # on cree un cascade dans l'objet barre_menu qui contient menu_partie

    menu_help=t.Menu(barre_menu,tearoff=0)
    menu_help.add_command(label="Afficher l'aide        F2",command=afficher_aide)
    nom_fenetre.bind("<F2>",lambda event: afficher_aide())
    barre_menu.add_cascade(label="?",menu=menu_help)

    nom_fenetre.config(menu=barre_menu) #on dit que le widget barre_menu doit apartient a fenetre (implementation)
