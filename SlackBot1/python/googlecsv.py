import pandas as pd
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from google.cloud import language_v1

# Token d'accès à l'API Slack
slack_token = "xoxb-5437654720864-5466696960867-cqSrDJflXfFSZHY5r3KZz1A7"

# Nom du channel
channel_name = "statorm31"

# Clé d'accès à l'API Google Cloud
google_cloud_key = r'H:\Desktop\SlackBot1\base_de_connaissances\cle.json'

# Créer une instance du client Slack
slack_client = WebClient(token=slack_token)

# Récupérer l'ID du channel en utilisant son nom
response = slack_client.conversations_list()
channels = response["channels"]
channel_id = None
for channel in channels:
    if channel["name"] == channel_name:
        channel_id = channel["id"]
        break

if channel_id is None:
    print(f"Le channel '{channel_name}' n'a pas été trouvé.")
    exit()

# Chemin vers le fichier Excel
chemin_fichier = r'H:\Desktop\SlackBot1\base_de_connaissances\info.xlsx'

# Charger les données du fichier Excel
df = pd.read_excel(chemin_fichier, engine='openpyxl')

# Créer une instance du client Google Cloud
client = language_v1.LanguageServiceClient.from_service_account_json(google_cloud_key)


def traiter_message(event):
    message_text = event["text"]
    if "<@A05D7EL0A69>" in message_text:
        # Extraction du texte après '@Bot'
        question = message_text.split("<@A05D7EL0A69>", 1)[1].strip()
        reponse = generer_reponse(question)
        envoyer_reponse(reponse)


def generer_reponse(requete_utilisateur):
    # Google Cloud pour analyser la requête de l'utilisateur
    document = language_v1.Document(content=requete_utilisateur, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_entities(request={'document': document})
    entities = response.entities
    keywords = [entity.name for entity in entities]

    # Recherche dans les données du fichier Excel
    reponse = ""
    for keyword in keywords:
        if "problèmes" in df.columns:
            reponse_df = df[df["problèmes"].str.contains(keyword, case=False, na=False)]
            if not reponse_df.empty:
                reponse += reponse_df.iloc[0]["solution"] + "\n"

    return reponse


def envoyer_reponse(reponse):
    if reponse:
        try:
            response = slack_client.chat_postMessage(
                channel=channel_id,
                text=reponse
            )
            print("Réponse envoyée avec succès dans Slack")
        except SlackApiError as e:
            print(f"Erreur lors de l'envoi de la réponse dans Slack : {e.response['error']}")


def main():
    while True:
        poser_question()


def poser_question():
    # Capturer la requête de l'utilisateur
    requete_utilisateur = input("Posez votre question : ")

    # Générer et afficher la réponse
    reponse = generer_reponse(requete_utilisateur)
    print("Réponse : ", reponse)
    envoyer_reponse(reponse)


if __name__ == '__main__':
    main()
