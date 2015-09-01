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

# Question 1 1.1 1)
def preprocess ( raw_text_file , corenlp_output ):
	" Function to make system call to coreNLP and create output file with annotations "
	
	if not os.path.exists ( corenlp_output ):
		os.makedirs( corenlp_output )
	
	call(["java -cp /home1/c/cis530/hw3/corenlp/stanford-corenlp-2012-07-09/stanford-corenlp-2012-07-09.jar:/home1/c/cis530/hw3/corenlp/stanford-corenlp-2012-07-09/stanford-corenlp-2012-07-06-models.jar:/home1/c/cis530/hw3/corenlp/stanford-corenlp-2012-07-09/xom.jar:/home1/c/cis530/hw3/corenlp/stanford-corenlp-2012-07-09/joda-time.jar -Xmx3g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner -filelist " + raw_text_file + " -outputDirectory " + corenlp_output],shell=True)

	return 


# Question 1 1.1 2)
def process_file ( input_xml , output_file ):
	" Function to create new file with same text replaced with named entities "
	# print "Enter"
	parseTree = eTree.parse( input_xml )
	root = parseTree.getroot()
	
	# traverseSentence = root.findall( './document/sentences' )
 	# print " For "
	# print traverseSentence
	# for eachSentence in traverseSentence :
		# print " eachsentence "
		# " to traverse every sentence in given input file "
	traverseToken = root.iter('token')
	# to start the process file with STOP keyword
	strFileData = "STOP"
	flag = 0
	
	for eachToken in traverseToken :
		" to traverse every token in a given xml file "
		word = eachToken[0].text
		namedEntity = eachToken[5].text
		# print word
		# print namedEntity, type(namedEntity), bool (namedEntity)
		# print ('0' == namedEntity)

		if word == '.':
			# print "STOP"
			strFileData = strFileData + " " + "STOP"
			flag = 0
		elif (namedEntity == 'O'):
			# print word
			if(len(word) == 1):
				# to check for non alpha numeric tokens
				if word.isalnum():
					strFileData = strFileData + " " + word.lower()
					flag = 0
				else :
					flag = 1
			else:
				strFileData = strFileData + " " + word.lower()
				flag = 0
		else:
			if ( flag == 0 ) :
				listTemp = strFileData.split()
                		lenListTemp = len ( listTemp )

                		if ( listTemp[ (lenListTemp - 1) ] != namedEntity ):
                        		strFileData = strFileData + " " + namedEntity		
				flag = 0
		
			else :
				strFileData = strFileData + " " + namedEntity
				flag = 0
	
	fileProcess = open ( output_file , "w" )
	fileProcess.write ( strFileData )
	fileProcess.close()

	return


# Question 1 1.2 1)


def getAllFiles ( Directory ):
        listFiles = []
        # to store all files in a list 
        if os.path.isdir( Directory ):
                "If Path Exists"
                # listFiles = []

                itest = 0
                for dirName, subDir, fileList in os.walk( Directory ):
                        # print('Found directory: %s' % dirName)

                        for fname in fileList:
                                fname = dirName + "/" + fname
                                itest = itest + 1
                                if ( itest <= 4 ):
                                	listFiles.append ( fname )
                        	# listFiles.append ( fname )
                        # print listFiles
        return listFiles



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


class BigramModel :

	"Common Class for creating Bigram Models for all list of files"
	
	# for keeping the list for counting frequency 
	listAllWords = []
	listAllWords_Distinct = []
	# for keeping the list of words per file to create bigram model 
	listWordFile_2D = []
	listBigramModels = []


	# creating two dictionaries for maintaing Bigram Model
	dictBigramCount = {}
	dictContextCount = collections.Counter()
	

	def __init__ ( self, trainfiles ):
		" Parameterized Constructor "
		self.trainfiles = trainfiles
		
		# listFiles = getAllFiles ( trainfiles )
		
		# to get list and 2D list of words
		listTemp = []
		for files in trainfiles:
                	" To fetch words file wise"
                	listTemp = load_file_words( files )
                	# to get list of words
			BigramModel.listAllWords.extend( listTemp )
			# to get list of words per file
			BigramModel.listWordFile_2D.append( listTemp )
                	listTemp = []
 
		
		# dictionary to store frequency of words
		dictTermNormalizedFrequency = {}
		countFrequency = 0

		print " Before Term Frequency Count Loop "
		
		dictTermNormalizedFrequency = collections.Counter ( BigramModel.listAllWords )

		#print dictTermNormalizedFrequency
		
		print " After Term Frequency Count Loop "
		
		# print dictTermNormalizedFrequency
		# print len(dictTermNormalizedFrequency)

		# replacing words appearing only once by <UNK>

		print " Before Word Replacement Count Loop "
		for key in dictTermNormalizedFrequency.keys() :
			" to replace words appearing once in each list "
			keyValue = int (dictTermNormalizedFrequency[key])
			# print key
			if ( keyValue == 1 ):
				# for replacing in BigramModel.listAllWords
				# print " Entering with Val 1 "
				if ( key in BigramModel.listAllWords):
					indexKey = BigramModel.listAllWords.index(key)
					BigramModel.listAllWords[indexKey] = "<UNK>"				
	
				# for replacing in BigramModel.listWordFile_2D
				for eachFile in BigramModel.listWordFile_2D:
					if( key in eachFile):
						# if key exists in current file
						indexKey = eachFile.index(key)
						eachFile[indexKey] = "<UNK>"
						break

		# print BigramModel.listAllWords
		print " After Word Replacement Count Loop "

		# to get the set with new words
		setAllWords = set ( BigramModel.listAllWords )

		BigramModel.listAllWords_Distinct = list ( setAllWords )

		# creating Bigram Models 
		print " Before Creating Bigram Model / Context Count Dict "
		strAppend = ""
		for eachFile in BigramModel.listWordFile_2D:
			" for creating bigram model "
			for iLen in range ( 0, (len(eachFile) - 1)):
				strAppend = "<" + eachFile[iLen] + "," + eachFile[iLen+1] + ">"
				# creating list of Bigram Models
				BigramModel.listBigramModels.append(strAppend)

				# for creating Context Count dictionary
				# dictContextCount = collections.Counter()

				BigramModel.dictContextCount.update ( {eachFile[iLen] : 1} )		

		print len(BigramModel.dictContextCount)
		
		print " After Creating Bigram Model / Context Count Dict "

		# count of bigram models 

		print " Before Creating Bigram Count Dict "
		
		BigramModel.dictBigramCount = collections.Counter ( BigramModel.listBigramModels )

		print len(BigramModel.dictBigramCount)
		
		print " Before Creating Bigram Count Dict "


	def logprob ( self, context, event ):
		
		if ( context not in BigramModel.listAllWords_Distinct ):
			context = "<UNK>"

		# for checking if event is there in list
		if ( event not in BigramModel.listAllWords_Distinct ):
			event = "<UNK>"

		# for checking the event occurence as per the context 
		strBigram = '<' + context + ',' + event + '>'
	
		# numerator and denominator values 
		numLog = 0.0
		denomLog = 0.0
		
		# dictBigramCount = {}
		if ( strBigram in BigramModel.dictBigramCount.keys() ) :
			numLog = BigramModel.dictBigramCount [ strBigram ]
			# for laplace smoothing
			numLog = numLog + 1
		else:
			# for bigrams that do not exist with laplace smoothing
			numLog = 1
		
		lenVocab = len ( BigramModel.listAllWords_Distinct )

		# dictContextCount = collections.Counter()
		if ( context in BigramModel.dictContextCount.keys() ) :
			denomLog = BigramModel.dictContextCount [ context ]
			denomLog = denomLog + lenVocab

		else :
			# if word doesnt appear as a context in bigrams
			denomLog = lenVocab


		# print "Num : " + str ( numLog ) + " Denom : " + str ( denomLog ) + " Length of Vocab : " + str ( lenVocab )

		valueLog = float ( float(numLog) / float(denomLog) )

                valueLogProb = float (math.log10(float(valueLog)))	
		
		return valueLogProb


	def print_model ( self, outputfile ):
                " To create a file with content1 : word1 logprob(word1) word2.. "

                strTempFile = ""
                
		# to calculate log prob of each pair in distinct list of words
		# BigramModel.listAllWords_Distinct
                
		lenList = len (BigramModel.listAllWords_Distinct)

                for row in range ( 0, lenList ):
                        # loop for row 
                        context = BigramModel.listAllWords_Distinct[row]
                        strTempFile = strTempFile + str(context) + ":"

                        for column in range ( 0, lenList ):
                                # loop for column
                                word = BigramModel.listAllWords_Distinct[column]
                                logProbWord = self.logprob( context , word )

                                strTempFile = strTempFile +  " " + str(word) + " " + str(logProbWord)


                        strTempFile = strTempFile + " " + "\n"
		

		# print strTempFile

                # writing in file
                fObject = open ( outputfile , "w" )
                fObject.write ( strTempFile )
                fObject.close()

	
	def getppl ( self , testfile ):
		" To get perplexity of the Bigram model generated for a particular file "
	
		probBigram = 0.0
		
		# to get all words in the given test file
		listWords_TestFile = load_file_words( testfile )
		lenTestFile = len ( listWords_TestFile )

		# to compute log prob on each bigram 
		for iLen in range ( 0, ( lenTestFile - 1 )):
			context = listWords_TestFile[iLen]
			event = listWords_TestFile[iLen + 1]

			logProbBigram = self.logprob( context , event )

			# log ab = log a + log b
			probBigram = float ( probBigram + logProbBigram )


		# to calculate likelihood
		likelihood = float ( probBigram ) / float ( lenTestFile )		
		
		
		# calculate perplexity 
		perplexity = float (math.pow ( 10, -(likelihood)))
		
		# print perplexity

		return perplexity
	
# Question 1 1.3 

def create_input_srilm ( inputDir , outputfile ):
        " Function to create output file after combining all files from test directory for  SRILM model "

        listFiles = getAllFiles ( inputDir )

        # to concatenate files

        strConTemp = ""

        for each_file in listFiles :
                infile = open ( each_file , "r")
                strTemp = infile.read()
                infile.close()
		
		# Before concat check for STOP in end and remove for redundancy 
		listTemp = strTemp.split()
		lenListTemp = len ( listTemp )
	
		if ( listTemp[ (lenListTemp - 1) ] == "STOP" ):
			strTemp = ' '.join ( listTemp [ 0 : lenListTemp - 1 ] )
	
                strConTemp = strConTemp + strTemp + " "

        # write in output file 

        outFile = open ( outputfile , "w" )
        outFile.write(strConTemp)
        outFile.close()

        return


def create_srilm_input_for_file ( inputfile , outputfile ):
        " Function to create output file after preprocessing input file for SRILM model "
        
	strTemp = ""
	infile = open ( inputfile , "r")
	strTemp = infile.read()
	infile.close()
	strTemp = strTemp.replace( "STOP","\n" )

	# write in output file 
	
	# outFile = open ( "input_SRILM.txt","w")
	outFile = open ( outputfile , "w" )
	outFile.write(strTemp)
	outFile.close()

	return

def create_srilm_model ( inputDir ):
	" Function to create SRILM Model "

	strpath = os.getcwd()
	inputFile = strpath + '/input_concat_traindata.txt'

	# only concatenating files
	create_input_srilm ( inputDir , inputFile )
	
	outputFile = strpath + '/input_traindata_srilm.txt'

	# converting to required processed file for Srilm model
	create_srilm_input_for_file ( inputFile , outputFile )
	
	# YOUR_TEXT_FILE = "/home1/a/aakritis/input_SRILM.txt"
	YOUR_TEXT_FILE = outputFile
	
	# calling ngram-count to build a language model 
	# call(["/home1/a/aakritis/srilm/ngram-count -unk -text " + YOUR_TEXT_FILE +  " -lm generic.srilm"],shell=True)


	# unigram model 
	call(["/home1/c/cis530/hw2/srilm/ngram-count -unk -order 1 -text " + YOUR_TEXT_FILE +  " -lm unigram_model.srilm"],shell=True)
	
	# bigram model 
	call(["/home1/c/cis530/hw2/srilm/ngram-count -unk -order 2 -cdiscount 0.75 -interpolate -text " + YOUR_TEXT_FILE +  " -lm bigram_model.srilm"],shell=True)
		
	# trigram model
	# - order 3 not required
	call(["/home1/c/cis530/hw2/srilm/ngram-count -unk -cdiscount 0.75 -interpolate -text " + YOUR_TEXT_FILE +  " -lm trigram_model.srilm"],shell=True)

	# print " Completed "
	
	# extracting 100 lines from each file
        #creating unigram.srilm
	
        strFinal = ""
	strcwd = os.getcwd()
	str_model_path = strcwd + '/unigram_model.srilm'
        inFile = open( str_model_path , "r" )
        strTemp = inFile.read()
        inFile.close()
        listLines = strTemp.splitlines()
        sizeList = len(listLines)

        for iLen in range ( (sizeList-100) , sizeList ):
                strFinal = strFinal + listLines[iLen] + "\n"

        outFile = open ( "unigram.srilm" , "w" )
        outFile.write( strFinal )
        outFile.close()

        #creating bigram.srilm
       	
	strFinal = ""
	str_model_path = strcwd + '/bigram_model.srilm'
	inFile = open( str_model_path , "r" )
        strTemp = inFile.read()
        inFile.close()
        listLines = strTemp.splitlines()
        sizeList = len(listLines)
        
	for iLen in range ( (sizeList-100) , sizeList ):
                strFinal = strFinal + listLines[iLen] + "\n"

        outFile = open ( "bigram.srilm" , "w" )
        outFile.write( strFinal )
        outFile.close()

        #creating trigram.srilm
        
	strFinal = ""
	str_model_path = strcwd + '/trigram_model.srilm'
        inFile = open( str_model_path , "r" )
        strTemp = inFile.read()
        inFile.close()
        listLines = strTemp.splitlines()
        sizeList = len(listLines)

        for iLen in range ( (sizeList-100) , sizeList ):
                strFinal = strFinal + listLines[iLen] + "\n"

        outFile = open ( "trigram.srilm" , "w" )
        outFile.write( strFinal )
        outFile.close()

        return


def get_srilm_ppl_for_file ( lm_file , test_file ):
	" Function returns ppl as per SRILM model for a given file "

	strpath = os.getcwd()
	outputFile = strpath + '/input_testfile_srilm_ppl.txt'

        # converting to required processed file for srilm model
        create_srilm_input_for_file ( test_file, outputFile )

	YOUR_MODEL_FILE = lm_file
	YOUR_TEST_FILE = outputFile
	
	# call(["/home1/a/aakritis/srilm/ngram -lm " +  YOUR_MODEL_FILE + " -ppl " +  YOUR_TEST_FILE],shell=True)

	# output = check_output(["/home1/c/cis530/hw2/srilm/ngram -lm " +  YOUR_MODEL_FILE + " -ppl " +  YOUR_TEST_FILE],shell=True)
	
	strCommand = "/home1/c/cis530/hw2/srilm/ngram -lm " +  YOUR_MODEL_FILE + " -ppl " +  YOUR_TEST_FILE

        output = os.popen(strCommand , "r" , 1).read()

	# print "Output" , type(output)
	# print output	
	
	listOutput = str(output).split()
	# print listOutput
	strCompare = 'ppl' + str('=')
	pplValue = 0.0

	if ( strCompare in listOutput ):
		# print 'in if'
		indexPPL = listOutput.index(strCompare)
		pplValue = listOutput[ indexPPL + 1 ]
	else:
		# handling an run time error where ppl= not found
		# print 'in else'
		
		pplValue = 1.0

	# print pplValue

	return pplValue


# Question 1 1.4 

def create_input_bigram ( inputDir , outputfile ):
        " Function to create output file after preprocessing input files directory for bigram  model "

        listFiles = getAllFiles ( inputDir )

        # to concatenate files  after replacing STOP by \n

        strConTemp = ""

        for each_file in listFiles :
                infile = open ( each_file , "r")
                strTemp = infile.read()
                infile.close()

		# Before concat check for STOP in end and remove for redundancy 
                listTemp = strTemp.split()
                lenListTemp = len ( listTemp )

		# removing STOP in end-of-file if exists
                if ( listTemp[ (lenListTemp - 1) ] == "STOP" ):
                        strTemp = ' '.join ( listTemp [ 0 : lenListTemp - 1 ] )
        

                strConTemp = strConTemp + strTemp + " "

        # write in output file 

        outFile = open ( outputfile , "w" )
        outFile.write(strConTemp)
        outFile.close()

        return

def get_all_ppl ( bigrammodel , directory ):
	" Function to get ppl for a given directory using bigram model "
	
	# creating input file 
        strpath = os.getcwd()
	testFile = strpath + '/input_testdata_bigram.txt'
	create_input_bigram ( directory , testFile )

	ppl = bigrammodel.getppl( testFile )
		
	return ppl 

def get_all_ppl_srilm ( lm_file , directory ) :
	" Function to get ppl for a given directory using srilm"

	strpath = os.getcwd()
	inputFile = strpath +  '/input_concat_testdata.txt'

        # only concatenating files for srilm model
        create_input_srilm ( directory , inputFile )

	# preprocessing and calculation of ppl for srilm model
	ppl_all_srilm = get_srilm_ppl_for_file ( lm_file , inputFile )
	
	return ppl_all_srilm

def write_ppl_results ( bigrammodel , directory , resultfile ):
	" Function to write ppl values to file "

	ppl0 = get_all_ppl ( bigrammodel , directory )

	strpath = os.getcwd()
	lm_file_unigram = strpath + '/unigram_model.srilm'
	ppl1 = float ( get_all_ppl_srilm ( lm_file_unigram , directory ) )

	lm_file_bigram = strpath + '/bigram_model.srilm'
	ppl2 = float ( get_all_ppl_srilm ( lm_file_bigram , directory ) )
		
	lm_file_trigram = strpath + '/trigram_model.srilm'
	ppl3 = float ( get_all_ppl_srilm ( lm_file_trigram , directory ) )


	# print " PPL values "
	# print ppl0 , ppl1 , ppl2 , ppl3 


	dict_ppl = { 0 : ppl0 , 1 : ppl1 , 2 : ppl2 , 3 : ppl3 }

	sorted_ppl = sorted ( dict_ppl.items(), key=operator.itemgetter(1) )
        
	listPpl = []
        
	for each_tuple in sorted_ppl :
                var = each_tuple[0]
                listPpl.append(var)
        
	strTemp = "LM ranking: "+ str(listPpl[0]) + " " + str(listPpl[1]) + " " + str(listPpl[2]) + " " + str(listPpl[3])
        
	fResult = open( resultfile , "w" )
        fResult.write( strTemp )
        fResult.close()

	return 

# Question 2.1
def get_distinctive_measure ( lm_file , mem_quote_file , nonmem_quote_file ):
	" Function to returb tuple for given mem and nonmem files ppl values"

	ppl_memquotes = get_srilm_ppl_for_file ( lm_file , mem_quote_file )
	ppl_nonmemquotes = get_srilm_ppl_for_file ( lm_file , nonmem_quote_file )

        tuple_quotes = ( ppl_memquotes , ppl_nonmemquotes )

	return tuple_quotes
	
def calculate_distinctive_measure ( lm_file , mem_quote_file , nonmem_quote_file  , corenlp_output ):
	" Function to get processed files for given mem and nonmem files"

	strpath = os.getcwd ()

	# for mem quote file
	# extract file name from absolute path
	
	listSplit_mem = mem_quote_file.split('/')
	lenSplit_mem = len ( listSplit_mem )	

	mem_file_name = listSplit_mem[ lenSplit_mem - 1 ]
	
	
	input_xml_mem = corenlp_output + "/" + mem_file_name + ".xml"
	
	output_file_mem = strpath + '/mem_quote_process.txt'

	process_file ( input_xml_mem , output_file_mem )

	# ppl_memquotes = get_srilm_ppl_for_file ( lm_file , output_file )

	# for non mem quote file	
	# extract file name from absolute path

        listSplit_nonmem = nonmem_quote_file.split('/')
        lenSplit_nonmem = len ( listSplit_nonmem )

        nonmem_file_name = listSplit_nonmem[ lenSplit_nonmem - 1 ]

        input_xml_nonmem = corenlp_output + "/" + nonmem_file_name + ".xml"
        output_file_nonmem = strpath + '/nonmem_quote_process.txt'

        process_file ( input_xml_nonmem , output_file_nonmem )

	# ppl_nonmemquotes = get_srilm_ppl_for_file ( lm_file , output_file )

	tuple_quotes = get_distinctive_measure ( lm_file , output_file_mem , output_file_nonmem )
	
	return tuple_quotes

def distinctive_highppl_percentage( lm_file , directory ):
	" Function to check tuples for every set of mem and nonmem quotes and return the percentage "

	listQuotesFiles = getAllFiles ( directory )

	# create xml folder by stanford core-nlp
	
	strListofFiles = "\n".join ( listQuotesFiles )

	fileOpen = open ( "file_paths.txt" , "w" )
	fileOpen.write ( strListofFiles )
	fileOpen.close ()

	strpath = os.getcwd ()
        # print " Current Working Directory " + strpath
        corenlp_output = strpath + '/' + "quotes_xml_files"

        preprocess ( "file_paths.txt" , corenlp_output )

	# listMemQuotes = []

	listNonMemQuotes = []

	for eachPath in listQuotesFiles:
		if ( "not_mem.txt" in eachPath ):
			listNonMemQuotes.append ( eachPath )		

	lenFiles = len ( listNonMemQuotes )
	
	tupleSet = ()
	countOccurence = 0.0

	for iLen in range ( 0 , lenFiles ):

		non_mem_file = listNonMemQuotes [ iLen ] 
		lsFileName = non_mem_file.split( '_' , 1 )
		
		mem_file = lsFileName[0] + "_mem.txt"

		tupleSet = calculate_distinctive_measure ( lm_file , mem_file  , non_mem_file , corenlp_output )
		

		if ( float(tupleSet[0]) > float(tupleSet[1]) ):
			countOccurence = countOccurence + 1


	print str ( countOccurence ) + " : Count of greater"

	perCentVal = float ( countOccurence ) / float ( lenFiles )

	print str ( perCentVal) + ": PercentValue"
	
	percent = float (perCentVal) * 100
	
	return percent 

def write_percent_ppl ( lm_file , directory , result_file ):

	percent = distinctive_highppl_percentage( lm_file , directory )
	
	strWrite = "\n" + "Percentage of memorable quotes from LM 3 with higher perplexity: " + str ( percent ) + "%"

	fileObj = open ( result_file , "a" )
	fileObj.write( strWrite )
	fileObj.close()

	return

# Question 3 3.1

def get_bestfit ( sentence , wordlist , bigrammodel ):
	" Function to get the best fit word for a given sentence. "
	
	dict_pplval = {}
	checkSentence = ""
	strAbsPath = ""
	strpath = os.getcwd ()

	for eachWord in wordlist :
		" Function to check ppl value by replacing <blank> by word "
		checkSentence  = sentence.replace ( "<blank>" , eachWord )
	
		# getting absolute path for new file 
		fileAbs = strpath + '/' + eachWord +'.txt'

		fileInput = open ( fileAbs , "w" )
		fileInput.write ( checkSentence )
		fileInput.close ()

		strAbsPath = strAbsPath + fileAbs + "\n"

	# writing file paths to file_list	
	file_nlp = open ( 'file_nlp.txt' , "w")
	file_nlp.write ( strAbsPath )
	file_nlp.close ()

	# run standford core nlp 
        corenlp_output = strpath + '/' + "sentences_xml_files"

        preprocess ( "file_nlp.txt" , corenlp_output )

	for eachWord in wordlist :
		" Creating processed text file "
		
		input_xml = corenlp_output + "/" + eachWord + ".txt.xml"
	        output_file = strpath + '/' + eachWord + '.txt'

		process_file ( input_xml , output_file )

		ppl = bigrammodel.getppl( output_file )
		
		dict_pplval [ eachWord ] = ppl
	
	sorted_ppl = sorted ( dict_pplval.items(), key=operator.itemgetter(1) )

        listPpl = []

        for each_tuple in sorted_ppl :
                var = each_tuple[0]
                listPpl.append(var)	

	return str(listPpl[0])

# Question 3 3.2

def write_bestfit_accuracy ( bigrammodel, result_file ):
	" Function to get accuracy of bestfit function for given fill in the blanks "

	intCountCorrect = 0

	sentence1 = "Stocks <blank> this morning."
	wordlist1 = [ 'plunged' , 'walked' , 'discovered' , 'rise' ]
	
	# best fit run
	
	bestfit1 = get_bestfit ( sentence1 , wordlist1 , bigrammodel )

	if ( bestfit1 == wordlist1 [ 0 ] ):
		intCountCorrect  = intCountCorrect + 1


	sentence2 = "Stocks plunged this morning, despite a cut in interest <blank> by the Federal Reserve."
	wordlist2 = [ 'rates' , 'patients' , 'researchers' , 'levels' ]

	# best fit run

        bestfit2 = get_bestfit ( sentence2 , wordlist2 , bigrammodel )

        if ( bestfit2 == wordlist2 [ 0 ] ):
                intCountCorrect  = intCountCorrect + 1

	sentence3 = "Stocks plunged this morning, despite a cut in interest rates by the <blank> Reserve."
	wordlist3 = [ 'Federal', 'university' , 'bank' , 'Internet' ]

	# best fit run

        bestfit3 = get_bestfit ( sentence3 , wordlist3 , bigrammodel )

        if ( bestfit3 == wordlist3 [ 0 ] ):
                intCountCorrect  = intCountCorrect + 1

	sentence4 = "Stocks plunged this morning, despite a cut in interest rates by the Federal Reserve, as Wall Street began <blank> for the first time."
	wordlist4 = [ 'trading' , 'wondering' , 'recovering' , 'hiring' ]

	# best fit run

        bestfit4 = get_bestfit ( sentence4 , wordlist4 , bigrammodel )

        if ( bestfit4 == wordlist4 [ 0 ] ):
                intCountCorrect  = intCountCorrect + 1

	sentence5 = "Stocks plunged this morning, despite a cut in interest rates by the Federal Reserve, as Wall Street began trading for the first time since last Tuesday's <blank> attacks."
	wordlist5 = [ 'terrorist' , 'heart' , 'doctor' , 'alien' ]

	# best fit run

        bestfit5 = get_bestfit ( sentence5 , wordlist5 , bigrammodel )

        if ( bestfit5 == wordlist5 [ 0 ] ):
                intCountCorrect  = intCountCorrect + 1

	
	accuracy = float ( intCountCorrect ) / float ( 5 ) 
	
	percentAccuracy = accuracy * 100

	# appending data to accuracy 
	
	strFile = "\nAccuracy for filling blanks with Bigram Language Model : " + str( percentAccuracy ) + "%"
	
	fileObj = open ( result_file , "a" )	
	fileObj.write ( strFile )
	fileObj.close()


	return 

# Question 3 3.3)

def fill_blank ( sentence , bigrammodel ):	
	" Function to return most likely value of <blank> "
	
	# to write sentence in file

	strpath = os.getcwd ()
	sentencePath = strpath + '/' + 'sentence.txt'
	fileSent = open ( "sentence.txt" , "w" )
	fileSent.write ( sentence )
	fileSent.close()

	# to write absolute path in file
	fileAbsolute = open ( "sentence_path.txt" , "w")
        fileAbsolute.write ( sentencePath )
        fileAbsolute.close()

	strpath = os.getcwd ()
        # print " Current Working Directory " + strpath
        corenlp_output = strpath + '/' + "sentence_xml_files"

	# calling core-nlp
	preprocess ( "sentence_path.txt" , corenlp_output )

	# pre process file
	input_xml = corenlp_output + "/sentence.txt.xml"
        output_file = 'sentenceProcessed.txt'

        process_file ( input_xml , output_file )

	fileRead = open ( 'sentenceProcessed.txt' , 'r' )
	strSentence = fileRead.read()
	fileRead.close()	

	# get context
	listSentence = strSentence.split()
	lenlist = len ( listSentence )
	
	if ( "<blank>" in listSentence ) :
		index = listSentence.index ( "<blank>" )
		context = listSentence [ index - 1 ]
	else :
		context = listSentence [ lenlist - 2 ]

	# for capturing events for current context
	listEvents = []
	dictEventProb = {}

	

	for eachKey in BigramModel.dictBigramCount.keys() :
		lenKey = len (eachKey)
		strGroup = eachKey[ 1 : (lenKey - 1) ]
		listSplit = strGroup.split(',')
		if ( listSplit[0] == context ):
			listEvents.append( listSplit[1] )
	
	for event in listEvents :
		# call logprob
		prob = float ( bigrammodel.logprob ( context , event ) )
		dictEventProb [ event ] = prob


	sorted_prob = sorted ( dictEventProb.items(), key=operator.itemgetter(1) )

        list_event = []

        for each_tuple in sorted_prob :
                var = each_tuple[0]
                list_event.append(var)

	list_event.reverse ()
	
	# handling empty list scenario
	if ( len( list_event ) == 0 ) :
		return 'NA'

	else :
		return list_event[0]

def write_predicted_words ( bigrammodel , result_file ): 
	" Function to write original : predicted word for given sentences "

	strOutputFile = "\n"
	
	sentence1 = "With great powers comes great <blank>"
	original1 = "responsibility"

	predicted1 = fill_blank ( sentence1 , bigrammodel )
	strOutputFile += original1 + ":" + predicted1 + "\n"


	sentence2 = "Say hello to my little <blank>"
	original2 = "friend"

	predicted2 = fill_blank ( sentence2 , bigrammodel )
        strOutputFile += original2 + ":" + predicted2 + "\n"


	sentence3 = "Hope is the quintessential human delusion, simultaneously the source of your greatest strength, and your greatest <blank>"
	original3 = "weakness"

	predicted3 = fill_blank ( sentence3 , bigrammodel )
	strOutputFile += original3 + ":" + predicted3 + "\n"
	

	sentence4 = "You either die a hero or you live long enough to see yourself become the <blank>"
	original4 = "villain"
	
	predicted4 = fill_blank ( sentence4 , bigrammodel )
	strOutputFile += original4 + ":" + predicted4 + "\n"

		
	sentence5 = "May the Force be with <blank>"
	original5 = "you"

	predicted5 = fill_blank ( sentence5 , bigrammodel )
	strOutputFile += original5 + ":" + predicted5 + "\n"

	sentence6 = "Every gun makes its own <blank>"
	original6 = "tune"

	predicted6 = fill_blank ( sentence6 , bigrammodel )
	strOutputFile += original6 + ":" + predicted6 + "\n"
	
	fileObj = open ( result_file , "a" )
	fileObj.write ( strOutputFile )
	fileObj.close ()

	return

def main ():
	" implementation of the main calling function "
	
	# get current working directory
	strdirpath = os.getcwd()	

	# Question 1 1.1 1)

	# File containing Absolute file paths
	raw_text_file = "/home1/c/cis530/hw3/corenlp/stanford-corenlp-2012-07-09/files.txt"
	# directory containing xml files for files in raw_text_file
	corenlp_output = strdirpath + '/' +  "core_nlp_output"
	
	# UNCOMMENT
	preprocess ( raw_text_file , corenlp_output )

	# test data 
	raw_text_file = strdirpath + '/raw_test.txt'
	# preprocess ( raw_text_file , corenlp_output )

	print "1 1.1 1)"
		
	# Question 1 1.1 2)

	input_xml = '/home1/a/aakritis/core_nlp_output/3178263.txt.xml'
	output_file = '/home1/a/aakritis/output_file_ner.txt'

	# UNCOMMENT
	# process_file ( input_xml , output_file )

	# test data 
	
	input_xml = '/home1/a/aakritis/core_nlp_output/test1.txt.xml'
	output_file = '/home1/a/aakritis/output_ner_test1.txt'

	# process_file ( input_xml , output_file )

	input_xml = '/home1/a/aakritis/core_nlp_output/test2.txt.xml'
        output_file = '/home1/a/aakritis/output_ner_test2.txt'

        # process_file ( input_xml , output_file )


	print "1 1.1 2)"


	# Question 1 1.2 1)
	
	# calling parameterized constructor of class BigramModel
	
	train_dir = '/home1/c/cis530/hw2/data/processed_train_set'

	listFiles = getAllFiles ( train_dir )
	
	# UNCOMMENT
	bigramModelObj = BigramModel(listFiles)

	print "1 1.2 1) a"


	# selecting random values for context and event 
	context = 'anyone'
	event = 'palaces'

	# UNCOMMENT
	# logProb = bigramModelObj.logprob ( context, event )
	# print str(logProb) + " : Log Prob Value "	

	print "1 1.2 1) b"

	# creating outputFileMatrix

	outputfile = strdirpath + '/output_context_word_prob.txt'
	
	# UNCOMMENT 
	# bigramModelObj.print_model ( outputfile )

	print "1 1.2 1) c"

	# question 1 1.2 2)

	# get perplexity for a given file 

	# test file Finance_2005_06_24_1682550_p.txt

	testfile = '/home1/c/cis530/hw2/data/processed_test_set/Finance_2006_03_05_1744447_p.txt'

	# UNCOMMENT 
	# ppl_one_bigram = bigramModelObj.getppl( testfile )
	
	print "1 1.2 2)"


	# question 1 1.3 1)

	trainfiles_srilm = '/home1/c/cis530/hw2/data/processed_train_set'

	
	# UNCOMMENT
	create_srilm_model ( trainfiles_srilm )
	
	print "1 1.3 1)"
	
	# question 1 1.3 2)

	# test run for one file using unigram model
	test_file = '/home1/c/cis530/hw2/data/processed_test_set/Finance_2006_03_05_1744447_p.txt'
	
	lm_file = strdirpath + '/unigram_model.srilm'
	
	# UNCOMMENT
	# ppl_one_unigram_srilm = get_srilm_ppl_for_file ( lm_file , test_file )

	print " 1 1.3 2) "


	# Question 1 1.4	

	testDirectory = '/home1/c/cis530/hw2/data/processed_test_set'

	# bigramModelObj

	# UNCOMMENT
	# ppl_all_bigram = get_all_ppl ( bigramModelObj , testDirectory )


	# running for Unigram.srilm
	directory = '/home1/c/cis530/hw2/data/processed_test_set'
	
	lm_file = strdirpath + '/unigram_model.srilm'

	# UNCOMMENT
	# ppl_all_unigram_srilm = get_all_ppl_srilm ( lm_file , directory ) 
	
	# writing output to result.txt

	result_file = strdirpath + '/results.txt'

	# UNCOMMENT
	write_ppl_results ( bigramModelObj , directory , result_file )
	
	print " 1 1.4 "


	# Question 2 2.1

	lm_file = strdirpath + '/trigram_model.srilm'
	mem_quote_file = '/home1/c/cis530/hw2/data/quotes/1566_mem.txt'
	nonmem_quote_file = '/home1/c/cis530/hw2/data/quotes/1566_not_mem.txt'

	# UNCOMMENT
	# tup_quotes = get_distinctive_measure( lm_file, mem_quote_file, nonmem_quote_file )
	
	# print "\n\n\n\n For a given mem and non-mem file : " + str ( tup_quotes )

	lm_file = strdirpath + '/trigram_model.srilm'
	directory = '/home1/c/cis530/hw2/data/quotes'

	# UNCOMMENT
	# percent = distinctive_highppl_percentage( lm_file , directory )


	result_file = strdirpath + '/results.txt'
	
	# UNCOMMENT
	write_percent_ppl ( lm_file , directory , result_file )

	print " 2 2.1 "	


	# Question 3 3.1

	sentence = "Stocks <blank> this morning."
	wordlist = [ 'plunged' , 'walked' , 'discovered' , 'rise' ]
	
	# UNCOMMENT
	# str_output = get_bestfit ( sentence , wordlist , bigramModelObj )

	print "3 3.1"
	
	# Question 3 3.2
	result_file = strdirpath + '/results.txt'
	
	print "3 3.2"
	
	# UNCOMMENT
	write_bestfit_accuracy ( bigramModelObj , result_file )

	# Question 3 3.3

	sentence = 'With great powers comes great <blank>'

	# UNCOMMENT
	# fillBlank = fill_blank ( sentence , bigramModelObj , result_file )

	result_file = strdirpath + '/results.txt'
	
	# UNCOMMENT
	write_predicted_words ( bigramModelObj , result_file )	

	print "3 3.3"

	return

if __name__ == "__main__":
	main()
