from BeautifulSoup import BeautifulSoup as Soup

# <s><i>1</i><t>12AM - 1AM</t><n>Variety Mix</n><nf></nf><d>Cheryl Waters</d><di>283</di></s>

PATH = '''/Users/moonmayoriii/Desktop/kexp/%d/%d_%d_%d_%d.txt'''

# Returns a new radio play object.
def parse_show(page):
	show_info = page.findAll(name="div", attrs={"id" : "show"})[0]
	result = {}
	result["show"] = show_info.find(name="n").text
	result["tagline"] = show_info.find(name="nf").text
	result["dj"] = show_info.find(name="d").text
	result["dj_id"] = show_info.find(name="di").text
	return result

# Returns 
def parse_playlist(page):
	songs =[]
	playlist = page.findAll(name="dl", attrs={"class" : "play"})
	for song in playlist:
		parsed_song = {}
		parsed_song["time"] = song.find(name="dd", attrs={"class" : "time"}).text
		parsed_song["artist"] = song.find(name="dd", attrs={"class" : "artist"}).text
		parsed_song["title"] = song.find(name="dd", attrs={"class" : "songtitle"}).text
		parsed_song["album"] = song.find(name="dd", attrs={"class" : "album"}).text
		parsed_song["release_year"] = song.find(name="dd", attrs={"class" : "releaseyear"}).text
		parsed_song["label"] = song.find(name="dd", attrs={"class" : "label"}).text
		parsed_song["comment"] = song.find(name="dd", attrs={"class" : "djcomments"}).text
		songs.append(parsed_song)
	return songs

for hour in range(0, 24):
	filename = PATH % (2002, 2002, 1, 1, hour)
	contents = open(filename).read()
	page = Soup(contents)

	radio_play = parse_show(page)
	songs = parse_playlist(page)

	print radio_play
	print songs
	print