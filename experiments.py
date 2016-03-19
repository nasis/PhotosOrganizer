import binascii

# Funny thing, a pair of images can look identical and arrive from the same source but has some
# very slight modification in the content
path1 = u'Z:\\Dropbox (Dropbox Team)\\\u05ea\u05de\u05d5\u05e0\u05d5\u05ea \u05d2\u05d9\u05d1\u05d5\u05d9\\\u05e9\u05d9\u05e8\\\u05e9\u05d9\u05e8- \u05dc\u05de\u05d9\u05d9\u05df\\\u05dc\u05de\u05d9\u05d9\u05df \u05d0\u05d5\u05dc\u05d9 \u05db\u05d1\u05e8 \u05e7\u05d9\u05d9\u05dd \u05e9\u05d9\u05e8 \u05e4\u05d5\u05dc\u05d9\u05df\\109NIKON\\DSCN4240.JPG'
path2 = u'Z:\\Dropbox (Dropbox Team)\\\u05ea\u05de\u05d5\u05e0\u05d5\u05ea \u05d2\u05d9\u05d1\u05d5\u05d9\\\u05e9\u05d9\u05e8\\\u05e9\u05d9\u05e8 \u05e4\u05d5\u05dc\u05d9\u05df 1-8.3.2010\\109NIKON\\DSCN4240.JPG'

with open(path1, "rb") as a, open(path2, "rb") as b:
    contenta = a.read()
    contentb = b.read()

with open(r"c:\temp\content.txt", "w") as c:
    print >>c, binascii.hexlify(contenta)
    print >>c, binascii.hexlify(contentb)
