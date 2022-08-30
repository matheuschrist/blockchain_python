from crypt import methods
from platform import node
from urllib import response
from criptomoeda import Blockchain
from flask import Flask,jsonify,request
from uuid import uuid4




app=Flask(__name__)
node_address=str(uuid4()).replace('-','')
blockchain=Blockchain()



@app.route('mine_block',methods=['GET'])
def mine_block():
    previous_block=blockchain.get_previous_block()
    previous_proof=previous_block['proof']
    proof=blockchain.proof_of_work(previous_proof)
    previous_hash=blockchain.hash(previous_block)
    blockchain.add_transaction(sender=node_address,
                               receiver='Matheus',
                               amount=1)
    block=blockchain.create_block(proof,previous_hash)
    response={'message':'Block Minerado com Sucesso',
              'index':block['index'],
              'timestamp':block['timestamp'],
              'proof':block['proof'],
              'previous_hash':block['previous_hash'],
              'transaction':block['transactions']
              }
    return jsonify(response),200

@app.route('/is_valid',methods=['GET'])
def i_valid():
    is_valid=blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response={'message':'Blockchain validada com Sucesso!'}
    else:
        response={'message':'Blockchain invalida!'}
        
    return jsonify(response),200


@app.route('/add_trasaction',methods=['POST'])
def add_trasaction():
    json=request.get_json()
    transactions_keys=['sender','receiver','amount']
