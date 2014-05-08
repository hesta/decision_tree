import math
import copy
import random


def majority_value(data, target_attr):
    """
    Creates a list of all values in the target attribute for each record
    in the data list object, and returns the value that appears in this list
    the most frequently.
    """
    return most_frequent([record[target_attr] for record in data])

def most_frequent(lst):
    """
    Returns the item that appears most frequently in the given list.
    """
    lst = lst[:]
    highest_freq = 0
    most_freq = None

    for val in unique(lst):
        if lst.count(val) > highest_freq:
            most_freq = val
            highest_freq = lst.count(val)
            
    return most_freq

def unique(lst):
    """
    Returns a list made up of the unique values found in lst.  i.e., it
    removes the redundant values in lst.
    """
    unique_lst = []

    # Cycle through the list and add each value to the unique list only once.
    for item in lst:
        if unique_lst.count(item) <= 0:
            unique_lst.append(item)
            
    # Return the list with all redundant values removed.
    return unique_lst

def eliminate_redundance(data, attributes, target_attr):
    """
    eliminate the attributes with only one value
    """
    
    temp_attributes = []
    # Return if there is only one column in the data
    if len(data) == 1:
       return (data, attributes)

    # Get the attributes list which is deleted later
    for attr in attributes:
        if attr != target_attr:
           vals = [record[attr] for record in data]
           if vals.count(vals[0]) == len(vals):
              temp_attributes.append(attr)
    
    # Delete attributes now
    for x in temp_attributes:
        attributes.remove(x)
        for record in data:
            del record[x]
        
    return (data, attributes)  
             
def choose_attribute(data, attributes, target_attr, fitness):
    """
    Cycles through all the attributes and returns the attribute with the
    highest information gain (or lowest entropy).
    """
    best_attr = None
    best = fitness(data, attributes[0], target_attr)  


    for attr in attributes:
        if attr!= target_attr:
           best_temp = fitness(data, attr, target_attr)
           if best_temp[1] <= best[1]:
              best = best_temp
              best_attr = attr
   
    print (best_attr, best)            
    return (best_attr, best[0])

def get_examples(data, attr_tuple):
    """
    Returns a list of all the records in <data> with the value of <attr>
    matching the given value.
    """
    lst1 = []
    lst2 = []     
   
    for record in data:
        if record[attr_tuple[0]] <= attr_tuple[1]:
           lst1.append(record)
        else:
           lst2.append(record)
    
    return (lst1, lst2)                  
       

def entropy(data, target_attr):
    """
    Calculates the entropy of the given data set for the target attribute.
    """
    val_freq = {}
    data_entropy = 0.0

    # Calculate the frequency of each of the values in the target attr
    for record in data:
        if (val_freq.has_key(record[target_attr])):
            val_freq[record[target_attr]] += 1.0
        else:
            val_freq[record[target_attr]] = 1.0

    # Calculate the entropy of the data for the target attribute
    for freq in val_freq.values():
        data_entropy += (-freq/len(data)) * math.log(freq/len(data), 2) 
        
    return data_entropy
    

def lst_entropy(lst):
    """
    Calulating entropy given only a list
    """
    
    val_freq = {}
    data_entropy = 0.0
    
    for element in lst:
        if (val_freq.has_key(element)):
            val_freq[element] += 1.0
        else:
            val_freq[element] = 1.0 
    
    for freq in val_freq.values():
        data_entropy += (-freq/len(lst)) * math.log(freq/len(lst), 2) 
        
    return data_entropy
    
            
def dynamic_bounds(data, attr, target_attr):
    """
    Use dynamic bounds to calculate the entropy for each bound in the same
    column.
    """
    # Caculating dynamic bounds to decrease the branches of the trees
    
    temp_data = []
    temp_entropy = {}
    
    # Get the subset of the data corresponding to the given attribute
    
    data_subset = [record[attr] for record in data]

    for val in unique(data_subset):
        for record in data_subset:
            if record <= val:
               temp_data.append(-1)
            else:
               temp_data.append(1)
        t = lst_entropy(temp_data)
        if t != 0.0: 
           temp_entropy[val] = lst_entropy(temp_data)    
        temp_data = []


    best = max(temp_entropy.iteritems(), key=lambda x:x[1])

    return best           


def create_decision_tree(data, attributes, target_attr, fitness_func):
    """
    Returns a new decision tree based on the examples given.
    """
    data_tuple = eliminate_redundance(data, attributes, target_attr)
    data = data_tuple[0]
    attributes = data_tuple[1]  
    vals = [record[target_attr] for record in data]
    
    if not data or (len(attributes) - 1) <= 0:
       default = majority_value(data, target_attr)
       print default
       return default
    
    elif vals.count(vals[0]) == len(vals):
       return vals[0]

    else:
        # Choose the next best attribute to best classify our data
        best = choose_attribute(data, attributes, target_attr, fitness_func)
        tree = {best:{}}
        # Create a new decision tree/sub-node for each of the values in the
        # best attribute field
        subdataset_tuple = get_examples(data, best)
        subattr = [attr for attr in attributes if attr != best[0]]
        subtree1 = create_decision_tree(
                subdataset_tuple[0],
                subattr,
                target_attr,
                fitness_func)
        subtree2 = create_decision_tree(
                subdataset_tuple[1],
                subattr,
                target_attr,
                fitness_func)
           
        tree[best]['left'] = subtree1
        tree[best]['right'] = subtree2

    return tree


def bagging(training_data, num_vertical, num_rows ):

    #list of the rows used to create smaller decision tree
    sub_dtree = []
    # Total number of subtrees
    num_subtrees = ( num_vertical / num_rows ) + 1
    for k in range(0, num_subtrees):
        sub_dtree.append(copy.deepcopy(random.sample(training_data, num_rows)))

    return sub_dtree      



def create_forest(training_data_lst, attributes, target_attr):

    #list of decision tree 
    forest = []
    for i in training_data_lst:
        forest.append(create_decision_tree(i, attributes, target_attr, dynamic_bounds))

    return forest

