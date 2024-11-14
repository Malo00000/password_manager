from cryptography.fernet import Fernet
import json
import os
import getpass

# Génération et sauvegarde de la clé de chiffrement avec mot de passe maître
def generate_key(password):
    key = Fernet.generate_key()
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    with open("master_password.enc", "wb") as pwd_file:
        pwd_file.write(encrypted_password)
    return key

# Chargement de la clé de chiffrement et vérification du mot de passe maître
def load_key_and_verify_password():
    key = open("secret.key", "rb").read()
    fernet = Fernet(key)
    with open("master_password.enc", "rb") as pwd_file:
        encrypted_password = pwd_file.read()
    while True:
        password = getpass.getpass("Entrez votre mot de passe maître pour continuer: ")
        try:
            if fernet.decrypt(encrypted_password).decode() == password:
                return key
            else:
                print("Mot de passe incorrect. Veuillez réessayer.")
        except Exception as e:
            print(f"Erreur de déchiffrement: {e}. Veuillez réessayer.")

# Initialisation de Fernet
def init_cipher(key):
    return Fernet(key)

# Stockage sécurisé des mots de passe
def store_passwords(password_dict, cipher):
    with open("passwords.enc", "wb") as password_file:
        encrypted_data = cipher.encrypt(json.dumps(password_dict).encode())
        password_file.write(encrypted_data)

# Récupération des mots de passe
def retrieve_passwords(cipher):
    with open("passwords.enc", "rb") as password_file:
        encrypted_data = password_file.read()
        decrypted_data = cipher.decrypt(encrypted_data)
    return json.loads(decrypted_data)

# Suppression d'un mot de passe
def delete_password(site, cipher):
    passwords = retrieve_passwords(cipher)
    if site in passwords:
        del passwords[site]
        store_passwords(passwords, cipher)
        return True
    return False

if __name__ == "__main__":
    if not os.path.exists("secret.key") or not os.path.exists("master_password.enc"):
        password = getpass.getpass("Créez un mot de passe maître: ")
        key = generate_key(password)
    else:
        key = load_key_and_verify_password()

    cipher = init_cipher(key)

    while True:
        action = input("Voulez-vous (A)jouter, (R)écupérer, (S)upprimer ou (Q)uitter? ").upper()
        if action == "A":
            site = input("Entrez le site web: ")
            pwd = input("Entrez le mot de passe: ")
            existing_passwords = retrieve_passwords(cipher) if os.path.exists("passwords.enc") else {}
            existing_passwords[site] = pwd
            store_passwords(existing_passwords, cipher)
            print("Mot de passe enregistré avec succès!")
        elif action == "R":
            site = input("Entrez le site web pour récupérer le mot de passe: ")
            passwords = retrieve_passwords(cipher)
            print(f"Mot de passe: {passwords.get(site, 'Non trouvé')}")
        elif action == "S":
            site = input("Entrez le site web pour supprimer le mot de passe: ")
            if delete_password(site, cipher):
                print("Mot de passe supprimé avec succès.")
            else:
                print("Aucun mot de passe trouvé pour ce site.")
        elif action == "Q":
            print("Au revoir!")
            break
