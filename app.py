#!flask/bin/python
from flask import Flask, render_template, jsonify, abort, make_response
from flask import url_for, request
from flask.ext.sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/1kg-phase3'
db = SQLAlchemy(app)

snps = [
    {
        'id': 1,
	'chr': u'1',
	'pos': 57183,
        'rsid': u'rs368339209',
        'ref': u'A', 
        'alt': u'G',
	'EAS_AF' :0,
	'AMR_AF':0,
	'AFR_AF':0.0008,
	'EUR_AF':0,
	'SAS_AF':0,
	'AA': u'.'
    },
    {
        'id': 2,
	'chr': u'1',
	'pos': 57100,
        'rsid': u'rs368339209',
        'ref': u'T',
        'alt': u'C',
        'EAS_AF' :0,
        'AMR_AF':0.45,
        'AFR_AF':0.08,
        'EUR_AF':0.44,
        'SAS_AF':0.1,
        'AA': u'C'
    },
]

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

snp1 = SNP("1", 57100, 'rs368339209', 'T', 'C', 'C', 0, 0.45, 0.08, 0.44, 0.11)
snp2 = SNP("1", 575453, 'rs368345439', 'A', 'C', 'a', 0.01, 0, 0, 0.04, 0)

db.session.add(snp1)
#db.session.add(snp2)
#db.session.commit()

def make_public_snp(snp):
    new_snp = {}
    for field in snp:
        if field == 'id':
            new_snp['uri'] = url_for('get_snp', chromosome = snp['chr'], position = snp['pos'], _external=True)
        else:
            new_snp[field] = snp[field]
    return new_snp


@app.route('/snps/api/v1.0/snps', methods=['GET'])
def get_tasks():
	return jsonify({'snps': [make_public_snp(snp) for snp in snps]})

@app.route('/snps/api/v1.0/snps/<chromosome>/<int:position>', methods=['GET'])
def get_snp(snp_id):
  
    #snp = [snp for snp in snps if snp['chr'] == chromosome and snp['pos'] ==position]
    if len(snp) == 0:
        abort(404)
    return jsonify({'snp': snp[0]})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)


