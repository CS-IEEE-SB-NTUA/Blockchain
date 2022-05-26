from msilib import datasizemask
from operator import ge
import random
import time
import hashlib
def newHash(msg=""): return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()

genBlockContent = {u'blockNum' : 0, u'prevHash': None, u'txtLen' : 1, u'transText' : None}
genBlockHash = newHash(genBlockContent)
genBlock = {u'hash' : genBlockHash, u'content' : genBlockContent}

chain = [genBlock]
print(chain)

def makeBlock(transText, prevBlock):
    prevHash = prevBlock[u'hash']
    blockNum = prevBlock[u'content'][u'blockNum'] + 1
    blockContent = {u'blockNum' : blockNum, u'prevHash': prevHash, u'txtLen' : len(transText), u'transText' : transText}
    blockHash = newHash(blockContent)
    block = {u'hash' : blockHash, u'content' : blockContent}
    chain.append(block)
    return block

makeBlock("Mana fere xrima", genBlock)
print(chain)

def checkingBlockHash (block) :
# Exception raised if the hash is no match to the block contents
  expectedHash = newHash (block['content'])
  if block['hash']!= expectedHash :
    raise Exception ('Hash does not match contents of block %s '%block['content']['blockNum'])
  return  

def isValidTxn (txn,state) :
# Assumption : Transaction is a dictionary keyed by account names
# Checking sum of the deposits and withdrawals is 0
  if sum(txn.values()) is not 0:
    return False
# Checking over draft of transactions
  for key in txn.keys():
    if key in state.keys() :
      acctBalance = state[key]
    else:
      acctBalance = 0
    if (acctBalance + txn[key]) < 0 :
      return False
    return True

def updateState(txn , state):
# Inputs: transfer amount (txn) and account balance (state)
# Returns: Updated state but no validation of transaction only
# update the state
# If the transaction == valid −> update the state
	state = state.copy () # Creates a working for key in txn :
	if key in state.keys():
		state[key] += txn[key]
	else:
		state[key] = txn[key]
	return state

def checkingBlockValidity(block , parent , state ):
# Checking following conditions :
# Is each transaction a valid update to the system state?
# Is Block hash valid for the block contents?
# Does block number go up by one compared to the parent block number? # Is the parent block 's hash referenced properly?
	prevblockNumber = parent[u'blockContent'][u'blockNum'] prevHash = prevBlock[u'hash']
	blockNumber = block[u'blockContent'][u'blockNum']
# Checking transaction validity ; if an invalid transaction −> error . for txn in block['contents']['txns']:
	if isValidTxn(txn, state):
		state = updateState(txn, state)
	else:
		raise Exception ('Invalid transaction in block %s : %s' % (blockNum, txn))
	checkingBlockHash(block) # Checks hashes −> error i f not accurate
	if blockNumber != (prevNumber + 1) :
		raise Exception('Hash does not match contents of block %s' %_ blockNum)
	if block['blockContent']['prevHash'] != prevHash:
		raise Exception ('Previous hash inaccurate at block %s' % blockNum)
	return state

def updateState(txn , state):
# Inputs: transfer amount (txn) and account balance (state)
# Returns: Updated state but no validation of transaction only_
# update the state
# If the transaction == valid −> update the state
	state = state.copy () # Creates a working for key in txn :
	if key in state.keys():
		state[key] += txn[key]
	else:
		state[key] = txn[key]
	return state

def checkingBlockValidity(block , parent , state ):
# Checking following conditions :
# Is each transaction a valid update to the system state?
# Is Block hash valid for the block contents?
# Does block number go up by one compared to the parent block number? # Is the parent block 's hash referenced properly?
	prevblockNumber = parent[u'blockContent'][u'blockNum'] prevHash = prevBlock[u'hash']
	blockNumber = block[u'blockContent'][u'blockNum']
# Checking transaction validity ; if an invalid transaction −> error . for txn in block['contents']['txns']:
	if isValidTxn(txn, state):
		state = updateState(txn, state)
	else:
		raise Exception ('Invalid transaction in block %s : %s' %(blockNum, txn))
    		checkingBlockHash(block) # Checks hashes −> error i f not accurate
	if blockNumber != (prevNumber + 1) :
    		raise Exception('Hash does not match contents of block %s' %(blockNum)
	if block['blockContent']['prevHash'] != prevHash:
		raise Exception ('Previous hash inaccurate at block %s' %(blockNum)
	return state


makeBlock("Mana fere xrima", genBlock)
print(chain)