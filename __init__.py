"""Moin Uploader (mule)

Uploads batches of files to a moin url.

Notes
=====

Request for nonexistent moin page
---------------------------------
import mechanize as mc
r = mc.urlopen('http://example.com/wiki/NonExistingPage')
 ...
 HTTPError: HTTP Error 404: NOTFOUND


Request for existing page w/ no credentials
-------------------------------------------
r = mc.urlopen('http://example.com/wiki/RealPageNoLogin')
 ...
 HTTPError: HTTP Error 403: Permission Denied


Add `?action=login` to the url to login to page first

"""