import socket
import ssl

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile='server.crt', keyfile='server.key')

sserveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sserveur.bind(('192.168.214.129', 50000))
sserveur.listen(5)

print("Serveur sur ecoute...")

while True:
    print("En attente de connexion...")
    sclient, addrclient = sserveur.accept()
    sclient = context.wrap_socket(sclient, server_side=True)
    print("Connexion de :", addrclient)
    
    try:
    	while True:
    		message = sclient.recv(1024)
    		if not message:
          		break # Si le client a fermer la connexion
    		print("Message reçu :", message.decode('utf-8'))
    		sclient.sendall(b"Message bien recived")
    except ConnectionResetError:
    	print("Connexion fermee par le client")
    finally:
    	sclient.close() #Fermeture du client 
sserveur.close() #Fermeture du serveur
