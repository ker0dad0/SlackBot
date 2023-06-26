import os
import openai

# Chemin vers le répertoire de base de connaissances
repertoire_base_connaissances = r'H:\Desktop\SlackBot1\base_de_connaissances'

# Clé d'accès à l'API OpenAI
openai.api_key = "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"


def charger_base_de_connaissances():
    base_de_connaissances = ""
    for fichier in os.listdir(repertoire_base_connaissances):
        chemin_fichier = os.path.join(repertoire_base_connaissances, fichier)
        with open(chemin_fichier, 'r', encoding='latin-1') as fichier:
            base_de_connaissances += fichier.read() + "\n"
    return base_de_connaissances

def generer_reponse(requete_utilisateur):
    # Charger les données de la base de connaissances
    base_de_connaissances = charger_base_de_connaissances()

    # Combinez la requête de l'utilisateur et la base de connaissances
    texte_combiné = requete_utilisateur + "\n" + base_de_connaissances

    # Utiliser l'API OpenAI pour générer une réponse
    response = openai.Completion.create(
        engine="ada",
        prompt=texte_combiné,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7
    )

    reponse = response.choices[0].text.strip()
    return reponse

def poser_question():
    # Capturer la requête de l'utilisateur
    requete_utilisateur = input("Posez votre question : ")
    
    # Générer et afficher la réponse
    reponse = generer_reponse(requete_utilisateur)
    print("Réponse : ", reponse)

def main():
    while True:
        poser_question()

if __name__ == '__main__':
    main()
