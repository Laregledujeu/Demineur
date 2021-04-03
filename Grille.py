import random as rd
import Open_Write_Fichier as OW #bibliotheque personnel qui permet d'ouvrir un fichier et d'ecrire dans les differents fichiers
import tkinter as t
import tkinter.messagebox as tm
import time

nombre_mines,taille,taille_carre=int(OW.ouvrir_fichier("Options.txt",5)),((int(OW.ouvrir_fichier("Options.txt",1)),int(OW.ouvrir_fichier("Options.txt",3)))),int(OW.ouvrir_fichier("Options.txt",7))
temps,localisation_drapeau=0,[]

def importer_options() :
    """Cette fonction sert a raffraichir les variables contenant les options 'importer_options()' """
    global taille,nombre_mines,taille_carre #je declare que je ne veux pas modifier la varioble de la fonction mais de __main__
    nombre_mines,taille,taille_carre=int(OW.ouvrir_fichier("Options.txt",5)),((int(OW.ouvrir_fichier("Options.txt",1)),int(OW.ouvrir_fichier("Options.txt",3)))),int(OW.ouvrir_fichier("Options.txt",7))
    #je declare que nombre de mines est egale la valeur de la ligne 5 du fichier Options.txt #je declare que nombre de mines est egale la valeur de la ligne 5 du fichier Options.txt #je declare que taille carre est egale a la valeur de la ligne 7 du fichier Options.txt

def creation_grille() :
    importer_options()
    """Permet de creer un tableau a double entrée a l'aide du niveau de difficulté choisi 'creation_grille(number)' """
    return([[0 for i in range(taille[0])] for j in range(taille[1])]) #je cree et retourne le tableau

def placer_Bombes(tableau,nombre) :
    """Permet de placer les bombes a des endroits aleatoires 'placer_bombes(number)' """
    for i in range(nombre) :#je fais une boucle for du nombre de mines a poser
        x,y=rd.randint(0,taille[1]-1),rd.randint(0,taille[0]-1) #je declare que le x et y de la case de la mine est entre 0 et la longueur de la grille
        if tableau[x][y]==-1 : #si c'est deja une mine
            tableau=placer_Bombes(tableau,1) #relance la fonction avec 1 mine a mettre
        else : #sinon je place la mine
            tableau[x][y]=-1 #la case est egal -1
    return(tableau) #je retourne la grille avec les mines

def afficher_tableau(tableau) :
    """Cette fonction est une fonction de debuggage, elle ne sert a rien a part afficher le tableau dans la console """
    for ligne in tableau : #je check toutes les case
        for element_ligne in ligne :
                if element_ligne==-1 : #si la case est un mine alors j'ecris 'm ' sans retour a la ligne
                    print("m ",end='')
                elif str(element_ligne) in "012345678" : #si c'est un nombre adjacent alors j'ecris 'valeur ' sans retour a la ligne
                    print(str(element_ligne)+" ",end='')
                else : #sinon j'ecris 'X ' sans retour a la ligne
                    print("X ",end='')
        print() #retour a la ligne

def bordure(liste_initial,action='A',valeur=-10) :
    """Permet de creer une bordure pour pouvoir scanner la grille sans containte 'bordure(list,str,int)' """
    if action=="A" :
        liste_initial.insert(0,[valeur]*taille[0]) #je cree un element qui fait la meme longeur que les autres lignes qui ne contient que 'valeur' et je le met a premier rang
        liste_initial.append([valeur]*taille[0]) #idem mais pour la derniere ligne
        for i in range(len(liste_initial)) : #je check toutes les lignes meme celle que je vient de creer
            liste_initial[i].insert(0,valeur) #pour chaque sous liste j'ajoute 'valeur' au premier rang
            liste_initial[i].append(valeur) #pour chaque sous liste j'ajoute 'valeur' au dernier rang
        return(liste_initial) #je retourne la grille modifier
    elif action=="S" :
        del liste_initial[0] #je suprime l'element de rang 0
        del liste_initial[-1] #je suprime le dernier element
        for i in range(len(liste_initial)) : #je check toutes les ligne
            del liste_initial[i][0] #je suprime le premier element
            del liste_initial[i][-1] #je suprime le dernier element
        return(liste_initial) #je retourne la grille modifier

def remplir_Cases(tableau_remplie) :
    """Permet de remplir les cases adjacentes au bombes 'remplir_Cases(list)' """
    tableau_remplie=bordure(tableau_remplie) #je cree un bordure pour pouvoir scanner sans contrainte
    for ligne in range(len(tableau_remplie)) : #je fais une double boucle for pour pouvoir scanner toutes la map
        for colonne in range(len(tableau_remplie[ligne])) :
            if tableau_remplie[ligne][colonne]==-1 : # si la case est une mine
                x,y=colonne-1,ligne-1
                for i in range(3) : #je fais un carre qui a pour centre la case qui est une mine
                    for j in range(3) :
                        if tableau_remplie[y+i][x+j]!=-1 : #si la case n'est pas une mine alors j'increment de 1
                            tableau_remplie[y+i][x+j]+=1
    return(bordure(tableau_remplie,"S")) #je retourne la tableau remplie avec les cases adjacents

def zone_decouvert(grille,y_cliquer,x_cliquer) :
    """Permet de donner une liste qui contient toute les cases qui sont a decouvrir lors d'un clique zone_dcouvert(list,int,int)
    liste=[(y,x),(y2,x2), .......... ]"""
    if grille[y_cliquer][x_cliquer]>0 or grille[y_cliquer][x_cliquer]==-1 : #si c'est une mine alors je sors de la fonction en retournant le tuple de la case cliquer
        return([(y_cliquer,x_cliquer)])
    grille=bordure(grille,"A") #je cree un bordure pour pouvoir scanner sans contrainte
    liste_0_a_regarder=[(y_cliquer+1,x_cliquer+1)] #je declare que la liste des case non check contient la case cliquer (+ 1 car il y a la bordure)
    liste_deja_regarder=[] #je declare que pour l'instant je n'est check aucune case
    while liste_0_a_regarder!=[] : #tant que la liste des cases non check n'est pas vide alors on continue
        x=liste_0_a_regarder[0][1] #x = le y de la premiere valeur de liste non check
        y=liste_0_a_regarder[0][0] #y = le x de la premiere valeur de liste non check
        #Je scan la zone en croix si un des valeurs est 0 est que je ne l'est pas deja check ou que n'est pas dans la file d'attente des checks alors je l'ajoute a la file d'attente
        if (grille[y][x-1]==0 and (y,x-1) not in liste_deja_regarder and (y,x-1) not in liste_0_a_regarder) :
            liste_0_a_regarder.append((y,x-1))
        if (grille[y-1][x]==0 and (y-1,x) not in liste_deja_regarder and (y-1,x) not in liste_0_a_regarder) :
            liste_0_a_regarder.append((y-1,x))
        if (grille[y][x+1]==0 and (y,x+1) not in liste_deja_regarder and (y,x+1) not in liste_0_a_regarder) :
            liste_0_a_regarder.append((y,x+1))
        if (grille[y+1][x]==0 and (y+1,x) not in liste_deja_regarder and (y+1,x) not in liste_0_a_regarder) :
            liste_0_a_regarder.append((y+1,x))
        liste_deja_regarder.append(liste_0_a_regarder[0]) #je dit que la valeur a etait check en la mettant dans le liste deja check
        del liste_0_a_regarder[0] #je la suprime de la liste non check
    liste_final=[]
    for y,x in liste_deja_regarder :
        for i in range(3) :
            for j in range(3) :
                if (y-1+j,x-1+i) not in liste_final and grille[y-1+j][x-1+i]>-1 :
                    liste_final.append((y-1+j,x-1+i))
    for coo in range(len(liste_final)): #on doit modifier les valeurs car ce sont les coordonnes avec la bordure
        liste_final[coo]=(liste_final[coo][0]-1,liste_final[coo][1]-1)
    grille=bordure(grille,"S") #je suprime la bordure
    return(liste_final) #je retourne la zone qui contient les 0

def afficher_mine(liste,interface) :
    """Check tous les cases si c'est un mine affiche une etoile"""
    ecart=3 #pemet de creer un ecart entre la mine et le bord du carre
    print(localisation_drapeau)
    for y,ligne in enumerate(liste) :
        for x,colonne in enumerate(ligne) :
            if (y,x) in localisation_drapeau :
                interface.create_rectangle(x*taille_carre+taille_carre/3,y*taille_carre+int(taille_carre/4),x*taille_carre+taille_carre-5,y*taille_carre+15,fill="green",outline="green")
            elif colonne==-1 :
                interface.create_line(x*taille_carre+ecart,y*taille_carre+ecart,x*taille_carre+taille_carre-ecart,y*taille_carre+taille_carre-ecart,width=1.5)
                interface.create_line(x*taille_carre+taille_carre-ecart,y*taille_carre+ecart,x*taille_carre+ecart,y*taille_carre+taille_carre-ecart,width=1.5)
                interface.create_line(x*taille_carre+int(taille_carre/2)+1,y*taille_carre+ecart,x*taille_carre+int(taille_carre/2)+1,y*taille_carre+taille_carre-ecart,width=1.5)
                interface.create_line(x*taille_carre+ecart,y*taille_carre+int(taille_carre/2)+1,x*taille_carre+taille_carre-ecart,y*taille_carre+int(taille_carre/2)+1,width=1.5)

def dessiner(nom_fenetre,reinitialiser=False) :
    global grille_interface
    """Permet de creer l'interface de la grille, generer la grille et de gerer les clics 'dessiner(class tkinter)' """
    def cliquer(event) :
        """Permet de savoir ou l'utilisateur a clique puis fait les actions neccesaires appres 'cliquer()' """
        update()
        x=int((event.x-event.x%taille_carre)/taille_carre) #je declare que x est le x de la souris - le reste de la division de x par taille carre puis je divise le tout par taille carre pour avoir les coordonne dans la grille[liste]
        y=int((event.y-event.y%taille_carre)/taille_carre) #idem pour y
        #print("Valeur de la case :",grille[mouse_y][mouse_x])
        decouvert=zone_decouvert(grille,y,x) #la liste de la zone decouverte est le return de la fonction zone_decouvert qui prend comme parametre la liste de la grille et le x et le y cliquer
        if grille[decouvert[0][0]][decouvert[0][1]]==-1 : # si c'est un mine
            afficher_mine(grille,grille_interface)
            grille_interface.update()
            choix=tm.askquestion("Fin de la partie","Vous avez perdu.\nVoulez-vous recommencer ?")
            if choix=="yes" :
                reinitialiser_var()
                dessiner(nom_fenetre)
                return()
            else :
                nom_fenetre.destroy()
                exit()
        for coord in decouvert : #boucle qui scan la zone
            if grille[coord[0]][coord[1]]>=1 : #si c'est un nombre adjacent d'une bombe
                couleur=["#E6E6E6","#0000FF","#00A000","#FF0000","#000080","#B00000","white","white","white"] #c'est la liste des couleurs qui s'affiche
                grille_interface.create_rectangle(coord[1]*taille_carre,coord[0]*taille_carre,coord[1]*taille_carre+taille_carre,coord[0]*taille_carre+taille_carre,outline="#C4C4C4",fill="#E6E6E6")
                #je cree un carre different du mode pas cliquer pour comprendre qu'on a deja cliquer
                grille_interface.create_text(coord[1]*taille_carre+taille_carre/2-1,coord[0]*taille_carre+taille_carre/2,text=grille[coord[0]][coord[1]],fill=couleur[grille[coord[0]][coord[1]]],font=20)
                #j'ecris le nombre qui correspond au coordonnes de la grille[list] puis je regarde sa valeur et c'est la valeur de la liste couleur que j'appelle pour la coloree
            else : #si c'est une zone de 0
                grille_interface.create_rectangle(coord[1]*taille_carre,coord[0]*taille_carre,coord[1]*taille_carre+taille_carre,coord[0]*taille_carre+taille_carre,width=1,outline="#C4C4C4",fill="#E6E6E6")
                #je cree un carre different du mode pas cliquer pour comprendre qu'on a deja cliquer

    def cliquer_droit(event) :
        """Trace un drapeau si la case est vide ou qu'il y a un ? sur la case 'cliquer_droit()' """
        global temps
        if temps==0 :
            temps=int(time.time())
        texte_temp.config(text=str(int(time.time()-temps)))
        global localisation_drapeau
        y=int((event.y-event.y%taille_carre)/taille_carre) #je declare que x est le x de la souris - le reste de la division de x par taille carre puis je divise le tout par taille carre pour avoir les coordonne dans la grille[liste]
        x=int((event.x-event.x%taille_carre)/taille_carre) #idem y
        if (y,x) not in localisation_drapeau : #si la case n'est pas dans la liste des drapeau deja mis
            localisation_drapeau.append((y,x)) #j'ajoute la case a la liste des drapeau deja mis
            grille_interface.create_rectangle(x*taille_carre,y*taille_carre,x*taille_carre+taille_carre,y*taille_carre+taille_carre,outline="#C8C8C8",fill="#DBDBDB")
            #je cree un carre de fond si il y avait deja quel que chose d'ecrit je le suprimer
            grille_interface.create_line(x*taille_carre+taille_carre/4,y*taille_carre+int(taille_carre/4),x*taille_carre+taille_carre/4,y*taille_carre+taille_carre,width=1.5)
            grille_interface.create_rectangle(x*taille_carre+taille_carre/3,y*taille_carre+int(taille_carre/4),x*taille_carre+taille_carre-5,y*taille_carre+15,fill="red",outline="red")
            texte_bombes.config(text=str(nombre_mines-len(localisation_drapeau)))
            if len(localisation_drapeau)==nombre_mines : #si le nombre de drapeau mis est egal au nombre de mines sur la grille
                check=False #si check est false alors cela veut dire que un des drapeaux est faux
                for coord in localisation_drapeau :
                    if grille[coord[0]][coord[1]]==-1 : #si la case est bien une mine alors je met true
                        check=True
                    else : #sinon je met False et je sors de la boucle pour
                        check=False
                        break
                if check : #si tous les drapeau sont correcte alors fenetre WIN
                    temp=" gagné en "+str(int(time.time()-temps))+" secondes.\n"
                    #permet d'importer le texte des stats puis de les modifier de les trier puis de ne prendre que ce que l'on veut
                    OW.modifier_fichier("Statistiques.txt","secondes,".join(sorted((((OW.ouvrir_fichier("Statistiques.txt",int(OW.ouvrir_fichier("Options.txt",9))))[:-1]+","+str(int(time.time()-temps))+" secondes,").split("secondes,")[:-1]),reverse=True)[:3])+"secondes",int(OW.ouvrir_fichier("Options.txt",9)))
                else : #sinon fenetre LOSE
                    temp=" perdu.\n"
                    afficher_mine(grille,grille_interface)
                choix=tm.askquestion("Fin de la partie","Vous avez"+temp+"Voulez-vous recommencer ?")
                ################ il faut enregistrer les scores dans statistiques
                if choix=="yes" :
                    dessiner(nom_fenetre)
                    reinitialiser_var()
                else :
                    nom_fenetre.destroy()
                    exit()
        elif (y,x) in localisation_drapeau : #donc si il y a deja un drapeau
            grille_interface.create_rectangle(x*taille_carre,y*taille_carre,x*taille_carre+taille_carre,y*taille_carre+taille_carre,outline="#C8C8C8",fill="#DBDBDB")
            #je trace un carre de fond pour suprimer le drapeau
            grille_interface.create_text(x*taille_carre+int(taille_carre/2),y*taille_carre+int(taille_carre/2),text="?",fill="white",font="30")
            #j'ecris un ? sur le carre dans la case
            localisation_drapeau.remove((y,x)) #je retire la case de la liste des drapeaux
            texte_bombes.config(text=str(nombre_mines-len(localisation_drapeau)))

    def reinitialiser_var() :
        """Reinitialise toutes les variables pour recommencer"""
        global localisation_drapeau,temps
        temps,localisation_drapeau=0,[]
        importer_options() #j'importe les options du fichier txt

    def update() :
        """Gere le timer avec une recurence"""
        global temps
        if temps==0 :
            temps=int(time.time())
        texte_temp.config(text=str(int(time.time()-temps)))
        nom_fenetre.after(1000,update)

    reinitialiser_var()
    grille=[]
    grille=remplir_Cases(placer_Bombes(creation_grille(),nombre_mines)) #je genere la grille avec les bombes et les cases adjacentes remplie
    afficher_tableau(grille) #je l'affiche pour pouvoir savoir si ca marche bien
    texte1=t.Label(nom_fenetre,text="Bombes restante(s) :").grid(row=0,column=0) # j'ecris un texte blanc pour faire de l'espace entre le bandeau et la grille
    texte_bombes=t.Label(nom_fenetre,text=str(nombre_mines)) #je cree un texte qui est la variable nombre_mines
    texte_bombes.grid(row=0,column=1) #j'affiche le texteg
    if reinitialiser==False :
        grille_interface=t.Canvas(nom_fenetre)
    nom_fenetre.after(1000,lambda : texte_temp.config(text="0"))
    grille_interface.config(width=taille[0]*taille_carre,height=taille[1]*taille_carre)
    grille_interface.grid(row=1,column=0,columnspan=2)
    for ligne in range(1,taille[1]+1) : #je trace ma grille avec une double boucle for
        for colonne in range(1,taille[0]+1) :
            grille_interface.create_rectangle(colonne*taille_carre-taille_carre,ligne*taille_carre-taille_carre,colonne*taille_carre,ligne*taille_carre,width=2,outline="#C8C8C8",fill="#DBDBDB")
            #je trace en fonction des parametres de la double boucle for avec des contours gris foncé de 2 pixels et qui a pour couleur de fond gris plus clair
    grille_interface.bind("<Button-1>",cliquer) #si l'utilisateur clique gauche SUR la grille alors j'appelle la fonction cliquer
    grille_interface.bind("<Button-3>",cliquer_droit) #si l'utilisateur clique droit  SUR la grille alors j'appelle la fonction cliquer_droit
    texte2=t.Label(nom_fenetre,text="Temps :").grid(row=2,column=0) # j'ecris un texte blanc pour faire de l'espace entre la fin de la fenetre et la grille
    texte_temp=t.Label(nom_fenetre,text="0")
    texte_temp.grid(row=2,column=1)
