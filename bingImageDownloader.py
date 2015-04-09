import urllib2
import json
import sys

keyBing = '1Mw/nqygNuaVQ7SUVTK7+hUeoMUNFxqZGZvYN5TESng'
credentialBing = 'Basic ' + (':%s' % keyBing).encode('base64')[:]
top = 50
query = '%27' + str(sys.argv[1]) + '%27'
filters = '%27Size%3AMedium%27'

i = 0

# we need 5000 images in groups of 50, so 100 iterations
for x in range(0, 100):
    offset = 0 * x * 50
    url = 'https://api.datamarket.azure.com/Bing/Search/v1/Image?' + 'Query=%s&$top=%d&$skip=%d&$format=json&ImageFilters=%s' % (query, top, offset, filters)

    request = urllib2.Request(url)
    request.add_header('Authorization', credentialBing)
    requestOpener = urllib2.build_opener()
    response = requestOpener.open(request) 

    results = json.load(response)

    for img in results['d']['results']:
        try:
            img_url = img['MediaUrl']
            raw_img = urllib2.urlopen(img_url).read()
            f = open("images/" + str(sys.argv[1]) + "/img" + str(i) + ".jpg", 'wb')
            f.write(raw_img)
            f.close()
            i += 1
        except IOError:
            continue

print "Downloaded " + str(i) + "images from Bing."