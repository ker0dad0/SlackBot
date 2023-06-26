from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import indexjson

slack_token = "xoxb-5437654720864-5465085293409-CZAISxJebkDCBZU8EFgdiuAa"
channel = "#statorm31"
bot_user_id = "A05D7EL0A69"  # Remplacez par l'ID utilisateur du bot

# Créer une instance du client Slack
slack_client = WebClient(token=slack_token)

def poser_question():
    try:
        # Envoyer une première question dans Slack
        response = slack_client.chat_postMessage(
            channel=channel,
            text="Hello!!"
        )
        print("Question envoyée avec succès dans Slack")
    except SlackApiError as e:
        print(f"Erreur lors de l'envoi de la question dans Slack : {e.response['error']}")
        return

    # Récupérer l'ID du message envoyé
    message_id = response["ts"]

    while True:
        try:
            # Attendre une réponse de l'utilisateur
            events = slack_client.conversations_history(
                channel=channel,
                latest=message_id,
                limit=1
            )
            if events["messages"]:
                user_response = events["messages"][0]["text"]
                print("Réponse de l'utilisateur :", user_response)

                # Générer et envoyer la réponse dans Slack
                reponse = indexjson.generer_reponse(user_response)
                try:
                    response = slack_client.chat_postMessage(
                        channel=channel,
                        text=reponse
                    )
                    print("Réponse envoyée avec succès dans Slack")
                except SlackApiError as e:
                    print(f"Erreur lors de l'envoi de la réponse dans Slack : {e.response['error']}")
                break  # Sortir de la boucle après avoir traité la réponse de l'utilisateur
        except SlackApiError as e:
            print(f"Erreur lors de la récupération de la réponse de l'utilisateur : {e.response['error']}")
            break

# Appeler la fonction poser_question pour commencer l'échange sur Slack
poser_question()
