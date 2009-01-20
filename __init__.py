"""Moin Uploader (mule)

Uploads batches of files to a moin url.

Notes
=====

Request for nonexistent moin page
---------------------------------
import mechanize as mc
r = mc.urlopen('http://compbio.sytes.net/LeslieLab/ChimericTFs/MatRedResults')
 ...
 HTTPError: HTTP Error 404: NOTFOUND


Request for existing page w/ no credentials
-------------------------------------------
r = mc.urlopen('http://compbio.sytes.net/LeslieLab')
 ...
 HTTPError: HTTP Error 403: Permission Denied


Add `?action=login` to the url to login to page first

"""
# import os
# import mechanize as mc
# url = "http://compbio.sytes.net/SteveLianoglou"
# login = "action=login"
# attach = "action=AttachFile"
# 
# # login first
# br = mc.Browser()
# br.open('?'.join((url, login)))
# # <form .. name="loginform"
# # <input type="text" name="name" size="32">
# # input type="password" name="password" size="32"
# br.select_form(name="loginform")
# br['name'] = 'SteveLianoglou'
# br['password'] = 'malakas'
# br.submit() # r now has the loaded page
# 
# # attach the files
# attach_page = br.open('?'.join((url,attach)))
# 
# # <form action="/LeslieLab" method="POST" enctype="multipart/form-data">
# # select the file upload form
# br.select_form(predicate=lambda x: x.enctype.startswith('multipart'))
# # <input type="file" name="file" size="50">
# fname = '/Users/stavros/Desktop/Picture1.png'
# br.form.add_file(open(fname), filename=os.path.basename(fname))
# fresponse = br.submit()

