import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import re

# Genius API credentials
GENIUS_API_TOKEN = "YOUR_GENIUS_API_TOKEN"

class LyricsExtractorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Lyrics Extractor")

        # Create input fields
        self.song_label = tk.Label(master, text="Song Title:")
        self.song_label.pack()
        self.song_entry = tk.Entry(master, width=40)
        self.song_entry.pack()

        self.artist_label = tk.Label(master, text="Artist:")
        self.artist_label.pack()
        self.artist_entry = tk.Entry(master, width=40)
        self.artist_entry.pack()

        # Create button to extract lyrics
        self.extract_button = tk.Button(master, text="Extract Lyrics", command=self.extract_lyrics)
        self.extract_button.pack()

        # Create text area to display lyrics
        self.lyrics_text = tk.Text(master, width=60, height=20)
        self.lyrics_text.pack()

    def extract_lyrics(self):
        song_title = self.song_entry.get()
        artist = self.artist_entry.get()

        if not song_title or not artist:
            messagebox.showerror("Error", "Please enter song title and artist")
            return

        # Make API request to Genius
        url = f"https://api.genius.com/search?q={song_title} {artist}"
        headers = {"Authorization": f"Bearer {GENIUS_API_TOKEN}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            for hit in data["response"]["hits"]:
                if hit["result"]["primary_artist"]["name"].lower() == artist.lower():
                    song_id = hit["result"]["id"]
                    song_url = hit["result"]["url"]
                    break
            else:
                messagebox.showerror("Error", "Song not found")
                return

            # Get lyrics from song URL
            page = requests.get(song_url)
            soup = BeautifulSoup(page.text, "html.parser")
            lyrics_div = soup.find("div", class_="lyrics")
            if lyrics_div:
                lyrics = lyrics_div.get_text()
            else:
                lyrics = ""
                for tag in soup.find_all("div", class_=re.compile("^Lyrics__Container")):
                    if tag.get_text():
                        lyrics += tag.get_text(separator="\n")

            # Display lyrics in text area
            self.lyrics_text.delete(1.0, tk.END)
            self.lyrics_text.insert(tk.END, lyrics.strip())

        else:
            messagebox.showerror("Error", "Failed to retrieve lyrics")

root = tk.Tk()
my_gui = LyricsExtractorGUI(root)
root.mainloop()
