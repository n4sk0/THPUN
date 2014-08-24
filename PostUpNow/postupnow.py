import os
import urllib

from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

import jinja2
import webapp2

import logging
logging.getLogger().setLevel(logging.DEBUG)

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(webapp2.RequestHandler):

    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            authenticated = True
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            authenticated = False

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'authenticated': authenticated,
        }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class About(webapp2.RequestHandler):

    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            authenticated = True
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            authenticated = False

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'authenticated': authenticated,
        }

        template = JINJA_ENVIRONMENT.get_template('about.html')
        self.response.write(template.render(template_values))

class FileUpload(webapp2.RequestHandler):

    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            authenticated = True
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            authenticated = False

        upload_url = blobstore.create_upload_url('/upload')

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'authenticated': authenticated,
            'upload_url': upload_url,
        }

        template = JINJA_ENVIRONMENT.get_template('file_upload.html')
        self.response.write(template.render(template_values))

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads('file')
        blob_info = upload_files[0]
        blob_reader = blob_info.open()
        lines = ''
        for line in blob_reader:
            lines += line
        blob_info.close()
        self.response.write(lines)
        #self.redirect('/serve/%s' % blob_info.key())

#We don't really need the server handler, it's here just in case we need it later on.
class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self, resource):
    resource = str(urllib.unquote(resource))
    blob_info = blobstore.BlobInfo.get(resource)
    self.send_blob(blob_info)


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/about', About),
    ('/file_upload', FileUpload),
    ('/upload', UploadHandler),
    ('/serve/([^/]+)?', ServeHandler)
], debug=True)
