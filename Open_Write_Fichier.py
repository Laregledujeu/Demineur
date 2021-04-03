import os

def ouvrir_fichier(nom_du_fichier,ligne="ALL") :
    """Retourne une chaine de caractere qui contient chaque ligne du texte grace au nom du texte 'ouvrir_fichier(char)' """
    fichier_original=open(nom_du_fichier,"r") #on ouvre le fichier en mode r => read
    if ligne=="ALL" :
        texte="".join(fichier_original.read())
        if texte=="" : #si texte = RIEN alors FALSE
            return(False)
        return(texte)
    else :
        texte=fichier_original.readlines()
        texte="".join(texte[ligne])
        if texte[0]=="#" :
            print("La ligne "+texte+"ne peut pas etre importer")
        else :
            return(texte)

def ecrire_fichier(nom_du_fichier,texte) :
    """Permet d'ecrire dans le fichier 'nom_du_fichier' la variable 'texte' 'ecrire_fichier(char,char)' """
    fichier=open(nom_du_fichier,"w") #j'ouvre le fichier en mode w => write
    fichier.write(texte) #j'ecris la chaine dans le fichier
    fichier.close() #je ferme le fichier

def modifier_fichier(nom_du_fichier,texte,ligne) :
    """Permet de remplacer le texte du fichier 'nom_du_fichier' par 'texte' a la 'ligne' 'modifier_fichier(char,char,number)' """
    fichier_original=open(nom_du_fichier,"r")
    texte_fichier_original=fichier_original.readlines()
    fichier_original.close()
    if ligne>=len(texte_fichier_original) :
        return(False)
    else :
        if texte_fichier_original[ligne][0]=="#" :
            print("Vous essayer de modifier une ligne qui ne peut pas etre modifiable ")
        else :
            texte_fichier_original[ligne]=texte+"\n"
            fichier_au_final=open(nom_du_fichier,"w")
            fichier_au_final.write("".join(texte_fichier_original))
            fichier_au_final.close()
