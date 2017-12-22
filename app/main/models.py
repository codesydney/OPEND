from app import db

class nsw_addresses (db.Model):
	year     = db.Column(db.Integer)
	address  = db.Column(db.String(100))
	suburb   = db.Column(db.String(100))
	state    = db.Column(db.String(100))
	postcode = db.Column(db.Integer)
	count    = db.Column(db.Integer)
	recid    = db.Column(db.Integer, primary_key = True)

	def __repr__(self):
		return '{} {} {} {} {} {} {}'.format(self.year, self.address, self.suburb, self.state, self.postcode, self.count, self.recid)