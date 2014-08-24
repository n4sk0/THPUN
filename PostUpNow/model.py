from google.appengine.ext import ndb

class BusinessStatus(ndb.Model):
    "Models an individual Status for a Business"
    status = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(indexed=False)

class Business(ndb.Model):
    """Models an individual Business entry"""
<<<<<<< HEAD
    name = ndb.StringProperty(indexed=False)
    latitude = ndb.StringProperty(indexed=False)
    longitude = ndb.StringProperty(indexed=False)
    address = ndb.StringProperty(indexed=False)
    city = ndb.StringProperty(indexed=False)
    zipCode = ndb.StringProperty(indexed=False)
    comment = ndb.StringProperty(indexed=False)
    status = ndb.StringProperty(indexed=False)
    statuses = ndb.StructuredProperty(BusinessStatus, repeated=True)
