class CurrentMusic:
    def __init__(self, title: str = "", artist: str = ""):
        self.title = title
        self.artist = artist

    def getArtist(self) -> str:
        return self.artist

    def setArtist(self, artist: str):
        self.artist = artist

    def getTitle(self) -> str:
        return self.title

    def setTitle(self, title: str):
        self.title = title

    def __str__(self):
        return f"CurrentMusic(title={self.title}, artist={self.artist})"
