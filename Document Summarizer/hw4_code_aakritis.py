from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
from nltk import word_tokenize
from numpy import zeros
from math import log
from subprocess import call
from subprocess import check_output
import os
import math
import operator
import collections
from itertools import repeat
from itertools import chain
import string

# Helper Functions 

def get_list_subdirs ( directory ) :
        " Function to return the list of files with absolute paths "
        list_dirs = []

        # to store all files in a list 
        if os.path.isdir( directory ):
                "If Path Exists"
                for dirName, subDir, fileList in os.walk ( directory ) :
                        for dname in subDir :
                                dname = dirName + "/" + dname
                                list_dirs.append ( dname )
	return list_dirs

def get_all_files ( directory ):
        listFiles = []
        # to store all files in a list 
        if os.path.isdir ( directory ) :
                "If Path Exists"
                # listFiles = []

                ###### for testing purpose ######
                # itest = 0
                for dirName, subDir, fileList in os.walk ( directory ) :
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

# Question 1.1
def process_ts_file ( directory ) :
	" Function to return ts files for each sub directory with list of words and their probabilites "
	
	str_dir_path = os.getcwd ()

	# extracting list of files from a given directory 
	list_all_dirs = get_list_subdirs ( directory )

	config_dir = str_dir_path + "/config_files"
	if not os.path.exists ( config_dir ):
		os.makedirs( config_dir )

	ts_dir = str_dir_path + "/ts_files"
        if not os.path.exists ( ts_dir ):
                os.makedirs( ts_dir )


	# for loop to work on subdirs
	for each_subdir in list_all_dirs : 
		# extract subdir name 
		list_name = each_subdir.split ( "/" )
		len_list = len ( list_name ) 
		name = list_name [ len_list - 1 ] 

		# create config.example file 
		fname = str_dir_path + "/config_files/" + "config." + name
		fConfig = open ( fname , "w" )
		inputDir = each_subdir 
		outputFile = str_dir_path + "/ts_files/aakritis_" + name + ".ts" 
		strFileData = "==== Do not change these values ==== \nstopFilePath = /home1/c/cis530/hw4/TopicWords-v2/stoplist-smart-sys.txt \nperformStemming = N \nbackgroundCorpusFreqCounts = /home1/c/cis530/hw4/TopicWords-v2/bgCounts-Giga.txt \ntopicWordCutoff = 0.1 \n\n==== Directory to compute topic words on ==== \n\ninputDir = " + inputDir + "\n\n==== Output File ==== \n\noutputFile = " + outputFile + "\n"
 		fConfig.write ( strFileData )
		fConfig.close ()
		
		# run java command for each config file
		call ( [ "java -Xmx1000m -cp /home1/c/cis530/hw4/TopicWords-v2 TopicSignatures " + fname ] , shell=True )
	return

# Question 1.1 2
def load_topic_words ( topic_file , n ) :
	" Function to return tuple of two lists as per size n and statistic values "
	tup_lists = ()

	dict_temp = {}	

	fObj = open ( topic_file , "r" )
	str_file_data = fObj.read ()
	fObj.close ()

	list_file_lines = str_file_data.split ("\n")

	list_file_lines = list_file_lines [ : ( len ( list_file_lines ) - 1 ) ]

	for each_line in list_file_lines :
		list_data_line = each_line.split()
		dict_word = list_data_line [ 0 ]
		dict_val = float ( list_data_line [ 1 ] )
		# to sort out only topic words from the given list of words
		if ( dict_val >= 10.0 )  :
			dict_temp [ dict_word ] = dict_val
	
	# sorting of dict in reverse order based on values
	sorted_words = sorted ( dict_temp.items(), key=operator.itemgetter(1), reverse = True )

        list_ordered_words = []

        for each_tuple in sorted_words :
                var = each_tuple[0]
                list_ordered_words.append(var)

	tup_lists = ( list_ordered_words [ 0 : n ] , list_ordered_words [ n : ] ) 

	return tup_lists

# Question 1.2 
def expand_keywords ( keylist , candidatelist , ic, outputfile ) :
	" Function to write txt files with details of expanded keywords along with key list "

	fObj = open ( outputfile , "w" )

	# to compute similar words for each keylist word
	for each_word in keylist :    
		list_each_word_syn = wn.synsets ( each_word , pos = wn.NOUN )
		
		# to check if noun sysnet exists 
		if ( len ( list_each_word_syn ) <> 0 ) :
			each_word_syn = list_each_word_syn [ 0 ] 
			fObj.write ( "[" + each_word + ":" + " ") 

			dict_other_word = { }

			for other_word in candidatelist :
				list_other_word_syn = wn.synsets ( other_word , pos = wn.NOUN ) 

				# to check if noun sysnet exists 
				if ( len ( list_other_word_syn )  <> 0 ) :
					other_word_syn = list_other_word_syn [ 0 ]
					
					# compute resnik similarity 
					res_sim = float ( each_word_syn.res_similarity ( other_word_syn , ic ) )
					
					if ( res_sim <> 0.0 ) :
						dict_other_word [ other_word ] = res_sim 

			# to sort list of non-zero resnik similarity words
			sorted_words = sorted ( dict_other_word.items(), key=operator.itemgetter(1), reverse = True )
			list_ordered_words = []

			for each_tuple in sorted_words :
				var = each_tuple[0]
                		list_ordered_words.append(var)

			str_other_words = " ".join ( list_ordered_words ) + "]" + "\n"
			fObj.write ( str_other_words ) 

	fObj.close ()

	return

# Question 2.1 
def summarize_baseline ( inputdir , outputfile ) :
	" Function to get 100 word summary for a given directory "
    
	# extract files from the given directory 
	list_all_files = get_all_files ( inputdir )
	# sorting files in alphabetical order 
	list_all_files.sort ( )

	len_files = len ( list_all_files )

	len_sum = 0 
	file_count = 0 

	f_out = open ( outputfile , "w" )

	# to restrict file length to 100 words
	while ( len_sum < 100 ) :
		if ( len_files > file_count ) :
			fObj = open ( list_all_files [ file_count ] , "r" )
			str_file_data = fObj.read ( )
			fObj.close ( )

			list_file_lines = str_file_data.split ( "\n" , 1 )
			str_sum_line = list_file_lines [ 0 ]

			# count words in str_sum_line 
			list_words = str_sum_line.split ( )		

			f_out.write ( str_sum_line + "\n" )

			file_count = file_count + 1
			len_sum = len_sum + len ( list_words )		

	f_out.close ( )
	
	return

# Helper function 
def cal_word_prob ( list_of_words ) :
	" Function to calculate P(W) and Q(W) values" 
	dict_values = { }
	
	# calculating Q(w) for each word
        denom = len ( list_of_words )

        # to get dictionary of counters from a list             
        dict_count_values = collections.Counter ( list_of_words )

        # to fetch values of Q(w)
        for each_key in  dict_count_values.keys () :
		if ( float ( denom ) <> 0.0 ) :
                	dict_values [ each_key ] = float ( float ( dict_count_values [ each_key ] ) / float ( denom ) )

	return dict_values

def calculate_kl_divergence ( dict_p_values , dict_q_values ) :
	" Function to calculate KL divergence values for given summary "

	sum_val = 0.0

	for each_word in dict_p_values.keys () :
		if each_word in dict_q_values.keys () :
			if ( dict_q_values [ each_word ] <> 0.0 ) :
				log_value = math.log ( float ( dict_p_values [ each_word ] / dict_q_values [ each_word ] ) )
				sum_add = float ( float ( dict_p_values [ each_word ] ) * float ( log_value ) )
				sum_val = sum_val + sum_add

	return sum_val

# Question 2.2 
def summarize_kl ( inputdir , outputfile ) :
	" Function to write summary for given directory based on KL greedy summarizer "

	# extract list of files from the given directory
	list_all_files = get_all_files ( inputdir )

	list_all_sentences = []
	list_all_words = []

	for each_file in list_all_files :
		fObj = open ( each_file , "r" )
                str_file_data = fObj.read ( )
		fObj.close ( )

		list_file_lines = str_file_data.split ( "\n" )
		# removing empty sentence and appending
		list_all_sentences.extend ( list_file_lines [ : ( len ( list_file_lines ) - 1 ) ] )

		# print len ( list_all_sentences ) 

		list_file_words = word_tokenize ( str_file_data ) 
		list_all_words.extend ( list_file_words )

	# print len ( list_all_sentences )
	# print list_all_sentences
	# remove redundant sentences 
	list_unique_sentences = list ( set ( list_all_sentences ) ) 

	# fetch list of stop words
	list_stop_words = []
	f_stop = open ( "/home1/c/cis530/hw4/stopwords.txt" , "r" )
	list_stop_words = str ( f_stop.read () ).split ( "\n" )
	# removing empty word in the end of file
	list_stop_words = list_stop_words [ : len ( list_stop_words ) - 1 ]

	# to fetch list of content words
	list_content_words = [ each_word for each_word in list_all_words if each_word not in list_stop_words ] 
	# print len ( list_content_words ) 

	# calculating Q(w) for each content word in cluster
	dict_q_values = cal_word_prob ( list_content_words )
	# print dict_q_values , len ( dict_q_values.keys() )

	str_summary = ""
	len_summary = 0

	# to get current len of list_unique_sentences
	len_sentences = len ( list_unique_sentences )

	# checking that summary length is < = 100 
	while ( ( len_summary < 100 ) and ( len_sentences <> 0 ) ) :
		
		# dictionary for KL divergence values 
        	dict_kl_divergence = { }

		for index in range ( 0 , len_sentences ) : 
			str_new_summary = str_summary + list_unique_sentences [ index ]			
	
			# fetch words in newly created summary 
			list_summary_words = word_tokenize ( str_new_summary )

			# to fetch only content words for given summary
			list_summary_content_words = [ each_word for each_word in list_summary_words if each_word not in list_stop_words ]
			# calculating P(w) for each content word in summary
			dict_p_values = cal_word_prob ( list_summary_content_words ) 			
			# print dict_p_values 
			# print len ( list_summary_content_words ) 
			
			dict_kl_divergence [ int ( index ) ] = float ( calculate_kl_divergence ( dict_p_values , dict_q_values ) )
		
		# print len ( dict_kl_divergence.keys () )
		# sorting dictionary for least KL value 
		index_sentence = 0
		sorted_sentences = sorted ( dict_kl_divergence.items(), key=operator.itemgetter(1) )
		# print sorted_sentences 
		if ( len ( dict_kl_divergence.keys ( ) ) <> 0 ) :
			index_sentence = int ( sorted_sentences [ 0 ][ 0 ] ) 
		else : 
			index_sentence = 0
		# print index_sentence
		# print dict_kl_divergence [ 4 ] , dict_kl_divergence [ 39 ]

		# add sentence in summary 
		str_summary = str_summary + list_unique_sentences [ index_sentence ] + "\n"
		
		# update length of summary 
		list_current_summary = str_summary.split ( )
		len_summary = len ( list_current_summary ) 
		
		# popping added element from the list
		list_unique_sentences.pop ( index_sentence ) 
		len_sentences = len ( list_unique_sentences )

	# writing summary to output file 
	fObj = open ( outputfile , "w" ) 
	fObj.write ( str_summary ) 
	fObj.close ( )

	return

def write_rouge_results ( outputfile ) :
	" Function to write rouge results for baseline and kl summarizer "

	fObj = open ( outputfile , "w" ) 
	fObj.write ( "baseline" + "\n" )
	
	str_baseline_output = check_output ( ["./ROUGE-1.5.5.pl -c 95 -r 1000 -n 2 -m -a -l 100 -x config_baseline.xml" ] , shell = True )
	fObj.write ( str_baseline_output + "\n" + "greedy kl" + "\n" )
	str_kl_output = check_output ( ["./ROUGE-1.5.5.pl -c 95 -r 1000 -n 2 -m -a -l 100 -x config_kl.xml" ] , shell = True )
	fObj.write ( str_kl_output ) 

	fObj.close ()
	
	return

def main () :
	" Function to write calling of all the above functions "

	str_dir_path = os.getcwd ()	

	# Question 1.1 1 
		
	directory = "/home1/c/cis530/hw4/dev_input"
	process_ts_file ( directory )
	
	print "1.1 1 Computed"
	

	# Question 1.1 2
	
	topic_file = str_dir_path + "/ts_files/" + "aakritis_dev_00.ts"
	n = 20
	tup_list = load_topic_words ( topic_file , n )
	
	print "1.1 2 Computed"


	# Question 1.2
	
	# to get list of all .ts file 
	ts_directory = str_dir_path + "/ts_files"
	list_all_files = get_all_files ( ts_directory ) 
	n = 20 

	text_directory = str_dir_path + "/expanded_topic_words_files"

	if not os.path.exists ( text_directory ):
		os.makedirs ( text_directory )

	# computing information content ( ic )
	brown_ic = wordnet_ic.ic ( 'ic-brown.dat' )

	for each_file in list_all_files : 

		# run load_topic_words to get key list and candidate list 
		tup_list = load_topic_words ( each_file , n )  # Question 1.1 2 
		keylist = tup_list [ 0 ] 
		candidatelist = tup_list [ 1 ] 
		
		# to extract file name 
		list_name = each_file.split ( "/" )
                len_list = len ( list_name )
                name_ext = list_name [ len_list - 1 ]

		name_split = name_ext.split ( "." , 1 )
		name = name_split[0] + ".txt"	

		outputfile = str_dir_path + "/expanded_topic_words_files/" + name

		expand_keywords ( keylist , candidatelist , brown_ic , outputfile ) 

		print name + " Written"
	print "1.2 Computed"
	

	# Question 2.1 
	
	directory = "/home1/c/cis530/hw4/dev_input"

	list_sub_dirs = get_list_subdirs ( directory )

	sum_directory = str_dir_path + "/summarize_baseline"
	
	if not os.path.exists ( sum_directory ):
		os.makedirs ( sum_directory )

	for each_subdir in list_sub_dirs :

		# extract dir name from dir path 
		list_name = each_subdir.split ( "/" )
		len_list = len ( list_name )
		name = "sum_" + list_name [ len_list - 1 ] + ".txt"
		outputfile = str_dir_path + "/summarize_baseline/" +  name

		summarize_baseline ( each_subdir , outputfile ) 
		
		print name + " Written"

	print "2.1 Computed"


	# Question 2.2
	
	directory = "/home1/c/cis530/hw4/dev_input"

        list_sub_dirs = get_list_subdirs ( directory )

        sum_directory = str_dir_path + "/summarize_kl"
        
        if not os.path.exists ( sum_directory ):
                os.makedirs ( sum_directory )

        for each_subdir in list_sub_dirs :

                # extract dir name from dir path 
                list_name = each_subdir.split ( "/" )
                len_list = len ( list_name )
                name = "sum_" + list_name [ len_list - 1 ] + ".txt"
                outputfile = str_dir_path + "/summarize_kl/" +  name

                summarize_kl ( each_subdir , outputfile ) 
                
                print name + " Written"	


	print "2.2 Computed"	
	
	
	# Question 2.3
	
	result_file = str_dir_path + "/results.txt"
	write_rouge_results ( result_file )

	print "2.3 Computed"

	return 

if __name__ == "__main__" :
	main ( )
