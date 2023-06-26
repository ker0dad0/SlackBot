import os
import json

# Fonction pour lire le fichier JSON et extraire les messages de chaque conversation
def lire_fichier_json(nom_fichier):
    conversations = {}
    conversation_count = 1  # Compteur de conversation
    with open(nom_fichier, 'r') as fichier:
        contenu = json.load(fichier)
        for message in contenu:
            if 'user' in message and 'text' in message:
                auteur = message['user']
                texte = message['text']
                thread_ts = message.get('thread_ts')
                if thread_ts:
                    conversation_key = f"conversation{thread_ts.split('.')[1]}"
                    if conversation_key in conversations:
                        conversations[conversation_key].append(f"{auteur}: {texte}")
                    else:
                        conversations[conversation_key] = [f"{auteur}: {texte}"]
                else:
                    # Nouvelle conversation
                    conversation_key = f"conversation{conversation_count}"
                    conversations[conversation_key] = [f"{auteur}: {texte}"]
                    conversation_count += 1
    return conversations

# Fonction pour enregistrer les conversations dans un fichier texte
def enregistrer_conversations(conversations, nom_fichier):
    with open(nom_fichier, 'a') as fichier:
        for conversation in conversations.values():
            fichier.write('\n'.join(conversation) + '\n\n')

# Chemin vers le répertoire contenant les fichiers JSON
repertoire = r'H:\Desktop\SlackBot1\bancs-m3-1'

# Enregistrement dans le fichier 'conversation.txt'
nom_fichier_sortie = r'H:\Desktop\SlackBot1\base_de_connaissances\conversation.txt'

# Parcours de tous les fichiers JSON dans le répertoire
# et enregistrement des conversations dans le fichier texte
for fichier in os.listdir(repertoire):
    if fichier.endswith('.json'):
        chemin_fichier = os.path.join(repertoire, fichier)
        conversations = lire_fichier_json(chemin_fichier)
        enregistrer_conversations(conversations, nom_fichier_sortie)

print("Toutes les conversations ont été fusionnées et enregistrées dans le fichier 'conversation.txt'.")