import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from requests_toolbelt import sessions
import uuid
import shutil
import time

def telecharger_image(url_image, nom_fichier):
    # Définir la session avec gestion du CORS
    session = sessions.BaseUrlSession(base_url=url_image)

    # Envoyer une requête GET pour obtenir l'image
    reponse = session.get(url_image)

    # Vérifier le code de statut
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

# Démarrer le driver Selenium en mode Headless avec le gestionnaire de pilotes
options = Options()
options.headless = True  # Firefox sans interface graphique mais ça marche pas, il s'ouvre quand même

# Utiliser le GeckoDriverManager pour récupérer le chemin de l'exécutable
gecko_path = GeckoDriverManager().install()

# Créer une instance du pilote Firefox avec le mode headless
driver = webdriver.Firefox(options=options)

try:
    driver.get(url_page)

    # Défilement de la page jusqu'en bas 
    scroll_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Attendre le déliement de la page
        new_scroll_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")
        if new_scroll_height == scroll_height:
            break
        scroll_height = new_scroll_height

    # Attendre de défilement de la page
    driver.implicitly_wait(5)

    # Rechercher toutes les balises img sur la page
    images = driver.find_elements("css selector", "img")

    # DL des images
    for image in images:
        # Générer un nom de fichier unique pour chaque image
        nom_fichier = os.path.join(dossier_destination, f"image_{str(uuid.uuid4())}.jpg")

        telecharger_image(image.get_attribute("src"), nom_fichier)
finally:
    # Fermeture du navigateur
    driver.quit()
