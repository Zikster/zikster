#!/usr/bin/env python

import musicbrainzngs
import sys

ARTIST_SCORE_TRESHOLD = 75

musicbrainzngs.set_useragent(
    "zikster",
    "0.0.1",
    "https://github.com/Zikster/zikster/",
)

def filter_artists(artists):
  return [a for a in artists if int(a['ext:score']) >= ARTIST_SCORE_TRESHOLD]

def print_artist(artist):
  print("{name} ({id})".format(name=artist['name'], id=artist['id']))
  print_artist_releases(artist)
  
def print_artist_releases(artist):
  for release_group in artist["release-group-list"]:
    print("{title} ({type})".format(title=release_group["title"], type=release_group["type"]))

if __name__ == '__main__':
  args = sys.argv[1:]
  if len(args) != 1:
    sys.exit("usage: {} ARTIST".format(sys.argv[0]))
  artist = args

  # We need to search for the artist first to get the artist's id
  result = musicbrainzngs.search_artists(artist=artist, type='group')
  
  # Here we filter the list to have a matching artist
  artists = filter_artists(result['artist-list'])
  
  # Then, we need to fetch the artist's releases
  artist_list = []
  for a in artists:
    artist_list.append(musicbrainzngs.get_artist_by_id(a['id'], includes=["release-groups"], release_type=["album","ep"]))
    
  for a in artist_list:
    print_artist(a['artist'])
