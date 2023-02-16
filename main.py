import rumps
import string
import webbrowser
import threading

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URi


p1 = "For Soulful Reasons"
p2 = "Funk & Soul"


class Spotify(rumps.App):
    def __init__(self):
        super(Spotify, self).__init__(name = "Spotify", icon="Spotify.png")
        
        # this is the playlist set up
        
        self.trackName = "Nothing"
        self.trackID = ""
        self.scope = "user-library-read user-read-playback-state user-library-modify"
        self.spFetch = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = CLIENT_ID,client_secret = CLIENT_SECRET,redirect_uri = REDIRECT_URi,scope=self.scope))
        self.p1 = "For Soulful Reasons"
        self.p2 = "Funk & Soul"
        
    @rumps.clicked("Add to Your Library")
    def addToLibrary(self,sender):
        response = self.spFetch.current_playback()
        item = response['item']
        trackID = item['id']
        self.spFetch.current_user_saved_tracks_add([trackID])
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
            webbrowser.open_new_tab(auth_url)
    
    @rumps.timer(30)
    def updatePlayback (self, sender):
        thread = threading.Thread(target = self.getTrack)
        thread.start()
        
    def getTrack(self):
        # Get response from API
        response = self.spFetch.current_playback()
        item = response['item']
        self.trackName = item['name']
        self.title = self.trackName
    
    def login_serial():
        print ("logging")
        return
    
    def getP2(self,sender):
        playlists = self.spFetch.current_user_playlists()
        for i in range(len(playlists["items"])):
            print (playlists["items"][i]["name"])
        return

# this idiom means that when importing this file, this won't be ran!
if __name__ == '__main__':
    Spotify().run()
