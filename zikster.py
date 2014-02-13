#!/usr/bin/env python

import musicbrainzngs
import sys, os

from tinytag import TinyTag

ARTIST_SCORE_TRESHOLD = 75

musicbrainzngs.set_useragent(
    "zikster",
    "0.0.1",
    "https://github.com/Zikster/zikster/",
)

class Artist:
  def __init__(self):
    pass

  def filter_artists(self, artists):
    return [a for a in artists if int(a['ext:score']) >= ARTIST_SCORE_TRESHOLD]

  def print_artist(self, artist):
    print("{name} ({id})".format(name=artist['name'], id=artist['id']))
    self.print_artist_releases(artist)
  
  def print_artist_releases(self, artist):
    for release_group in artist["release-group-list"]:
      print("{title} ({type})".format(title=release_group["title"], type=release_group["type"]))
      
  def find_artist_releases(self, artist):
    # We need to search for the artist first to get the artist's id
    result = musicbrainzngs.search_artists(artist=artist, type='group')
    
    # Here we filter the list to have a matching artist
    artists = self.filter_artists(result['artist-list'])
    
    # Then, we need to fetch the artist's releases
    artist_list = []
    for a in artists:
      artist_list.append(musicbrainzngs.get_artist_by_id(a['id'], includes=["release-groups"], release_type=["album","ep"]))
      
    for a in artist_list:
      self.print_artist(a['artist'])

class FileScanner:
  def __init__(self, root_folder):
    self.root_folder = root_folder
    
  def scan(self):
    if(self.root_folder):
      for dirName, subdirList, fileList in os.walk(self.root_folder, topdown=False):
        print('Found directory: %s' % dirName)
        for fname in fileList:
          print('\t%s' % fname)
          info = None
          try:
            info = TinyTag.get(dirName+"/"+fname)
          except LookupError:
            pass
          
          if not info == None:
            print('found tinytag -> artist:%s album:' % info.artist, info.album)

if __name__ == '__main__':
  args = sys.argv[1:]
  if len(args) != 1:
    sys.exit("usage: {} ARTIST".format(sys.argv[0]))
  
  # First, scan the root folder and store each individual artist with their albums  
  scanner = FileScanner('.')
  scanner.scan()
  
  # Then, get each artist releases and find missing releases
  #artist = Artist()
  #artist.find_artist_releases(args)
  
  # For each missing release, show link to buy album
  
