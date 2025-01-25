import os

def create_note():
    title = input("Enter the title of your note: ")
    content = input("Enter the content of your note: ")
    with open(f"{title}.txt", "w") as file:
        file.write(content)
    print(f"Note '{title}' created successfully!")

def read_note():
    title = input("Enter the title of the note to read: ")
    if os.path.exists(f"{title}.txt"):
        with open(f"{title}.txt", "r") as file:
            content = file.read()
        print(f"\n--- {title} ---\n{content}\n")
    else:
        print("Note not found!")

def update_note():
    title = input("Enter the title of the note to update: ")
    if os.path.exists(f"{title}.txt"):
        with open(f"{title}.txt", "r") as file:
            print("Current content:")
            print(file.read())
        new_content = input("Enter the new content for the note: ")
        with open(f"{title}.txt", "w") as file:
            file.write(new_content)
        print(f"Note '{title}' updated successfully!")
    else:
        print("Note not found!")

def delete_note():
    title = input("Enter the title of the note to delete: ")
    if os.path.exists(f"{title}.txt"):
        os.remove(f"{title}.txt")
        print(f"Note '{title}' deleted successfully!")
    else:
        print("Note not found!")

def list_notes():
    notes = [f for f in os.listdir() if f.endswith('.txt')]
    if notes:
        print("\nAvailable notes:")
        for note in notes:
            print(f"- {note[:-4]}")
    else:
        print("No notes available.")

def main():
    while True:
        print("\n--- Notepad Application ---")
        print("1. Create a new note")
        print("2. Read a note")
        print("3. Update a note")
        print("4. Delete a note")
        print("5. List all notes")
        print("6. Exit")
        choice = input("Choose an option (1-6): ")

        if choice == "1":
            create_note()
        elif choice == "2":
            read_note()
        elif choice == "3":
            update_note()
        elif choice == "4":
            delete_note()
        elif choice == "5":
            list_notes()
        elif choice == "6":
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
