import tkinter
from song_finder import get_song

class App:
    def __init__(self, master):
        self.master = master
        self.master.title = "Spotify Song Finder"
        self.create_gui()

    def create_gui(self):
        """
        Draw the widgets
        """

        # Create song info widgets
        label = tkinter.Label(self.master, text="Song Name:")
        label.grid(row=0, column=0)
        
        self.title_entry = tkinter.Entry(self.master)
        self.title_entry.grid(row=0, column=1)
 
        label2 = tkinter.Label(self.master, text="Artist Name:")
        label2.grid(row=1, column=0)
        
        self.artist_entry = tkinter.Entry(self.master)
        self.artist_entry.grid(row=1, column=1)

        self.search_button = tkinter.Button(self.master, text="search", command=self.search)
        self.search_button.grid(row=2, column=1)

        # Create song display widgets
        tkinter.Label(self.master, text="Found Songs").grid(row=0, column=2)
        self.song_box = tkinter.Listbox(self.master)
        self.song_box.grid(row=1, column=2)

    def search(self):
        print "searching"
        song = get_song(title=self.title_entry.get(), artist=self.artist_entry.get())
        if isinstance(song, dict):
            self.song_box.insert(tkinter.END, "{} - {}".format(song['artists'][0]['name'], song['name']))
        elif isinstance(song, list):
            for s in sorted(song, key=lambda x:x['artists'][0]['name']):
                self.song_box.insert(tkinter.END, "{} - {}".format(s['artists'][0]['name'], s['name']))
        self.fix_box()

    def fix_box(self):
        """Resizes and reorders songs"""
        items = list(set(self.song_box.get(0, tkinter.END)))
        
        self.song_box.delete(0, tkinter.END)
        for song in sorted(items):
            self.song_box.insert(tkinter.END, song)

        self.song_box.config(width=0)
        self.master.winfo_toplevel().wm_geometry("")

if __name__ == '__main__':
    root = tkinter.Tk()
    app = App(root)
    root.mainloop()
