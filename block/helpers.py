# A set of helper functions for calculations etc
import hashlib


def hashPairs(id1, id2):
    """
    concats 2 strings and hashes them
    """
    pairs = id1 + id2
    return hashlib.sha256(pairs.encode('utf-8')).hexdigest()

def findMerkleRoot(tnxList):
    """
    Generating the merkle root for a list of transactions
    :param tnxList: the list of transactions
    :return: merkle root (a hash)
    """
    if len(tnxList) == 1:
        return tnxList[0]

    tnxList.sort() # sort transaction list so that the lesser of the pairs will be concat first
    newList = []
    for i in range(0, len(tnxList) - 1, 2):
        newList.append(hashPairs(tnxList[i], tnxList[i+1]))

    # check if there is an odd number, if so hash it with itself
    if len(tnxList) % 2 != 0:
        newList.append(hashPairs(tnxList[-1], tnxList[-1]))

    return findMerkleRoot(newList)

def findMerklePath(tnxList, transactionId, path=[]):
    """
    function to be used by a full-node to provide a path in the merkle tree of a transactionId
    :param tnxList: the list of transactions
    :param transactionId: the transaction id for the transaction being verified
    :param path: set to empty list by default, only to be used during recursion
    :return: a list of hashes
    """

    if len(tnxList) == 1:
        return path

    tnxList.sort() # sort transaction list so that the lesser of the pairs will be concat first
    newList = []
    for i in range(0, len(tnxList) - 1, 2):
        if tnxList[i] == transactionId:
            path.append(tnxList[i+1])
            transactionId = hashPairs(tnxList[i], tnxList[i+1])

        if tnxList[i+1] == transactionId:
            path.append(tnxList[i])
            transactionId = hashPairs(tnxList[i], tnxList[i+1])

        newList.append(hashPairs(tnxList[i], tnxList[i+1]))

    if len(tnxList) % 2 != 0:
        if transactionId == tnxList[-1]:
            path.append(tnxList[-1])
            transactionId = hashPairs(tnxList[-1], tnxList[-1])
        newList.append(hashPairs(tnxList[-1], tnxList[-1]))

    return findMerklePath(newList, transactionId, path)



def findTransaction(merklePath, merkleRoot, transactionId):
    """
    determine whether a transaction is in a block
    :param merklePath: list of hashes that is a path in the merkle tree that leads to a specific transaction
    :param transactionId: the transaction id of trhe transactions being verified
    :return: boolean value on whether the transaction was found
    """


    tnxHash = transactionId
    if len(merklePath) != 0: # NOTE: this is only true if transaction id are hashed the same with merkle roots
        for i in range(0, len(merklePath)):
            # since merkleRoot hashes smallest to largest, we respect that order here
            if merklePath[i] < tnxHash:
                tnxHash = hashPairs(merklePath[i], tnxHash)
            else:
                tnxHash = hashPairs(tnxHash, merklePath[i])

    if tnxHash == merkleRoot:
        return True
    else:
        return False
