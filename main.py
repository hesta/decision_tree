
from __future__ import with_statement
from train import *
from classify import *
import sys
import os.path
import csv
import random

def get_filenames():
    """
    Get the filename of training data and classification data
    """
    # Ask user to input the training data filename and classification data file
    # if there is no filename at the biginning
    if len(sys.argv) < 3:
        training_filename = raw_input("Training Filename: ")
        test_filename = raw_input("Test Filename: ")
    # otherwise, read the filenames from the command line
    else:
        training_filename = sys.argv[1]
        test_filename = sys.argv[2]
    def file_exists(filename):
        if os.path.isfile(filename):
            return True
        else:
            print "Error: The file '%s' does not exist." % filename
            return False
    # Print an error and exit execution if there is no target file
    if ((not file_exists(training_filename)) or
        (not file_exists(test_filename))):
        sys.exit(0)
    # Return the filenames of the training and classification data files
    return training_filename, test_filename

def read_in(filename):

    with open(filename, 'r') as fin:
        row = csv.reader(fin)
        data = []   
        for attr in row:
            dict = {}
            i = 0
            length = len(attr)-1
            for element in attr:
                if i == length:
                    dict[i] = (element[0].upper() == 'T')
                else:
                    if element == '?':
                        dict[i] = 0.0
                    else:  
                        dict[i] = float(element)
                i = i + 1
            data.append(dict)
    
    return data, length

#there is still bug in this function, needs improvement or rewrite 
def bagging( training_data, attributes, target_attr, num_vertical ):
    sub_dtree = []
    # Number of rows in each subtree which is randomly selected
    num_rows = 10
    # Total number of subtrees
    num_subtrees = ( num_vertical / num_rows ) + 1
    num_key = []
    for k in range(0, num_subtrees):
        sub_data = []
        key = 0
        temp_key = 0
        for num in range(0, num_rows+1):
            key = random.randint(0, num_vertical-1)
            if key == temp_key:
               continue
            else:
                temp_key = key
                sub_data.append(training_data[key])
                num_key.append(key)
        print len(attributes)
        t = create_decision_tree(sub_data, attributes, target_attr, dynamic_bounds)
        print len(attributes)
        sub_dtree.append(t)
        print 'we have already build', k+1, 'of', num_subtrees, 'decision tree'
    
    return sub_dtree      


if __name__ == "__main__":

    training_filename, test_filename = get_filenames()
    # Input the filename
    training_data, training_length = read_in( training_filename ) 

    print "------------------------\n"
    print "------- Training -------\n"
    print "------------------------\n"
    print "\n" 
    attr = [i for i in range(training_length+1)]
    dtree = create_decision_tree(training_data, attr, training_length, dynamic_bounds)

    #forest = bagging(training_data, attr, 320, 100)
    
    """
    classification = []
    for testdata in test_data:
        for dtree in forest:
            sub_result = []
            sub_classification = classify(dtree, [testdata])
            # sub_result is to keep the classification result from each decision
            # tree of each data
            sub_result.append(sub_classification)
            num_false = sub_result.count(False)
            num_true = sub_result.count(True)
            if num_true > num_false:
                classification.append(True)
            else:
                classification.append(False)
    """
    training_data = ''
    test_data, test_length = read_in( test_filename )
    print "------------------------\n"
    print "--   Classification   --\n"
    print "------------------------\n"
    print "\n" 
    classification_result = classify(dtree, test_data)

    # Output the classification
    with open('result.csv', 'wb') as result_classify:
        result_file = csv.writer(result_classify)
        num_result = 0
        for result in classification_result: 
            print result
            num_result = num_result + 1
            if str(result) == 'True':
                result_file.writerow([num_result])
     
      
