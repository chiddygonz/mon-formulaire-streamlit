import json

# Assurez-vous que le fichier gcp_service_account.json est dans le même dossier
# Ou ajustez le chemin d'accès si nécessaire
try:
    with open("gcp_service_account.json", "r") as f:
        secrets_data = json.load(f)

    toml_secret = "[gcp_service_account]\n"
    for key, value in secrets_data.items():
        if key == "private_key":
            # Pour la clé privée, nous utilisons des guillemets triples pour gérer les retours à la ligne
            # et nous nous assurons qu'il n'y a pas de nouvelle ligne après la fin de la clé.
            toml_secret += f'private_key = """{value.strip()}"""\n'
        elif isinstance(value, str):
            toml_secret += f'{key} = "{value}"\n'
        else:
            toml_secret += f'{key} = {value}\n'

    print("--- Copiez tout le texte ci-dessous et collez-le dans les secrets de Streamlit Cloud ---")
    print(toml_secret)
    print("--- Fin du texte à copier ---")

except FileNotFoundError:
    print("Erreur : Le fichier 'gcp_service_account.json' n'a pas été trouvé.")
    print("Assurez-vous qu'il est dans le même dossier que 'generate_secret.py' ou modifiez le chemin.")
except json.JSONDecodeError:
    print("Erreur : Le fichier 'gcp_service_account.json' n'est pas un JSON valide. Il est peut-être corrompu.")