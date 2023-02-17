import rumps
from webbrowser import open_new_tab
from threading import Thread

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth


CLIENT_ID = "5392917b5bd1465aa781c5b5536f4fde"
CLIENT_SECRET = "43cae063d9e94a05b087648987a3a59f"


REDIRECT_URi = "http://127.0.0.1:5000/"

p1 = "Les Deux Alps"
p2 = "Funk & Soul"


class Spotify(rumps.App):
    def __init__(self):
        super(Spotify, self).__init__(name = "Rumpify")
        
        # this is the playlist set up
        
        self.trackName = "Nothing"
        self.trackID = ""
        self.scope = "user-library-read user-read-playback-state user-library-modify playlist-modify-private playlist-modify-public"
        self.spFetch = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = CLIENT_ID,client_secret = CLIENT_SECRET,redirect_uri = REDIRECT_URi,scope=self.scope))
        self.userPlaylists = self.spFetch.current_user_playlists()
        for i in range (len(self.userPlaylists)):
            if p1 == self.userPlaylists["items"][i]["name"]:
                self.p1ID = self.userPlaylists["items"][i]["id"]
        self.p2 = "Funk & Soul"
        self.user = self.spFetch.me()
        self.userID = self.user["id"]
        
    @rumps.clicked("Add to Your Library")
    def addToLibrary(self,sender):
        response = self.spFetch.current_playback()
        item = response['item']
        trackID = item['id']
        self.spFetch.current_user_saved_tracks_add([trackID])
        return
    
    @rumps.clicked("Add to " + p1)
    def addToP1(self,sender):
        response = self.spFetch.current_playback()
        item = response['item']
        trackID = item['id']
        self.spFetch.playlist_add_items(self.p1ID, [trackID])
        return
    
    @rumps.clicked("Login")
    def addto(self, sender):
        if sender.title!="Login":
            self.title = f" Adding {sender.title}"
            self.track = sender.title
        else:
            # login proceedure
            auth_manager = SpotifyOAuth(client_id = CLIENT_ID,
                            client_secret = CLIENT_SECRET,
                            redirect_uri = REDIRECT_URi,
                            scope = self.scope,)
            auth_url = auth_manager.get_authorize_url()
            open_new_tab(auth_url)
    

    @rumps.timer(30)
    def updatePlayback (self, sender):
        thread = Thread(target = self.getTrack)
        thread.start()
    
    def getTrack(self):
        # Get response from API
        response = self.spFetch.current_playback()
        item = response['item']
        self.trackName = item['name']
        self.title = "🔈" + self.trackName


# this idiom means that when importing this file, this won't be ran!
if __name__ == '__main__':
    
    Spotify().run()
