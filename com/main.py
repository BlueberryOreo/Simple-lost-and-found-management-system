import window
import os

if __name__ == "__main__":
    if not os.path.exists("./data"):
        os.mkdir("./data")
    if not os.path.exists("./data/picture"):
        os.mkdir("./data/picture")
    if not os.path.exists("./data/data.dat"):
        open("./data/data.dat", "wt")
    window.Create()
