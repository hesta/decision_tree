'''
@Author: Songtao Hei, Yiming Wang, Yujun Liu
Classify function.
Use test data to classify.
'''

from train import *

def get_classification(record, tree):
    """
    This function recursively traverses the decision tree and returns a
    classification for the given record.
    """
    # If the current node is a boolean type, then we've reached a leaf node and
    # we can return it as our answer
    if type(tree) == type(True):
       return tree
    
    # Traverse the tree further until a leaf node is found.
    else:
        attr = tree.keys()[0]
        if record[attr[0]] <= attr[1]:
           temp = tree[attr]['left']
           return get_classification(record, temp)
        else:
           temp = tree[attr]['right']
           return get_classification(record, temp)
 
def classify(tree, data):
    '''
    Returns a list of classifications for each of the records in the data
    list as determined by the given decision tree.
    '''
    classification = []
    
    for record in data:
        classification.append(get_classification(record, tree))

    return classification
