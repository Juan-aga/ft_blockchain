from time import time
import hashlib
import json

class Blockchain:
	def __init__(self):
		self.chain = []
		self.current_transactions = []
		self.create_block(proof=100, previous_hash='0')
		self.difficulty = 0

	def create_block(self, proof, previous_hash):
		block = {
			'index': len(self.chain) + 1,
			'timestamp': time(),
			'transactions': self.current_transactions,
			'proof': proof,
			'previous_hash': previous_hash or self.hash(self.chain[-1]),
		}
		self.current_transactions = []
		self.chain.append(block)
		return block

	def new_transaction(self, sender, recipient, amount):
		self.current_transactions.append({
				'sender': sender,
				'recipient': recipient,
				'amount': amount,
				})
		return self.last_block['index'] + 1

	@staticmethod
	def hash(block):
		block_string = json.dumps(block, sort_keys=True).encode()
		return hashlib.sha256(block_string).hexdigest()

	@property
	def last_block(self):
		return self.chain[-1]

	def proof_of_work(self, last_proof, difficulty):
		proof = 0
		valid = "0" * (difficulty - 1) + "4242"
		while self.valid_proof(last_proof, proof, difficulty, valid) is False:
			proof += 1
		return proof

	@staticmethod
	def valid_proof(last_proof, proof, difficulty, valid):
		guess = f'{last_proof}{proof}'.encode()
		guess_hash = hashlib.sha256(guess).hexdigest()
		test = guess_hash[- len(valid):] == valid
		if test is True:
			print ("valid: ", valid)
			print (guess_hash)
		return test

	@property
	def new_difficulty(self):
		dif = len(self.chain) // 2 + 1
		print("Difficulty: ", dif)
		return int(dif)
