from flask import Flask, request, render_template, redirect
import sqlite3
from datetime import datetime



def get_db_connection():
    conn = sqlite3.connect('jeu.db')  # Assurez-vous que le fichier DB existe
    conn.row_factory = sqlite3.Row  # Pour accéder aux colonnes par nom
    return conn

app = Flask(__name__)
def max_variable(a, b, c, d, j1, j2, j3, j4):
    # Créer un dictionnaire avec les noms des variables comme clés et leurs valeurs comme valeurs
    variables = {j1: a, j2: b, j3: c, j4: d}
    
    # Trouver le nom de la variable avec la valeur maximale
    max_var = max(variables, key=variables.get)
    
    return max_var
# Fonction pour insérer les données dans la base de données
def insert_data(date, joueur1_bande,joueur1_nom, joueur1_points, joueur2_bande,joueur2_nom, joueur2_points,
                joueur3_bande,joueur3_nom, joueur3_points, joueur4_bande,joueur4_nom, joueur4_points):
    
    conn = sqlite3.connect('jeu.db')
    cursor = conn.cursor()
    vainqueur = max_variable(joueur1_points, joueur2_points, joueur3_points, joueur4_points, joueur1_nom, joueur2_nom, joueur3_nom, joueur4_nom)
    # Insertion des données dans la table
    cursor.execute('''
        INSERT INTO partie (date,joueur1_nom, joueur2_nom, joueur3_nom, joueur4_nom, joueur1_bande, joueur2_bande, joueur3_bande, joueur4_bande, joueur1_points, 
                            joueur2_points, joueur3_points, joueur4_points, vainqueur)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,? ,? ,?)
    ''', (date, joueur1_nom, joueur2_nom, joueur3_nom, joueur4_nom, 
          joueur1_bande, joueur2_bande, joueur3_bande, joueur4_bande, 
          joueur1_points, joueur2_points, joueur3_points, joueur4_points, vainqueur))
    
    conn.commit()
    conn.close()
    
    
# Route pour la page de formulaire
@app.route('/')
def index():
    conn = get_db_connection()
    parties = conn.execute('SELECT * FROM partie').fetchall()
    conn.close()
    return render_template('index.html', parties=parties)



# Route pour traiter les données du formulaire
@app.route('/process_data', methods=['GET', 'POST'])
def process_data():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        date = request.form['date']
        
        # Récupérer les informations des joueurs
        joueur1_bande = request.form.get('joueur1_bande')
        joueur1_nom = request.form.get('joueur1_nom')
        joueur1_points = int(request.form.get('joueur1_points', 0))
        
        joueur2_bande = request.form.get('joueur2_bande')
        joueur2_nom = request.form.get('joueur2_nom')
        joueur2_points = int(request.form.get('joueur2_points', 0))
        
        joueur3_bande = request.form.get('joueur3_bande')
        joueur3_nom = request.form.get('joueur3_nom')
        joueur3_points = int(request.form.get('joueur3_points', 0))
        
        joueur4_bande = request.form.get('joueur4_bande')
        joueur4_nom = request.form.get('joueur4_nom')
        joueur4_points = int(request.form.get('joueur4_points', 0))
        
        print("Joueur 1 d : ", joueur1_bande)
        # Insérer les données dans la base de données
        insert_data(date, joueur1_bande,joueur1_nom, joueur1_points,
                    joueur2_bande,joueur2_nom, joueur2_points, joueur3_bande,joueur3_nom, joueur3_points,
                    joueur4_bande,joueur4_nom, joueur4_points)
        

        return redirect('/')
    
    return render_template('ajouter.html')



@app.route('/stats', methods=['GET'])
def stats():
    conn = get_db_connection()

    # Calculer le nombre total de parties
    total_parties = conn.execute('SELECT COUNT(*) FROM partie').fetchone()[0]

    # Calculer le pourcentage de victoires par joueur
    # On va récupérer tous les noms des joueurs qui sont vainqueurs
    query_vainqueurs = 'SELECT vainqueur FROM partie'
    vainqueurs = [row['vainqueur'] for row in conn.execute(query_vainqueurs).fetchall()]
    
    # Calcul des victoires pour chaque joueur
    joueurs_noms = list(set(vainqueurs))  # Récupérer tous les noms uniques des joueurs vainqueurs
    victoires = {joueur: vainqueurs.count(joueur) for joueur in joueurs_noms}

    pourcentage_victoires_par_joueur = {
        joueur: (victoires[joueur] / total_parties * 100) if total_parties > 0 else 0
        for joueur in victoires
    }

   # Requête pour récupérer les vainqueurs de toutes les parties
    # Requête pour récupérer la bande du vainqueur de chaque partie
    query_vainqueurs = 'SELECT vainqueur, joueur1_bande, joueur2_bande, joueur3_bande, joueur4_bande, joueur1_nom, joueur2_nom, joueur3_nom, joueur4_nom FROM partie'
    vainqueurs_bandes = []

    # Extraire la bande du joueur vainqueur pour chaque partie
    for row in conn.execute(query_vainqueurs).fetchall():
        vainqueur = row['vainqueur']

        # Selon le vainqueur, ajouter la bande correspondante
        if vainqueur == row['joueur1_nom']:  # Comparer avec le nom du joueur 1
            vainqueurs_bandes.append(row['joueur1_bande'])
        elif vainqueur == row['joueur2_nom']:  # Comparer avec le nom du joueur 2
            vainqueurs_bandes.append(row['joueur2_bande'])
        elif vainqueur == row['joueur3_nom']:  # Comparer avec le nom du joueur 3
            vainqueurs_bandes.append(row['joueur3_bande'])
        elif vainqueur == row['joueur4_nom']:  # Comparer avec le nom du joueur 4
            vainqueurs_bandes.append(row['joueur4_bande'])

    # Calcul des victoires pour chaque bande
    bandes_noms = list(set(vainqueurs_bandes))  # Récupérer tous les noms uniques des bandes
    bd_victoires = {bande: vainqueurs_bandes.count(bande) for bande in bandes_noms}

    # Calcul du pourcentage de victoires par bande
    pourcentages_vict_par_bande = {
        bande: (bd_victoires[bande] / total_parties * 100) if total_parties > 0 else 0
        for bande in bd_victoires
    }

    # Trouver la bande ayant le plus gagné
    bande_ayant_le_plus_gagne = max(pourcentages_vict_par_bande, key=pourcentages_vict_par_bande.get)



    # Générer les statistiques pour chaque joueur
    statistiques_joueurs = []
    for joueur in joueurs_noms:
        nombre_victoires = victoires[joueur]
        pourcentage_victoires = pourcentage_victoires_par_joueur[joueur]
        
        # Récupérer le nom et la bande du joueur
        joueur_bande = None
        for i in range(1, 5):  # On suppose qu'il y a 4 joueurs maximum
            joueur_nom = conn.execute(f'SELECT DISTINCT joueur{i}_nom FROM partie WHERE joueur{i}_nom = ?', (joueur,)).fetchone()
            if joueur_nom:
                joueur_bande = conn.execute(f'SELECT DISTINCT joueur{i}_bande FROM partie WHERE joueur{i}_nom = ?', (joueur,)).fetchone()[0]
                break

        statistiques_joueurs.append({
            'nom': joueur,
            'bande': joueur_bande,
            'nombre_victoires': nombre_victoires,
            'pourcentage_victoires': pourcentage_victoires
        })

    conn.close()

    # Renvoyer les données au template
    return render_template(
        'stats.html',
        total_parties=total_parties,
        pourcentage_victoires_par_joueur=pourcentage_victoires_par_joueur,
        bande_ayant_le_plus_gagne=bande_ayant_le_plus_gagne,
        statistiques_joueurs=statistiques_joueurs
    )

@app.route('/ajouter_carte', methods=['GET', 'POST'])
def ajouter_carte():
    if request.method == 'POST':
        nom = request.form['nom']
        type_carte = request.form['type']
        saison = request.form['saison']
        alliance = request.form['alliance']
        numero_serie = request.form['numero_serie']
        disponibilite = request.form['disponibilite']

        conn = get_db_connection()
        conn.execute('INSERT INTO cartes (nom, type, saison, alliance, numero_serie, disponibilite) VALUES (?, ?, ?, ?, ?, ?)',
                     (nom, type_carte, saison, alliance, numero_serie, disponibilite))
        conn.commit()
        conn.close()

        return redirect('/collection')

    return render_template('ajouter_carte.html')


@app.route('/collection', methods=['GET', 'POST'])
def collection():
    search = request.args.get('search', '')
    conn = get_db_connection()
    query = """
        SELECT nom, type, saison, alliance, numero_serie, disponibilite
        FROM cartes
        WHERE nom LIKE ? OR type LIKE ? OR saison LIKE ? OR alliance LIKE ?
    """
    cartes = conn.execute(query, (f'%{search}%', f'%{search}%', f'%{search}%', f'%{search}%')).fetchall()
    conn.close()
    return render_template('collection.html', cartes=cartes)

from flask import jsonify

@app.route('/modifier_disponibilite', methods=['POST'])
def modifier_disponibilite():
    data = request.json
    carte_id = data['id']
    saison = data['saison']
    nouvelle_disponibilite = data['nouvelle_disponibilite']

    conn = get_db_connection()
    conn.execute('''
        UPDATE cartes
        SET disponibilite = ?
        WHERE id = ? AND saison = ?
    ''', (nouvelle_disponibilite, carte_id, saison))
    conn.commit()
    conn.close()

    return jsonify({"id": carte_id, "saison": saison, "nouvelle_disponibilite": nouvelle_disponibilite})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
