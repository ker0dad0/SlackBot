import json
import openai
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Clé d'accès à l'API OpenAI
openai.api_key = "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"

# Token d'accès à l'API Slack
slack_token = "xoxb-5437654720864-5465085293409-CZAISxJebkDCBZU8EFgdiuAa"

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

# Chemin vers le fichier JSON
chemin_fichier = r'H:\Desktop\SlackBot1\base_de_connaissances\2023-06-20.json'

# Charger les données du fichier JSON
with open(chemin_fichier, "r") as fichier:
    donnees = json.load(fichier)

def traiter_message(event):
    message_text = event["text"]
    if "<@A05D7EL0A69>" in message_text:
        # Extraction du texte après '@Bot'
        question = message_text.split("<@A05D7EL0A69>", 1)[1].strip()
        poser_question(question)



def generer_reponse(requete_utilisateur, base_de_connaissances):
    prompt = f"statorm31 correspond à une extract de slack des échanges du support AIDA, et que chaque conversation représente un default MOM sur l'une des OP de la ligne stator M3.1"
    prompt += "La ligne stator M3.1 est constituée des OP (op115.01; op115.02; etc; op120.01 etc), y en a plein donc un OP est constitué de 'op' et un 'numéro' et '.' et un autre 'numéro'."
    prompt += "Pour la base de connaissances qu'on va te donner, concentre-toi juste sur les 'text', c'est là où se trouvent les réponses que nous cherchons. Ne perds pas de temps à lire le fichier JSON en entier."
    prompt += "Une OP représente une opération de production réalisé sur une ligne de production"
    prompt += "Les opérations OP 130 et OP 140 font partie de la ligne de production Stator M3.1"
    prompt += "l'outil MOM: Manufacturing Operator Management, est un outil qui permet de récolter la traçabilité des produits fabriqués sur chaque ligne à à toutes les étapes du process. Nous avons donc activé cette outil sur chaque OP de la ligne stator M3.1. Il arrive que le MOM passe en défaut sur l'une des OP de la ligne. Le type de default, la cause et la solution à apporter peuvent être multiple."
    prompt += "l'impression de l'étiquette Galia à lieu dans l'OP 470 sur la ligne d'Assemblage M3.1"
    prompt += f"{base_de_connaissances}\nQuestion : {requete_utilisateur}\nRéponse :"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        temperature=0.01,
        n=5,  # Augmenter le nombre de réponses générées
        stop=None
    )
    
    best_choice = None
    best_score = float('-inf')
    for choice in response.choices:
        score = choice.get("score", 0)
        if score > best_score:
            best_choice = choice
            best_score = score

    reponse = best_choice["text"].strip() if best_choice else ""
    return reponse



def poser_question():
    # Capturer la requête de l'utilisateur
    requete_utilisateur = input("Posez votre question : ")

    # Générer et stocker les réponses dans une liste
    reponses = []
    for segment in donnees:
        base_de_connaissances = json.dumps(segment)
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
        poser_question()

if __name__ == '__main__':
    main()
