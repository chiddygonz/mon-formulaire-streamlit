import streamlit as st
import gspread
from datetime import datetime, time, date # Importez time et date en plus de datetime

# --- Configuration Google Sheets (ne change pas par rapport à ce qui a fonctionné) ---
try:
    gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    # Remplacez VOTRE_URL_GOOGLE_SHEET par l'URL de votre Google Sheet
    spreadsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1BHB0xxPLZNyj42G8rwvo7wqLU5qfhJaUNJXMdSqvDxE/edit?gid=0#gid=0")
    worksheet = spreadsheet.worksheet("Sheet1") # Assurez-vous que c'est le bon nom de feuille
except Exception as e:
    st.error(f"Erreur de connexion à Google Sheets : {e}")
    st.stop() # Arrête l'exécution de l'application si la connexion échoue

# --- Titre de l'application ---
st.title("👶 Suivi de Bébé")
st.markdown("---")

# --- Sélecteur de type d'activité ---
type_activite = st.selectbox(
    "Quelle activité souhaitez-vous enregistrer ?",
    ["Sélectionner...", "Tétée / Biberon", "Couche", "Sommeil", "Autre"]
)

st.markdown("---")

# --- Formulaire principal avec sections conditionnelles ---
# Utilisation de st.form pour que tous les champs soient soumis en même temps
with st.form("enregistrement_activite_bebe"):
    st.subheader("Informations de l'activité")

    # Champs communs à toutes les activités
    col1, col2 = st.columns(2)
    with col1:
        date_activite = st.date_input("Date de l'activité", value=date.today())
    with col2:
        heure_debut = st.time_input("Heure de début", value=datetime.now().time())

    heure_fin = None
    details = ""
    notes = ""

    # Sections conditionnelles basées sur le type d'activité
    if type_activite == "Tétée / Biberon":
        st.markdown("##### Détails de l'alimentation")
        heure_fin = st.time_input("Heure de fin", value=datetime.now().time())
        type_alimentation = st.radio("Type d'alimentation", ["Tétée", "Biberon"], horizontal=True)

        if type_alimentation == "Tétée":
            cote_allaitement = st.radio("Côté", ["Gauche", "Droit", "Les deux"], horizontal=True)
            details = f"Tétée - Côté: {cote_allaitement}"
        else: # Biberon
            quantite_biberon = st.number_input("Quantité (ml)", min_value=0, value=60, step=10)
            details = f"Biberon - Quantité: {quantite_biberon} ml"

    elif type_activite == "Couche":
        st.markdown("##### Détails de la couche")
        type_couche_options = st.multiselect(
            "Type de couche",
            ["Pipi", "Caca"],
            default=["Pipi"] # Valeur par défaut
        )
        details = ", ".join(type_couche_options)
        notes = st.text_area("Notes (couleur, consistance...)", "")

    elif type_activite == "Sommeil":
        st.markdown("##### Détails du sommeil")
        heure_fin = st.time_input("Heure de fin du sommeil", value=datetime.now().time())
        type_sommeil = st.radio("Type de sommeil", ["Sieste", "Nuit"], horizontal=True)
        details = f"Type: {type_sommeil}"
        notes = st.text_area("Notes (agitation, endormissement...)", "")

    elif type_activite == "Autre":
        st.markdown("##### Détails de l'activité 'Autre'")
        details = st.text_input("Brève description de l'activité", "")
        notes = st.text_area("Notes supplémentaires", "")
        # Optionnel: si 'Autre' a une durée
        heure_fin = st.time_input("Heure de fin (optionnel)", value=datetime.now().time())


    # Bouton de soumission du formulaire
    submitted = st.form_submit_button("👶 Enregistrer l'activité")

    if submitted:
        if type_activite == "Sélectionner...":
            st.warning("Veuillez sélectionner un type d'activité.")
        else:
            try:
                # Préparer les données à envoyer
                # Convertir les objets date/time en chaînes pour Google Sheets
                row_data = [
                    str(date_activite),
                    type_activite,
                    str(heure_debut),
                    str(heure_fin) if heure_fin else "", # Gérer le cas où heure_fin est None
                    details,
                    notes
                ]
                
                # Écrire la nouvelle ligne dans Google Sheets
                worksheet.append_row(row_data)
                st.success("✅ Activité enregistrée avec succès dans Google Sheets !")
                st.balloons() # Petite animation de célébration

            except Exception as e:
                st.error(f"❌ Erreur lors de l'enregistrement dans Google Sheets : {e}")

st.markdown("---")

# --- Affichage des dernières activités (pour vérifier que ça marche) ---
st.subheader("Historique des dernières activités")
try:
    # Récupérer toutes les données de la feuille
    all_records = worksheet.get_all_records()
    if all_records:
        # Afficher les 10 dernières activités dans un tableau
        # Les records sont des dictionnaires, nous pouvons les convertir en DataFrame si besoin
        import pandas as pd
        df = pd.DataFrame(all_records)
        # Inverser l'ordre pour avoir les plus récentes en haut
        st.dataframe(df.tail(10).sort_values(by="Date", ascending=False).reset_index(drop=True))
    else:
        st.info("Aucune activité enregistrée pour le moment.")
except Exception as e:
    st.error(f"Erreur lors de la récupération des données : {e}")