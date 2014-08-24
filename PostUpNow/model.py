from google.appengine.ext import ndb

class Business(ndb.Model):
    """Models an individual Business entry"""
    name = ndb.StringProperty(indexed=False)
    address = ndb.StringProperty(indexed=False)
    city = ndb.StringProperty(indexed=False)
    zipCode = ndb.StringProperty(indexed=False)
    statuses = ndb.StructuredProperty(BusinessStatus, repeated=True)

class BusinessStatus(ndb.Model):
    "Models an individual Status for a Business"
    status = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(indexed=False)
