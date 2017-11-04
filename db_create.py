from app import db
from models import nsw_birth_rates

#create the database and the db tables
db.create_all()

#create the database and the db tables
db.session.add(nsw_birth_rates("2014","Albion Park NSW 2527","Albion Park","NSW","2527","193","1"))
db.session.add(nsw_birth_rates("2011","Annandale NSW 2038","Annandale","NSW","2038","187","2"))
db.session.add(nsw_birth_rates("2016","Armidale NSW 2350","Armidale","NSW","2350","266","3"))
db.session.add(nsw_birth_rates("2001","Arncliffe NSW 2205","Arncliffe","NSW","2205","181","4"))
db.session.add(nsw_birth_rates("2006","Artarmon NSW 2064","Artarmon","NSW","2064","181","5"))
db.session.add(nsw_birth_rates("2016","Ashfield NSW 2131","Ashfield","NSW","2131","325","6"))
db.session.add(nsw_birth_rates("2016","Auburn NSW 2144","Auburn","NSW","2144","751","7"))

#commit the changes
db.session.commit()