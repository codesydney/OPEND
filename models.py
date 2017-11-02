from app import db

class nsw_birth_rates(db.Model):

	__tablename__ = "nsw_birth_rates"
	__table_args__ = {'extend_existing': True} 

	year     = db.Column(db.Integer)
	locality = db.Column(db.String(100))
	suburb   = db.Column(db.String(100))
	state    = db.Column(db.String(100))
	postcode = db.Column(db.Integer)
	count    = db.Column(db.Integer)
	recid    = db.Column(db.Integer, primary_key = True)

	def __init__(self, year, locality, suburb, state, postcode, count, recid):
		self.year = year
		self.locality = locality
		self.suburb = suburb
		self.state = state
		self.postcode = postcode
		self.count = count
		self.recid = recid 

	def __repr__(self):
		return '{} {} {} {} {} {} {}'.format(self.year, self.locality, self.suburb, self.state, self.postcode, self.count, self.recid)