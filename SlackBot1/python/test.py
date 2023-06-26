import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slackeventsapi import SlackEventAdapter
import openai

# Clé d'accès à l'API OpenAI
openai.api_key = "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"

# Token d'accès à l'API Slack
slack_token = "xoxb-5437654720864-5466696960867-cqSrDJflXfFSZHY5r3KZz1A7"

# Nom du channel
channel_name = "statorm31"

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

# Chemin vers le fichier texte de base de connaissances
chemin_fichier = r'H:\Desktop\SlackBot1\base_de_connaissances\conversation.txt'

# Charger les données du fichier texte
with open(chemin_fichier, 'r') as fichier:
    base_de_connaissances = fichier.read()

# Initialiser l'adaptateur d'événements Slack
slack_events_adapter = SlackEventAdapter("1aef5f76aa866c01234702f5f5931c09", "/slack/events")

@slack_events_adapter.on("message")
def traiter_message(event_data):
    message = event_data["event"]
    if message.get("subtype") is None and "<@A05D7EL0A69>" in message.get("text", ""):
        # Extraction du texte après '@Bot'
        question = message["text"].split("<@A05D7EL0A69>", 1)[1].strip()
        reponse = generer_reponse(question)
        envoyer_reponse(reponse)

def generer_reponse(requete_utilisateur):
    # OpenAI pour générer une réponse basée sur la requête de l'utilisateur et les données du fichier texte
    prompt = f"{base_de_connaissances}\nQuestion : {requete_utilisateur}\nRéponse :"
    instructions = "Le problème pourrait nécessiter une discussion plus approfondie. veuillez lire attentivement la discussion et fournir une réponse complète à la fin. prenez en compte tous les éléments mensionnés."

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{prompt}\nInstructions : {instructions}",
        max_tokens=300,
        temperature=0,
        n=1,
        stop=None
    )
    reponse = response.choices[0].text.strip()
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

if __name__ == '__main__':
    slack_events_adapter.start(host="0.0.0.0", port=5000)

