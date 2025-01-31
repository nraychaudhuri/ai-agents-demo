import requests


def download_db():
    url = "https://storage.googleapis.com/benchmarks-artifacts/chinook/Chinook.db"

    response = requests.get(url)

    if response.status_code == 200:
        # Open a local file in binary write mode
        with open("Chinook.db", "wb") as file:
            # Write the content of the response (the file) to the local file
            file.write(response.content)
        print("File downloaded and saved as Chinook.db")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")


from langchain_community.utilities import SQLDatabase

# db = SQLDatabase.from_uri("sqlite:///Chinook.db")
# print(db.dialect)
# print(db.get_usable_table_names())
# result = db.run("SELECT * FROM Artist LIMIT 10;")

# print(result)


def get_db():
    db = SQLDatabase.from_uri("sqlite:///chinook.db")
    return db
