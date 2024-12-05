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
            vainqueur TEXT
        )
    ''')
    
    # Création de la table "cartes"
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cartes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('objectif', 'stratagème', 'équipement', 'sort')),
            saison TEXT NOT NULL CHECK(saison IN ('Shadepsire', 'Nightvault', 'Beastgrave', 'Direchasm', 'Starter set 2021', 'Harrowdeep', 'Nethermaze', 'Gnarlwood', 'Wyrdhollow', 'Starter set 2023', 'Deathgorge', 'Wintermaw')),
            alliance TEXT NOT NULL CHECK(alliance IN ('mort', 'chaos', 'destruction', 'ordre')),
            numero_serie TEXT NOT NULL UNIQUE,
            disponibilite TEXT NOT NULL CHECK(disponibilite LIKE 'Deck' OR disponibilite IN ('dispo', 'non posséder'))
        )
    ''')

    conn.commit()
    conn.close()

# Appelez cette fonction une fois pour créer ou mettre à jour les tables
create_table()
