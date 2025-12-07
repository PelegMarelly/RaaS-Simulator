import os

TARGET_FOLDER = "Ransomware_Test_Folder"

def create_environment():
    if not os.path.exists(TARGET_FOLDER):
        os.makedirs(TARGET_FOLDER)
        print(f"[+] Created folder: {TARGET_FOLDER}")

    files_to_create = [
        ("secret.txt", "This is a secret password."),
        ("financial.csv", "ID,Name,Salary\n1,Avi,10000\n2,Ben,20000"),
        ("image.png", "Fake image content"),
        ("work_doc.docx", "Important work document content.")
    ]

    for filename, content in files_to_create:
        file_path = os.path.join(TARGET_FOLDER, filename)
        with open(file_path, "w") as f:
            f.write(content)
        print(f"[+] Created file: {file_path}")

    print("\nEnvironment Ready!")

if __name__ == "__main__":
    create_environment()
