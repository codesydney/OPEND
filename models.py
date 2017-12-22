from app import db

class nsw_addresses(db.Model):

	__tablename__ = "nsw_addresses"
	__table_args__ = {'extend_existing': True} 

	year     = db.Column(db.Integer)
	address  = db.Column(db.String(100))
	suburb   = db.Column(db.String(100))
	state    = db.Column(db.String(100))
	postcode = db.Column(db.Integer)
	count    = db.Column(db.Integer)
	recid    = db.Column(db.Integer, primary_key = True)

	def __init__(self, year, address, suburb, state, postcode, count, recid):
		self.year = year
		self.address = address
		self.suburb = suburb
		self.state = state
		self.postcode = postcode
		self.count = count
		self.recid = recid 

	def __repr__(self):
		return '{} {} {} {} {} {} {}'.format(self.year, self.address, self.suburb, self.state, self.postcode, self.count, self.recid)