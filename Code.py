from msilib import datasizemask
from operator import ge
import random
import time
import hashlib

names = ["Adam", "NikosSf", "Thanasis", "Vaggelis", "Mary", "Stella", "NikosG", "Dimitris"]


def newHash(msg=""): 
	return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()


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

for i in range (5):
  makeTrans(5)


def makeTrans(maxValue):  
  members = random.choices(names, k=2)
  payer = members[0]
  receiver = members[1]
  if (payer == receiver):
    return makeTrans(maxValue)
  amountRec = random.randint(1,maxValue)
  amountPay = -1*amountRec
  if(random.randint(1,10) == 5) :
    amountRec += 1
  print(f"Random transaction : {payer} pays {receiver} {-1*amountPay} HuskIEEEs and {receiver} receives {amountRec}")
  return {u'payer':amountPay, u'receiver': amountRec}


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
	prevblockNumber = parent[u'blockContent'][u'blockNum'] 
	prevHash = parent[u'hash']
	blockNumber = block[u'blockContent'][u'blockNum']
# Checking transaction validity ; if an invalid transaction −> error . 
	for txn in block['contents']['txns']:
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


def checkChain(chain):
    # Work through the chain from the genesis block (which gets special treatment), 
    #  checking that all transactions are internally valid,
    #    that the transactions do not cause an overdraft,
    #    and that the blocks are linked by their hashes.
    # This returns the state as a dictionary of accounts and balances,
    #   or returns False if an error was detected

    
    ## Data input processing: Make sure that our chain is a list of dicts
    if type(chain)==str:
        try:
            chain = json.loads(chain)
            assert( type(chain)==list)
        except:  # This is a catch-all, admittedly crude
            return False
    elif type(chain)!=list:
        return False
    
    state = {}
    ## Prime the pump by checking the genesis block
    # We want to check the following conditions:
    # - Each of the transactions are valid updates to the system state
    # - Block hash is valid for the block contents

    for txn in chain[0]['contents']['txns']:
        state = updateState(txn,state)
    checkBlockHash(chain[0])
    parent = chain[0]
    
    ## Checking subsequent blocks: These additionally need to check
    #    - the reference to the parent block's hash
    #    - the validity of the block number
    for block in chain[1:]:
        state = checkBlockValidity(block,parent,state)
        parent = block
        
    return state



