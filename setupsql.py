import sqlite3

def create_table():
    conn = sqlite3.connect('jeu.db')  # Crée ou ouvre une base de données nommée jeu.db
    cursor = conn.cursor()
    
    # Création de la table "partie"
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS partie (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            joueur1_nom TEXT,
            joueur2_nom TEXT,
            joueur3_nom TEXT,
            joueur4_nom TEXT,
            joueur1_bande TEXT,
            joueur2_bande TEXT,
            joueur3_bande TEXT,
            joueur4_bande TEXT,
            joueur1_points INTEGER,
            joueur2_points INTEGER,
            joueur3_points INTEGER,
            joueur4_points INTEGER,
            vainqueur INTEGER
        )
    ''')
    
    conn.commit()
    conn.close()

# Appelez cette fonction une fois pour créer la table
create_table()
