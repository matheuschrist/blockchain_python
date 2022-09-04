import json
from urllib import response
from criptomoeda import Blockchain
from flask import Flask,jsonify,request
from uuid import uuid4




app=Flask(__name__)
node_address=str(uuid4()).replace('-','')
blockchain=Blockchain()



@app.route('/mine_block',methods=['GET'])
def mine_block():
    previous_block=blockchain.get_previous_block()
    previous_proof=previous_block['proof']
    proof=blockchain.proof_of_work(previous_proof)
    previous_hash=blockchain.hash(previous_block)
    blockchain.add_transaction(sender=node_address,
                               receiver='Carol',
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
    if not all (key in json for key in transactions_keys):
        return "Dados inconsistentes entre as partes",400
    index=blockchain.add_transaction(json['sender'],
                                    json['receiver'],
                                    json['amount'])
    response={'menssage':f'Nova Trasação adicionada ao registro {index}'}
    return jsonify(response),201


@app.route('/connect_node',methods=['POST'])
def connect_node():
    json=request.get_json()
    nodes=json.get('nodes')
    if nodes is None:
        return "Vazio",400
    for node in nodes:
        blockchain.add_nodes(node)
    response={'message':'Conexão realizada com sucesso entre os seguimtes nós :','total_nodes':list(blockchain.nodes)}
    return jsonify(response),201
     
@app.route('/replace_chain',methods=['GET'])
def replace_chain():
    is_chain_replaced=blockchain.replace_chain()
    if is_chain_replaced:
        response={'message':'Nós atualizados com sucesso',
                    'new_chain':blockchain.chain}
    else:
        response={'message':'Não é necessário atualizar os nós da rede',
                    'new_chain':blockchain.chain}

    return jsonify(response),201

app.run(host='0.0.0.0',port=5001)
