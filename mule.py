#!/usr/bin/env python
"""
Overview
========

MoinUpLoader (mule) is a utility that makes it easy to attach files to MoinMoin
wiki pages in a non-annoying way.

mule provides a simple command line interface to send a file,or batches of files 
(all files in a given directory, for example), to a specified wiki page. 

Requirements
============

Requirez the mechanize_ Python module, and Python > 2.4


License
=======
Copyright (c) Steve Lianoglou, 2008

This code is released under the `Creative Commons Attribution 3.0 License`_ .


.. _mechanize: http://wwwsearch.sourceforge.net/mechanize
.. _Creative Commons Attribution 3.0 License: http://creativecommons.org/licenses/by/3.0/us/

"""

from __future__ import division

import os, urllib2, re
import mechanize as mc

__author__ = 'Steve Lianoglou'
__docformat__ = 'restructuredtext en'

class Mule(object):
    """Works with a MoinMoin attachment page"""
    actions = {'attach' : 'AttachFile', 'login' : 'login'}
    
    @staticmethod
    def from_config(conf, site=None, page=None, verbose=False):
        """Create and configure a Mule object from a config file.
        
        At a minimum, there must be a domain defined in the given
        site specified in the config file.
        
        """
        from ConfigParser import ConfigParser, NoOptionError
        conf = os.path.expanduser(conf)
        if not os.path.isfile(conf):
            raise IOError("Can't open config file %s:" % conf)
        cp = ConfigParser()
        cp.read(conf)
        if len(cp.sections()) == 0:
            raise ConfigError("Bad config file")
        if site is None:
            site = cp.sections()[0]
            print "[Mule] section not specified, using `%s`" % site
        elif site not in cp.sections():
            raise AttributeError("Specified site (%s) is not listed " \
                                 "in the config file (%s)" % conf)
        # host,username,password,page = None,None,None,None
        try:
            domain = cp.get(site, 'domain')
        except NoOptionError, e:
            raise ConfigError('A host is required (at a minimum) to ' \
                              'instantiate a Mule object')
        opts = {'username' : None, 'password' : None}
        for var in opts:
            if cp.has_option(site, var):
                opts[var] = cp.get(site, var)
        return Mule(domain, page=page, verbose=verbose, **opts)
    
    def __init__(self, host, page=None, username=None, password=None, verbose=False):
        """Initialize the Mule object to work with the given moin `url`"""
        if not host:
            raise AttributeError("Need to define a host")
        self.host = host
        self.page = page
        self.username = username
        self.password = password
        self.browser = mc.Browser()
        self.logged_in = False
        if username is not None and password is not None:
            self.login(verbose=verbose)
    
    def login(self, username=None, password=None, verbose=False):
        if username is not None:
            self.username = username
        if password is not None:
            self.password = password
        if self.username is None or self.password is None:
            raise AttributeError("No username / password")
        
        self.browser.open(self.action_url('login'))
        self.browser.select_form(name="loginform")
        self.browser['name'] = self.username
        self.browser['password'] = self.password
        
        try:
            self.browser.submit()
        except urllib2.HTTPError, e:
            self.logged_in = False
            raise LoginError('Illegal Login: %s' % str(e))
        
        if verbose:
            print "[Mule] Login successful"
        self.logged_in = True
        
    
    def attach(self, filepath, page=None, content_type=None, filename=None,
               sanitize=re.compile('[ /]'), verbose=False):
        """Attaches the file located at `filepath` to the current `page`.
        
        As of Moin 1.7.2, we use the fact that the upload form is the one
        with ``enctype`` attribute equal to "multipart/form-data" to select
        it out of the page (it has no form ``name`` attribute we can select)
        """
        if not self.logged_in:
            raise MuleError("Need to log in before attaching any files")
        filepath = os.path.expanduser(filepath)
        if not os.path.isfile(filepath):
            raise AttributeError("Unable to read file: %s" % filepath)
        if page is not None:
            self.page = page
        if self.page is None:
            raise AttributeError("Unspecified page to attach to")
        if filename is None:
            filename = os.path.basename(filepath)
        
        if sanitize is not None:
            filename = sanitize.sub('', filename)
        
        self.browser.open(self.action_url('attach'))
        self.browser.select_form(predicate=lambda x: x.enctype.startswith('multipart'))
        self.browser.form.add_file(open(filepath), content_type=content_type,
                                   filename=filename)
        if verbose:
            print "[Mule] uploading file '%s' as '%s'" % (filepath, filename)
        response = self.browser.submit()
        return response
    
    def action_url(self, action, page=None, verbose=False):
        if page is None:
            page = self.page
        if page is None:
            print "[Mule] WARNING : no page defined for action"
            page = ''
            # raise MuleError("Can't create action url w/o defined page")
        try:
            action = Mule.actions[action]
        except KeyError, e:
            raise MuleError('Unknown action: %s' % action)
        action = 'http://%s/%s?action=%s' % (self.host, page, action)
        if verbose:
            print "[Mule] Action url: %s" % action
        return action
    

class MuleError(Exception):
    def __init__(self, msg=None):
        if msg is None:
            msg = 'Unspecified Exception'
        Exception.__init__(self, msg)

class LoginError(MuleError):
    def __init__(self, msg=None):
        MuleError.__init__(self, msg)

class ConfigError(MuleError):
    def __init__(self, msg=None):
        MuleError.__init__(self, msg)


###############################################################################
# You can run mule from the command line to send a file, or a directory of files,
# to a moinmoin instance
def _build_parser():
    from optparse import OptionParser
    usage = """usage: %prog [options] PAGE FILE [FILE2 FILE3 ...]
    
    Uploads FILE to the moinmoin page specified in PAGE.
    
    If FILE is a directory, then all the files in the directory will be
    uploaded. You can specify a regex pattern with --filter in order to
    select a subset of the files in the directory.
    
    If there is no ~/.mule config file to parse, you are required to
    specify values for username, password, and domain via the OPTIONS.
    """
    parser = OptionParser(usage=usage)
    parser.add_option('-u', '--username', dest='username',
                      help="Override passwsord set in ~/.mule",
                      default=None)
    parser.add_option('-p', '--password', dest='password',
                      help="Override password set in ~/.mule",
                      default=None)
    parser.add_option('-d', '--domain', dest='domain',
                      help="Overriede the host set in ~/.mule",
                      default=None)
    parser.add_option('-f', '--filter', dest='filter',
                      help="If you are uploading an entire directory, you can " \
                           "specify a regular expression here to only send " \
                           "the files that match the pattern.",
                      default=".*")
    parser.add_option('-c', '--config', dest='config', 
                      help="Destination of the mule config file where defaults " \
                           "for host/username/password/etc. can be found. The " \
                           "default place we look is ~/.mule",
                      default="~/.mule")
    parser.add_option('-s', '--site', '--which-site', dest='site',
                      help="Pick a particular site ([section]) from the config "\
                           "file to use the settings for",
                      default=None)
    parser.add_option("-v", '--verbose', action="store_true", dest="verbose",
                      default=False, help="Crank up the verbosity")
    parser.add_option("-q", '--quiet', action="store_false", dest="verbose",
                      help="Makes mule quiet (default)")
    parser.add_option('-t', '--test', action="store_true", dest='testing', 
                      default=False,
                      help="Sets testing flag to true. This lists the files " \
                           "that will be sent without actually sendint them.")
    return parser

def _setup():
    from ConfigParser import ConfigParser
    parser = _build_parser()
    (options,args) = parser.parse_args()
    if len(args) < 2:
        parser.error("Illegal number of arguments.\nYou have to specify, at " \
                     "least, which wiki page (PAGE) you want to uplaod to " \
                     "and what file (FILE) you are sending.")
    page,files = args[0],args[1:]
    options.config = os.path.expanduser(options.config)
    mule = None
    try:
        mule = Mule.from_config(options.config, site=options.site, 
                                page=page, verbose=options.verbose)
    except IOError, e:
        # no .mule config file
        pass
    except AttributeError, e:
        # specified site is not defined in the config file
        parser.error("You are specificing an undefined site in your %s " \
                     "config file: %s" % (options.config, options.site))
    except ConfigError, e :
        # there is no domain name defined in the given site
        # config section or the config file is bad (no sites
        # defined)
        pass
    
    if mule is None:
        if options.domain is None:
            parser.error("No domain is defined for mule to connect to")
        else:
            mule = Mule(options.domain, page=page)
    print "[Mule] Connection established to %s" % mule.host
    
    if not mule.logged_in:
        if options.username is not None:
            mule.username = options.username
        if options.password is not None:
            mule.password = options.password
        try:
            mule.login()
        except AttributeError, e:
            parser.error("You need to specify a username, password, and domain " \
                         "to send the files to.")
    return mule, files, options

def _run(mule, files, options):
    import re
    pattern = re.compile(options.filter)
    for fname in files:
        if os.path.isfile(fname):
            send = [fname]
        elif os.path.isdir(fname):
            send = [os.path.join(fname,f) for f in os.listdir(fname) \
                    if pattern.match(f) and not f.startswith('.')]
            if len(send) == 0:
                print "No files in %s that match pattern %s" \
                      % (fname, options.filter)
                continue
        else:
            send = False
        
        if send:
            for cargo in send:
                if options.testing:
                    print cargo
                else:
                    mule.attach(cargo, verbose=True)
        else:
            print "Don't know what to do with %s" % fname

if __name__ == '__main__':
    mule, files, options = _setup()
    _run(mule, files, options)