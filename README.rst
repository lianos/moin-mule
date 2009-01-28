MoinUpLoadEr (``mule``) is a utility that makes it easy
to attach files to MoinMoin_ wiki pages in a non-annoying way. ``mule`` provides a simple
command line interface to send a file, or batches of files (all files in a
given directory, for example), to a specified wiki page.

This allows you to avoid the tedium involved in attaching files via MoinMoin's
web form and sending them one by one (you know it's a pain!).


Introduction
============

In order to attach a file to a MoinMoin_ page, you need to:

  1. Have the file on your local computer
  2. Browse to the ``Attachments`` page for the current page you are working on.
  3. Add a file to the attachment form in "the usual" web-way, that is:
  
    i. Click on the ``Browse`` button in the web form
    ii. Navigate to the file you want to upload on your system via the
        file selection dialogue.
    iii. Submit the form

Rinse wash and repeat *for all of the files you want to upload* to the page. Often
times I've found myself wanting to upload a chunk of files all at the same time
and this process gets frustrating rather quickly. This is what gave birth to
`mule`.

Instead of doing the attach/submit process 20 times for each of the png images
in your local ``/local/dir/with/many/files`` folder, you can send them
all to the ``http://example.com/MyWikiPage`` like so::

  $ mule --filter=.*png MyWikiPage /local/dir/with/many/files


The above command will select all of the files inside the
``/local/dir/with/many/files`` folder on your computer with filenames that
match the regular expression defined in ``filter`` and send them to the
``MyWikiPage`` on your "preferred server."

-----

.. NOTE::

  MoinMoin has a "surge protection" feature which prevents users from hitting
  the wiki too many times per second. This is a good thing, since it prevents
  the wiki from abuse, but it can be bad if you're trying to upload a gazillion
  files at once.

  The surge protection setting is MoinMoin-install specific, so you'll have to 
  figure out what your maximum attachment-request per minutes are set to.

  You can find out more about surge protection on MoinMoin's SurgeProtection_
  information page.

-----

That's the basic idea ... easy, right!? You might be wondering how `mule`
knows what server you are trying to send your files to, and what username
to log in to the server as, but that is all explained below in the
[[#Configuration]] section.

If you're interested on how to install and use your own `mule`, read on ...

Installation
============

``mule`` is a Python script that depends on the mechanize_ python module. The following steps should get it installed and running if you're on  Mac or Linux machine (Windows installation should be similarly easy, but I don't know the specifics off hand).

Installing the mule Tool
~~~~~~~~~~~~~~~~~~~~~~~~

  1. You'll need to download ``mule``. Let's assume that the file is saved on your CPU at ``/Somewhere/on/my/cpu/lies/mule.py``.
  
  2. You'll need to enable its execution bit::
  
      $ chmod +x /Somewhere/on/my/cpu/lies/mule.py
  
  3. Add ``mule.py`` to your ``$PATH`` (optionally as ``mule``). Here are some (mutually exclusive) ways you might do that:

    - Make a "mule" ``alias`` for it (this can be added permanently by dropping it into your ``.bashrc`` or ``.bash_profile`` file)::
    
        $ alias mule='/Somewhere/on/my/cpu/lies/mule.py'
    
    - Make a symbolic link to it from a directory that's already in your ``$PATH``. Assuming ``/usr/local/bin`` is in your path, you can::
    
        $ ln -s /Somewhere/on/my/cpu/lies/mule.py /usr/local/bin/mule

    - Just move `mule.py` to somewhere in your ``$PATH``::
    
        $ mv /Somewhere/on/my/cpu/lies/mule.py /usr/local/bin/mule

Installing the mechanize module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See the mechanize_ page to see how to install it.

If you're on a relatively modern system, you probably have easy_install_ installed, which would be the path of least resistance to get ``mechanize``. You can invoke EasyInstall it to install ``mechanize`` like so::

  $ sudo easy_install mechanize

Alternatively, you can download the module itself and install it the old fashioned way using ``distutils`` (```$ python setup.py install ...``)

Configuration
=============

Using a Config File
~~~~~~~~~~~~~~~~~~~

By default, ``mule`` looks for a ``~/.mule`` config file for the username, password,
and server settings (domain or IP address) it should use when sending files. The
config file allows you to specify as many different MoinMoin servers you like
to make it easy to use ``mule`` with different wikis.

If you have more than one server configuration in your ``mule`` config file,
the configuration information for the first site will be chosen, unless you
specify an other site via the command line switches ``-s`` or ``--site``.

This is an example of ``mule`` config file with two different settings::

  [wiki1]
  username=SteveLianoglou
  password=GetYourOwnPassword
  domain=myfirstwiki.com

  [scipy]
  username=SteveLianoglou
  password=GetYourOwn
  domain=scipy.org

-----

.. CAUTION::

  You'll realize that the passwords are stored in plain text, which really
  isn't a great idea. I plan on allowing for the ability to encrypt
  the password in the `mule` config later, but it's not really high on my
  priority list.

  If you don't like that, you can leave the server and username
  configuration as it is, and enter the password via
  the command line.

-----

Using the Command Line
~~~~~~~~~~~~~~~~~~~~~~

``mule`` has several command line switches you can use to tweak how it works.
You can see all of them by passing ``mule`` the ``--help`` switch.

You can override any of the settings in the ``~/.mule`` config file via the command
line. You can go as far as not having a config file at all, and entering all
of the server and login information manually each time.

::

  ## Having a mule config w/ only username and domain information
  $ mule --password=GetYourOwn wiki/page file1.png file2.png file3.png

  ## Sending files to the non-default server
  $ mule --site=scipy wiki/page file1.png file2.png file3.png
  

-----

.. NOTE::

  If your `mule` config file has more than one site in it, and you don't specify 
  which site to use from the command line, it won't always pick the first one 
  listed in the file.
  
  If you just have one site listed, you don't have to pass in the ``--site`` flag, 
  as it will automatically pick it.

-----


Usage Examples
==============

Let's assume that you have a ``~/.mule`` config file as shown in the example above. 
You can send all the PNGs in the current directory to the `MyWiki/SubPage` page like so::

  $ mule --filter=.*png --site=wiki1 MyWiki/SubPage
  

Note that the option passed to the ``--filter`` flag is a regular expression.
It's not your standard unix style pattern matching (``--filter=*png`` would 
**not** have worked).


If you had only one site defined in your ``~/.mule`` config file, you don't need 
to pass any ``--site`` flag::

  $ mule --filter=.*png MyWiki/SubPage

If you don't have any ``~/.mule`` config file, you can pass in the values from the
command line. The command below just sends the ``Picture1.png`` file to the 
`MyWiki/SubPage`` page::

  $ mule -u SteveLianoglou -p GetYourOwnPassword -d myfirstwiki.com MyWiki/SubPage Picture1.png

Even if you have a ``~/.mule`` config file, any command line switch that you pass
in will override what is read from the config file. You can take advantage of that
if you'd like to enjoy the convenience of a config file without having to have it 
store your password.


To Do
=====

 - Deal with attachments already existing on the target web page
 - Encrypt the passwords stored in the ``~/.mule`` config file
 - Deal with sending files to a page that doesn't exist
 - Figure out how to deal with ``NOTE`` and ``CAUTION`` admonitions CSS for github.
 - Restructure this directory


.. _MoinMoin: http://moinmo.in
.. _SurgeProtection: http://moinmo.in/HelpOnConfiguration/SurgeProtection
.. _mechanize: http://wwwsearch.sourceforge.net/mechanize
.. _easy_install: http://peak.telecommunity.com/DevCenter/EasyInstall