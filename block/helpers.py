# A set of helper functions for calculations etc
import hashlib

# this could be wrong lol
def doubleHash(myString):
    return hashlib.sha256(hashlib.sha256(myString.encode('utf-8')).hexdigest().encode('utf-8')).hexdigest()

# this could be wrong too lol, but you'd still get a hash tho
def hashPairs(id1, id2):

    x = id1[::-1]
    y = id2[::-1]

    return doubleHash(x + y)[::-1]

def findMerkleRoot(myList):
    # base case: if only 1 item, return that item
    if len(myList) == 1:
        return myList[0]

    newList = []
    for i in range(0, len(myList) - 1, 2):
        newList.append(hashPairs(myList[i], myList[i+1]))

    # check if there is an odd number, if so hash it with itself
    if len(myList) % 2 != 0:
        newList.append(hashPairs(myList[-1], myList[-1]))

    return merkle(newList)
