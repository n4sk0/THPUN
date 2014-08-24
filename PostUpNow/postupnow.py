import os
import urllib
from model import Business
from model import BusinessStatus
import csv

from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

import jinja2
import webapp2

import logging
import json


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

        dbmarkers = Business.query().fetch()
        markers = []
        for marker in dbmarkers:
            markers.append({'name':marker.name,
                         'address':marker.address,
                         'city':marker.city,
                         'zipCode':marker.zipCode,
                         'statuses':marker.statuses,
                         'comment':marker.comment
            })

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'authenticated': authenticated,
            'markers': json.dumps(markers),
        }
        logging.getLogger().setLevel(logging.DEBUG)
        logging.info(markers)
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


class Contact(webapp2.RequestHandler):

    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('contact.html')
        self.response.write(template.render(template_values))


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads('file')
        blob_info = upload_files[0]
        #blob_reader = blob_info.open()
        #lines = ''
        #for line in blob_reader:
        #    Business b;
        with blob_info.open() as input:
            result = zip((line.split('\t') for line in input))
            for line in result:
                logging.info(len(line))
                b = Business(name= line[0][0], address = line[0][1], city = line[0][2], zipCode = line[0][3], comment = line[0][4])
                b.put()
        #blob_info.close()

        #self.response.write(result)
        #self.redirect('/serve/%s' % blob_info.key())


#We don't really need the server handler, it's here just in case we need it later on.
class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)

class UpdateHandler(webapp2.RequestHandler):
    def get(self):
        name = self.request.get('name')
        address = self.request.get('address')

        status = self.request.get('status')
        dbmarkers = Business.query(Business.address == address, Business.name == name).fetch()
        logging.getLogger().setLevel(logging.DEBUG)
        logging.info(name)
        logging.info(address)
        logging.info(status)
        logging.info(dbmarkers)
        for marker in dbmarkers:
            marker.status = status
            marker.put()
        self.response.write('success')

application = webapp2.WSGIApplication([
    ('/', MainPage),
	('/about', About),
    ('/contact', Contact),
    ('/file_upload', FileUpload),
    ('/upload', UploadHandler),
    ('/serve/([^/]+)?', ServeHandler),
    ('/update', UpdateHandler)
], debug=True)
