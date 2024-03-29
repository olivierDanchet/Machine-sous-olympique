import pygame  # Importation du module pygame
import random  # Importation du module random
import time  # Importation du module time

# Définition des couleurs
DARK_GREEN = (10, 65, 10)
GREEN = (30, 100, 30)
LIGHT_GREEN = (40, 165, 40)
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
LIGHT_BLUE = (0, 185, 255)
GREY = (50, 50, 50)
LIGHT_GREY = (110, 110, 110)
BLACK = (0, 0, 0)
ORANGE = (255, 90, 0)


# Définir les class de boutons
# Class boutons sans image
class Button:
    def __init__(self, x, y, width, height, text, action=None, color=None, color_border=None,
                 border_ext=None, border_int=None, color_font=None, taille=None):
        # Crée un rectangle pour le bouton avec les coordonnées et les dimensions fournies
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text  # Stockage de texte à afficher sur le bouton
        self.font = pygame.font.Font(None, size=taille)  # Initialisation de la police pour le texte du bouton
        self.action = action  # Stockage de l'action à exécuter lorsque le bouton est cliqué
        self.color = color  # Stockage de la couleur de l'intérieur du bouton
        self.color_border = color_border  # Stockage de la couleur de la bordure du bouton
        self.border_ext = border_ext  # Stockage de la taille du coin de la bordure extérieur du bouton
        self.border_int = border_int  # Stockage de la taille du coin de la bordure intérieur du bouton
        self.color_font = color_font  # Stockage de la couleur du texte du bouton

    def draw(self, screen, color=None, color_border=None, border_ext=None, border_int=None, color_font=None):
        # Dessine le fond du bouton avec une couleur verte (GREEN)
        pygame.draw.rect(screen, self.color, self.rect, border_radius=self.border_ext)
        # Dessine une bordure plus claire autour du bouton
        pygame.draw.rect(screen, self.color_border, self.rect.inflate(-6, -6), border_radius=self.border_int)
        # Rend le texte du bouton avec la police spécifiée et la couleur DARK_GREEN
        text_surface = self.font.render(self.text, True, self.color_font)
        text_rect = text_surface.get_rect(center=self.rect.center)  # Centre le texte au milieu du bouton
        screen.blit(text_surface, text_rect)  # Affiche le texte sur l'écran

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:  # Vérifie si un événement de clic de souris a eu lieu
            # Vérifie si la position du clic de souris est à l'intérieur des limites du bouton
            if self.rect.collidepoint(event.pos):
                if self.action:  # Vérifie si une action est associée au bouton
                    self.action()  # Exécute l'action associée au bouton


# Class boutons avec image
class Button1:
    def __init__(self, image, x, y, action=None):
        self.image = image  # Initialise le bouton avec une image, des coordonnées x et y, et une action facultative
        self.rect = self.image.get_rect()  # Récupère le rectangle de l'image pour les calculs de collision
        self.rect.topleft = (x, y)  # Positionne le coin supérieur gauche du rectangle à l'emplacement spécifié
        self.action = action  # Stocke l'action à exécuter lorsque le bouton est cliqué

    def draw(self, surface):
        # Dessine l'image du bouton sur la surface spécifiée aux coordonnées rectangulaires
        surface.blit(self.image, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:  # Vérifie si un événement de clic de souris a eu lieu
            # Vérifie si la position du clic de souris est à l'intérieur des limites du bouton
            if self.rect.collidepoint(event.pos):
                if self.action:  # Vérifie si une action est associée au bouton
                    self.action()  # Exécute l'action associée au bouton


# Liste d'affichage des tuiles du background de la machine à sous
tile_map = [[0, 0, 0, 0, 0, 0, 9, 8, 8, 8, 8, 8, 7, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 2, 14, 14, 14, 14, 14, 6, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 9, 8, 8, 8, 12, 8, 8, 8, 12, 8, 8, 8, 7, 0, 0, 0],
            [0, 0, 0, 2, 1, 1, 1, 13, 1, 1, 1, 13, 1, 1, 1, 6, 0, 0, 0],
            [0, 0, 0, 2, 1, 1, 1, 10, 1, 1, 1, 10, 1, 1, 1, 6, 0, 0, 0],
            [0, 0, 0, 2, 1, 1, 1, 15, 1, 1, 1, 15, 1, 1, 1, 6, 0, 0, 0],
            [0, 0, 0, 2, 1, 1, 1, 13, 1, 1, 1, 13, 1, 1, 1, 6, 0, 0, 0],
            [0, 0, 0, 3, 4, 4, 4, 11, 4, 4, 4, 11, 4, 4, 4, 5, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

pygame.init()  # Initialisation de pygame

# Liste de verification des gain
lst_verif = [[7, 7, 7], [1, 1, 1], [9, 9, 9], [8, 8, 8], [6, 6, 6], [13, 13, 13], [12, 12, 12], [11, 11, 11],
             [5, 5, 5], [4, 4, 4], [2, 2, 2], [3, 3, 3], [10, 10, 10], [5, 7, 7], [1, 1, 5], [5, 9, 9], [5, 8, 8],
             [5, 6, 6], [5, 13, 13], [5, 12, 12], [5, 11, 11], [4, 4, 5], [2, 2, 5], [3, 3, 5],
             [5, 10, 10], [5, 5, 7], [1, 5, 5], [5, 5, 9], [5, 5, 8], [5, 5, 6], [5, 5, 13], [5, 5, 12],
             [5, 5, 11], [4, 5, 5], [2, 5, 5], [3, 5, 5], [5, 5, 10], [6, 6, 8], [6, 6, 9], [6, 8, 8],
             [8, 8, 9], [6, 9, 9], [8, 9, 9], [6, 8, 9], [5, 6, 8], [5, 6, 9], [5, 8, 9], [11, 11, 12],
             [11, 11, 13], [11, 12, 12], [12, 12, 13], [11, 13, 13], [12, 13, 13], [11, 12, 13], [5, 11, 12],
             [5, 11, 13], [5, 12, 13]]

lst_aleatoire = []  # Liste des symboles tirés

# Liste des gains de la machine à sous
recompense = [1000, 500, 250, 250, 250, 200, 200, 200, 150, 100, 50, 50, 50, 1000, 500, 250, 250, 250, 200,
              200, 200, 100, 50, 50, 50, 1000, 500, 250, 250, 250, 200, 200, 200, 100, 50, 50, 50, 200,
              200, 200, 200, 200, 200, 200, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 100, 100, 100]

c = 64  # Dimension caractéristique des sprites (côté c)
SCREEN_WIDTH = 19*c  # Taille de la largeur de la fenêtre
SCREEN_HEIGHT = 11*c  # Taille de la hauteur de la fenêtre
bet = 1  # Variable de la mise mise de base à 1
erreur = "READY"  # Variable des potentielles erreurs
touche = ""  # Variable du texte qui montre les touches à utiliser
file = open("file/coins", "r")  # Ouverture du fichier du stock des coins en mode lecture
coins = int(file.read())  # Variable des coins mise à la valeur du fichier de stock des coins
file.close()  # Fermeture du fichier du stock des coins
aleatoire = 7  # Variable du premier tirage
aleatoire1 = 7  # Variable du deuxième tirage
aleatoire2 = 7  # Variable du troisième tirage
# Configuration du rectangle du joueur bg1
largeur_joueur = 148  # Largeur du joueur 1 du bg1
hauteur_joueur = 232  # Hauteur du joueur 1 du bg1
x_perso = 200  # Position en X du personnage 1 du bg1
y_perso = 445  # Position en Y du personnage du bg1
# Configuration du rectangle de l'ennemi du bg1
largeur_ennemi = 62  # Largeur de la haie (ennemi) du bg1
hauteur_ennemi = 120  # Hauteur de la haie (ennemi) du bg1
x_obj = 1500  # Position en X de la haie (ennemi) du bg1
y_obj = 560  # Position en Y de la haie (ennemi) du bg1
# Configuration du rectangle du joueur bg2
largeur_joueur2 = 37  # Largeur de l'image du personnage 2 du bg2
hauteur_joueur2 = 145  # Hauteur de l'image du personnage 2 du bg2
hauteur_carre_joueur2 = 5  # Hauteur du carré des collisions du personnage 2 du bg2
x_perso2 = 560  # Position en X du personnage 2 du bg2
y_carre_perso2 = 144  # Position en Y du carré des collisions du personnage 2 du bg2
x_carre_perso2 = 30  # Position en X du carré des collisions du personnage 2 du bg2
# Configuration du rectangle du sol du bg2
largeur_sol = 1216  # Largeur de l'image du sol du bg2
hauteur_sol = 1  # Hauteur de l'image du sol du bg2
y_sol = 626  # Position en Y du sol du bg2
# Configuration du rectangle de la pierre du bg2
largeur_stone = 93  # Largeur de l'image de la pierre du bg2
hauteur_stone = 1  # Hauteur de l'image de la pierre du bg2
x_obj2 = 500  # Position en X de la pierre du bg2
y_obj2 = 350  # Position en Y de la pierre du bg2
# Configuration du rectangle de la pierre 2 du bg2
largeur_stone1 = 93  # Largeur de l'image de la deuxième pierre du bg2
hauteur_stone1 = 1  # Hauteur de l'image de la deuxième pierre du bg2
x_obj2_1 = 700  # Position en X de la deuxième pierre du bg2
y_obj2_1 = 50  # Position en Y de la deuxième pierre du bg2
# Configuration du personnage du bg4
x_perso4 = 550  # Position en X du personnage 4 du bg4
y_perso4 = 300  # Position en Y du personage 4 du bg4
# Variables booléennes
image_visible = False  # Variable d'affichage de la notice
text2_visible = True  # Variable d'affiche du texte des coins et de son fond
text_visible = True  # Variable d'affichage de tous les textes sauf du texte des coins
but_visible = False  # Variable d'affichage du bouton de fermeture de la notice
image_visible1 = False  # Variable d'affichage du menu 1
but_visible1 = False  # Variable d'affichage du bouton de fermeture du menu 1
but_activer = False  # Variable d'activation de tous les boutons de la machine à sous boutons
allumer = True  # Variable d'affichage des lumières
lumiere_gain = False  # Variable d'affichage des lumières de gain bigwin
lumiere_gain1 = False  # Variable d'affichage des lumières2 de gain bigwin
lumiere_gain2 = False  # Variable d'affichage des lumières de gain jackpot
lumiere_gain3 = False  # Variable d'affichage des lumières2 de gain jackpot
jackpot_visible = False  # Variable d'affichage du panneau jackpot
bigwin_visible = False  # Variable d'affichage du panneau bigwin
run = False  # Variable qui active les touches du clavier lié aux boutons de la machine à sous
tour = False  # Variable d'activation de l'animation des rouleaux de la machine à sous
bloquer = False  # Variable qui bloque l'utilisation du bouton spin quand les rouleaux tournent
ecran_accueil = True  # Variable qui affiche l'écran d'accueil
bg1 = False  # Variable qui affiche le mini-jeux 1
bg2 = False  # Variable qui affiche le mini-jeux 2
bg3 = False  # Variable qui affiche le mini-jeux 3
bg4 = False  # Variable qui affiche le mini-jeux 4
croix = False  # Variable qui affiche la croix des mini-jeux
jump = False  # Variable qui autorise ou non le saut du personnage du bg1
gauche = False  # Variable qui verifie le côté gauche du personnage 4 du bg4
droit = False  # Variable qui verifie le côté droit du personnage 4 du bg4
ecran_gain = False  # Variable qui affiche l'écran de fin des mini-jeux
ok = True  # Variable de verification si les jeux sont en cours
course = False  # Variable de qui fait courir le personnage du bg3 si la bonne touche est appuyé
ecran_debut = False  # Variable qui affiche l'écran avant le lancement des jeux
droit2 = False  # Variable qui fait aller le personnage du bg2 vers la droite
gauche2 = False  # Variable qui fait aller le personnage du bg2 vers la gauche
saut = False  # Variable qui autorise le saut du personnage du bg2
pos_joueur = False  # Variable qui verifie que le personnage soit sur le sol ou pas


# Fonction du bouton de l'écran d'accueil
def accueil():
    global ecran_accueil, run, but_activer  # Définir variable global
    ecran_accueil = False  # Fermeture de l'écran d'accueil
    run = True  # Activation des touches du clavier
    but_activer = True  # Activation des boutons


# Fonction qui sauvegarde le nombre de coins
def save_file():
    file1 = open("file/coins", 'w')  # ouverture du fichier des coins en mode écriture
    file1.write(str(coins))  # Mise à jour du fichier de coins
    file1.close()  # Fermeture du fichier de coins


# Fonction d'augmentation de la mise
def plus():
    global bet, erreur  # Définir variable global
    erreur = "READY"  # Variable erreur mis a READY
    if bet == 64:  # Si la variable mise (bet) vaut 64
        erreur = "Max bet atteint"  # Erreur retourne une erreur
    if bet != 64:  # Si la variable mise (bet) est different de 64
        pygame.mixer.Sound.play(audio4)  # Le son est joué
        bet = bet * 2  # La variable mise (bet) est doublée


# Fonction de diminution de la mise
def moins():
    global bet, erreur  # Définir variable global
    erreur = "READY"  # Variable erreur mis a READY
    if bet == 1:  # Si la variable mise (bet) vaut 1
        erreur = "Min bet atteint"  # Erreur retourne une erreur
    if bet != 1:  # Si la variable mise (bet) est different de 1
        pygame.mixer.Sound.play(audio4)  # Le son est joué
        bet = bet // 2  # La variable mise (bet) est divisée par 2


# Fonction de mise au maximum de la mise
def maxi():
    global bet, erreur  # Définir variable global
    erreur = "READY"  # Variable erreur mis a READY
    if bet == 64:  # Si la variable mise (bet) vaut 64
        erreur = "Bet déjà au max"  # Erreur retourne une erreur
    if bet != 64:  # Si la variable mise (bet) est different de 64
        pygame.mixer.Sound.play(audio4)  # Le son est joué
        bet = 64  # La variable bet vaut 64


# Fonction de retour à la machine à sous et ferme la notice
def back_notice():
    global image_visible, text_visible, but_visible, run, text2_visible, but_activer  # Définir variable global
    image_visible = False  # L'image de la notice s'enlève
    text_visible = True  # Le texte réapparait
    text2_visible = True  # Le texte des coins réapparait
    but_visible = False  # Le bouton de retour à la machine à sous disparait
    run = True  # Reactivation des touches du clavier
    but_activer = True  # Reactivation des boutons de la machine à sous


# Fonction ouverture de la notice
def notice():
    global image_visible, text_visible, but_visible, run, text2_visible, but_activer  # Définir variable global
    image_visible = True  # L'image de la notice s'affiche
    text_visible = False  # Le texte disparait
    text2_visible = False  # Le texte des coins disparait
    but_visible = True  # Le bouton de retour à la machine à sous apparait
    run = False  # Désactivation des touches du clavier
    but_activer = False  # Désactivation des boutons de la machine à sous


# Fonction retour à la machine à sous et fermeture du menu 1
def back_menu1():
    global image_visible1, text_visible, but_visible1, run, but_activer  # Définir variable global
    image_visible1 = False  # L'image du menu1 s'enlève
    text_visible = True  # Le text réapparait
    but_visible1 = False  # Le bouton de retour à la machine à sous disparait
    run = True  # Reactivation des touches du clavier
    but_activer = True  # Reactivation des boutons de la machine à sous


# Fonction ouverture du menu 1
def menu1():
    global image_visible1, text_visible, but_visible1, run, but_activer  # Définir variable global
    image_visible1 = True  # L'image du menu1 s'affiche
    text_visible = False   # Le texte disparait
    but_visible1 = True  # Le bouton de retour à la machine à sous apparait
    run = False  # Désactivation des touches du clavier
    but_activer = False  # Désactivation des boutons de la machine à sous


# Fonction lancement de la machine à sous
def tourne():
    # Définir variable global
    global coins, erreur, jackpot_visible, bigwin_visible, tour, lst_aleatoire, bloquer, but_visible1, v_coins
    if not bloquer:  # Si les rouleaux ne tournent pas
        pygame.mixer.Sound.play(audio3)  # Le son est joué
        bloquer = True  # Les rouleaux tournent et bloquage des boutons
        jackpot_visible = False  # Le jackpot est enlevé
        bigwin_visible = False  # Le bigwin est désactivé
        erreur = "READY"  # Aucune erreur
        price = 5*bet  # Le prix du tour est à 5*la mise
        if coins >= price:  # Si le joueur a suffisamment de coins
            coins = coins - price  # La mise jouée est enlevé de ces coins
            v_coins = str(coins) + " $"  # Met le nombre de coins dans la variable du texte du cadre rouge et jaune
            save_file()  # Sauvegarde des coins
            choix = random.randint(1, 13)  # Tirage aléatoire du premier rouleau
            choix1 = random.randint(1, 13)  # Tirage aléatoire du second rouleau
            choix2 = random.randint(1, 13)  # Tirage aléatoire du troisième rouleau
            lst_aleatoire = [choix, choix1, choix2]  # Choix aléatoire tiré mis dans une liste
            tour = True  # Démarrage de l'animation des rouleaux et des potentiels gains
            lst_aleatoire.sort()  # Triage de la liste des choix aléatoire obtenue
        else:  # si le joueur n'a pas suffisamment de coins
            erreur = "Fond insuffisant"  # Erreur écrit une erreur
            bloquer = False  # Déblocage des boutons


# Fonction pour recommencer le jeu
def try_again():
    # Définir variable global
    global bg1, bg2, bg3, bg4, ecran_gain, resultat, resultat_coins, ecran_debut  # Définir variable globale
    if bg1:  # Si le jeu 1 est en cours
        j1()  # appel de la fonction du démarrage du jeu 1
    if bg2:  # Si le jeu 2 est en cours
        j2()  # appel de la fonction du démarrage du jeu 2
    if bg3:  # Si le jeu 3 est en cours
        j3()  # appel de la fonction du démarrage du jeu 3
    if bg4:  # Si le jeu 4 est en cours
        j4()  # appel de la fonction du démarrage du jeu 4
    ecran_debut = False  # Désactivation de l'écran de debut
    ecran_gain = False  # Désactivation de l'écran de fin
    resultat = ""  # Variable du contenu du texte qui affiche le resultat remis à 0
    resultat_coins = 0  # Remise à 0 du résultat des gains de coins


# Fonction pour quitter le jeu
def quitter():
    # Définir variable global
    global bg1, bg2, bg3, bg4, ecran_gain, resultat, resultat_coins, ecran_debut, text2_visible, croix, v_coins
    if bg1:  # Si le jeu 1 est en cours
        bg1 = False  # Ferme le jeu 1
    if bg2:  # Si le jeu 2 est en cours
        bg2 = False  # Ferme le jeu 2
    if bg3:  # Si le jeu 3 est en cours
        bg3 = False  # Ferme le jeu 3
    if bg4:  # Si le jeu 4 est en cours
        bg4 = False  # Ferme le jeu 4
    ecran_gain = False  # Désactivation de l'écran de fin
    ecran_debut = False  # Désactivation de l'écran de debut
    text2_visible = True  # Affichage du texte des coins
    croix = False  # Fermeture du bouton de la croix
    resultat = ""  # Variable du contenu du texte qui affiche le resultat remis à 0
    resultat_coins = 0  # Remise à 0 du résultat des gains de coins
    v_coins = str(coins) + " $"  # Met le nombre de coins dans la variable du texte du cadre rouge et jaune


# Fonction lancement mini-jeux 1
def j1():
    # Définir variable global
    global bg1, x_bg, y_perso, jump, x_obj, compte_pts, croix, ok, moins_pixel, ecran_debut, temps_activation, touche
    temps_activation = 0  # Temps avant que les boutons de l'écran du debut soit utilisable
    ecran_debut = True  # Affichage de l'écran de debut
    bg1 = True  # Affichage du fond du jeu numero 1
    x_bg = 0  # Mise à 0 du fond du jeu 1
    y_perso = 445  # Mise du personnage 1 du bg1 à son point d'origine
    x_obj = 1500  # Mise de l'ennemie du bg1 à son point d'origine
    jump = False  # Désactivation du saut
    compte_pts = 0  # Mise à 0 du nombre de points
    croix = True  # Affichage du bouton croix
    ok = True  # Activation du jeu
    moins_pixel = 20  # mise à 20 du nombre de pixels que va perdre le X du fond du bg1
    touche = "| ^ |"  # Variable du texte qui affiche les touches


# Fonction de verification des collisions du jeu 1
def check_collision(sprite, group):
    # Retourne si oui ou non une collision a lieu
    return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)


# Fonction lancement mini-jeux 2
def j2():
    # Définir variable global
    global bg2, text2_visible, ok, ecran_debut, temps_activation, compte_s, compte_pts_bg2, compteur_saut2, y_bg2, \
        vitesse, verif_precedente, y_sol, x_obj2, y_obj2, x_obj2_1, y_obj2_1, x_perso2, verif_apres, verif_obj, touche
    temps_activation = 0  # Temps avant que les boutons de l'écran du debut soit utilisable
    ecran_debut = True  # Affichage de l'écran de debut
    bg2 = True  # Affichage du fond du jeu numero 2
    text2_visible = True  # Texte des coins s'enlève
    ok = True  # Activation du jeu
    compte_s = 0  # Remise à 0 de la variable de verification si le saut est en cours
    compte_pts_bg2 = 0  # Remise à 0 du compteur les points obtenue
    y_bg2 = 0  # Remise à 0 de la position du fond du bg2
    vitesse = 10  # Vitesse du personnage mis à 10
    compteur_saut2 = 0  # Remise à 0 du compteur de saut
    verif_precedente = 0  # Variable de récuperation de la position en Y des objets du bg2
    x_perso2 = 560  # Remise du personnage du bg2 à sa position d'origine
    y_sol = 626  # Remise du sol du bg2 à sa position d'origine
    x_obj2 = 500  # Remise de la position en X de l'objet 1 du bg2 a sa position d'origine
    y_obj2 = 350  # Remise de la position en Y de l'objet 1 du bg2 a sa position d'origine
    x_obj2_1 = 700  # Remise de la position en X de l'objet 2 du bg2 a sa position d'origine
    y_obj2_1 = 50  # Remise de la position en Y de l'objet 2 du bg2 a sa position d'origine
    verif_apres = 0  # Remise à 0 de la variable de verification du joueur par rapport aux objets du bg2
    verif_obj = 0  # Remise à 0 de la variable de verification des objets du bg2
    touche = "| < | ESPACE | > |"  # Variable du texte qui affiche les touches


# Fonction lancement mini-jeux 3
def j3():
    global bg3, text2_visible, ok, ecran_debut, temps_activation, touche  # Définir variable global
    temps_activation = 0  # Temps avant que les boutons de l'écran du debut soit utilisable
    ecran_debut = True  # Affichage de l'écran de debut
    bg3 = True  # Affichage du fond du jeu numero 3
    text2_visible = False  # Texte des coins s'enlève
    ok = True  # Activation du jeu
    touche = "| ESPACE |"  # Variable du texte qui affiche les touches


# Fonction lancement mini-jeux 4
def j4():
    # Définir variable global
    global bg4, v_coins, y_bg4, x_perso4, y_perso4, compte_nb_bg, verif_cote, y_obj_bg4, seconde, croix, ok, \
        ecran_debut, temps_activation, touche
    temps_activation = 0  # Temps avant que les boutons de l'écran du debut soit utilisable
    ecran_debut = True  # Affichage de l'écran de debut
    bg4 = True  # Affichage du fond du jeu numero 4
    seconde = 20  # Mise à 20 (secondes) la variable du temps du jeu 4
    v_coins = str(seconde) + " s"  # Affichage du temps avec le texte des coins
    y_bg4 = 0  # Remise à 0 la position du fond du bg4
    x_perso4 = 550  # Remise de la position en X du personnage du bg2 à sa position d'origine
    y_perso4 = 300  # Remise de la position en Y du personnage du bg2 à sa position d'origine
    compte_nb_bg = 0  # Remise à 0 du compteur de fond qui ont défilé
    verif_cote = 0  # Remise à 0 la variable de verification du joueur du bg4 par rapport à la ligne d'arriver
    y_obj_bg4 = -272  # Remise du fond du bg4 à sa position d'origine
    croix = True  # Variable qui affiche le bouton de la croix
    ok = True  # Activation du jeu
    touche = "| < | > |"  # Variable du texte qui affiche les touches


def croix_active():
    # Définir variable global
    global bg1, bg2, bg3, bg4, croix, text2_visible, coins, v_coins, ecran_gain, resultat_coins, resultat, compte_pts, \
        ok, moins_pixel, compteur_saut, seconde, ecran_debut
    if bg1:  # Si bg1 activé
        resultat_coins = compte_pts  # Récuperation des gains du jeu 1
        coins = coins + compte_pts  # Ajout des gains aux coins
        j1()  # Relance du jeu 1 afin de remettre les variables à 0
        ok = False  # Désactivation du OK car fin du jeu
        moins_pixel = 0  # Remise à 0 de la variable du décalage du nombre de pixels des élement du bg1
        compteur_saut = 0  # Remise à 0 du nombre de sauts au cas où le personnage est en saut lors de l'activation
        save_file()  # Sauvegarde des coins
    if bg2:  # Si bg1 activé
        resultat_coins = compte_pts_bg2  # Récuperation des gains du jeu 2
        coins = coins + resultat_coins  # Ajout des gains aux coins
        save_file()  # Sauvegarde des coins
        j2()  # Relance du jeu 2 afin de remettre les variables à 0
    if bg4:  # Si bg1 activé
        ecran_debut = False  # Désactivation de l'écran de debut
        seconde = 0  # Mise à 0 des secondes, car pas de gain si le joueur quitte le jeu
    resultat = "PERDU"  # Variable qui affiche perdu avec le texte qui indique le resultat
    croix = False  # Croix est désactivé
    text2_visible = True  # Text2_visible est réactivé
    v_coins = str(coins) + " $"  # Met le nombre de coins dans la variable du texte du cadre rouge et jaune
    ecran_gain = True  # Affichage de l'écran de fin
    ecran_debut = False  # Désactivation de l'écran de debut


pygame.display.set_caption("Machine à sous Olympique")  # Titre de la fenêtre
icon = pygame.image.load("assets/logo.ico")  # Logo de la fenêtre
pygame.display.set_icon(icon)  # Affectation et affichage du logo
# Taille de la fenêtre avec les variables SCREEN_WIDTH et SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Récupération de la planche d'images de la machine à sous
machine_a_sous_tile = pygame.image.load("assets/machine_a_sous_tile.png").convert_alpha()

# Récupération de la planche d'images de la machine à sous
perso1 = pygame.image.load("assets1/perso1.png").convert_alpha()
# Récupération de la planche d'images de la machine à sous
perso2 = pygame.image.load("assets2/perso2.png").convert_alpha()
# Récupération de la planche d'images de la machine à sous
perso3 = pygame.image.load("assets3/perso3.png").convert_alpha()
# Récupération de la planche d'images de la machine à sous
perso3_1 = pygame.image.load("assets3/perso3_1.png").convert_alpha()
# Récupération de la planche d'images de la machine à sous
perso3_2 = pygame.image.load("assets3/perso3_2.png").convert_alpha()
# Récupération de la planche d'images de la machine à sous
perso3_3 = pygame.image.load("assets3/perso3_3.png").convert_alpha()
# Récupération de la planche d'images de la machine à sous
perso4 = pygame.image.load("assets4/perso4.png").convert_alpha()

# Récuperation de l'image de fond de l'écran d'accueil
img_ecran_acceuil = pygame.image.load("assets/fond_ecran_acceuil.png").convert_alpha()
# Positionnement de l'image de fond de l'écran d'accueil
img_ecran_acceuil_rect = img_ecran_acceuil.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
# Récuperation de l'image de la notice
notice_image = pygame.image.load("assets/notice.png").convert_alpha()
# Positionnement de l'image de la notice
notice_rect = notice_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
# Récuperation de l'image du menu1
menu1_image = pygame.image.load("assets/menu1.png").convert_alpha()
# Positionnement de l'image du menu1
menu1_rect = menu1_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

# Récuperation de l'image du bouton de la croix
img_croix = pygame.image.load("assets/croix.png").convert_alpha()
# Positionnement de l'image de la croix
img_croix_rect = img_croix.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
# Récuperation image du bouton de l'écran d'accueil
button_image = pygame.image.load("assets/bouton_ecran_acceuil.png").convert_alpha()

logo1 = pygame.image.load("assets/logo_j1.png").convert_alpha()  # Récuperation logo jeu 1
logo1_rect = logo1.get_rect(center=(SCREEN_WIDTH // 2 - 135, SCREEN_HEIGHT // 2 - 115))  # Positionnement du logo jeu 1

logo2 = pygame.image.load("assets/logo_j2.png").convert_alpha()  # Récuperation logo jeu 2
logo2_rect = logo2.get_rect(center=(SCREEN_WIDTH // 2 + 165, SCREEN_HEIGHT // 2 - 115))  # Positionnement du logo jeu 2

logo3 = pygame.image.load("assets/logo_j3.png").convert_alpha()  # Récuperation logo jeu 3
logo3_rect = logo3.get_rect(center=(SCREEN_WIDTH // 2 - 135, SCREEN_HEIGHT // 2 + 80))  # Positionnement du logo jeu 3

logo4 = pygame.image.load("assets/logo_j4.png").convert_alpha()  # Récuperation logo jeu 4
logo4_rect = logo4.get_rect(center=(SCREEN_WIDTH // 2 + 165, SCREEN_HEIGHT // 2 + 80))  # Positionnement du logo jeu 4

lumiere_image = pygame.image.load("assets/lumiere1.png").convert_alpha()  # Récuperation de la 1ère image de lumière
# Récuperation de la seconde image de lumière
lumiere1_image = pygame.image.load("assets/lumiere2.png").convert_alpha()  # Récuperation de la 2ème image de lumière
# Récuperation de la troisième image de lumière
lumiere2_image = pygame.image.load("assets/lumiere3.png").convert_alpha()  # Récuperation de la 3ème image de lumière
# Récuperation de la quatrième image de lumière
lumiere3_image = pygame.image.load("assets/lumiere4.png").convert_alpha()  # Récuperation de la 4ème image de lumière
# Récuperation de la cinquième image de lumière
lumiere4_image = pygame.image.load("assets/lumiere5.png").convert_alpha()  # Récuperation de la 5ème image de lumière
# Récuperation de la sixième image de lumière
lumiere5_image = pygame.image.load("assets/lumiere6.png").convert_alpha()  # Récuperation de la sixième image de lumière
# positionnement des images de lumière
lumiere_rect = lumiere_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

jackpot_image = pygame.image.load("assets/jackpot.png").convert_alpha()  # Récuperation de l'image du jackpot
bigwin_image = pygame.image.load("assets/bigwin.png").convert_alpha()  # Récuperation de l'image du bigwin
# Positionnement des images de gain
win_rect = jackpot_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 256))

fond_mise = pygame.image.load("assets/fond_mise.png").convert_alpha()  # Récuperation du fond de la mise
# Positionnement du fond de la mise
fond_mise_rect = fond_mise.get_rect(center=(SCREEN_WIDTH // 2 - 422, SCREEN_HEIGHT // 2 + 268))

fond_coins = pygame.image.load("assets/fond_coins.png").convert_alpha()  # Récuperation du fond des coins
# Positionnement du fond des coins
fond_coins_rect = fond_coins.get_rect(center=(SCREEN_WIDTH // 2 - 410, SCREEN_HEIGHT // 2 - 255))

fond_erreur = pygame.image.load("assets/fond_erreur.png").convert_alpha()  # Récuperation du fond des erreurs
# Positionnement du fond dse erreur
fond_erreur_rect = fond_erreur.get_rect(center=(SCREEN_WIDTH // 2 + 2, SCREEN_HEIGHT // 2 + 270))

img_bg1 = pygame.image.load("assets1/fond_j1.png").convert_alpha()  # Récuperation de l'image de fond du jeu 1
img_bg2 = pygame.image.load("assets2/fond_j2.png").convert_alpha()  # Récuperation de l'image de fond du jeu 2
# Positionnement de l'image de fond du jeu 2
img_bg2_rect = img_bg2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
img_bg3 = pygame.image.load("assets3/fond_j3.png").convert_alpha()  # Récuperation de l'image de fond du jeu 3
# Positionnement de l'image de fond du jeu 3
img_bg3_rect = img_bg3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
img_bg4 = pygame.image.load("assets4/fond_j4.png").convert_alpha()  # Récuperation de l'image de fond du jeu 4

# Récuperation elements jeux
# Récuperation du fond de l'écran de gain et de debut
img_gain = pygame.image.load("assets/ecran_gain.png").convert_alpha()
# Positionnement du fond de l'écran de gain et de debut
img_gain_rect = img_gain.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

img_haie = pygame.image.load("assets1/haie.png").convert_alpha()  # Récuperation de l'objet haie (ennemie) du jeu 1

img_wall = pygame.image.load("assets2/mur.png").convert_alpha()  # Récuperation de l'objet 1er mur du jeu 2

img_wall1 = pygame.image.load("assets2/mur1.png").convert_alpha()  # Récuperation de l'objet 2ème mur du jeu 2

img_sol = pygame.image.load("assets2/bas.png").convert_alpha()  # Récuperation de l'objet sol du jeu 2

img_stone = pygame.image.load("assets2/roche.png").convert_alpha()  # Récuperation de l'objet pierre du jeu 2

img_drapeau = pygame.image.load("assets3/drapeau.png").convert_alpha()  # Récuperation de l'objet drapeau du jeu 3
# Positionnement de l'objet drapeau du jeu 3
img_drapeau_rect = img_drapeau.get_rect(center=(SCREEN_WIDTH // 2 + 510, SCREEN_HEIGHT // 2 + 100))

img_fin = pygame.image.load("assets4/fin.png").convert_alpha()  # Récuperation de l'objet ligne d'arriver du jeu 4

# Récuperation des sons
audio = pygame.mixer.Sound("sounds/slot_sound.mp3")  # Sons des rouleaux
audio1 = pygame.mixer.Sound("sounds/win.mp3")  # Sons de jackpot
audio2 = pygame.mixer.Sound("sounds/win2.mp3")  # Sons de bigwin
audio3 = pygame.mixer.Sound("sounds/coinsound.mp3")  # Sons coins
audio4 = pygame.mixer.Sound("sounds/coinsound2.mp3")  # Sons de mise

tiles = []  # Récupération des images correspondant aux tiles (tuiles) de l'arrière-plan de la machine à sous
tiles_perso_j1 = []  # Récupération des images correspondant aux tiles (tuiles) du personnage du jeu 1
tiles_perso_j2 = [[], [], []]  # Récupération des images correspondant aux tiles (tuiles) du personnage du jeu 2
tiles_perso_j3_1 = []  # Récupération des images correspondant aux tiles (tuiles) du personnage 1 du jeu 3
tiles_perso_j3_2 = []  # Récupération des images correspondant aux tiles (tuiles) du personnage 2 du jeu 3
tiles_perso_j3_3 = []  # Récupération des images correspondant aux tiles (tuiles) du personnage 3 du jeu 3
tiles_perso_j3_4 = []  # Récupération des images correspondant aux tiles (tuiles) du personnage 4 du jeu 3
tiles_perso_j4 = []  # Récupération des images correspondant aux tiles (tuiles) du personnage du jeu 4

# Boutons de la fenêtre
# Bouton pour lancer la machine à sous
button = Button((SCREEN_WIDTH - 150) // 2 + 390, (SCREEN_HEIGHT - 60) // 2 + 275, 125, 60,
                "SPIN", action=tourne, color=GREEN, color_border=LIGHT_GREEN, border_ext=28,
                border_int=26, color_font=DARK_GREEN, taille=36)

# Bouton pour ouvrir la notice
button1 = Button((SCREEN_WIDTH - 150) // 2 + 580,
                 (SCREEN_HEIGHT - 60) // 2 - 275, 60, 60, "?", action=notice,
                 color=BLUE, color_border=LIGHT_BLUE, border_ext=28, border_int=26, color_font=WHITE, taille=36)

# Bouton pour ouvrir le menu1
button2 = Button((SCREEN_WIDTH - 150) // 2 + 340, (SCREEN_HEIGHT - 60) // 2 - 275, 180, 60,
                 "MINI-JEUX", action=menu1, color=GREEN, color_border=LIGHT_GREEN, border_ext=28,
                 border_int=26, color_font=DARK_GREEN, taille=36)

# Bouton pour augmenter la mise (bet)
button3 = Button((SCREEN_WIDTH - 150) // 2 - 272,
                 (SCREEN_HEIGHT - 60) // 2 + 275, 25, 25, "^", action=plus,
                 color=GREY, color_border=LIGHT_GREY, border_ext=0, border_int=0, color_font=BLACK, taille=20)

# Bouton pour diminuer la mise (bet)
button4 = Button((SCREEN_WIDTH - 150) // 2 - 272,
                 (SCREEN_HEIGHT - 60) // 2 + 297, 25, 25, "v", action=moins,
                 color=GREY, color_border=LIGHT_GREY, border_ext=0, border_int=0, color_font=BLACK, taille=20)

# Bouton pour mettre la mise (bet) au maximum
button5 = Button((SCREEN_WIDTH - 150) // 2 - 250,
                 (SCREEN_HEIGHT - 60) // 2 + 275, 47, 47, "MAX", action=maxi,
                 color=GREY, color_border=LIGHT_GREY, border_ext=0, border_int=0, color_font=BLACK, taille=20)

# Bouton de fermeture de la notice
button6 = Button((SCREEN_WIDTH - 150) // 2 + 580,
                 (SCREEN_HEIGHT - 60) // 2 + 275, 60, 60, "<-", action=back_notice,
                 color=BLUE, color_border=LIGHT_BLUE, border_ext=28, border_int=26, color_font=WHITE, taille=36)

# Bouton de fermeture du menu1
button7 = Button((SCREEN_WIDTH - 150) // 2 + 580, (SCREEN_HEIGHT - 60) // 2 + 275, 60, 60,
                 "<-", action=back_menu1, color=GREEN, color_border=LIGHT_GREEN, border_ext=28,
                 border_int=26, color_font=DARK_GREEN, taille=36)

# Bouton de l'écran d'accueil qui permet de rentrer dans le jeu (machine à sous)
button8 = Button1(button_image, SCREEN_WIDTH // 2 - 235, SCREEN_HEIGHT // 2 + 75, action=accueil)

# Bouton pour commencer le premier jeu
button9 = Button((SCREEN_WIDTH - 150) // 2 - 150, (SCREEN_HEIGHT - 60) // 2 - 30, 180, 60,
                 "COMMENCER", action=j1, color=GREEN, color_border=LIGHT_GREEN, border_ext=28,
                 border_int=26, color_font=DARK_GREEN, taille=36)

# Bouton pour commencer le second jeu
button10 = Button((SCREEN_WIDTH - 150) // 2 + 150, (SCREEN_HEIGHT - 60) // 2 - 30, 180, 60,
                  "COMMENCER", action=j2, color=GREEN, color_border=LIGHT_GREEN, border_ext=28,
                  border_int=26, color_font=DARK_GREEN, taille=36)

# Bouton pour commencer le troisième jeu
button11 = Button((SCREEN_WIDTH - 150) // 2 - 150, (SCREEN_HEIGHT - 60) // 2 + 165, 180, 60,
                  "COMMENCER", action=j3, color=GREEN, color_border=LIGHT_GREEN, border_ext=28,
                  border_int=26, color_font=DARK_GREEN, taille=36)

# Bouton pour commencer le quatrième jeu
button12 = Button((SCREEN_WIDTH - 150) // 2 + 150, (SCREEN_HEIGHT - 60) // 2 + 165, 180, 60,
                  "COMMENCER", action=j4, color=GREEN, color_border=LIGHT_GREEN, border_ext=28,
                  border_int=26, color_font=DARK_GREEN, taille=36)

# Bouton de l'écran d'accueil qui permet de rentrer dans le jeu (machine à sous)
button13 = Button1(img_croix, SCREEN_WIDTH // 2 + 500, SCREEN_HEIGHT // 2 - 325, action=croix_active)

button14 = Button((SCREEN_WIDTH - 150) // 2 - 135,
                  (SCREEN_HEIGHT - 60) // 2 + 45, 200, 60, "RECOMMENCER", action=try_again,
                  color=GREEN, color_border=LIGHT_GREEN, border_ext=0, border_int=0,
                  color_font=WHITE, taille=36)

button15 = Button((SCREEN_WIDTH - 150) // 2 + 85,
                  (SCREEN_HEIGHT - 60) // 2 + 45, 200, 60, "QUITTER", action=quitter,
                  color=GREEN, color_border=LIGHT_GREEN, border_ext=0, border_int=0,
                  color_font=WHITE, taille=36)

button16 = Button((SCREEN_WIDTH - 150) // 2 - 135,
                  (SCREEN_HEIGHT - 60) // 2 + 45, 200, 60, "COMMENCEZ", action=try_again,
                  color=GREEN, color_border=LIGHT_GREEN, border_ext=0, border_int=0,
                  color_font=WHITE, taille=36)

for i in range(16):  # Decoupage image pour arriere plan
    tile = machine_a_sous_tile.subsurface(pygame.Rect(i*c, 0, c, c))  # Découpage de la ligne d'indice 0
    tiles.append(tile)  # Ajout de chaque image dans la liste tiles

for i1 in range(15):  # Decoupage planche personage jeu 1
    tile_p1 = perso1.subsurface(pygame.Rect(i1*152, 0, 152, 235))  # Découpage de la ligne d'indice 0
    tiles_perso_j1.append(tile_p1)   # Ajout de chaque image dans la liste tiles_perso_j1

for i2 in range(3):
    tile_p2 = perso2.subsurface(pygame.Rect(i2*95, 0, 95, 145))
    tiles_perso_j2[0].append(tile_p2)  # Ajout de chaque image dans la liste tiles_perso_j2

for i2_1 in range(16):
    tile_p2 = perso2.subsurface(pygame.Rect(i2_1*95, 145, 95, 145))
    tiles_perso_j2[1].append(tile_p2)  # Ajout de chaque image dans la liste tiles_perso_j2

for i2_2 in range(16):
    tile_p2 = perso2.subsurface(pygame.Rect(i2_2*95, 290, 95, 145))
    tiles_perso_j2[2].append(tile_p2)  # Ajout de chaque image dans la liste tiles_perso_j2

for i3_1 in range(17):
    tile_p3 = perso3.subsurface(pygame.Rect(i3_1*94, 0, 94, 145))
    tiles_perso_j3_1.append(tile_p3)  # Ajout de chaque image dans la liste tiles_perso_j3

for i3_2 in range(17):
    tile_p3_1 = perso3_1.subsurface(pygame.Rect(i3_2*94, 0, 94, 145))
    tiles_perso_j3_2.append(tile_p3_1)  # Ajout de chaque image dans la liste tiles_perso_j3_1

for i3_3 in range(17):
    tile_p3_2 = perso3_2.subsurface(pygame.Rect(i3_3*94, 0, 94, 145))
    tiles_perso_j3_3.append(tile_p3_2)  # Ajout de chaque image dans la liste tiles_perso_j3_2

for i3_4 in range(17):
    tile_p3_3 = perso3_3.subsurface(pygame.Rect(i3_4*94, 0, 94, 145))
    tiles_perso_j3_4.append(tile_p3_3)  # Ajout de chaque image dans la liste tiles_perso_j3_3

for i4 in range(4):
    tile_p4 = perso4.subsurface(pygame.Rect(i4*96, 0, 96, 385))
    tiles_perso_j4.append(tile_p4)  # Ajout de chaque image dans la liste tiles_perso_j4

# Variable boucle principale
running = True  # lancement de la boucle principale

temps_precedent = time.time()  # Variable de récuperation du temps au commencement du programme
# Seconde variable de récuperation du temps au commencement du programme ou on enlève 10
# pour pas avoir de delaie au lancement de la machine à sous
compte_temp = time.time() - 10
compteur_rouleau = 0  # Compteur du nombre d'images affiché pendant l'animation des rouleaux
son = 0  # Variable qui compte le nombre de sons
img = 0  # Variable image du joueur du jeu 1
img2 = 0  # Variable image du joueur du jeu 2
img2_dir = 0  # Variable qui donne le sens de l'image du joueur du jeu 2
img3 = 16  # Variable image du joueur du jeu 3
img3_1 = 16  # Variable image du joueur 2 du jeu 3
img3_2 = 16  # Variable image du joueur 3 du jeu 3
img3_3 = 16  # Variable image du joueur 4 du jeu 3
x_bg = 0  # Variable de la position en X du fond du bg1 (jeu 1)
compteur_saut = 0  # Variable qui compte le nombre de sauts en cours du personnage du jeu 1
compte_pts = 0  # Variable qui compte les points obtenus dans le jeu 1
v_coins = str(coins) + " $"  # Variable qui indique quoi afficher sur le texte des coins
y_bg4 = 0  # Variable de la position en Y du fond du bg4 (jeu 4)
compte_nb_bg = 0  # Variable qui compte le nombre de fonds qui ont defilés sur le bg4 (jeu 4)
verif_cote = 0  # Variable qui verifie quel bras (quelles touches) est activé
choix_perso4 = tiles_perso_j4[0]  # Variable de récuperation de l'image du personnage à afficher sur le bg4
y_obj_bg4 = -272  # Variable de la position en Y de la ligne d'arriver du bg4
seconde = 20  # Variable du compte à rebours du bg4
moins_pixel = 20  # Variable du nombre de pixels à enlever au bg1 dans le jeu 1
resultat = ""  # Variable du resultat à la fin de chaque jeu
resultat_coins = 0  # Variable de récuperation du nombre de coins gagné à la fin de chaque jeu
x_perso3 = 15  # Variable position en X du personnage 1 du bg3
x_perso3_1 = 15  # Variable de la position en X du personnage 2 du bg3
x_perso3_2 = 15  # Variable de la position en X du personnage 3 du bg3
x_perso3_3 = 15  # Variable de la position en X du personnage 4 du bg3
temps_activation = 0  # Variable du temps avant que les boutons de l'écran du debut soit appuyable
y_bg2 = 0  # Variable de la position en Y du fond du bg2 (jeu 2)
vitesse = 10  # Variable du nombre de pixels de déplacement du personnage du bg2
compteur_saut2 = 0  # Variable qui compte le nombre de sauts en cours du personnage du bg2
compte_s = 0  # Variable qui verifie si oui ou non le personnage du bg2 est en saut
compte_pts_bg2 = 0  # Variable qui compte le nombre de points obtenus dans le bg2
verif_precedente = 0  # Variable qui verifie la position du personnage du bg4
verif_apres = 0  # Variable qui verifie la position est sur l'objet du bg4 ou pas
verif_obj = 0  # Variable qui verifie la position de l'objet du bg4
v_droit = 0  # Variable qui verifie si le bouton droit est activé ou pas


while running:  # Boucle principale

    temps_actuel = time.time()  # Récuperation du temps actuel du programme

    # Boucle des événements
    for event in pygame.event.get():

        if event.type == pygame.QUIT:  # Si la fenêtre est fermé la boucle s'arrête
            running = False  # Arrêt de la boucle

        if event.type == pygame.KEYDOWN:  # Si une touche est appuyé
            if event.key == pygame.K_ESCAPE:  # Si la touche ECHAP est appuyé
                running = False  # Arrêt de la boucle
            if run:  # Si les touches clavier sont activés
                if event.key == pygame.K_SPACE:  # Si la touche ESPACE est appuyé
                    tourne()  # La fonction tourne se lance
                if event.key == pygame.K_UP:  # Si la touche FLECHE DE HAUT est appuyé
                    plus()  # La fonction plus se lance
                if event.key == pygame.K_DOWN:  # Si la touche FLECHE DU BAS est appuyé
                    moins()  # La fonction moins se lance
                if event.key == pygame.K_RIGHT:  # Si la touche FLECHE DE DROITE est appuyé
                    maxi()  # La fonction maxi se lance
                if event.key == pygame.K_COMMA:  # Si la touche VIRGULE est appuyé
                    notice()  # La fonction notice se lance
                if event.key == pygame.K_DOLLAR:  # Si la touche DOLLAR est appuyé
                    menu1()  # La fonction menu1 se lance
            if not run and not bg4 and not bg3 and not bg2 and not bg1:  # Si pas de jeux activés
                if event.key == pygame.K_LEFT:  # Si la touche FLECHE DE GAUCHE est appuyé
                    back_notice()  # La fonction back_notice se lance
                    back_menu1()  # La fonction back_menu1 se lance
            if bg1 and not ecran_gain and not bg4 and not bg3 and not bg2:  # Si le jeu 1 est activés
                if event.key == pygame.K_UP and not jump:  # Si FLECHE DU HAUT est appuyé et le saut désactivé
                    jump = True  # Le jump s'active
            if bg2 and not ecran_gain and not bg1 and not bg3 and not bg4:  # Si le jeu 2 est activés
                if event.key == pygame.K_RIGHT:  # Si FLECHE DE DROITE est appuyé
                    droit2 = True  # La direction droite2 est activée
                elif event.key == pygame.K_LEFT:  # Sinon si FLECHE DE GAUCHE est appuyé
                    gauche2 = True   # La direction gauche2 est activée
                if compte_s == 0:  # Si le compteur de saut est à 0 (donc pas de saut en cours)
                    if event.key == pygame.K_SPACE:  # Si ESPACE est appuyé
                        saut = True  # Le saut s'active
            if bg3 and not ecran_gain and not bg4 and not bg2 and not bg1:  # Si le jeu 3 est activés
                if event.key == pygame.K_SPACE:  # Si ESPACE est appuyé
                    course = True  # La course du joueur s'active
            if bg4 and not ecran_gain and not bg3 and not bg2 and not bg1:  # Si le jeu 4 est activés
                # Si FLECHE DE GAUCHE est appuyé et le bras droit est activé ou aucun bras n'est activé
                if event.key == pygame.K_LEFT and v_droit == 0:
                    gauche = True  # L'image du bras gauche S'affiche
                # Si FLECHE DE DROITE est appuyé et bras droit désactivé
                if event.key == pygame.K_RIGHT and v_droit == 1:
                    droit = True  # L'image du bras gauche S'affiche
        if event.type == pygame.KEYUP:  # Si FLECHE DU HAUT est appuyé
            if bg2 and not bg1 and not bg3 and not bg4:  # Si jeu 2 est activé
                if event.key == pygame.K_RIGHT:  # Si FLECHE DE DROITE est relâché
                    droit2 = False  # La direction droite2 est désactivée
                if event.key == pygame.K_LEFT:  # Si FLECHE DE GAUCHE est relâché
                    gauche2 = False  # La direction gauche2 est désactivée
        if but_activer:  # Si les boutons sont activés
            button.handle_event(event)  # Le bouton peut être appuyé
            button1.handle_event(event)  # Le bouton peut être appuyé
            button2.handle_event(event)  # Le bouton peut être appuyé
            button3.handle_event(event)  # Le bouton peut être appuyé
            button4.handle_event(event)  # Le bouton peut être appuyé
            button5.handle_event(event)  # Le bouton peut être appuyé
        if but_visible:  # Si le bouton de la notice est visible
            button6.handle_event(event)  # Le bouton peut être appuyé
        # Si les boutons du menu1 sont visibles
        if but_visible1 and not ecran_gain and not ecran_debut and not bg1 and not bg2 and not bg3 and not bg4:
            button7.handle_event(event)  # Le bouton peut être appuyé
            button9.handle_event(event)  # Le bouton peut être appuyé
            button10.handle_event(event)  # Le bouton peut être appuyé
            button11.handle_event(event)  # Le bouton peut être appuyé
            button12.handle_event(event)  # Le bouton peut être appuyé
        if ecran_accueil:  # Si l'écran d'accueil est visible
            button8.handle_event(event)  # Le bouton peut être appuyé
        if bg1 or bg2 or bg3 or bg4:  # Si un des 4 jeux est visible
            button13.handle_event(event)  # Le bouton peut être appuyé
        if ecran_gain and not ecran_debut:  # Si l'écran de gain est visible
            button14.handle_event(event)  # Le bouton peut être appuyé
            button15.handle_event(event)  # Le bouton peut être appuyé
        if ecran_debut and not ecran_gain and temps_activation == 1:  # Si l'écran du debut est visible
            button15.handle_event(event)  # Le bouton peut être appuyé
            button16.handle_event(event)  # Le bouton peut être appuyé

    # Double boucle pour afficher le contenu du tableau
    for colonne in range(len(tile_map[0])):
        for ligne in range(len(tile_map)):
            screen.blit(tiles[tile_map[ligne][colonne]], (c*colonne, c*ligne))  # Affiche du tableau sur la fenêtre

    # Text
    font = pygame.font.Font(None, 36)  # Création de la police 1
    text = font.render("X" + str(bet), True, WHITE)  # Créer le texte avec la police crée précèdement
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2 - 375, SCREEN_HEIGHT // 2 + 270))  # Positionnement du texte

    font1 = pygame.font.Font(None, 60)  # Création de la police 2
    text1 = font1.render(erreur, True, ORANGE)  # Créer le texte avec la police crée précèdement
    text_rect1 = text1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 270))  # Positionnement du texte

    text2 = font.render(str(v_coins), True, ORANGE)  # Créer le texte avec la police crée précèdement
    text_rect2 = text2.get_rect(center=(SCREEN_WIDTH // 2 - 410, SCREEN_HEIGHT // 2 - 255))  # Positionnement du texte

    text3 = font.render(str(bet * 5) + " $", True, WHITE)  # Créer le texte avec la police crée précèdement
    text_rect3 = text3.get_rect(center=(SCREEN_WIDTH // 2 - 450, SCREEN_HEIGHT // 2 + 270))  # Positionnement du texte

    text4 = font.render(resultat, True, WHITE)  # Créer le texte avec la police crée précèdement
    text_rect4 = text4.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))  # Positionnement du texte

    # Créer le texte avec la police crée précèdement
    text5 = font.render("Vous avez gagné " + str(resultat_coins) + " $", True, WHITE)
    text_rect5 = text5.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))  # Positionnement du texte

    font2 = pygame.font.Font(None, 45)  # Création de la police 3
    font3 = pygame.font.Font(None, 28)  # Création de la police 4
    # Créer le texte avec les polices créent précèdement
    text6 = font2.render("Saut de haie", True, WHITE)
    # Créer le texte avec les polices créent précèdement
    text6_0_1 = font3.render("| ^ |", True, WHITE)
    # Créer le texte avec les polices créent précèdement
    text6_1 = font2.render("Escalade", True, WHITE)
    # Créer le texte avec les polices créent précèdement
    text6_1_1 = font3.render("| < | Espace | > |", True, WHITE)
    # Créer le texte avec les polices créent précèdement
    text6_2 = font2.render("Athlétisme", True, WHITE)
    # Créer le texte avec les polices créent précèdement
    text6_2_2 = font3.render("| Espace |", True, WHITE)
    # Créer le texte avec les polices créent précèdement
    text6_3 = font2.render("Natation", True, WHITE)
    # Créer le texte avec les polices créent précèdement
    text6_3_3 = font3.render("| < | > |", True, WHITE)

    # Positionnement du texte
    text_rect6 = text6.get_rect(center=(SCREEN_WIDTH // 2 - 330, SCREEN_HEIGHT // 2 - 115))
    text_rect6_0_1 = text6_0_1.get_rect(center=(SCREEN_WIDTH // 2 - 330, SCREEN_HEIGHT // 2 - 90))
    text_rect6_1 = text6_1.get_rect(center=(SCREEN_WIDTH // 2 + 330, SCREEN_HEIGHT // 2 - 115))
    text_rect6_1_1 = text6_1_1.get_rect(center=(SCREEN_WIDTH // 2 + 330, SCREEN_HEIGHT // 2 - 90))
    text_rect6_2 = text6_2.get_rect(center=(SCREEN_WIDTH // 2 - 320, SCREEN_HEIGHT // 2 + 80))
    text_rect6_2_2 = text6_2_2.get_rect(center=(SCREEN_WIDTH // 2 - 320, SCREEN_HEIGHT // 2 + 105))
    text_rect6_3 = text6_3.get_rect(center=(SCREEN_WIDTH // 2 + 330, SCREEN_HEIGHT // 2 + 80))
    text_rect6_3_3 = text6_3_3.get_rect(center=(SCREEN_WIDTH // 2 + 330, SCREEN_HEIGHT // 2 + 105))

    font3 = pygame.font.Font(None, 45)  # Changement de la taille de la police du text
    font3.set_underline(True)  # Surligne le texte
    text7 = font3.render("Touches", True, WHITE)  # Créer le texte avec la police crée précèdement
    text7_1 = font2.render(str(touche), True, WHITE)  # Créer le texte avec la police crée précèdement
    text7_rect = text7.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))  # Positionnement du texte
    text7_1_rect = text7_1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))  # Positionnement du texte

    button.draw(screen)  # Affichage du bouton sur la fenêtre
    button1.draw(screen)  # Affichage du bouton sur la fenêtre
    button2.draw(screen)  # Affichage du bouton sur la fenêtre
    button3.draw(screen)  # Affichage du bouton sur la fenêtre
    button4.draw(screen)  # Affichage du bouton sur la fenêtre
    button5.draw(screen)  # Affichage du bouton sur la fenêtre

    if coins >= 1000000000000:  # Si les coins dépassent 1.000.000.000.000
        coins = 999999999999  # Les coins sont mis à 999.999.999.999 (coins max)
        save_file()  # Sauvegarde des coins

    # Si le temps actuel moins le temps du debut du programme est plus grand ou égal à 1
    if temps_actuel - temps_precedent >= 1:
        temps_precedent = temps_actuel  # Variable du temps du debut du programme devient la valeur du temps actuel
        if ecran_debut:  # Si l'écran du debut est activé
            temps_activation = 1  # Variable temps_activation mise à 1
        if bg2:  # Si le bg2 (jeu 2) est affiché
            if not gauche2 and not droit2 and not saut:  # Si le personnage ne saute pas, ne va ni à droite ou à gauche
                img2_dir = 0  # Variable qui donne le sens de l'image ne donne aucun sens, mais le personnage de face
                img2 = 0  # L'image du personnage du 2 est à 0 soit l'image du personnage de face
        if bg3:  # Si le bg3 (jeu 3) est affiché
            if not course:  # Si le personnage ne court pas (est à l'arrêt)
                img3 = 16  # L'image du personnage du bg3 est à 16 soit l'image du personnage de face
        if bg4 and ok and not ecran_debut:  # Si le bg4 (jeu 4) est affiché
            seconde = seconde - 1  # Le compte à rebours perd 1 seconde
            v_coins = str(seconde) + " s"  # Affichage du compte à rebours sur le texte des coins
            if seconde <= 0:  # Si le compte à rebours atteint 0
                seconde = 0  # Mise à 0 du compte à rebours
                resultat_coins = seconde  # récuperation des gains en fonction du temps restant
                # Activation de la fonction du jeu 4 pour remettre toute les variables du jeu 4 à leurs états d'origine
                j4()
                ecran_debut = False  # Désactivation de l'écran du debut
                ecran_gain = True  # Affichage de l'écran des gains
                ok = False  # Désactivation du jeu
                croix = False  # Disparition du bouton croix
                resultat = "PERDU"  # Le resultat du jeu affiche perdu
        if jackpot_visible and not bg1 and not bg2 and not bg3 and not bg4:  # Si le jackpot est gagné
            if lumiere_gain2:  # Si la lumière du gain 2 est visible
                temps_precedent = temps_actuel - 0.9  # Variable temps du debut devient temps actuel moins 0,9
                lumiere_gain = False  # Lumière gain est désactivée
                lumiere_gain1 = False  # Lumière gain 1 est désactivée
                lumiere_gain2 = False  # Lumière gain 2 est désactivée
                lumiere_gain3 = True  # Lumière gain est activée
            elif lumiere_gain3:  # Sinon si la lumière gain 3 est activée
                temps_precedent = temps_actuel - 0.9  # Variable temps du debut devient temps actuel moins 0,9
                lumiere_gain = False  # Lumière gain est désactivée
                lumiere_gain1 = False  # Lumière gain 1 est désactivée
                lumiere_gain2 = True  # Lumière gain 2 est activée
                lumiere_gain3 = False  # Lumière gain 3 est désactivée
            else:  # Sinon si lumière gain 2 et 3 ne sont pas activé
                temps_precedent = temps_actuel - 0.9  # Variable temps du debut devient temps actuel moins 0,9
                lumiere_gain = False  # Lumière gain est désactivée
                lumiere_gain1 = False  # Lumière gain 1 est désactivée
                lumiere_gain2 = True  # Lumière gain 2 est activée
                lumiere_gain3 = False  # Lumière gain 3 est désactivée
        elif bigwin_visible and not bg1 and not bg2 and not bg3 and not bg4:  # Sinon si bigwin est gagné
            if lumiere_gain:  # Si lumière gain est activé
                temps_precedent = temps_actuel - 0.9  # Variable temps du debut devient temps actuel moins 0,9
                lumiere_gain = False  # Lumière gain est désactivée
                lumiere_gain1 = True  # Lumière gain 1 est activée
                lumiere_gain2 = False  # Lumière gain 2 est désactivée
                lumiere_gain3 = False  # Lumière gain 3 est désactivée
            elif lumiere_gain1:
                temps_precedent = temps_actuel - 0.9  # Variable temps du debut devient temps actuel moins 0,9
                lumiere_gain = True  # Lumière gain est activée
                lumiere_gain1 = False  # Lumière gain 1 est désactivée
                lumiere_gain2 = False  # Lumière gain 2 est désactivée
                lumiere_gain3 = False  # Lumière gain 3 est désactivée
            else:  # Sinon si lumière gain et 1 ne sont pas activé
                temps_precedent = temps_actuel - 0.9  # Variable temps du debut devient temps actuel moins 0,9
                lumiere_gain = True  # Lumière gain est activée
                lumiere_gain1 = False  # Lumière gain 1 est désactivée
                lumiere_gain2 = False  # Lumière gain 2 est désactivée
                lumiere_gain3 = False  # Lumière gain 3 est désactivée
        elif allumer:  # Sinon si allumer est activé
            lumiere_gain = False  # Lumière gain est désactivée
            lumiere_gain1 = False  # Lumière gain 1 est désactivée
            lumiere_gain2 = False  # Lumière gain 2 est désactivée
            lumiere_gain3 = False  # Lumière gain 3 est désactivée
            allumer = False  # Allumer est désactivée
        else:  # Sinon si jackpot, bigwin et allumer ne sont pas activé
            lumiere_gain = False  # Lumière gain est désactivée
            lumiere_gain1 = False  # Lumière gain 1 est désactivée
            lumiere_gain2 = False  # Lumière gain 2 est désactivée
            lumiere_gain3 = False  # Lumière gain 3 est désactivée
            allumer = True  # Allumer est activé

    if tour:  # Si tour est activé
        if compteur_rouleau < 50:  # Si compteur est plus petit que 50
            # Si le temps actuel moins le temps du debut du programme est plus grand ou égal à 10
            if temps_actuel - compte_temp >= 10:
                aleatoire = random.randint(1, 13)  # Choisis une image aléatoire pour l'animation du rouleau 1
                aleatoire1 = random.randint(1, 13)  # Choisis une image aléatoire pour l'animation du rouleau 2
                aleatoire2 = random.randint(1, 13)  # Choisis une image aléatoire pour l'animation du rouleau 3
                compteur_rouleau = compteur_rouleau + 1  # Ajout de 1 a la variable compteur
        if 75 > compteur_rouleau >= 50:  # Si compteur est compris entre 50 et 75
            # Si le temps actuel moins le temps du debut du programme est plus grand ou égal à 10
            if temps_actuel - compte_temp >= 10:
                aleatoire2 = lst_aleatoire[0]  # Affichage du nombre aleatoire (nombre final) de la liste lst_aleatoire
                aleatoire1 = random.randint(1, 13)  # Choisis une image aléatoire pour l'animation du rouleau 2
                aleatoire = random.randint(1, 13)  # Choisis une image aléatoire pour l'animation du rouleau 3
                compteur_rouleau = compteur_rouleau + 1  # Ajout de 1 a la variable compteur
                if son == 0:  # Si la variable son vaut 0
                    pygame.mixer.Sound.play(audio)  # Le son est joué
                    son = 1  # Variable son vaut 1
        if 100 > compteur_rouleau >= 75:  # Si compteur est compris entre 75 et 100
            # Si le temps actuel moins le temps du debut du programme est plus grand ou égal à 10
            if temps_actuel - compte_temp >= 10:
                aleatoire = lst_aleatoire[1]  # Affichage du nombre aleatoire (nombre final) de la liste lst_aleatoire
                aleatoire1 = random.randint(1, 13)  # Choisis une image aléatoire pour l'animation du rouleau 3
                compteur_rouleau = compteur_rouleau + 1  # Ajout de 1 a la variable compteur
                if son == 1:  # Si la variable son vaut 1
                    pygame.mixer.Sound.play(audio)  # Le son est joué
                    son = 2  # Variable son vaut 2
        if compteur_rouleau == 100:  # Si compteur vaut 100
            compteur_rouleau = 0  # Compteur vaut 0
            aleatoire1 = lst_aleatoire[2]  # Affichage du nombre aleatoire (nombre final) de la liste lst_aleatoire
            if son == 2:  # Si la variable son vaut 2
                pygame.mixer.Sound.play(audio)  # Le son est joué
                son = 0  # Remise a 0 de la variable son
            for gain in lst_verif:  # Pour tous les gains de la liste lst_verif
                if lst_aleatoire == gain:  # Si lst_aleatoire vaut un des gains de la liste lst_verif
                    # Récuperation de la somme du gain avec l'indice du gain de la liste lst_verif
                    gain_coin = recompense[lst_verif.index(gain)]
                    coins = coins + (gain_coin * bet)  # Ajout des gains aux coins fois la mise de depart
                    # Met le nombre de coins dans la variable du texte du cadre rouge et jaune
                    v_coins = str(coins) + " $"
                    save_file()  # Sauvegarde des coins
                    erreur = "+ " + str(gain_coin * bet) + " $"  # Affichage du nombre de coins gagné
                    # Si le gain est 7 7 7 ou 5 7 7 ou 5 5 7 (5 = joker)
                    if lst_aleatoire == [7, 7, 7] or lst_aleatoire == [5, 7, 7] or lst_aleatoire == [5, 5, 7]:
                        jackpot_visible = True  # Jackpot activé
                        pygame.mixer.Sound.play(audio1)  # Le son est joué
                    else:  # Sinon si n'importe quelle autre gain
                        bigwin_visible = True  # Bigwin activé
                        pygame.mixer.Sound.play(audio2)  # Le son est joué
            tour = False  # tour est désactivé
            bloquer = False  # bloquage des boutons est désactivé

    # Récuperation des images des rouleaux de la machine à sous (rouleau 1)
    img_image = pygame.image.load("assets/" + str(aleatoire) + ".png").convert_alpha()
    # Récuperation des images des rouleaux de la machine à sous (rouleau 2)
    img_image1 = pygame.image.load("assets/" + str(aleatoire1) + ".png").convert_alpha()
    # Récuperation des images des rouleaux de la machine à sous (rouleau 3)
    img_image2 = pygame.image.load("assets/" + str(aleatoire2) + ".png").convert_alpha()
    # Positionnement du rouleau 1
    img_rect = img_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 33))
    # Positionnement du rouleau 2
    img_rect1 = img_image1.get_rect(center=(SCREEN_WIDTH // 2 + 256, SCREEN_HEIGHT // 2 + 33))
    # Positionnement du rouleau 3
    img_rect2 = img_image2.get_rect(center=(SCREEN_WIDTH // 2 - 256, SCREEN_HEIGHT // 2 + 33))

    if but_visible:  # Si but est visible (notice visible)
        button6.draw(notice_image)  # Affichage du bouton sur la fenêtre notice

    if but_visible1:  # Si but 1 est visible (menu 1 visible)
        button7.draw(menu1_image)  # Affichage du bouton sur la fenêtre menu1
        button9.draw(menu1_image)  # Affichage du bouton sur la fenêtre menu1
        button10.draw(menu1_image)  # Affichage du bouton sur la fenêtre menu1
        button11.draw(menu1_image)  # Affichage du bouton sur la fenêtre menu1
        button12.draw(menu1_image)  # Affichage du bouton sur la fenêtre menu1

    screen.blit(img_image, img_rect)  # Affichage rouleau 1
    screen.blit(img_image1, img_rect1)  # Affichage rouleau 2
    screen.blit(img_image2, img_rect2)  # Affichage rouleau 3

    screen.blit(fond_mise, fond_mise_rect)  # Affichage fond des mises
    screen.blit(fond_erreur, fond_erreur_rect)  # Affichage fond des erreurs

    if jackpot_visible:  # Si jackpot visible
        screen.blit(jackpot_image, win_rect)  # Affichage image jackpot

    if bigwin_visible:  # Si bigwin visible
        screen.blit(bigwin_image, win_rect)  # Affichage image bigwin

    if allumer:  # Si allumer visible
        screen.blit(lumiere_image, lumiere_rect)  # Affichage lumière
    else:  # Sinon si allumer n'est pas visible
        screen.blit(lumiere1_image, lumiere_rect)  # Afficher lumière 1

    if lumiere_gain:  # Si lumière gain visible
        screen.blit(lumiere2_image, lumiere_rect)  # Afficher lumière 2

    if lumiere_gain1:  # Si lumière gain1 visible
        screen.blit(lumiere3_image, lumiere_rect)  # Afficher lumière 3

    if lumiere_gain2:  # Si lumière gain2 visible
        screen.blit(lumiere4_image, lumiere_rect)  # Afficher lumière 4

    if lumiere_gain3:  # Si lumière gain3 visible
        screen.blit(lumiere5_image, lumiere_rect)  # Afficher lumière 5

    if image_visible:  # Si image visible visible (notice visible)
        screen.blit(notice_image, notice_rect)  # Affichage de l'image de la notice sur la fenêtre

    if image_visible1:  # Si image visible 1 visible (menu1 visible)
        screen.blit(menu1_image, menu1_rect)  # Affichage de l'image du menu1 sur la fenêtre
        screen.blit(logo1, logo1_rect)  # Affichage de l'image du logo du jeu 1
        screen.blit(logo2, logo2_rect)  # Affichage de l'image du logo du jeu 2
        screen.blit(logo3, logo3_rect)  # Affichage de l'image du logo du jeu 3
        screen.blit(logo4, logo4_rect)  # Affichage de l'image du logo du jeu 4
        screen.blit(text6, text_rect6)  # Affichage du nom du jeu 1
        screen.blit(text6_1, text_rect6_1)  # Affichage du nom du jeu 2
        screen.blit(text6_2, text_rect6_2)  # Affichage du nom du jeu 3
        screen.blit(text6_3, text_rect6_3)  # Affichage du nom du jeu 4
        screen.blit(text6_0_1, text_rect6_0_1)  # Affichage des touches à utiliser pour le jeu 1
        screen.blit(text6_1_1, text_rect6_1_1)  # Affichage des touches à utiliser pour le jeu 2
        screen.blit(text6_2_2, text_rect6_2_2)  # Affichage des touches à utiliser pour le jeu 3
        screen.blit(text6_3_3, text_rect6_3_3)  # Affichage des touches à utiliser pour le jeu 4

    if bg1:  # Si jeu 1 lancé
        if not ecran_debut:
            v_coins = str(compte_pts) + " $"  # Affiche les points en cours du jeu 1 avec le texte des coins
            x_collision_obj = x_obj + 48  # Met la position en X du rectangle de collision au niveau de la barrière
            # Création du rectangle de collision joueur
            rectangle_joueur = pygame.Rect(x_perso, y_perso, largeur_joueur, hauteur_joueur)
            # Création du rectangle de collision ennemie (haie)
            rectangle_ennemi = pygame.Rect(x_collision_obj, y_obj, largeur_ennemi, hauteur_ennemi)
            pygame.draw.rect(screen, BLACK, rectangle_joueur)  # Affichage du rectangle joueur
            pygame.draw.rect(screen, BLACK, rectangle_ennemi)  # Affichage du rectangle ennemi
            pygame.time.Clock().tick(50)  # Programme mis à 50 fps (image par seconde)
            if rectangle_joueur.colliderect(rectangle_ennemi):  # Si rectangle joueur touche rectangle ennemi
                resultat_coins = compte_pts  # Récuperation des gains
                coins = coins + compte_pts  # Ajout des gains aux coins
                # Activation de la fonction du jeu 1 pour remettre toute les variables du jeu 1 à leurs états d'origine
                j1()
                ecran_debut = False  # Désactivation de l'écran du debut
                ok = False  # Désactivation du jeu
                croix = False  # Disparition du bouton croix
                ecran_gain = True  # Affichage de l'écran de gain
                moins_pixel = 0  # Nombre de pixels à enlever mis à 0
                compteur_saut = 0  # Compteur de saut mis à 0 (arrêt du saut)
                resultat = "PERDU"  # Le resultat du jeu affiche perdu
            else:  # Sinon si le rectangle joueur ne touche pas le rectangle ennemi
                x_bg = x_bg - moins_pixel  # La position en X du fond perd le nombre de pixels de moins_pixel
                if x_bg > -1216:  # Si la position en X du fond est plus grand que la position en X -1216
                    screen.blit(img_bg1, (x_bg, 0))  # Affichage du fond du jeu 1 sur la fenêtre
                    screen.blit(img_bg1, (x_bg+1216, 0))  # Affichage du fond du jeu 1 sur la fenêtre
                else:  # Sinon si la position en X du fond est plus petite que la position ene X -1216
                    x_bg = 0  # Le fond est remis à la position en X 0
                    screen.blit(img_bg1, (x_bg, 0))  # Affichage du fond du jeu 1 sur la fenêtre
                # Si la variable de l'image du joueur et plus grande que la taille de la liste
                if img >= len(tiles_perso_j1):
                    img = 0  # L'image du joueur revient à la première image de la liste
                if temps_actuel - compte_temp >= 1 and not jump and ok:  # Si pas en saut et toutes les secondes
                    screen.blit(tiles_perso_j1[img], (x_perso, y_perso))  # Affichage du joueur
                    img = img + 1  # change l'image du joueur
                elif ok:  # Sinon si le jeu est activé
                    if img > 7:  # Si l'image du joueur est plus grand que 7
                        screen.blit(tiles_perso_j1[12], (x_perso, y_perso))  # Affichage de l'image 12
                    else:  # sinon si l'image du joueur est inférieur à 7
                        screen.blit(tiles_perso_j1[4], (x_perso, y_perso))  # Affichage de l'image 4
                else:  # Sinon si pas ok
                    screen.blit(tiles_perso_j1[0], (x_perso, y_perso))  # L'image se remet à 0
                if jump:  # Si le saut est activé
                    if compteur_saut <= 12:  # Si le compteur de saut et inférieur ou égale à 12
                        y_perso = y_perso - 20  # Le personnage monte
                        compteur_saut = compteur_saut + 1  # Compteur de saut augmente de 1
                    elif 12 < compteur_saut <= 25:  # Sinon si le compteur de saut est compris entre 12 et 25 inclus
                        y_perso = y_perso + 20  # Le personnage redescend
                        compteur_saut = compteur_saut + 1  # Compteur de saut augmente de 1
                    else:  # Sinon si compteur de saut est supérieur à 25
                        jump = False  # Désactivation du saut
                        compteur_saut = 0  # Remise à 0 du compteur de saut
                        y_perso = 445  # Remise de la position en Y du personnage à sa position d'origine
                if x_obj <= -100:  # Si la position en X de l'objet (ennemi) est inférieur ou égale à -100
                    pos_aleatoire = random.randint(0, 500)  # Choix aleatoire d'une future position
                    x_obj = 1500 + pos_aleatoire  # L'objet est remis à sa position d'origine + la position aléatoire
                screen.blit(img_haie, (x_obj, y_obj))  # Affichage de l'objet (ennemi)
                x_obj = x_obj - moins_pixel  # Mouvement de l'objet et enlèvent le nombre de pixels de moins_pixel
                if 0 <= x_obj < 20:  # Si l'objet est compris entre 0 et 20
                    compte_pts = compte_pts + 5  # ajout de 5 points au compteur de points
            if not ok:  # Si le jeu n'est pas activé
                v_coins = str(coins) + " $"  # Met le nombre de coins dans la variable du texte du cadre rouge et jaune
                save_file()  # Sauvegarde des coins
        elif ecran_debut:  # Sinon si l'écran du debut est visible
            screen.blit(img_bg1, (0, 0))  # Mise à 0 de la position du fond

    if bg2:  # Si jeu 2 lancé
        pygame.time.Clock().tick(50)  # Programme mis à 50 fps (image par seconde)
        # Création du rectangle de collision du personnage du bg2
        rectangle_joueur2 = pygame.Rect(x_perso2 + x_carre_perso2, 482 + y_carre_perso2,
                                        largeur_joueur2, hauteur_carre_joueur2)
        rectangle_sol = pygame.Rect(0, y_sol, largeur_sol, hauteur_sol)  # Création du rectangle de collision du sol
        # Création du rectangle de collision de la 1ère pierre du bg2
        rectangle_stone = pygame.Rect(x_obj2, y_obj2, largeur_stone, hauteur_stone)
        # Création du rectangle de collision de la 2ème pierre
        rectangle_stone1 = pygame.Rect(x_obj2_1, y_obj2_1, largeur_stone1, hauteur_stone1)
        pygame.draw.rect(screen, BLACK, rectangle_joueur2)  # Affichage du rectangle du personnage
        pygame.draw.rect(screen, BLACK, rectangle_sol)  # Affichage du rectangle du sol
        pygame.draw.rect(screen, BLACK, rectangle_stone)  # Affichage du rectangle de la 1ère pierre
        pygame.draw.rect(screen, BLACK, rectangle_stone1)  # Affichage du rectangle de la 2ème pierre
        screen.blit(img_bg2, (0, 0))  # Affichage du fond du bg2 (jeu 2)
        if not ecran_debut:  # Si l'écran du debut n'est pas affiché
            if not ecran_gain:  # Si l'écran de gain n'est pas affiché
                v_coins = str(compte_pts_bg2) + " pts"  # Affichage des points en cours avec le texte des coins
            else:  # Sinon
                v_coins = str(coins) + " $"  # Met le nombre de coins dans la variable du texte du cadre rouge et jaune
            screen.blit(img_wall, (0, 0))  # Affichage du mur 1
            screen.blit(img_wall1, (907, 0))  # Affichage du mur 2
            screen.blit(img_stone, (x_obj2, y_obj2))  # Affichage de la pierre 1
            screen.blit(img_stone, (x_obj2_1, y_obj2_1))  # Affichage de la pierre 2
            screen.blit(tiles_perso_j2[img2_dir][img2], (x_perso2, 482))  # Affichage du personnage
            screen.blit(img_sol, (0, y_sol))  # Affichage du sol
            croix = True  # Variable qui affiche le bouton croix
            # Si la position en Y de la pierre 1 est inférieur à 0 ou
            # si la position en Y de la pierre 2 est inférieur à 0
            if y_obj2 < 0 or y_obj2_1 < 0:
                resultat_coins = compte_pts_bg2  # Récuperation des gains
                coins = coins + resultat_coins  # Ajout des gains aux coins
                ecran_gain = True  # Affichage de l'écran de gain
                resultat = "PERDU"  # Le resultat affiche perdu
            if y_obj2 > 800:  # Si la position en Y de la pierre 1 est supérieur à 800
                x_obj2 = random.randint(495, 505)  # Choix aleatoire de la prochaine position en X de la pierre1
                y_obj2 = y_obj2 - 550  # La pierre 1 est remise à sa position en Y d'origine
            if y_obj2_1 > 800:  # Si la position en Y de la pierre 2 est supérieur à 800
                y_obj2_1 = y_obj2_1 - 550  # La pierre 2 est remise à sa position en Y d'origine
                x_obj2_1 = random.randint(695, 705)  # Choix aleatoire de la prochaine position en X de la pierre2
            # Si les pierres 1 ou 2 sont comprise entre la position en Y du rectangle du personnage + 482 et la position
            # en Y du rectangle du personnage + 487 ou
            # si la position en Y du rectangle du personnage + 482 vaut la position en Y du sol
            if (482 + y_carre_perso2 < y_obj2_1 <= 487 + y_carre_perso2 or
                    482 + y_carre_perso2 < y_obj2 <= 487 + y_carre_perso2 or 482 + y_carre_perso2 == y_sol):
                # Si collision entre le personnage et le sol ou une collision entre le personnage et les pierres
                if (rectangle_joueur2.colliderect(rectangle_sol) or rectangle_joueur2.colliderect(rectangle_stone) or
                        rectangle_joueur2.colliderect(rectangle_stone1)):
                    compte_s = 0  # Variable mis à 0 car le personnage ne saute pas
                    pos_joueur = False  # Fin de saut
                    # Prochaine verification prend la valeur de la pierre sur laquelle le personnage se trouve
                    verif_obj_apres = verif_obj
                    if y_obj2 > y_obj2_1:  # Si la pierre 1 est plus basse que la pierre 2
                        verif_precedente = y_obj2  # L'ancienne verif devient la position en Y de la pierre 1
                        verif_obj = 2  # Valeur de la pierre sur laquelle le personnage se trouve
                    else:  # Sinon si la pierre 1 est plus haute que la pierre 2
                        verif_precedente = y_obj2_1  # L'ancienne verif devient la position en Y de la pierre 2
                        verif_obj = 1  # Valeur de la pierre sur laquelle le personnage se trouve
                    if verif_obj_apres != verif_obj:  # Si les verifications sont différentes
                        verif_apres = 0  # Remise à 0 de la future verif
                    # Si la verif d'avant vaut la position en Y du carré du personnage + 483 et la verif d'après vaut 0
                    if verif_precedente == y_carre_perso2 + 483 and verif_apres == 0:
                        compte_pts_bg2 = compte_pts_bg2 + 1  # Ajout d'un point
                        verif_apres = 1  # La verif d'après vaut 1
            # Si collision entre le personnage et le sol et que le personnage et avant la position du sol
            if rectangle_joueur2.colliderect(rectangle_sol) and y_sol >= 482 + hauteur_joueur2:
                y_sol = 482 + hauteur_joueur2  # Le sol récupère sa position d'origine
            # Sinon si collision entre personnage et pierre 1 et que le personnage et avant la position de la pierre 1
            elif (rectangle_joueur2.colliderect(rectangle_stone) and
                  y_obj2 >= 482 + hauteur_joueur2):
                y_obj2 = 482 + hauteur_joueur2  # La pierre 1 récupère sa position d'origine
            # Sinon si collision entre personnage et pierre 2 et que le personnage et avant la position de la pierre 2
            elif (rectangle_joueur2.colliderect(rectangle_stone1) and
                  y_obj2_1 >= 482 + hauteur_joueur2):
                y_obj2_1 = 482 + hauteur_joueur2  # La pierre 2 récupère sa position d'origine
            elif (not saut and not rectangle_joueur2.colliderect(rectangle_stone) and
                  not rectangle_joueur2.colliderect(rectangle_sol) and
                  not rectangle_joueur2.colliderect(rectangle_stone1)):  # Si personnage dans les airs
                y_sol = y_sol - 5  # Le sol remonte
                y_obj2 = y_obj2 - 5  # La pierre 1 remonte
                y_obj2_1 = y_obj2_1 - 5  # La pierre 2 remonte
                vitesse = 3  # Vitesse de déplacement du joueur mis à 3
                pos_joueur = True  # Activation de la variable qui indique si le personnage est dans les airs
            if droit2:  # Si direction droite
                if not pos_joueur and not saut:  # Si le joueur ne saute et n'est pas dans les airs
                    vitesse = 10  # Vitesse de déplacement égale 10
                    # Indique qu'il faut prendre la liste des images de droite dans la liste des images du personnage
                    img2_dir = 1
                    if img2 >= len(tiles_perso_j2[img2_dir]) - 1:  # Si la valeur de l'image dépasse la taille de la lst
                        img2 = 0  # L'image est mise à 0
                    elif 0 <= img2 < 8:  # Sinon si l'image est comprise entre 0 inclus et 8
                        if temps_actuel - compte_temp >= 1:  # Si 1 seconde est passé
                            img2 = img2 + 1  # L'image augmente de 1
                    else:  # Sinon si compris entre 8 inclus jusqu'à la fin de la liste
                        if temps_actuel - compte_temp >= 1:  # Si 1 seconde est passé
                            img2 = img2 + 1  # L'image augmente de 1
                x_perso2 = x_perso2 + vitesse  # Le personnage se déplace à droite du nombre de pixels de la vitesse
            if gauche2:  # Si direction gauche
                if not pos_joueur and not saut:  # Si le joueur ne saute et n'est pas dans les airs
                    vitesse = 10  # Vitesse de déplacement égale 10
                    # Indique qu'il faut prendre la liste des images de gauche dans la liste des images du personnage
                    img2_dir = 2
                    if img2 >= len(tiles_perso_j2[img2_dir]) - 1:  # Si la valeur de l'image dépasse la taille de la lst
                        img2 = 0  # L'image est mise à 0
                    elif 0 <= img2 < 8:  # Sinon si l'image est comprise entre 0 inclus et 8
                        if temps_actuel - compte_temp >= 1:  # Si 1 seconde est passé
                            img2 = img2 + 1  # L'image augmente de 1
                    else:  # Sinon si compris entre 8 inclus jusqu'à la fin de la liste
                        if temps_actuel - compte_temp >= 1:  # Si 1 seconde est passé
                            img2 = img2 + 1  # L'image augmente de 1
                x_perso2 = x_perso2 - vitesse  # Le personnage se déplace à droite du nombre de pixels de la vitesse
            if saut:  # Si le personnage saute
                compte_s = 1  # Variable mis à 1 car le personnage saute
                vitesse = 3  # La vitesse de déplacement est mis à 3 pixels
                if compteur_saut2 <= 0:  # Si le compteur de saut est inférieur ou égale à 0
                    img2_dir = 0  # La 1ère liste dans la liste est choisis
                    img2 = 1  # L'image du personnage passe à 1
                    compteur_saut2 = compteur_saut2 + 1  # Le compteur de saut augmente de 1
                elif 1 <= compteur_saut2 < 35:  # Sinon si le compteur de saut est compris entre 1 inclus et 35
                    img2 = 2  # L'image du personnage passe à 2
                    y_sol = y_sol + 10  # Le sol descent
                    y_obj2 = y_obj2 + 10  # La pierre 1 descent
                    y_obj2_1 = y_obj2_1 + 10  # La pierre 2 descent
                    compteur_saut2 = compteur_saut2 + 1  # Le compteur de saut augmente de 1
                else:  # Sinon
                    compteur_saut2 = 0  # Remise à 0 du compteur de saut
                    saut = False  # Désactivation du suat
            # 301 = position en X du mur 1 + largeur du mur 1
            if x_perso2 <= 301:  # Si la position en X du personnage est inférieur ou égale à 301 (verif avec le mur 1)
                x_perso2 = 302  # La position en X du personnage devient 302
            # 883 = position en X du mur 2 / 65 = largeur du personnage
            if x_perso2 >= 883 - 65:  # Si la position en X du personnage est supérieur à 883 - 65 (verif avec le mur 2)
                x_perso2 = 882 - 65  # La position en X du personnage devient 882 - 65
        elif ecran_debut:  # Si l'écran de debut est activé
            screen.blit(img_bg2, (0, 0))  # Affichage du fond du bg2 à sa position d'origine
            screen.blit(img_wall, (0, 0))  # Affichage du mur 1 du bg2 à sa position d'origine
            screen.blit(img_wall1, (907, 0))  # Affichage du mur 2 du bg2 à sa position d'origine
            screen.blit(tiles_perso_j2[0][0], (560, 482))  # Affichage du personnage du bg2 à sa position d'origine
            screen.blit(img_stone, (x_obj2, y_obj2))  # Affichage de la pierre 1 du bg2 à sa position d'origine
            screen.blit(img_stone, (x_obj2_1, y_obj2_1))  # Affichage de la pierre 2 du bg2 à sa position d'origine
            screen.blit(img_sol, (0, 626))  # Affichage du sol du bg2 à sa position d'origine

    if bg3:  # Si jeu 3 lancé
        pygame.time.Clock().tick(50)  # Programme mis à 50 fps (image par seconde)
        if not ecran_debut:  # Si écran du debut désactivé
            screen.blit(img_bg3, img_bg3_rect)  # Affichage du fond du jeu 3 sur la fenêtre
            screen.blit(img_drapeau, img_drapeau_rect)  # Affichage du drapeau de fin
            screen.blit(tiles_perso_j3_4[img3_3], (x_perso3_3, 400))  # Affichage du perso 1
            screen.blit(tiles_perso_j3_3[img3_2], (x_perso3_2, 448))  # Affichage du perso 2
            screen.blit(tiles_perso_j3_2[img3_1], (x_perso3_1, 496))  # Affichage du perso 3
            screen.blit(tiles_perso_j3_1[img3], (x_perso3, 544))  # Affichage du perso 4
            croix = True  # Variable qui affiche le bouton croix
            if not ecran_gain:  # Si écran de gain désactivé
                aleatoire_vitesse_pnj1 = random.randint(10, 50)  # Choix aleatoire du personnage non-joueur 1
                aleatoire_vitesse_pnj2 = random.randint(10, 50)  # Choix aleatoire du personnage non-joueur 2
                aleatoire_vitesse_pnj3 = random.randint(10, 50)  # Choix aleatoire du personnage non-joueur 3
                # Si l'image du pnj 1 est supérieur ou égale à la taille de la liste -2
                if img3_3 >= len(tiles_perso_j3_4) - 2:
                    img3_3 = 0  # Image remise à 0
                elif 8 > img3_3 >= 0:  # Sinon si l'image du pnj 1 est supérieur ou égale à 0
                    if temps_actuel - compte_temp >= 1:  # Si une seconde est passé
                        img3_3 = img3_3 + 1  # L'image du png 1 augmente de 1
                else:  # Sinon
                    if temps_actuel - compte_temp >= 1:  # Si une seconde est passé
                        img3_3 = img3_3 + 1  # L'image du png 1 augmente de 1
                x_perso3_3 = x_perso3_3 + aleatoire_vitesse_pnj3//9  # Déplacement du pnj 1
                # Si l'image du pnj 2 est supérieur ou égale à la taille de la liste -2
                if img3_2 >= len(tiles_perso_j3_3) - 2:
                    img3_2 = 0  # Image remise à 0
                elif 8 > img3_3 >= 0:  # Sinon si l'image du pnj 2 est supérieur ou égale à 0
                    if temps_actuel - compte_temp >= 1:  # Si une seconde est passé
                        img3_2 = img3_2 + 1  # L'image du png 2 augmente de 1
                else:  # Sinon
                    if temps_actuel - compte_temp >= 1:  # Si une seconde est passé
                        img3_2 = img3_2 + 1  # L'image du png 2 augmente de 1
                x_perso3_2 = x_perso3_2 + aleatoire_vitesse_pnj2//7  # Déplacement du pnj 2
                # Si l'image du pnj 3 est supérieur ou égale à la taille de la liste -2
                if img3_1 >= len(tiles_perso_j3_2) - 2:
                    img3_1 = 0  # Image remise à 0
                elif 8 > img3_1 >= 0:  # Sinon si l'image du pnj 3 est supérieur ou égale à 0
                    if temps_actuel - compte_temp >= 1:  # Si une seconde est passé
                        img3_1 = img3_1 + 1  # L'image du png 3 augmente de 1
                else:  # Sinon
                    if temps_actuel - compte_temp >= 1:  # Si une seconde est passé
                        img3_1 = img3_1 + 1  # L'image du png 3 augmente de 1
                x_perso3_1 = x_perso3_1 + aleatoire_vitesse_pnj1//10  # Déplacement du pnj 3
            if course:  # Si le personnage court
                # Si l'image du personnage est supérieur ou égale à la taille de la liste -2
                if img3 >= len(tiles_perso_j3_1) - 2:
                    img3 = 0  # Remise à 0 de l'image
                elif 8 > img3 >= 0:  # Sinon si l'image du personnage est compris entre 0 et 0 inclus
                    if temps_actuel - compte_temp >= 1:  # Si 1 seconde est passé
                        img3 = img3 + 1  # L'image du personnage augmente de 1
                    if img3 == 7:  # Si l'image du personnage vaut 7
                        course = False  # Arrêt de la course
                else:  # Sinon
                    if temps_actuel - compte_temp >= 1:  # Si 1 seconde est passé
                        img3 = img3 + 1  # L'image augmente de 1
                    if img3 == 16:  # Si l'image vaut 16
                        course = False  # Arrêt de la course
                x_perso3 = x_perso3 + 5  # Le joueur avance de 5 pixels
            if x_perso3 >= 1125:  # Si la position en X du personnage est égale à celle de l'arrivée
                ecran_gain = True  # Affichage de l'écran de gain
                resultat = "GAGNÉ"  # Le resultat affiche gagné
                resultat_coins = 20  # Récuperation des gains
                coins = coins + resultat_coins  # Ajout des gains aux coins
                save_file()  # Sauvegarde des coins
            # Sinon si un des pnj arrive à l'arrivée
            elif x_perso3_1 >= 1125 or x_perso3_2 >= 1125 or x_perso3_3 >= 1125:
                ecran_gain = True  # Affichage de l'écran des gains
                resultat = "PERDU"  # Le resultat affiche perdu
        elif ecran_debut:  # Sinon si l'écran du debut est affiché
            screen.blit(img_bg3, img_bg3_rect)  # Affichage du fond du bg3

    if bg4:  # Si jeu 4 lancé
        pygame.time.Clock().tick(50)  # Programme mis à 50 fps (image par seconde)
        if not ecran_debut:  # Si l'écran du debut n'est pas affiché
            if y_perso4 <= 100:  # Si la position en Y du personnage du bg4 est inférieur ou égale à 100
                coins = coins + seconde  # Ajout des gains aux coins
                resultat_coins = seconde  # Récuperation des gains
                # Activation de la fonction du jeu 4 pour remettre toute les variables du jeu 4 à leurs états d'origine
                j4()
                ecran_debut = False  # Désactivation de l'écran du debut
                ecran_gain = True  # Affichage de l'écran des gains
                ok = False  # Désactivation du jeu
                croix = False  # Disparition du bouton de la croix
                resultat = "GAGNÉ"  # Le resultat affiche gagné
            # Si la position en Y du personnage du bg4 est inférieur à 704 et que le compteur de fond est inférieur à 40
            if y_bg4 < 704 and compte_nb_bg < 40:
                screen.blit(img_bg4, (0, y_bg4))  # Affichage du fond du jeu 4 sur la fenêtre
                screen.blit(img_bg4, (0, y_bg4 - 704))  # Affichage du fond du jeu 4 sur la fenêtre
            else:  # Sinon
                y_bg4 = 0  # Remise à 0 de la position en Y du fond du bg4
                screen.blit(img_bg4, (0, y_bg4))  # Affichage du fond du jeu 4 sur la fenêtre
            # Si le compteur de fond est compris entre 37 et 40 et que la position en Y de l'arrivée est inférieur à 0
            if 40 > compte_nb_bg > 37 and y_obj_bg4 < 0:
                y_obj_bg4 = y_obj_bg4 + 70  # Ajout de 70 pixels à la position en Y de l'arrivée
            elif y_obj_bg4 > 0:  # Sinon si la position en Y de l'arrivée supérieure à 0
                y_obj_bg4 = 0  # Remise à 0 de la position en Y de l'arrivée
            if gauche:  # Si gauche est activé
                if compte_nb_bg == 40:  # Si le compteur de fond vaut 40
                    y_perso4 = y_perso4 - 20  # La position en Y du personnage du bg4 avance
                    choix_perso4 = tiles_perso_j4[3]  # Affichage dernière image du personnage
                    choix_perso4 = tiles_perso_j4[2]  # Affichage image du personnage avec le bras gauche
                elif verif_cote == 0:  # Sinon si aucun bras n'est activé
                    choix_perso4 = tiles_perso_j4[2]  # Affichage image du personnage avec le bras gauche
                    y_bg4 = y_bg4 + 20  # La position en Y du fond du bg4 recule
                    verif_cote = 1  # Variable active les bras
                    compte_nb_bg = compte_nb_bg + 1  # Le nombre de fonds augmente de 1
                elif verif_cote == 1:  # Sinon si les bras sont activé
                    choix_perso4 = tiles_perso_j4[3]  # Affichage dernière image du personnage
                    choix_perso4 = tiles_perso_j4[2]  # Affichage image du personnage avec le bras gauche
                    y_bg4 = y_bg4 + 20  # La position en Y du fond du bg4 recule
                    compte_nb_bg = compte_nb_bg + 1  # Le nombre de fonds augmente de 1
                gauche = False  # Désactivation de gauche
                v_droit = 1  # La variable passe au bouton droit
            elif droit:  # Sinon si droit activé
                if compte_nb_bg == 40:  # Si le compteur de fond vaut 40
                    y_perso4 = y_perso4 - 20  # La position en Y du personnage du bg4 avance
                    choix_perso4 = tiles_perso_j4[3]  # Affichage dernière image du personnage
                    choix_perso4 = tiles_perso_j4[1]  # Affichage image du personnage avec le bras droit
                else:  # Sinon
                    choix_perso4 = tiles_perso_j4[3]  # Affichage dernière image du personnage
                    choix_perso4 = tiles_perso_j4[1]  # Affichage image du personnage avec le bras droit
                    verif_cote = 1  # Variable active les bras
                    y_bg4 = y_bg4 + 20  # La position en Y du fond du bg4 recule
                    compte_nb_bg = compte_nb_bg + 1  # Le nombre de fonds augmente de 1
                droit = False  # Désactivation de droit
                v_droit = 0  # La variable passe au bouton gauche
            else:  # Sinon
                choix_perso4 = tiles_perso_j4[0]  # Affichage de la première image du personnage
            screen.blit(img_fin, (0, y_obj_bg4))  # Affichage de la ligne d'arrivée
            screen.blit(choix_perso4, (x_perso4, y_perso4))  # Affichage du personnage
        elif ecran_debut:  # Sinon si l'écran du debut est activé
            screen.blit(img_bg4, (0, 0))  # Affichage du fond du bg4

    if text_visible:  # Si le texte est visible
        screen.blit(text, text_rect)  # Affichage du texte de la mise sur la fenêtre
        screen.blit(text1, text_rect1)  # Affichage du texte des erreurs sur la fenêtre
        screen.blit(text3, text_rect3)  # Affichage du texte de la mise final sur la fenêtre

    if croix:  # Si croix est visible
        button13.draw(screen)  # Affichage du bouton croix sur la fenêtre bg1

    if ecran_debut:  # Si l'écran du debut est visible
        croix = False  # Disparition du bouton croix
        screen.blit(img_gain, img_gain_rect)  # affichage du fond de gain
        button15.draw(img_gain)  # Affichage du bouton QUITTER
        button16.draw(img_gain)  # Affichage du bouton COMMENCER
        screen.blit(text7, text7_rect)  # Affichage du texte Touches
        screen.blit(text7_1, text7_1_rect)  # Affichage des touches à utiliser pendant les jeux

    if ecran_gain:  # Si l'écran de gain est visible
        screen.blit(img_gain, img_gain_rect)  # Affichage du fond de gain
        screen.blit(text4, text_rect4)  # Affichage du texte le resultat des jeux
        screen.blit(text5, text_rect5)  # Affichage du texte du nombre de coins gagné
        button14.draw(img_gain)  # Affichage du bouton RECOMMENCER
        button15.draw(img_gain)  # Affichage du bouton QUITTER
        text2_visible = True  # Affichage du texte avec le nombre total de coins
        if bg2:  # Si jeu 2 activé
            j2()  # Relance du jeu 2 afin de remettre les variables à 0
            ecran_debut = False  # Désactivation de l'écran du debut
        if bg3:  # Si jeu 3 activé
            x_perso3 = 15  # Remet la position en X du joueur 0 à l'origine
            x_perso3_1 = 15  # Remet la position en X du joueur 1 à l'origine
            x_perso3_2 = 15  # Remet la position en X du joueur 2 à l'origine
            x_perso3_3 = 15  # Remet la position en X du joueur 3 à l'origine
            img3 = 16  # Remet l'image du joueur 0 à l'origine
            img3_1 = 16  # Remet l'image du joueur 1 à l'origine
            img3_2 = 16  # Remet l'image du joueur 2 à l'origine
            img3_3 = 16  # Remet l'image du joueur 3 à l'origine
        v_coins = str(coins) + " $"  # Met le nombre de coins dans la variable du texte du cadre rouge et jaune
        save_file()  # Sauvegarde des coins

    if text2_visible:  # Si le texte des coins est visible
        screen.blit(fond_coins, fond_coins_rect)  # Affichage du fond des coins sur la fenêtre
        screen.blit(text2, text_rect2)  # Affichage du texte des coins sur la fenêtre

    if ecran_accueil:  # Si l'écran d'accueil est visible
        screen.blit(img_ecran_acceuil, img_ecran_acceuil_rect)  # Affichage du fond de l'écran d'accueil sur la fenêtre
        button8.draw(img_ecran_acceuil)  # Affichage du bouton sur la fenêtre

    pygame.display.flip()  # Met à jour l'affichage pour rendre les changements visibles à l'écran

pygame.quit()  # Quitte le module Pygame proprement en libérant toutes les ressources utilisées
