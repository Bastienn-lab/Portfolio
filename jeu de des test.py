from turtle import *

from random import randint

screensize(400, 250)

n1 = randint(1,6)

n2 = randint(1,6)

sommejoueur = n1 + n2

n3 = randint(1,6)

n4 = randint(1,6)

sommeordi = n3 + n4

def aller(x,y):
    """deplacement du crayon aux coordonnées de la fenêtre graphique"""
    up()
    
    goto(x,y)
    
    down()    
    
#aller(x,y)


def carre(x,y,n):
    """dessine un carré à la position (x,y) et de la dimension n du coté.
    :x: et :y: les coordonnées du coin bas à gauche du carré
    :n: la valeur en pixel du coté du carré"""
    
    color("black")
    
    begin_fill()		
    
    for i in range(4):
        
        forward(150) 
        
        left(90)	
    
    end_fill()


def point(x,y,r,couleur):
    """dessine un rond plein de couleur à la position (x,y) et de rayon."""
     
    up()
    
    goto(x,y)
    
    down()
    
    color(couleur)
    
    begin_fill()
    
    circle(r)          
    
    end_fill()


def dessinede(x,y,couleur,chiffre):
    """dessine un dé avec les points du chiffre en couleur à la position (x,y).
    x et y; la position de départ (du coin bas à gauche) du dé
    couleur: la couleur du dé(rouge joueur et bleu ordinateur)
    chiffre: la valeur à afficher en nombre de point(s)"""
    cote_de = abs(150)							
    
    rayon_p = int(cote_de/10)					
    
    x_milieu = x+int(cote_de/2) 				
    
    y_milieu = y+int(cote_de/2)-int(cote_de/10) 
    
    ecart = int(cote_de/3)		
    
    color("white")
    
    carre(x,y,cote_de)
    
    if chiffre == 2 or chiffre == 3 or chiffre == 4 or chiffre == 5 or chiffre == 6:    
        
        point( x_milieu - ecart,   y_milieu + ecart,  rayon_p ,couleur)  
    
    if chiffre == 4 or chiffre == 5 or chiffre == 6:    
        
        point( x_milieu + ecart,   y_milieu + ecart,  rayon_p ,couleur)
   
    if chiffre == 6: 
       
        point( x_milieu - ecart,   y_milieu,  rayon_p, couleur)    
    
    if chiffre == 1 or chiffre == 3 or chiffre == 5: 
       
        point( x_milieu,   y_milieu,  rayon_p, couleur)
    
    if chiffre == 6: 
        
        point( x_milieu + ecart,   y_milieu,  rayon_p, couleur)    
    
    if chiffre == 4 or chiffre == 5 or chiffre == 6:    
        
        point( x_milieu - ecart,   y_milieu - ecart,  rayon_p ,couleur)
   
    if chiffre == 2 or chiffre == 3 or chiffre == 4 or chiffre == 5 or chiffre == 6:    
        
        point( x_milieu + ecart,   y_milieu - ecart,  rayon_p ,couleur)
     

def deuxdes(x,y,couleur):
    """dessine les deux dés lancés au hasard à partir de la position x,y
    et retourne la somme des deux dés
    :x: et :y: la position du premier dé (du coin bas à gauche) 
    :couleur: la couleur des deux dés
    retourne la somme des deux dés"""
    aller(x, y)
    
    dessinede(x, y, "blue", n1)
   
    x += 160
   
    aller(x, y)
    
    dessinede(x, y, "blue", n2)
   
    print("la somme des deux dé du joueur est: ",sommejoueur)
    
    x+=160 
    
    aller(x+50,y)
    
    dessinede(x+50, y, "red", n3)
   
    x+=160 
   
    aller(x+50,y)
    
    dessinede(x+50, y,"red", n4)
    
    print("la somme des deux dé de l'ordi est: ",sommeordi)
    pass 
    
def manche(x,y):
    """Exécute et dessine une manche entre les deux joueurs
    :x: et :y: la position de départ (du coin bas à gauche) du premier dé de la manche
    Affiche le résultat de la manche (gagnée,perdue,égalité)
    retourne 1 si le joueur gagne, retourne 0 si égalité et -1 si perdu"""
    deuxdes(x, y,color)
    
    Rjoueur = sommejoueur
    
    Rordi = sommeordi
  
    if Rjoueur > Rordi:
      
        print("bien joué,tu as gagné")
   
    elif Rjoueur <Rordi:
      
        print("dommage,tu as perdu")
   
    elif Rjoueur == Rordi:
      
        print(" il y a égalité")
    

def jeux(x, y):
    """execution du jeu: appel les manches, comptage les points du joueur 
    et affiche le résultat du joueur des que possible """
    setup(1000,500,100,100)                        

    sommeordi = n3 + n4
    
    manche(x, y)
    
    aller(x, y)   
             
    nouvelle_manche = input("Voulez-vous rejouer\noui=nouvelle manche\nnon=aurevoir\n")
    if nouvelle_manche == "oui":

        jeux(-350,0)
    
    else:
       
        print("aurevoir")

jeux(-350,0)

exitonclick()
