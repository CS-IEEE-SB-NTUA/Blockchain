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