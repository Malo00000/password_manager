from cryptography.fernet import Fernet
import json
import os

# Génération et sauvegarde de la clé de chiffrement
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    return key

# Chargement de la clé de chiffrement
def load_key():
    return open("secret.key", "rb").read()

# Initialisation de Fernet
def init_cipher():
    key = load_key()
    return Fernet(key)

# Stockage sécurisé des mots de passe
def store_passwords(password_dict):
    cipher = init_cipher()
    with open("passwords.enc", "wb") as password_file:
        encrypted_data = cipher.encrypt(json.dumps(password_dict).encode())
        password_file.write(encrypted_data)

# Récupération des mots de passe
def retrieve_passwords():
    cipher = init_cipher()
    with open("passwords.enc", "rb") as password_file:
        encrypted_data = password_file.read()
        decrypted_data = cipher.decrypt(encrypted_data)
    return json.loads(decrypted_data)

# Suppression d'un mot de passe
def delete_password(site):
    passwords = retrieve_passwords()
    if site in passwords:
        del passwords[site]
        store_passwords(passwords)
        return True
    return False

if __name__ == "__main__":
    if not os.path.exists("secret.key"):
        generate_key()
    
    while True:
        action = input("Voulez-vous (A)jouter, (R)écupérer, (S)upprimer ou (Q)uitter? ").upper()
        if action == "A":
            site = input("Entrez le site web: ")
            pwd = input("Entrez le mot de passe: ")
            existing_passwords = retrieve_passwords() if os.path.exists("passwords.enc") else {}
            existing_passwords[site] = pwd
            store_passwords(existing_passwords)
            print("Mot de passe enregistré avec succès!")
        elif action == "R":
            site = input("Entrez le site web pour récupérer le mot de passe: ")
            passwords = retrieve_passwords()
            print(f"Mot de passe: {passwords.get(site, 'Non trouvé')}")
        elif action == "S":
            site = input("Entrez le site web pour supprimer le mot de passe: ")
            if delete_password(site):
                print("Mot de passe supprimé avec succès.")
            else:
                print("Aucun mot de passe trouvé pour ce site.")
        elif action == "Q":
            print("Au revoir!")
            break
