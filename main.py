
from train import *
from classify import *
import sys
import os.path
import csv


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




if __name__ == "__main__":

    training_filename, test_filename = get_filenames()
    # Input the filename
    training_data, training_length = read_in( training_filename ) 

    print "------------------------\n"
    print "------- Training -------\n"
    print "------------------------\n"
    print "\n" 

    attr = [i for i in range(training_length+1)]
    #dtree = create_decision_tree(training_data, attr, training_length, dynamic_bounds)

    forest = create_forest(bagging(training_data, 300, 10), attr, training_length)


    training_data = ''
    test_data, test_length = read_in( test_filename )
    print "------------------------\n"
    print "--   Classification   --\n"
    print "------------------------\n"
    print "\n" 
    #classification_result = classify(dtree, test_data)

    classification_result = classify_forest(forest, test_data)

    # Output the classification
    with open('result.csv', 'wb') as result_classify:
        result_file = csv.writer(result_classify)
        for result in classification_result: 
            print result
            result_file.writerow([str(result)])
     
      
