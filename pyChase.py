"""
"       Auteurs                 : Russo Christian, Russotti Leandro.
"       Dernière modification   : 06.01.2021.
"       Projet                  : PyChase.
"       Description             : Jeu de labyrinthe avec un minotaure.
"""


from fourni import simulateur, pathfinder
from outils import \
    creer_image, \
    creer_minotaure, creer_case_vide, creer_sortie, creer_mur, creer_personnage, \
    coordonnee_x, coordonnee_y, est_egal_a

# Variable globale pour la mort du joueur
joueur_mort: bool = False

# Constante à utiliser
NIVEAU_DIFFICULTE: int = 5


# Fonctions à développer

def jeu_en_cours(joueur: list) -> str:
    """
    Fonction testant si le jeu est encore en cours et retournant un string comme réponse sur l'état de la partie.
    :param joueur: La liste des joueurs du niveau en cours
    :return: un string "mort" si le joueur est mort ou "fini" si le joueur s'est echappé. Retourne "" si la partie
             est en cours
    """
    # Variable contenant l'état de la partie.
    state: str = ""

    # Si le joueur est mort, met la variable état a mort
    if joueur_mort:
        state = "mort"

    # Si le joueur contient encore des données, met la variable vide.
    elif any(joueur):
        state = ""

    # Sinon, met la variable état a terminé.
    else:
        state = "fini"

    # Retourne l'état.
    return state


def charger_niveau(carte: list, joueur: list, minotaures: list, sorties: list, murs: list, path: str):
    """
    Fonction permettant de charger depuis un fichier.txt et de remplir les différentes listes permettant le
    fonctionnement du jeu (joueur, minotaures, murs, sorties)
    :param carte: liste de liste comportant toutes les entités (joueur, minotaures, murs, sorties). C'est la grille du jeu.
    :param joueur: liste contenant le joueur
    :param minotaures: liste des minotaures
    :param sorties: liste des sorties
    :param murs: liste des murs
    :param path: chemin du fichier.txt
    """
    global joueur_mort
    joueur_mort = False

    # Ouverture du fichier. (level1,2,3.txt)
    with open(path, "r") as level:
        # Initialisation des variables nécessaires
        x: int = 0
        y: int = 0
        count: int = 0

        # Recupueré toutes les lignes differentes grace au readline.
        texte = level.read()
        lignes = texte.split()

        # Prendre les lignes une par une
        for ligne in lignes:

            carte.append(list(ligne))

            # prendre les characteres 1 par 1.
            for char in ligne:
                if char == "#":
                    murs.append(creer_mur(x, y))
                elif char == "$":
                    minotaures.append(creer_minotaure(x, y))
                elif char == "@":
                    joueur.append((creer_personnage(x, y)))
                elif char == ".":
                    sorties.append((creer_sortie(x, y)))

                x += 1
                count += 1

            # Incrémenter Y et remettre X a 0 quand on arrive a la fin de la ligne
            if count % len(ligne) == 0:
                x = 0
                y += 1


def avancer_minotaure(minotaures: list, joueur: list, murs: list, carte: list, can, liste_image: list):
    """
        Fonction permettant de faire avancer le(s) minotaure(s) grâce à l'algorithme de pathfinding. Suivant le niveau
        de difficulté, le minotaure va avancer d'un certain nombre de cases vers le joueur. Si le joueur est trop
        proche, celui-ci est éliminé.
        :param minotaures: La liste de minotaure
        :param joueur: La liste contenant le joueur
        :param murs: La liste contenant les murs
        :param carte : La liste de liste formant la grille du jeu
        :param can: Canvas (ignorez son fonctionnement), utile uniquement pour créer_image()
        :param liste_image : Liste contenant les références sur les images
    """
    # Création des variables de coordonés du minautore
    x_minotaure: int = minotaures[0].x
    y_minotaure: int = minotaures[0].y

    # Création des variables de coordonés du minautore
    x_joueur: int = joueur[0].x
    y_joueur: int = joueur[0].y

    # Création des variables contenant l'emplacement initial du minautore et l'emplacement final (les coordonés initiale du joueur)
    start: list = [x_minotaure, y_minotaure]
    end: list = [x_joueur, y_joueur]

    # Création des prochaines coordonés du minautore.
    next_minotaure_x: int = 0
    next_minotaure_y: int = 0

    # Appele la fonction fournie dans outils.py qui va définir le chemin le plus court selon le niveau.
    newPath: list = pathfinder.search(murs, carte, 1, start, end)

    # Boucle parcourant les listes de liste et les listes
    for index, i in enumerate(newPath):
        # Si on trouve un chemin possible dans la liste, update les prochaines coordonés du minautore NIVEAU_DIFFICULTE = nombre de case parcourue par le minotaure
        if NIVEAU_DIFFICULTE in i:
            next_minotaure_x = i.index(NIVEAU_DIFFICULTE)
            next_minotaure_y = index

    # Si le joueur n'est pas a l'emplacement du déplacement du minotaure, avance le minotaure normalement.
    if any(NIVEAU_DIFFICULTE in line for line in newPath):
        minotaures.clear()
        minotaures.append(creer_personnage(next_minotaure_x, next_minotaure_y))
        creer_image(can, x_minotaure, y_minotaure, liste_image[6])
    # Sinon, se déplace a l'emplacement du joueur et le tue.
    else:
        minotaures.clear()
        global joueur_mort
        joueur_mort = True
        joueur.clear()
        minotaures.append(creer_personnage(x_joueur, y_joueur))
        creer_image(can, x_minotaure, y_minotaure, liste_image[6])


def definir_mouvement(direction: str, can, joueur: list, murs: list, minotaures: list, sorties: list, carte: list,
                      liste_image: list):
    """
    Fonction permettant de définir la case de destination selon la direction choisie.
    :param direction: Direction dans laquelle le joueur se déplace (droite, gauche, haut, bas)
    :param can: Canvas (ignorez son fonctionnement), utile uniquement pour créer_image()
    :param joueur: Liste des joueurs
    :param murs: Liste des murs
    :param minotaures: Liste des minotaures
    :param sorties: Liste des sorties
    :param carte: La liste de liste formant la grille du jeu
    :param liste_image: Liste contenant les références sur les images
    :return:
    """

    # Déclaration des ancienne coordonées du joueur.
    old_x: int = joueur[0].x
    old_y: int = joueur[0].y

    # Déclaration des nouvelles coordonées du joueur.
    new_x: int = 0
    new_y: int = 0

    # Test des directions + ajout des nouvelles coordonés
    if direction == "gauche":
        new_x = old_x - 1
        new_y = old_y
    if direction == "droite":
        new_x = old_x + 1
        new_y = old_y
    if direction == "haut":
        new_y = old_y - 1
        new_x = old_x
    if direction == "bas":
        new_y = old_y + 1
        new_x = old_x

    # création de la variable destination (nécessaire pour effectuer_mouvement)
    coordonnee_destination = creer_case_vide(new_x, new_y)
    effectuer_mouvement(coordonnee_destination, minotaures, murs, joueur, sorties, carte, can, liste_image, new_x,
                        new_y)

    # Remplacer l'ancienne image par une case vide (6 = image du sol)
    creer_image(can, old_x, old_y, liste_image[6])


def effectuer_mouvement(coordonnee_destination, minotaures: list, murs: list, joueur: list, sorties: list, carte: list,
                        can,
                        liste_image: list, deplace_joueur_x: int, deplace_joueur_y: int):
    """
    Fonction permettant d'effectuer le déplacement ou de ne pas l'effectuer si celui-ci n'est pas possible.
    Voir énoncé "Quelques règles".
    ----------Cette methode est appelée par mouvement.--------------
    :param coordonnee_destination: variable CaseVide ayant possiblement des coordonnées identiques à une autre variable
    (murs, minotaure, casevide)
    :param minotaures: liste des minotaures
    :param murs: liste des murs
    :param joueur: liste des joueurs
    :param sorties: Liste des sorties
    :param carte: La liste de liste formant la grille du jeu
    :param can: Canvas (ignorez son fonctionnement), utile uniquement pour créer_image()
    :param liste_image: Liste contenant les références sur les images
    :param deplace_joueur_x: coordonnée en x à laquelle le joueur va être après le mouvement
    :param deplace_joueur_y: coordonnée en y à laquelle le joueur va être après le mouvement
    """

    # Si la destination est un mur, fait avancer le minotaure.
    if coordonnee_destination in murs:
        avancer_minotaure(minotaures, joueur, murs, carte, can, liste_image)
    # Sinon, avance le joueur a la nouvelle destination
    else:
        # Supprime l'ancien dessin du joueur
        joueur.clear()
        # Si la destination n'est pas la sortie, avance l'image du joueur
        if coordonnee_destination not in sorties:
            joueur.append(creer_personnage(deplace_joueur_x, deplace_joueur_y))
        # Si l'emplacement du joueur est la meme que celle du minotaure, tue le joueur et termine la partie.
        if deplace_joueur_x == minotaures[0].x and deplace_joueur_y == minotaures[0].y:
            joueur.clear()
            global joueur_mort
            joueur_mort = True


def chargement_score(scores_file_path: str, dict_scores: dict):
    """
    Fonction chargeant les scores depuis un fichier.txt et les stockent dans un dictionnaire
    :param scores_file_path: le chemin d'accès du fichier
    :param dict_scores:  le dictionnaire pour le stockage
    :return:
    """
    # Ouvres le fichier et le stock dans la variable scorefile.
    with open(scores_file_path, "r") as scorefile:
        for lines in scorefile:
            # Supprime les saut de ligne
            texte = lines.strip()
            # Sépare les scores des differents niveau.
            score = texte.split(";")
            # Prend la première entrée du score (le numéro du niveau) et le stock dans numniveau
            numNiveau = score[0]
            count = 0
            dict_scores[numNiveau] = []
            # Pour chaque score, sauf la première entrée, l'ajoute dans le dictionnaire dict_scores.
            for s in score:
                if count != 0:
                    dict_scores[numNiveau].append(float(s))
                count += 1


def maj_score(niveau_en_cours: int, dict_scores: dict) -> str:
    """
    Fonction mettant à jour l'affichage des scores en stockant dans un str l'affichage visible
    sur la droite du jeu.
    ("Niveau x
      1) 7699
      2) ... ").
    :param niveau_en_cours: le numéro du niveau en cours
    :param dict_scores: le dictionnaire pour stockant les scores
    :return str: Le str contenant l'affichage pour les scores ("\n" pour passer à la ligne)
    """
    # Création de la variable résultat contenant l'affichage du score.
    resultat: str = "Niveau " + str(niveau_en_cours) + "\n"
    # Triage du dictionnaire.
    dict_scores[str(niveau_en_cours)] = sorted(dict_scores[str(niveau_en_cours)],
                                               key=lambda x: float('inf') if x == 0.0 else x)

    # pour chaque score dans le dictionnaire du niveau en cours, ajoute une ligne dans la variable résultat.
    for i, score in enumerate(dict_scores[str(niveau_en_cours)]):
        if i < 10:
            resultat += str(i + 1) + ") " + str(score) + "\n"
    return resultat


def enregistre_score(temps_niveau: float, temps_initial: float, dict_scores: dict, niveau_en_cours: int):
    """
    Fonction enregistrant un nouveau score réalisé par le joueur.
    :param temps_niveau: le temps qu'il reste à la fin du niveau
    :param temps_initial: le temps initial du niveau
    :param dict_scores: Le dictionnaire stockant les scores
    :param niveau_en_cours: Le numéro du niveau en cours
    """
    # Calcul du nouveau score (le temps initial - le temps effectué) garder 2 décimales.
    nouveauScore: float = round(temps_initial - temps_niveau, 2)
    # Ajout du nouveau score dans le dictionnaire.
    dict_scores[str(niveau_en_cours)].append(nouveauScore)


def update_score_file(scores_file_path: str, dict_scores: dict):
    """
    Fonction sauvegardant tous les scores dans le fichier.txt. Celle-ci est appelée à la fermeture de l'application.
    :param scores_file_path: le chemin d'accès du fichier de stockage des scores
    :param dict_scores: Le dictionnaire stockant les scores
    """
    resultat: str = ""
    # Ouverture du fichier score dans la variable scorefile
    with open(scores_file_path, "w+") as scorefile:
        # Parcoure le dictionnaire des scores et recupère la clé + les valeures correspondantes a la clé
        for key, values in dict_scores.items():
            resultat += str(key) + ";"
            # Boucle parcourant la liste des scores par niveaux.
            for i, value in enumerate(values):
                # Si c'est le dernier score de la liste, n'ajoute pas de ;.
                if i + 1 != len(values):
                    resultat += str(value) + ";"
                else:
                    resultat += str(value)
            resultat += "\n"
            # Sauvegarde dans le fichier.
            scorefile.write(resultat)
            resultat = ""


if __name__ == '__main__':
    simulateur.simulate()
