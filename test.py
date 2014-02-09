import sys
import logging
from musicbrainz2.webservice import Query, ArtistFilter, ArtistIncludes, WebServiceError
import musicbrainz2.model as m

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

if len(sys.argv) < 2:
  print "Usage: test.py 'artist name'"
  sys.exit(1)

# Find artist from string
q = Query()
try:
# Search for all artists matching the given name. Limit the results
# to the 5 best matches. The offset parameter could be used to page
# through the results.
#
  f = ArtistFilter(name=sys.argv[1], limit=5)
  artistResults = q.getArtists(f)
except WebServiceError, e:
  print 'Error:', e
  sys.exit(1)
	
# No error occurred, so display the results of the search. It consists of
# ArtistResult objects, where each contains an artist.
#

# We choose the one that matches above our threshold
found_artist = None
for result in artistResults:
  if result.score > 75:
    found_artist = result.artist
    break

try:
# The result should include all official albums.
#
  inc = ArtistIncludes(releases=(m.Release.TYPE_OFFICIAL, m.Release.TYPE_ALBUM), tags=True, releaseGroups=True)
  artist = q.getArtistById(found_artist.id, inc)
except WebServiceError, e:
  print 'Error:', e
  sys.exit(1)

print "Id         :", artist.id
print "Name       :", artist.name
print "SortName   :", artist.sortName
print "UniqueName :", artist.getUniqueName()
print "Type       :", artist.type
print "BeginDate  :", artist.beginDate
print "EndDate    :", artist.endDate
print "Tags       :", ', '.join([t.value for t in artist.tags])
print

if len(artist.getReleases()) == 0:
  print "No releases found."
else:
  print "Releases:"

for release in artist.getReleases():
  print
  print "Id        :", release.id
  print "Title     :", release.title
  print "ASIN      :", release.asin
  print "Text      :", release.textLanguage, '/', release.textScript
  print "Types     :", release.types

print

if len(artist.getReleaseGroups()) == 0:
  print
  print "No release groups found."
else:
  print
  print "Release groups:"

for rg in artist.getReleaseGroups():
  print
  print "Id        :", rg.id
  print "Title     :", rg.title
  print "Type      :", rg.type

print
