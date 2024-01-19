import streamlit as st
import pandas as pd

# ... (Configuration de la page et style personnalisé) ...

# Création de la connexion à la base de données
conn = st.connection('suivie_db', type='sql')


# --- GENERAL SETTINGS ---
AUTHOR = "Noel Snelson"
CONTACT = "Snelsonpro@gmail.com"

# --- SIDEBAR ---
with st.sidebar:
    st.title('BUT')
    st.write("""Dans le cadre d'une enquête sur l'utilisation de l'intelligence artificielle, 
             l'IUT Paris Cité cherche à obtenir l'avis des étudiants sur cette question.""")
    st.write(f"**Auteur:** {AUTHOR}")
    st.write(f"**Contact:** {CONTACT}")

# ... (Reste de votre code pour la connexion à la base de données et l'interface utilisateur) ...

    
    # Formulaire de suppression
    with st.form("form_delete"):
        st.markdown("## 🗑️ Supprimer un enregistrement")
        delete_id = st.number_input("Entrez l'ID à supprimer", min_value=1, step=1)
        submit_delete = st.form_submit_button("Supprimer l'enregistrement")

        if submit_delete:
            with conn.session as s:
                # Exécuter la requête de suppression
                s.execute(
                    'DELETE FROM Info WHERE ID = :id;',
                    params=dict(id=delete_id)
                    )
                s.commit()

# Header
st.header("📝 Enquête")

# Formulaire de contact
with st.form("Formulaire"):
    st.markdown("## 📋 Formulaire de contact")
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        people_name = st.text_input("Nom de famille")
        phone_number = st.text_input("Numéro de téléphone")
        Fillière = st.selectbox("Fillière", ["GEA", "STID", "CA", "TC", "INFO"])


    with col2:
        people_username = st.text_input("Prénom")
        email = st.text_input("Email")

    with col3:
        Réponse = st.text_area("Votre avis sur l'utilisation des IA")

    # Validation du numéro de téléphone
    try:
        int(phone_number)
        if len(phone_number) != 10:
            st.error("Le numéro de téléphone doit contenir 10 chiffres.")
            phone_valid = False
        else:
            phone_valid = True
    except ValueError:
        st.error("Veuillez renseigner un chiffre pour le numéro de téléphone.")
        phone_valid = False

    # Validation de l'email
    if '@' not in email:
        st.error("Veuillez entrer une adresse email valide.")
        email_valid = False
    else:
        email_valid = True

    is_valid = phone_valid and email_valid

    submitted = st.form_submit_button("Soumettre")
    if submitted and is_valid:
       with conn.session as s:
            # Créer la table si elle n'existe pas avec ID auto-incrémenté
            s.execute(
                '''CREATE TABLE IF NOT EXISTS Info (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                    people_name TEXT, 
                    people_username TEXT, 
                    phone_number INT,
                    Fillière TEXT,
                    email TEXT,
                    Réponse TEXT
                );'''
            )
            # Insérer les nouvelles données dans la base de données
            s.execute(
                '''INSERT INTO Info (people_name, people_username, phone_number, Fillière, email, Réponse) 
                   VALUES (:name, :username, :phone, :Fillière, :email, :Réponse);''',
                params=dict(name=people_name, username=people_username, phone=phone_number, Fillière=Fillière, email=email, Réponse=Réponse)
            )
            s.commit()

# Affichage des données
st.markdown("## 📊 Données enregistrées")
with conn.session as s:
    st.cache_data.clear()
    query_result = conn.query('SELECT * FROM Info')
    df = pd.DataFrame(query_result)
    df.set_index('ID', inplace=True)

    # Style du DataFrame
    st.dataframe(df.style.apply(lambda x: ['background: lightblue' if x.name % 2 == 0 else '' for i in x], axis=1))
