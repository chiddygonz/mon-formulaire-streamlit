import streamlit as st
import gspread
from datetime import datetime

# --- Configuration des identifiants Google Sheets ---
# Pour le déploiement sur Streamlit Cloud, vous utiliserez les Secrets de Streamlit.
# Pour l'exécution locale, assurez-vous que 'gcp_service_account.json' est dans le même dossier.
try:
    # Tente de charger les informations d'identification via les secrets de Streamlit (pour le déploiement)
    gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
except FileNotFoundError:
    # Si le fichier n'est pas trouvé (exécution locale), charge depuis le fichier JSON
    gc = gspread.service_account(filename="gcp_service_account.json")

# Ouvrir la feuille de calcul par son nom (utilisez le nom exact que vous avez donné)
try:
    spreadsheet = gc.open("DonneesUtilisateursStreamlit") # <-- REMPLACEZ PAR LE NOM DE VOTRE FEUILLE GOOGLE
except gspread.exceptions.SpreadsheetNotFound:
    st.error("Feuille Google non trouvée. Vérifiez le nom et les permissions.")
    st.stop()

worksheet = spreadsheet.worksheet("Sheet1") # <-- REMPLACEZ SI VOTRE ONGLET N'EST PAS 'Feuille1'

# --- Titre de l'application ---
st.title("Formulaire d'enregistrement d'utilisateur")
st.write("Veuillez remplir les informations ci-dessous.")

# --- Création du formulaire ---
with st.form("user_form"):
    st.header("Informations personnelles")

    nom = st.text_input("Nom :")
    prenom = st.text_input("Prénom :")
    age = st.number_input("Âge :", min_value=0, max_value=120, value=25, step=1)

    submitted = st.form_submit_button("Enregistrer les informations")

if submitted:
            if nom and prenom and age:
                # Récupérer la date et l'heure actuelles
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Ajouter une nouvelle ligne à la feuille Google
                try:
                    worksheet.append_row([nom, prenom, age, current_time])
                    st.success("Informations enregistrées avec succès dans Google Sheets !")
                    # Optionnel : effacer le formulaire après soumission réussie
                    # ANCIEN : st.experimental_rerun()
                    st.rerun() # <-- REMPLACEZ ICI !
                except Exception as e:
                    st.error(f"Une erreur est survenue lors de l'enregistrement : {e}")
                    st.warning("Vérifiez les permissions de votre compte de service et le partage de la feuille.")
            else:
                st.warning("Veuillez remplir tous les champs du formulaire.")

# --- Optionnel : Afficher les données existantes (pour debug/vérification) ---
st.subheader("Données enregistrées (dernières 10 entrées)")
try:
    data = worksheet.get_all_records() # Récupère toutes les lignes comme une liste de dictionnaires
    if data:
        # Afficher les dernières entrées, ou toutes si moins de 10
        st.dataframe(data[-10:][::-1]) # Affiche les 10 dernières entrées, les plus récentes en haut
    else:
        st.info("Aucune donnée enregistrée pour le moment.")
except Exception as e:
    st.error(f"Impossible de charger les données existantes : {e}")