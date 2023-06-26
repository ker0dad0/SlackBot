import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from google.cloud import language_v1

# Token d'accès à l'API Slack
slack_token = "xoxb-5437654720864-5465085293409-CZAISxJebkDCBZU8EFgdiuAa"

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

# Chemin vers le fichier JSON
chemin_fichier = r'H:\Desktop\SlackBot1\base_de_connaissances\2023-06-20.json'

# Charger les données du fichier JSON
with open(chemin_fichier, "r") as fichier:
    donnees = json.load(fichier)

# Créer une instance du client Google Cloud
client = language_v1.LanguageServiceClient.from_service_account_json(google_cloud_key)

def traiter_message(event):
    message_text = event["text"]
    if "<@A05D7EL0A69>" in message_text:
        # Extraction du texte après '@Bot'
        question = message_text.split("<@A05D7EL0A69>", 1)[1].strip()
        poser_question(question)

def generer_reponse(requete_utilisateur, base_de_connaissances):
    # Google Cloud pour analyser la requête de l'utilisateur
    document = language_v1.Document(content=requete_utilisateur, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_entities(request={'document': document})
    entities = response.entities
    keywords = [entity.name for entity in entities]

    # Recherche dans les données du fichier JSON
    reponse = ""
    for segment in base_de_connaissances:
        segment_text = segment["text"]
        segment_keywords = segment.get("keywords", [])
        matching_keywords = set(segment_keywords).intersection(keywords)
        if matching_keywords:
            reponse += segment_text + "\n"

    return reponse

def poser_question(requete_utilisateur):
    # Générer et stocker les réponses dans une liste
    reponses = []
    for segment in donnees:
        base_de_connaissances = segment["text"]
        reponse = generer_reponse(requete_utilisateur, base_de_connaissances)
        reponses.append(reponse)

    # Sélectionner la meilleure réponse
    if reponses:
        meilleure_reponse = max(reponses, key=len)
        print("Réponse : ", meilleure_reponse)

        # Envoyer la réponse dans Slack
        try:
            response = slack_client.chat_postMessage(
                channel=channel_id,
                text=meilleure_reponse
            )
            print("Réponse envoyée avec succès dans Slack")
        except SlackApiError as e:
            print(f"Erreur lors de l'envoi de la réponse dans Slack : {e.response['error']}")

def main():
    while True:
        requete_utilisateur = input("Posez votre question : ")
        poser_question(requete_utilisateur)

if __name__ == '__main__':
    main()
