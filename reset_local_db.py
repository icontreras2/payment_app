import os
import shutil

CUR_DIR = os.getcwd()

def reset_local_db():
    """Resets the Development Database with (Newer) Data + Models"""
    print("Start: Reset DB")
    print(">>> Deleting All Tables from Database")
    if os.path.exists(f"{CUR_DIR}/db.sqlite3"):
        os.remove(f"{CUR_DIR}/db.sqlite3")
    else:
        print(f"The file '{CUR_DIR}/db.sqlite3' does not yet exist.")

    print(">>> Deleting Migrations File to Ensure Updated Models")
    if os.path.isdir(f"{CUR_DIR}/payment_app/migrations"):
        shutil.rmtree(f"{CUR_DIR}/payment_app/migrations")
    else:
        print(f"The '{CUR_DIR}/payment_app/migrations' directory does not yet exist.")
    print("Finish: Reset DB")

if __name__ == "__main__":
    reset_local_db()