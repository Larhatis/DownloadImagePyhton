from selenium import webdriver
from requests_toolbelt import sessions
import os
import uuid
import shutil

# Fonction pour télécharger une image
def telecharger_image(url_image, nom_fichier):
    # Définir la session avec gestion du CORS
    session = sessions.BaseUrlSession(base_url=url_image)

    # Envoyer une requête GET pour obtenir l'image
    reponse = session.get(url_image)

    # Vérifier le code de status
    if reponse.status_code == 200:
        # Enregistrer l'image dans un fichier
        with open(nom_fichier, "wb") as fichier:
            fichier.write(reponse.content)
    else:
        print(f"Erreur lors du téléchargement de l'image {url_image} : {reponse.status_code}")

# Dossier où les images seront téléchargées
dossier_destination = 'images_telechargees'

# Créer le dossier de destination s'il n'existe pas
os.makedirs(dossier_destination, exist_ok=True)

# Demander à l'utilisateur l'URL de la page web
url_page = input("Entrez l'URL de la page web : ")

# Démarrer le driver Selenium
driver = webdriver.Chrome()

# Accéder à la page web
driver.get(url_page)

# Trouver toutes les balises img
images = driver.find_elements("css selector", "img")

# Télécharger les images
for image in images:
    # Générer un nom de fichier unique avec un UUID
    nom_fichier = os.path.join(dossier_destination, f"image_{str(uuid.uuid4())}.jpg")

    # Télécharger l'image
    telecharger_image(image.get_attribute('src'), nom_fichier)

# Fermer le driver Selenium
driver.quit()
