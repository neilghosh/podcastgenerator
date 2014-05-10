import sys
import re
import urllib2
import urllib
import getopt
import httplib
import StringIO
import datetime
import time
from email import utils

maxItems = 2000

nowdt = datetime.datetime.now()
nowtuple = nowdt.timetuple()
nowtimestamp = time.mktime(nowtuple)
now = utils.formatdate(nowtimestamp)

ins = open( "links.txt", "r" )
output = StringIO.StringIO()
output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
output.write('<rss version="2.0">\n')
output.write('<channel>\n')
output.write('<title>Golpocast</title>\n')
output.write('<description>Bangla Stories</description>\n')
output.write('<link>http://neilghosh.com</link>\n')
output.write('<language>en-us</language>\n')
output.write('<copyright>Copyright 2014</copyright>\n')
output.write('<lastBuildDate>'+now+'</lastBuildDate>\n')
output.write('<pubDate>'+now+'</pubDate>\n')
output.write('<docs>http://neilghosh.com</docs>\n')
output.write('<webMaster>neil.ghosh@gmail.com</webMaster>\n')

items = 0 
temp = ins.read().splitlines()
for url in temp:
    if items > maxItems:
        break
    print "Reading " + url  
    request = urllib2.Request(url)
    request.get_method = lambda : 'HEAD'
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError, err:
        print "Unable to fetch "+url
        continue
    modifiedDate = response.info().getheader('Last-Modified').strip()
    output.write('<item>\n')
    output.write('<title>'+url.split('/')[-1].split('.')[0]+'</title>\n')
    output.write('<link>'+url+'</link>\n')
    output.write('<guid>'+url+'</guid>\n')
    output.write('<description>'+url.split('/')[-2]+'</description>\n')
    output.write('<enclosure url="'+url+'" length="'+response.info().getheader('Content-Length').strip()+'" type="audio/mpeg"/>\n')
    output.write('<category>'+url.split('/')[-2]+'</category>\n')
    output.write('<pubDate>'+modifiedDate+'</pubDate>\n')
    output.write('</item>\n')
    items = items +1

ins.close()
output.write('</channel>\n')
output.write('</rss>\n')

print output.getvalue()
f = open('feed.rss', 'w')
f.write(output.getvalue()+"\n")
f.close
output.close();
