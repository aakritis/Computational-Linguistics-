import os
from subprocess import call
from subprocess import check_output
# import subprocess
import xml.etree.ElementTree as eTree
import math
# converting string to dictionary
# import json
import operator
import collections
from itertools import repeat
from xml.etree.ElementTree import Element
from itertools import chain
from liblinearutil import *

# Question 1
def preprocess_corenlp ( raw_text_directory , corenlp_output ):
        " Function to make system call to coreNLP and create output file with annotations "
	
	listAllFiles = getAllFiles ( raw_text_directory )

	strListofFiles = "\n".join ( listAllFiles )
	
	strDirPath = os.getcwd ()

	raw_text_file = strDirPath + "/" + "file_list.txt"
	
        fileOpen = open ( raw_text_file , "w" )
        fileOpen.write ( strListofFiles )
        fileOpen.close ()

        if not os.path.exists ( corenlp_output ):
                os.makedirs( corenlp_output )

	# adding parse to CALL
        call(["java -cp /home1/c/cis530/hw3/corenlp/stanford-corenlp-2012-07-09/stanford-corenlp-2012-07-09.jar:/home1/c/cis530/hw3/corenlp/stanford-corenlp-2012-07-09/stanford-corenlp-2012-07-06-models.jar:/home1/c/cis530/hw3/corenlp/stanford-corenlp-2012-07-09/xom.jar:/home1/c/cis530/hw3/corenlp/stanford-corenlp-2012-07-09/joda-time.jar -Xmx3g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,parse -filelist " + raw_text_file + " -outputDirectory " + corenlp_output],shell=True)

        return

def getAllFiles ( Directory ):
        listFiles = []
        # to store all files in a list 
        if os.path.isdir( Directory ):
                "If Path Exists"
                # listFiles = []

		###### for testing purpose ######
                # itest = 0
                for dirName, subDir, fileList in os.walk( Directory ):
                        # print('Found directory: %s' % dirName)

                        for fname in fileList:
                                fname = dirName + "/" + fname
				###### for testing purpose ######
                                # itest = itest + 1
                                # if ( itest <= 4 ):
					# listFiles.append ( fname )
				# UNCOMMENT
				listFiles.append ( fname )
        return listFiles


# Question 2 2.1
def extract_top_words ( xml_directory ):
	" Function to return 2000 most common words from the documents in the directory "

	listAllWords = []

	# dictWordCount = collections.Counter () 

	listXMLfiles = getAllFiles ( xml_directory )

	for each_xml_file in listXMLfiles :
		" To access each file in XML directory and store words "
		listFileWords = extract_xml_words ( each_xml_file )
		listAllWords.extend ( listFileWords )

	# print listAllWords

	dictWordCount = collections.Counter ( listAllWords )

	sorted_words = sorted ( dictWordCount.items(), key=operator.itemgetter(1), reverse = True )

        listOrderedWords = []

	# print sorted_words

        for each_tuple in sorted_words :
                var = each_tuple[0]
                listOrderedWords.append(var)
	
	list_2000_words = listOrderedWords [ 0 : 2000 ]	

	# print list_2000_words

	return list_2000_words

def extract_xml_words ( xml_file ) :
	" Function to extract words from given corenlp xml file "

	listAllWords = []	
	parseTree = eTree.parse( xml_file )
	root = parseTree.getroot()
	traverseToken = root.iter('token')
	for each_token in traverseToken :
		" to traverse every token in a given xml file "
		word = each_token[0].text.encode('ascii', 'ignore')
		word = word.lower ()
		# print word
		listAllWords.append ( word )

	return listAllWords


# Question 2 2.2 
def map_unigrams(xml_filename, top_words) :
	" Function to return a vector in a feature space of top_words " 

	output_list = []
	listCurrentWords = []

	# extracting words from given xml_filename
	if os.path.exists ( xml_filename ) :
		listCurrentWords = extract_xml_words ( xml_filename )

	for each_word in top_words :
		" to check if the current word in top_words is in current file "
		if ( each_word in listCurrentWords ):
			output_list.append ( 1 )
		else :
			output_list.append ( 0 )
		
	return output_list

# Question 3 3.1

def cosine_similarity ( X, Y ):
        " Function to return float value of cosine similarity "
        floatCosineSim = 0.0
        numerator_Cosine = 0.0
        denom_X = 0.0
        denom_Y = 0.0
        denom_X_Sqrt = 0.0
        denom_Y_Sqrt = 0.0
        denominator_Cosine = 0.0

        flagX = 0
        flagY = 0

        for listVal in X :
                if ( listVal <> 0 ):
                        flagX = 1
                        break
        if( flagX == 0 ):
                # print " X is a Zero Vector "
                return 0.0

        for listVal in Y :
                if ( listVal <> 0 ):
                        flagY = 1
                        break
        if ( flagY == 0 ):
                # print " Y is a Zero Vector "
                return 0.0

        for i in range ( 0, len(X)):
                # numerator calculation
                numerator_Cosine = numerator_Cosine + ( X[i] * Y[i] )

                # denominator values calculation
                denom_X = denom_X + (X[i] * X[i])
                denom_Y = denom_Y + (Y[i] * Y[i])

        denom_X_Sqrt = math.sqrt( denom_X )
        denom_Y_Sqrt = math.sqrt( denom_Y )
        denominator_Cosine = (denom_X_Sqrt * denom_Y_Sqrt)

        # print "Numerator ", numerator_Cosine
        # print "Denominator ", denominator_Cosine      
        floatCosineSim = float(numerator_Cosine)/ float(denominator_Cosine)
        return floatCosineSim

# Adding default parameter to run extract_similarity for Question 8
def extract_similarity(top_words , default_flag = 0) :
	" Function to return 2D Dictionary for word2vec similarity"
	
	file_vector = ""
	
	if ( default_flag == 0 ):
		# reading vector components from given file 
		file_vector = "/project/cis/nlp/tools/word2vec/vectors.txt"

	else :
		file_vector = os.getcwd() + "/vectors_train.txt"
	
	dictWordVector = {}
	strReadFile = ""
	
	if os.path.exists ( file_vector ) :
		fileOpen = open ( file_vector , "r" )
		strReadFile = fileOpen.read ()
		fileOpen.close ()
		
	# spliting string based on \n
	list_lines = strReadFile.splitlines()

	###### for testing purpose ######
	# list_lines = list_lines [ 0 : 100 ]

	lenLines = len ( list_lines )
	# removing first line from vector file
	for each_line in range ( 1 , lenLines ):
		" to create vectors for each word "
		listTemp = list_lines[each_line].split()
		strkey = listTemp[0]
		listVal = listTemp [1:]
		# converting to list of floats
		listFloat = [float(iVal) for iVal in listVal]
		dictWordVector [ strkey ] = listFloat

	# to get the length of a vector
	lenVec = len ( dictWordVector.values()[0] )

	dictCosineSimilarity = {}
 
	for each_word in top_words :

		dictCosine_val = {}

		if ( each_word in dictWordVector.keys() ) :
			vector_word1 = dictWordVector [ each_word ]  
		# else :
			# vector_word1 = list(repeat(0,lenVec))
		# dictCosine_val = {}

			for other_word in top_words :
				if ( each_word <> other_word ) :
					if ( other_word in dictWordVector.keys() ) :
						vector_word2 = dictWordVector [ other_word ]
					# else :
						# vector_word2 = list(repeat(0,lenVec))
				
						floatCosine = cosine_similarity ( vector_word1 , vector_word2 )
						if ( floatCosine <> 0.0 ) :
							dictCosine_val[ other_word ] = floatCosine
			
			if ( len ( dictCosine_val.keys () ) <> 0 ) :
				dictCosineSimilarity [ each_word ] = dictCosine_val
	
	return dictCosineSimilarity 

# Question 3 3.2
def map_expanded_unigrams( xml_file , top_words , similarity_matrix ):
	" Function to return list of real nos between 0 and 1 for top_words "

	# to extract unigram vector
	list_vector = map_unigrams ( xml_file , top_words ) 

	lenlist = len ( list_vector )
	list_0_vector = []
	list_1_vector = []

	# extract non-zero top words from vector
	for each_index in range ( 0 , lenlist ) :
		if ( list_vector[ each_index ] == 0 ) :
			list_0_vector.append ( top_words [ each_index ] )
		else :
			list_1_vector.append ( top_words [ each_index ] )

	# to get maximum of similarity scores with non-zero top_words
	for each_element in list_0_vector :
	
		# compute if the element exists in similarity_matrix
		if ( each_element in similarity_matrix.keys () ) :
		
			dict_element = similarity_matrix [ each_element ]
			
			# remove unwanted non-zero elements from list_1_vector
			set_unwanted = set ( list_1_vector ) - set ( dict_element.keys() )
			set_wanted = set ( list_1_vector ) - set ( set_unwanted )
		
			# reduce dict_element to only element from wanted list_1_vector
			dict_wanted = { required_key : dict_element [ required_key ] for required_key in set_wanted }

			similarity_value = 0.0

			if ( len ( dict_wanted.keys () ) <> 0 ) :
				sorted_dict = sorted ( dict_wanted.items(), key=operator.itemgetter(1), reverse = True )
				if ( sorted_dict [0][1] < 0.0 ) :
					similarity_value = 0.0
				else :
					similarity_value = sorted_dict[0][1]
			else :
				similarity_value = 0.0
			
			# to get index of each_element in top_words	
			index = top_words.index ( each_element ) 
			list_vector[ index ] = similarity_value

	return list_vector

# Question 4 4.1

def extract_xml_tuples ( xml_file ) :
        " Function to extract tupples from given corenlp xml file "

        list_file_tuples = []
        parseTree = eTree.parse( xml_file )
        root = parseTree.getroot()
	
	# traverse dep tag in basic-dependencies tag
        for each_dep in root.findall('document/sentences/sentence/basic-dependencies/dep') :
			
		# extract value of child tags of dep
		dependent = each_dep.find('dependent').text.lower().encode('ascii', 'ignore')
		governor = each_dep.find('governor').text.lower().encode('ascii', 'ignore')

		# extract value of attribute of dep
		relation = str ( each_dep.get('type').lower().encode('ascii', 'ignore') )

		# creating tuple		
		tup_temp = ( relation , governor , dependent )
		
		# creating list of tuples
		list_file_tuples.append ( tup_temp )

        return list_file_tuples


def extract_top_dependencies(xml_directory) :
	" Function to extract top 2000 dependency relations "

	list_all_tuples = []

	# get absolute paths of file in list
        listXMLfiles = getAllFiles ( xml_directory )

	# get list of all tuples from files
        for each_xml_file in listXMLfiles :
                " To access each file in XML directory and store words "
                listFileTuples = extract_xml_tuples ( each_xml_file )
                list_all_tuples.extend ( listFileTuples )

	# dictionary of count of tuples
	dict_tup_count = collections.Counter ( list_all_tuples )
	
	# sorting dictionary to extract top 2000 tuples
        sorted_tuples = sorted ( dict_tup_count.items(), key=operator.itemgetter(1), reverse = True )

        listOrderedTuples = []

        for each_tuple in sorted_tuples :
                var = each_tuple[0]
                listOrderedTuples.append(var)

        list_2000_tup = listOrderedTuples [ 0 : 2000 ]

        return list_2000_tup

# Question 4 4.2
def map_dependencies ( xml_filename , dependency_list ):
	" Function to return list of 0's and 1's for dependencies in a file"

	list_dependencies_vector = []

	list_current_tuple = []

        # extracting tuples from given xml_filename
        if os.path.exists ( xml_filename ) :
                list_current_tuple = extract_xml_tuples ( xml_filename )	

	for each_tuple in dependency_list :
		" to check if the current tuple in dependency_list is in current file "
		if ( each_tuple in list_current_tuple ):
			list_dependencies_vector.append ( 1 )
                else :
                        list_dependencies_vector.append ( 0 )

	return list_dependencies_vector


# Question 5.1
def extract_parse_rules ( xml_file ):
	" Function to extract rules from the parse genertaed the file "

	list_file_rules = []

        parseTree = eTree.parse( xml_file )
        root = parseTree.getroot()

        # traverse parse tag in file
        for each_parse in root.findall('document/sentences/sentence/parse') :
		str_parser = each_parse.text.encode('ascii', 'ignore')

		# to extract rule from grammer using stack properties
		list_split_parse = str_parser.split ()

		list_stack = []
		
		for each_string in list_split_parse :
			" To form stack and extractt rules "
			
			if ('(' in each_string) :
				" for push operation in stack "

				if  ( len ( list_stack ) == 0 ) :
					" to add ROOT in the list as the first element "
						
					each_string = each_string.replace ( '(' , '' )
					list_stack.append ( each_string )

				else :
					" to add current Non-Terminal as a rule in below string and add a new string "	
					
					each_string = each_string.replace ( '(' , '' )				
	
					len_list = len ( list_stack )
					str_current = list_stack [ len_list - 1 ]
					list_stack [len_list - 1] = str_current + "_" + each_string 		

					list_stack.append ( each_string )

			elif ( ')' in each_string ) :
				" for pop operation in stack "

				count_pop = int ( each_string.count ( ')' ) )

				for pop in range ( 0 , count_pop ) :

					if ( pop == 0 ) :
						list_stack.pop( )

					else :
						" to create list of rules "
						str_rule = list_stack.pop( )

						# commented sorting of rules
						
						# list_rules = str_rule.split ( '_' )					
						# list_sort = list_rules[ 1 : ]
						# list_sort.sort ( )
						
						# str_final_rule = list_rules [ 0 ] + '_' + '_'.join ( list_sort )

						# storing rules popped from stack into list
						
						list_file_rules.append ( str_rule )

		# print list_file_rules	

	return list_file_rules 


def extract_prod_rules(xml_directory) :
	" Function to extract top 2000 rules from parse "

	list_all_rules = []

        # get absolute paths of file in list
        listXMLfiles = getAllFiles ( xml_directory )

        # get lisr of all tuples from files
        for each_xml_file in listXMLfiles :
                " To access each file in XML directory and store words "
                listFileRules = extract_parse_rules ( each_xml_file )
          
		# store sorted list of rules 
	      	list_all_rules.extend ( listFileRules )

        # dictionary of count of tuples
        dict_rule_count = collections.Counter ( list_all_rules )

        # sorting dictionary to extract top 2000 tuples
        sorted_rules = sorted ( dict_rule_count.items(), key=operator.itemgetter(1), reverse = True )

        listOrderedRules = []

        for each_rule in sorted_rules :
                var = each_rule[0]
                listOrderedRules.append(var)

        list_2000_rules = listOrderedRules [ 0 : 2000 ]

        return list_2000_rules


# Question 5 5.2
def map_prod_rules(xml_filename, rules_list) :
        " Function to return list of 0's and 1's for rules in a file"

        list_rule_vector = []

        list_current_rule = []

        # extracting tuples from given xml_filename
        if os.path.exists ( xml_filename ) :
                list_current_rule = extract_parse_rules ( xml_filename )

        for each_rule in rules_list :
                " to check if the current rule in rules_list is in current file "
                if ( each_rule in list_current_rule ):
                        list_rule_vector.append ( 1 )
                else :
                        list_rule_vector.append ( 0 )

        return list_rule_vector

# Question 6 6.2
def process_corpus( xml_dir, top_words, similarity_matrix, top_dependencies, prod_rules, default_parameter = 'train1' ) :
	" Function to write files in format of LIBLINEAR tool kit "

	# extract files in current directory
	list_all_files = getAllFiles ( xml_dir )
	
	
	iCounter = 0

	str_dir_path = os.getcwd ()

        file_name_1 = str_dir_path + "/" + default_parameter + "_1.txt"
        fObj1= open ( file_name_1 , "w" )

        file_name_2 = str_dir_path + "/" + default_parameter + "_2.txt"
        fObj2= open ( file_name_2 , "w" )
      

        file_name_3 = str_dir_path + "/" + default_parameter + "_3.txt"
        fObj3= open ( file_name_3 , "w" )
        

        file_name_4 = str_dir_path + "/" + default_parameter + "_4.txt"
        fObj4 = open ( file_name_4 , "w" )
       

        file_name_5 = str_dir_path + "/" + default_parameter + "_5.txt"
        fObj5 = open ( file_name_5 , "w" )

	for xml_filename in list_all_files :
		iCounter += 1
		print iCounter

		str_file_lexical = ""
        	str_file_expanded = ""
        	str_file_dependency = ""
        	str_file_rules = ""
        	str_file_all = ""

		# extract file name from absolute path 
		list_file_name = xml_filename.split ("/")
		len_file = len ( list_file_name )
		str_file_name = list_file_name [ len_file - 1 ]		
	
		# setting final string
		str_file_lexical = str_file_name
		str_file_expanded = str_file_name
		str_file_dependency = str_file_name
		str_file_rules = str_file_name
		str_file_all = str_file_name
	
		# to extract vector for binary lexical 
		vector_lexical = map_unigrams( xml_filename, top_words )
		vector_expanded = map_expanded_unigrams( xml_filename, top_words, similarity_matrix )
		vector_dependency = map_dependencies ( xml_filename , top_dependencies ) 	
		vector_rules = map_prod_rules ( xml_filename , prod_rules )

		vector_all = list ( chain ( vector_lexical , vector_dependency , vector_rules ) )


		# for extracting non-zero binary lexical values into string to write file
		len_vector_lexical = len ( vector_lexical )
		for each_index in range ( 0 , len_vector_lexical ) :
			if ( vector_lexical [ each_index ]  <> 0 ) :
				str_file_lexical = str_file_lexical + " " + str ( each_index + 1 ) + ":" + str ( vector_lexical [ each_index ] )
		str_file_lexical = str_file_lexical + "\n"

		fObj1.write(str_file_lexical)

		# for extracting non-zero expanded lexical values into string to write file
                len_vector_expanded = len ( vector_expanded )
                for each_index in range ( 0 , len_vector_expanded ) :
                        if ( vector_expanded [ each_index ]  <> 0 ) :
                                str_file_expanded = str_file_expanded + " " + str ( each_index + 1 ) + ":" + str ( vector_expanded [ each_index ] )
                str_file_expanded = str_file_expanded + "\n"


		fObj2.write(str_file_expanded)



		# for extracting non-zero dependency values into string to write file
                len_vector_dependency = len ( vector_dependency )
                for each_index in range ( 0 , len_vector_dependency ) :
                        if ( vector_dependency [ each_index ]  <> 0 ) :
                                str_file_dependency = str_file_dependency + " " + str ( each_index + 1 ) + ":" + str ( vector_dependency [ each_index ] )
                str_file_dependency = str_file_dependency + "\n"

		fObj3.write(str_file_dependency)



		# for extracting non-zero dependency values into string to write file
                len_vector_rules = len ( vector_rules )
                for each_index in range ( 0 , len_vector_rules ) :
                        if ( vector_rules [ each_index ]  <> 0 ) :
                                str_file_rules = str_file_rules + " " + str ( each_index + 1 ) + ":" + str ( vector_rules [ each_index ] )
                str_file_rules = str_file_rules + "\n"


		fObj4.write(str_file_rules)

		# for extracting non-zero dependency values into string to write file
                len_vector_all = len ( vector_all )
                for each_index in range ( 0 , len_vector_all ) :
                        if ( vector_all [ each_index ]  <> 0 ) :
                                str_file_all = str_file_all + " " + str ( each_index + 1 ) + ":" + str ( vector_all [ each_index ] )
                str_file_all = str_file_all + "\n"

		fObj5.write(str_file_all)


	# closing files
	
	fObj1.close()
        fObj2.close()
        fObj3.close()
        fObj4.close()
        fObj5.close()
	
	return 

# run process_corpus for feature 6
def process_corpus_new_feature( xml_dir, top_words, similarity_matrix, default_parameter = 'train' ) :
        " Function to write files in format of LIBLINEAR tool kit "

        # extract files in current directory
        list_all_files = getAllFiles ( xml_dir )

        # str_file_expanded = ""

	str_dir_path = os.getcwd ()

        file_name_6 = str_dir_path + "/" + default_parameter + "_6.txt"
        fObj = open ( file_name_6 , "w" )

	counter = 0

        for xml_filename in list_all_files :

		counter += 1
		print counter
		str_file_expanded = ""
                # extract file name from absolute path 
                list_file_name = xml_filename.split ("/")
                len_file = len ( list_file_name )
                str_file_name = list_file_name [ len_file - 1 ]

                # setting final string
                str_file_expanded = str_file_name
                
		# to extract vector for binary lexical 
                vector_expanded = map_expanded_unigrams( xml_filename, top_words, similarity_matrix )

                # for extracting non-zero expanded lexical values into string to write file
                len_vector_expanded = len ( vector_expanded )
                for each_index in range ( 0 , len_vector_expanded ) :
                        if ( vector_expanded [ each_index ]  <> 0 ) :
                                str_file_expanded = str_file_expanded + " " + str ( each_index + 1 ) + ":" + str ( vector_expanded [ each_index ] )
                str_file_expanded = str_file_expanded + "\n"
		fObj.write ( str_file_expanded )


        fObj.close ( )


        return

# Question 6 6.3
def process_binary_classifier ( list_domain , filename ):
	" Function to create binary classifiers based on domain "

	# read file data
	fObj = open ( filename , "r" )
	str_read_file = fObj.read ( )
 	fObj.close ( )

	list_read_file = str_read_file.splitlines()

	# extract file name 
	list_file_name = filename.split ( "." )
	str_file_name = list_file_name [ 0 ]
	
	for each_domain in list_domain :
		# list_read_file = str_read_file.splitlines()
		str_new_file = ""

		for each_line in list_read_file :
			list_each_line = each_line.split ( ' ' , 1 )
			str_label = ""
			
			if ( each_domain in list_each_line [ 0 ] ):		
				str_label = "1"
			else : 
				str_label = "-1"
			
			str_new_file = str_new_file + str_label + " " + list_each_line [ 1 ] + "\n"


		file_name = str_file_name + "_" + each_domain + ".txt"
		fObj_new = open (  file_name , "w" )
		fObj_new.write ( str_new_file )
		fObj_new.close ( )

	return

# Question 6 6.4

def precision ( actual , predicted , val ):
	" Function to calculate precision "

	num = 0.0
	denom = 0.0
	
	len_predicted = len ( predicted )

	# for numerator
	for index in range ( 0 , len_predicted ) :
		if ( predicted [ index ] == val ) :
			if ( actual [ index ] == val ) :
				num = num + 1.0

	# for denominator 

	denom = float ( predicted.count ( val ) )

	prec = 0.0
	if ( denom <> 0.0 ) :
		prec = float ( num / denom )
	else : 
		prec = 0.0
	
	return prec 

def recall ( actual , predicted , val ) :
	" Function to calculate recall "
	num = 0.0
        denom = 0.0

        len_actual = len ( actual )

        # for numerator
        for index in range ( 0 , len_actual ) :
                if ( actual [ index ] == val ) :
                        if ( predicted [ index ] == val ) :
                                num = num + 1.0

        # for denominator 
        denom = float ( actual.count ( val ) )

	rec = 0.0
	if ( denom <> 0.0 ) :
        	rec = float ( num / denom )
	else :
		rec = 0.0

        return rec

def fscore ( precision , recall ) :
	" Function to calculate fscore "

	num = float ( 2 * precision * recall )
	denom = float ( precision + recall )

	fsc = 0.0

	if ( denom <> 0.0 ):
		fsc = float ( num ) / float ( denom )
	else :
		fsc = 0.0
	
	return fsc

# add default flag to decide results file # for extra credit question 8
def run_classifier ( train_file , test_file , default_flag = 0 ) :
	" Function to return tuple for classifier values "

	y , x = svm_read_problem ( train_file )

	len_y = float ( len ( y ) )
	# count of -1.0
	count_negative = float ( y.count ( -1.0 ) )

	# count of 1.0
	count_positive = float ( y.count ( 1.0 ) )

	positive_per = float ( count_negative / len_y )
	negative_per = float ( count_positive / len_y )

	param = '-s 0 -w1 ' + str( positive_per ) + ' -w-1 ' + str ( negative_per )

	m = train ( y , x , param )	
	y2 , x2 = svm_read_problem ( test_file )
	p_labels , p_acc , p_vals = predict ( y2 , x2 , m , '-b 1' )

	# probabilites of label 1 

	prob_val = []

	if ( m.label[0] == 1 ) :
		for each_element in p_vals :
			prob_val.append ( each_element [0] )
	else :
		for each_element in p_vals :
                        prob_val.append ( each_element [1] )

	
	# Precision / Recall / F-score	
	Pos_P = precision ( y2 , p_labels , 1.0 )
	Pos_R = recall ( y2 , p_labels , 1.0 )
	Pos_F = fscore ( Pos_P , Pos_R )

	Neg_P = precision ( y2 , p_labels , -1.0 )
	Neg_R = recall ( y2 , p_labels , -1.0 )
	Neg_F = fscore ( Neg_P , Neg_R )

	# ret_tuple = ( Pos_P , Pos_R , Pos_F , Neg_P , Neg_R , Neg_F )	

	# ret_tuple_string = ( str ( each_key ) for each_key in ret_tuple )

	list_file_name = test_file.split ( '.' , 1 ) 
	extract_data = list_file_name[0].split ('_')

	ret_tuple = ( Pos_P , Pos_R , Pos_F , Neg_P , Neg_R , Neg_F , p_acc[0] )

	ret_tuple_string = ( str ( each_key ) for each_key in ret_tuple )

	str_write_file = "# " + " ".join ( ret_tuple_string ) + " " + extract_data [2] + ":" + str ( extract_data [1] ) + "\n"

	# File writing for each file 
	if ( default_flag == 0 ):
		fObj = open ( "results.txt" , "a" )
		fObj.write ( str_write_file )
		fObj.close ( )	
	else :
		fObj = open ( "extra_credit_results.txt" , "a" )
                fObj.write ( str_write_file )
                fObj.close ( )



	tup = ( p_labels , ret_tuple , prob_val )
	
	return tup


# Question 7 
# adding default parameter to decide results file # for extra credit Question 8 
def generate_input_prob ( list_domains , list_feature_set , default_flag = 0 ) :
	" Function to return probabilities of 1 in each domain based on accuracy "
	
	dict_probabilites = {}
	list_acc_feature = []

	dict_best_probabilites = {}

	for each_domain in list_domains :
		dict_temp = {}
		for each_feature in list_feature_set :
			train_file = "train_" + str(each_feature) + "_" + each_domain + ".txt"
			test_file = "test_" + str(each_feature) + "_" + each_domain + ".txt"

			tup_values = run_classifier ( train_file , test_file , default_flag ) 
			
			# to store probabilites of 1 
			key = ( each_domain , each_feature )
			dict_probabilites [ key ] = tup_values[2]

			# to store values of accuracy in dict 
			list_p_acc = tup_values [1]
			dict_temp [ each_feature ] = list_p_acc [ len ( list_p_acc ) - 1 ] 
			
		# sorting dict to get max value 
		sorted_dict = sorted ( dict_temp.items(), key=operator.itemgetter(1), reverse = True )
		list_acc_feature.append ( sorted_dict[0][0] )

	# after calculating for entire domain 
	dict_feature_count = collections.Counter ( list_acc_feature )	
	sorted_dict = sorted ( dict_feature_count.items(), key=operator.itemgetter(1), reverse = True )
	best_feature_val = sorted_dict[0][0]
		

	for each_key in dict_probabilites.keys() :
		
		domain = each_key [ 0 ]
		feature = each_key [ 1 ]

		if ( feature == best_feature_val ) :
			dict_best_probabilites [ domain ] = dict_probabilites [ each_key ]
				
	return dict_best_probabilites 

# adding default parameter to decide results file # for extra credit Question 8 
def classify_documents ( health_prob , computers_prob , research_prob , finance_prob , default_flag = 0) :
	" Function to classify documents and report accuracy "
	
	len_compute = len ( health_prob )

	domains = [ "health" , "computers" , "research" , "finance" ]

	list_predicted_domains = []	

	# to generate predicted domains list
	for el_index in range ( 0 , len_compute ) :
		list_vals = [ health_prob [ el_index ] , computers_prob [ el_index ] , research_prob [ el_index ] , finance_prob [ el_index ] ]
		index_max = list_vals.index ( max ( list_vals ) )
		
		list_predicted_domains.append ( domains [ index_max ] )

	# to compare with actual domains list
	fObj = open ( "test_1.txt" , "r" )
	str_read_file = fObj.read ( )
	fObj.close ( )

	list_read_file = str_read_file.splitlines()	

	len_size = len ( list_read_file )

	# numerator for accuracy 
	num = 0.0

	for each_index in range ( 0 , len_size ) :
		file_each_line = list_read_file[ each_index ].split ( ' ' , 1 )
		str_label = ""
		if ( list_predicted_domains [ each_index ] in file_each_line[0].lower() ):
			num = num + 1.0
	
	denom = float ( len_size )

	accuracy = float ( num / denom ) * 100

	strOutput = "Accuracy of predictions : " + str ( accuracy ) + "%" + "\n"

	if ( default_flag == 0 ) :
		fResults = open ( "results.txt" , "a" )
		fResults.write ( strOutput )
		fResults.close ()
	else :
		fResults = open ( "extra_credit_results.txt" , "a" )
                fResults.write ( strOutput )
                fResults.close ()


	return list_predicted_domains


# Question 8 # extra credit 

def load_file_words( filePath ):
        " Function to get list of words in a file"
        listTokens = []
        if os.path.isfile( filePath ):
                # print Exists
                fileObject = open(filePath,"r")
                stringConverter = fileObject.read()
                listTokens = stringConverter.split()
                fileObject.close()
        else:
                print "Not Exists"

        return listTokens;



def create_vector_file ( train_data_directory ) :
	" Function to create training data vector file using word2vec "
	
	list_all_files = getAllFiles ( train_data_directory ) 

	list_all_words = []	

	for each_xml_file in list_all_files :
		" To access each file in XML directory and store words "
                listFileWords = extract_xml_words ( each_xml_file )
                list_all_words.extend ( listFileWords )


	str_write_file = " ".join ( list_all_words )

	# create input file 
	fInput = open ( "words_train.txt" , "w" )
	fInput.write ( str_write_file.lower () )
	fInput.close ()

	# calling word2vec to create vectors_train.txt
	os.system ( "./word2vec -train  words_train.txt -output vectors_train.txt -debug 2 -size 200 -window 5 -sample 1e-4 -negative 5 -hs 0 -binary 0 -cbow 1" )
	
	return


# main function implementation
def main ():
	" Function to implement MAIN for calling of all the functions "

	strDirPath = os.getcwd ()

	# Question 1
	
	# provided xml_data folder for data

	raw_text_directory = "/home1/c/cis530/hw3/test_data"
        corenlp_output = strDirPath + '/' + "test_data"
        
	print "Question 1"
	
	# Question 6 6.2

	corenlp_output_train_data = "/home1/c/cis530/hw3/xml_data"

	corenlp_output_test_data = strDirPath + '/' + "test_data"

	# for train data 
	'''
	# Question 2.1
	# UNCOMMENT
	top_words = extract_top_words ( corenlp_output_train_data ) 
	print "Top_Words Computed"

	# Question 3.1
	similarity_matrix =  extract_similarity ( top_words )
	print "Similarity Matrix Computed"

	# Question 4.1
	# UNCOMMENT
	top_dependencies = extract_top_dependencies( corenlp_output_train_data )
	print "Top Dependencies Computed"	

	# Question 5.1
	# UNCOMMENT
	prod_rules = extract_prod_rules( corenlp_output_train_data )
	print "Prod Rules Computed"	

	# parameters from 2.1 , 3.1 , 4.1 , 5.1
	# UNCOMMENT
	process_corpus ( corenlp_output_train_data, top_words, similarity_matrix, top_dependencies, prod_rules )
	print "Process Corpus Train"
	
	# for test data 

        # parameters from 2.1 , 3.1 , 4.1 , 5.1
	# UNCOMMENT
	# process_corpus ( corenlp_output_test_data, top_words, similarity_matrix, top_dependencies, prod_rules , 'test' ) 

	print " Process Corpus Test "
	print "Question 6 6.2"        
	
	# Question 6 6.3

	str_dir_path = os.getcwd ( )
	list_domains = [ "Computers" , "Health" , "Research" , "Finance" ]

	# UNCOMMENT 
	process_binary_classifier ( list_domains , str_dir_path + "/test_1.txt" )
	print "Test 1 done "
	process_binary_classifier ( list_domains , str_dir_path + "/test_2.txt" )
	print "Test 2 done "
	process_binary_classifier ( list_domains , str_dir_path + "/test_3.txt" )
	print "Test 3 done "
	process_binary_classifier ( list_domains , str_dir_path + "/test_4.txt" )
	print "Test 4 done "
	process_binary_classifier ( list_domains , str_dir_path + "/test_5.txt" )
	print "Test 5 done "
	
	process_binary_classifier ( list_domains , str_dir_path + "/train_1.txt" )
	print "Train 1 done"
	process_binary_classifier ( list_domains , str_dir_path + "/train_2.txt" )
	print "Train 2 done"
	process_binary_classifier ( list_domains , str_dir_path + "/train_3.txt" )
	print "Train 3 done"
	process_binary_classifier ( list_domains , str_dir_path + "/train_4.txt" )
	print "Train 4 done"
	process_binary_classifier ( list_domains , str_dir_path + "/train_5.txt" )
	print "Train 5 done"	

	print "Question 6 6.3"
	'''

	# Question 7

	list_domains = [ "Research" , "Finance" , "Computers" , "Health" ]
	list_feature_set = [ 1 , 2 , 3 , 4 , 5 ]

	'''
	domains_probabilites  = generate_input_prob ( list_domains , list_feature_set )


	computers_prob = []
	health_prob = []
	research_prob = []
	finance_prob = []


	for each_key in domains_probabilites.keys() :
		if ( each_key == "Computers" ) :
			computers_prob = domains_probabilites [ each_key ]
		elif ( each_key == "Health" ) :
			health_prob = domains_probabilites [ each_key ]
		elif ( each_key == "Research" ) :
			research_prob = domains_probabilites [ each_key ]
		else :
			finance_prob = domains_probabilites [ each_key ]

	list_predicted_domains = classify_documents ( health_prob , computers_prob , research_prob , finance_prob )

	print list_predicted_domains

	print "Question 7"
	
	'''

	# Question 8 Extra Credit 

	print "Start of Question 8"
	
	
	# UNCOMMENT 
	# create_vector_file ( corenlp_output_train_data )  # creating vector file 

	# Question 2.1
        # UNCOMMENT
        top_words = extract_top_words ( corenlp_output_train_data ) 
        print "Top_Words Computed"

        # Question 3.1
        ###### for testing purpose - reduced length of top_words ######
        similarity_matrix_new =  extract_similarity ( top_words , 1 )
        print "Similarity Matrix for new vectors Computed"

	process_corpus_new_feature( corenlp_output_train_data, top_words, similarity_matrix_new )
	print "Train 6 File Created" 
	process_corpus_new_feature( corenlp_output_test_data, top_words, similarity_matrix_new, 'test' )  
	print "Test 6 File Created"

	
	# creating binary classifiers 
	str_dir_path = os.getcwd ( )
        list_domains = [ "Computers" , "Health" , "Research" , "Finance" ]

        # UNCOMMENT 
        process_binary_classifier ( list_domains , str_dir_path + "/test_6.txt" )
        print "Test 6 done "
        process_binary_classifier ( list_domains , str_dir_path + "/train_6.txt" )
        print "Train 6 done "


	# performing performance checks and reporting accuracy
	
	list_domains = [ "Research" , "Finance" , "Computers" , "Health" ]
	# passing extra feature set in comparision 
        list_feature_set = [ 1 , 2 , 3 , 4 , 5 , 6 ]
        ###### list_domains = ["Computers"] ######
        ###### list_feature_set = [1] ######


        domains_probabilites  = generate_input_prob ( list_domains , list_feature_set , 1 )

	print " generate input completed "

        computers_prob = []
        health_prob = []
        research_prob = []
        finance_prob = []


        for each_key in domains_probabilites.keys() :
                if ( each_key == "Computers" ) :
                        computers_prob = domains_probabilites [ each_key ]
                elif ( each_key == "Health" ) :
                        health_prob = domains_probabilites [ each_key ]
                elif ( each_key == "Research" ) :
                        research_prob = domains_probabilites [ each_key ]
                else :
                        finance_prob = domains_probabilites [ each_key ]

        list_predicted_domains = classify_documents ( health_prob , computers_prob , research_prob , finance_prob , 1 ) 

        print list_predicted_domains


	return 


if __name__ == "__main__":
        main()



