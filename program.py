import sqlite3
from subprocess import run


def encodeBase62(num, decode=False):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    if decode:
        if isinstance(num, bytes):
            num = num.decode("ascii")
        output = 0
        for ch in num:
            output = output * 62 + alphabet.index(ch)
        return output
    if num == 0:
        return alphabet[0]
    output = ""
    while num > 0:
        resto = num % 62
        output = alphabet[resto] + output
        num //= 62
    return output

class LinkShortener:
    def setup(self):
        self.db = sqlite3.connect("links.db")
        self.curs = self.db.cursor()
        self.curs.execute("""
            CREATE TABLE IF NOT EXISTS links (
                id INTEGER PRIMARY KEY,
                url TEXT NOT NULL
            )
        """)
        self.db.commit()
    def createLink(self, link):
        self.curs.execute(
            "INSERT INTO links (url) VALUES (?)",
            (link,)
        )
        self.db.commit()
        shortLink = encodeBase62(self.curs.lastrowid)
        print(f"Your shortened link is: {shortLink}, don't forget it ;)")
    def openLink(self, shortLink):
        dbId = encodeBase62(shortLink, decode=True)
        self.curs.execute("SELECT * FROM links WHERE id = (?)", (dbId,))
        row = self.curs.fetchone()
        if row is not None:
            url = row[1]
            run(f"start {url}", shell=True)
        else:
            print("Link doesn't exist!")
    def deleteLink(self, shortLink):
        dbId = encodeBase62(shortLink, decode=True)
        self.curs.execute("DELETE FROM links WHERE id = (?)", (dbId,))
        self.db.commit()
        if self.curs.rowcount > 0:
            print("Link deleted successfully!")
        else:
            print("Link doesn't exist!")
    def searchLink(self, shortLink):
        dbId = encodeBase62(shortLink, decode=True)
        self.curs.execute("SELECT * FROM links WHERE id = (?)", (dbId,))
        row = self.curs.fetchone()
        if row is not None:
            print(f"This short link opens {row[1]}")
        else:
            print("Link doesn't exist!")

            
def main():
    app = LinkShortener()
    app.setup()
    while True:
        print("\n=== Welcome to the link shortener app! ===")
        print("=== Options:")
        print("=== 1 - Create Link")
        print("=== 2 - Open Link")
        print("=== 3 - Delete link")
        print("=== 4 - Search Link")
        print("=== 0 - Quit App")
        match input("Choose your option: "):
            case "1":
                link_to_shorten = input("Type the link you wish to shorten: ").strip()
                if not link_to_shorten.lower().startswith(("http://", "https://")):
                    print("Please enter a URL starting with http:// or https://.")
                    continue
                app.createLink(link_to_shorten)
            case "2":
                link_to_open = input("Type the shortened link you wish to open: ")
                app.openLink(link_to_open)
            case "3":
                link_to_delete = input("Type the shortened link you wish to delete: ")
                app.deleteLink(link_to_delete)
            case "4":
                link_to_print = input("Type the shortened link you wish to search: ")
                app.searchLink(link_to_print)
            case _:
                print("Invalid option!")
                continue
        
if __name__ == "__main__":
    main()