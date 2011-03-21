import urllib2
import threading
import time

def url(year, month, day, hour):
	return "http://kexp.org/playlist/playlist.aspx?t=1&year=%d&month=%d&day=%d&hour=%d" % (year, month, day, hour)

def page(year, month, day, hour):
    name = "%d_%d_%d_%d" % (year, month, day, hour)
    return open(name + ".txt", "w")

def scrape_page(year, month, day, hour):
	f = page(year, month, day, hour)
	u = url(year, month, day, hour)
	html = urllib2.urlopen(u)
	f.write(html.read())
	f.close()

def scrape(year, month, day):
	for hour in range(0, 24):
		first = True
		while(threading.active_count() > 24):
			if first:
				#print "waiting before", year, month, day, hour
				first = False
		threading.Thread(target=scrape_page, args=(year, month, day, hour)).start()

def days_in_month(month):
	if month == 2:
		return 28
	elif month in [4,6,9,11]:
		return 30
	else:
		return 31

for year in range(2002,2011):
	for month in range(1, 12 + 1):
		for day in range(1, days_in_month(12) + 1):
			print year, month, day
			scrape(year, month, day)