from app import db

class nsw_addresses(db.Model):

	__tablename__ = "nsw_addresses"
	__table_args__ = {'extend_existing': True} 

	address_detail_pid = db.Column(db.String(20), primary_key=True)
	address            = db.Column(db.String(150))
	locality_name      = db.Column(db.String(100))
	postcode           = db.Column(db.String(4))
	longitude          = db.Column(db.String(20))
	latitude           = db.Column(db.String(20))
	mb_2016_code       = db.Column(db.String(20))

	def __repr__(self):
		return '{} {} {} {} {} {} {}'.format(self.address_detail_pid, \
			                                 self.address, \
			                                 self.locality_name, \
			                                 self.postcode, \
			                                 self.longitude, \
			                                 self.latitude, \
			                                 self.mb_2016_code)