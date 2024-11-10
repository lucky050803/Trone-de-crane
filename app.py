from flask import Flask, request, render_template, redirect
import sqlite3
from datetime import datetime
def get_db_connection():
    conn = sqlite3.connect('jeu.db')  # Assurez-vous que le fichier DB existe
    conn.row_factory = sqlite3.Row  # Pour accéder aux colonnes par nom
    return conn

app = Flask(__name__)
def max_variable(a, b, c, d):
    # Créer un dictionnaire avec les noms des variables comme clés et leurs valeurs comme valeurs
    variables = {'J1': a, 'J2': b, 'J3': c, 'J4': d}
    
    # Trouver le nom de la variable avec la valeur maximale
    max_var = max(variables, key=variables.get)
    
    return max_var
# Fonction pour insérer les données dans la base de données
def insert_data(date, joueur1_bande,joueur1_nom, joueur1_points, joueur2_bande,joueur2_nom, joueur2_points,
                joueur3_bande,joueur3_nom, joueur3_points, joueur4_bande,joueur4_nom, joueur4_points):
    
    conn = sqlite3.connect('jeu.db')
    cursor = conn.cursor()
    vainqueur = max_variable(joueur1_points, joueur2_points, joueur3_points, joueur4_points)
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



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
