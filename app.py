#!flask/bin/python
from flask import Flask, jsonify, abort, make_response
from flask import url_for, request



app = Flask(__name__)

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
    snp = [snp for snp in snps if snp['chr'] == chromosome and snp['pos'] ==position]
    if len(snp) == 0:
        abort(404)
    return jsonify({'snp': snp[0]})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)


