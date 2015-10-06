#!flask/bin/python
from flask import Flask, render_template, jsonify, abort, make_response
from flask import url_for, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/1kg-phase3'
heroku = Heroku(app)
db = SQLAlchemy(app)

class SNP(db.Model):
	__tablename__ = "snps"
	id = db.Column(db.Integer, primary_key=True)
	chr = db.Column(db.String(100))
	pos = db.Column(db.Integer)
	rsid = db.Column(db.String(100))
	ref = db.Column(db.String(1))
	alt = db.Column(db.String(1))
	AA = db.Column(db.String(1))
	EAS_AF = db.Column(db.Float)
	AMR_AF = db.Column(db.Float)
	AFR_AF = db.Column(db.Float)
	EUR_AF = db.Column(db.Float)
	SAS_AF = db.Column(db.Float)
	def __init__(self, chr, pos, rsid, ref, alt, AA, EAS, AMR, AFR, EUR, SAS):
		self.chr = chr
		self.pos = pos
		self.rsid = rsid
		self.ref = ref
		self.alt = alt
		self.AA = AA
		self.EAS_AF = EAS
		self.AMR_AF = AMR
		self.AFR_AF = AFR
		self.EUR_AF = EUR
		self.SAS_AF = SAS
	@property
	def serialize(self):
		return{
			'id':  self.id,
			'chr': self.chr,
			'pos': self.pos,
			'rsid': self.rsid,
			'ref': self.ref,
			'alt': self.alt,
			'AA': self.AA,
			'EAS_AF': self.EAS_AF,
			'AMR_AF': self.AMR_AF,
			'AFR_AF': self.AFR_AF,
			'EUR_AF': self.EUR_AF,
			'SAS_AF': self.SAS_AF
		}

db.drop_all()
db.create_all()
snp1 = SNP("1", 57100, 'rs368339209', 'T', 'C', 'C', 0, 0.45, 0.08, 0.44, 0.11)
snp2 = SNP("1", 575453, 'rs368345439', 'A', 'C', 'a', 0.01, 0, 0, 0.04, 0)

db.session.add(snp1)
db.session.add(snp2)
db.session.commit()

@app.route('/snps/api/v1.0/snps', methods=['GET'])
def get_snps():
	snpquery = db.session.query(SNP)
	return jsonify(snp_list = [i.serialize for i in snpquery.all()])

@app.route('/snps/api/v1.0/snps/<chromosome>/<int:position>', methods=['GET'])
def get_snp(chromosome, position):
    snpquery = db.session.query(SNP).filter(SNP.chr == chromosome).filter(SNP.pos == position)
    #snp = [snp for snp in snps if snp['chr'] == chromosome and snp['pos'] ==position]
    #if len(snp) == 0:
    #    abort(404)
    return jsonify(snp_list=[i.serialize for i in snpquery.all()])


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)


