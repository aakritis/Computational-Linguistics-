import os
import glob
import math
import operator
# from operator import itemgetter, attrgetter

# rootDirectory = "/home1/c/cis530/hw1/data/corpus/starbucks"
# update values 
# rootDirectory_main = "/home1/c/cis530/hw1/data/all_data/"
# listFiles = []
# listTokens = []
aakritis_listAllFiles = []
# flagGlobal = 1
# listAllWords = []
# dictTermNormalizedFrequency = {}
# listAllWords_2D = []
# dictInverseDocumentFrequency = {}
# fileBrownCluster = "/home1/c/cis530/hw1/data/brownwc.txt"


# question 1 a)
def get_all_files( directory ):
	"Function to fetch all files from multi-level directory"
	if os.path.isdir( directory ):
		"If Path Exists"
		# to get relative paths
		listFiles = []
		for dirName, subDir, fileList in os.walk(directory):
    			# print('Found directory: %s' % dirName)
    			for fname in fileList:
				fname = dirName + "/" + fname
				# fname = fname[31:]
				# to fetch relative paths
				listFName = fname.split("/")
				count = len(listFName)
				relativeFilePath = "/" + listFName[count-2] + "/" + listFName[count-1]
				# global listFiles
				listFiles.append(relativeFilePath)
				# print len(listFiles)
	return listFiles;


# Question 1 b)
def load_file_tokens( filePath ):
	" Function to get list of words in a file"
	listTokens = []
	charSum = ""
	if os.path.isfile( filePath ):
		# print Exists
		fileObject = open(filePath,"r")
		stringConverter = fileObject.read()
		# stringConverter = "Beautiful, is; better*than\nugly"
		# print stringConverter
		for charC in stringConverter:
			if charC.isalnum():
				charSum = charSum + charC
			elif charC.isspace():
				if len(charSum) > 0:
					charSum = charSum.lower()
					# global listTokens
					listTokens.append(charSum)
					charSum = ""
			else:
				if len(charSum) > 0:
					charSum = charSum.lower()
					# global listTokens
					listTokens.append(charSum)
					charSum = ""
	else:
		print "Not Exists"
	return listTokens;

# Question 1 c)
# to get all absolute paths of files in a directory
def get_Files_AllDirectories( directory ):
        "Function to fetch all files from multi-level directory"
        if os.path.isdir( directory ):
                "If Path Exists"
                for currentFile in glob.glob( os.path.join(directory,'*')):
                        if os.path.isdir(currentFile):
                                # print "got a directory :" + currentFile
                                get_Files_AllDirectories(currentFile)
                        else:
                                # print "processing files:" + currentFile
                                global aakritis_listAllFiles   # Needed to modify global copy of listAllFiles
                                aakritis_listAllFiles.append(currentFile)
                                #listAllFiles

        else:
                "If Path Doesn't Exist"
                print "The path mentioned does not exist"

        return aakritis_listAllFiles;

def load_collection_tokens ( directory ):
	" Function to load the words from all files in directory "
	listTemp = []
	listAllWords = []
	global aakritis_listAllFiles
	aakritis_listAllFiles = []
	aakritis_listAllFiles = get_Files_AllDirectories(directory)
	# print listAllFiles
	for files in aakritis_listAllFiles:
		" To fetch tokens file wise"
		listTemp = load_file_tokens( files )
		# global listAllWords
		listAllWords.extend(listTemp)
		listTemp = []
	return listAllWords
	


# Question 2.1 a)
def get_tf ( itemlist ):
	" Funtion to return dictionary of words and normalized term frequency "
	dictTermNormalizedFrequency = {}
	tempDict = {}
	countFrequency = 0.0
	maxValue = 0.0
	for item in itemlist:
		" For loop to assign term frequency in dummy dictionary "
		countFrequency = itemlist.count(item)
		tempDict[item] = float(countFrequency)
	valueDict = tempDict.values() 
	maxValue = float(max(valueDict))
	
	normalFrequency = 0.0
	for item in itemlist:
		" For storing normalized term frequency "
		normalFrequency = float(tempDict[item]/maxValue)
		# global dictTermNormalizedFrequency
		dictTermNormalizedFrequency[item] = normalFrequency


	# adding artificial word " < U N K > " assuming it appeared once in all the documents
        # dictTermNormalizedFrequency["< U N K >"] = round(float(1.0/maxValue),5)

	# print tempDict
	# print valueDict
	# print maxValue
	# print dictTermNormalizedFrequency	

	return dictTermNormalizedFrequency

# Question 2.1 b)

def create_itemList():
	listAllWords_2D = []
	" Function to create 2D list "
	# here ... instead of using global varriable ... empty global varriable and re-run the function for larger data in 2.1 c)
	
	# print "Before", len(listAllFiles)
	global aakritis_listAllFiles
	aakritis_listAllFiles = []
	# print "After",len(listAllFiles)
	# global listAllFiles 
	aakritis_listAllFiles = get_Files_AllDirectories( "/home1/c/cis530/hw1/data/all_data"  )
	# print " After 2", len(listAllFiles)
	for files in aakritis_listAllFiles:
                " To fetch tokens file wise into 2D list "
                listTemp = load_file_tokens( files )
                # to create a 2D list - function append
		listAllWords_2D.append(listTemp)
                listTemp = []  
	return listAllWords_2D

def get_idf(itemlist):
	" Function to generate IDF for given itemlist "
	dictTempDocFrequency = {}
	dictInverseDocumentFrequency = {}
	NumberOfDocuments = len(itemlist)
	# print NumberOfDocuments 
	for list1 in itemlist:
		" List to compare occurence of words from one list to other "
		# countDoc = 1
		for item in list1:
			"to access particular item in current list"
			countDoc = 1
			if dictTempDocFrequency.has_key(item):
				continue
			for list2 in itemlist:
				" to check if item exists in another documents "
				if(list1 is not list2):
					" to remove redundant check with inital list itself"
					if (item in list2):
						countDoc = countDoc + 1
						continue
			dictTempDocFrequency[item] = countDoc
			# countDoc = 1
	
	for keys in dictTempDocFrequency.keys():
		" for calculating IDF for the given dictionary "
		valueTemp = float (dictTempDocFrequency[keys])
		# print valueTemp

		# if valueTemp == 293:
			# " testing purpose "
			# print keys
		valueLog = float( float(NumberOfDocuments) / valueTemp)
		valueIDF = math.log(float(valueLog))
		# global dictInverseDocumentFrequency
		dictInverseDocumentFrequency[keys] = float(valueIDF)

	# print dictInverseDocumentFrequency['inc']
	
	# adding artificial word " < U N K > "
	dictInverseDocumentFrequency["< U N K >"] = float(math.log(float(NumberOfDocuments)))

	return dictInverseDocumentFrequency


# Question 2.1 c)
def get_tfidf_top( dict1, dict2, k ):
	" get list of top k terms with highest tf-idf values "
	# dict1 = dictTermNormalizedFrequency 
	# dict2 = dictInverseDocumentFrequency
	dictTempTFIDF = {}
	listTermsBasedTFIDF = []
	default = 0.0
	# valueTempTFIDF = 1.0
	for keys in dict1.keys():
		" keys in dictTermNormalizedFrequency "
		valueTempTFIDF = 0.0
		checkLoopFlag = 0
		if(keys in dict2.keys()): 
			" for calculating TF-IDF values "
			checkLoopFlag = 1
			valueTempTFIDF = float ( float(dict1[keys]) * float(dict2[keys]))
			dictTempTFIDF[keys] = valueTempTFIDF 
		if(checkLoopFlag == 0):
			" if key in TF is not in IDF "
			# valueTempTFIDF = 0.0
			dictTempTFIDF[keys] = 0.0;
	
	# print dictTempTFIDF
	
	# for sorting dictionary based on values
	listSortedTFIDF = []
	for key, value in sorted(dictTempTFIDF.iteritems(), key=operator.itemgetter(1)):
		# print key, ':', value
		listSortedTFIDF.append(key)

	# for getting list in descending order
	listSortedTFIDF.reverse()
	# print len(listSortedTFIDF)
	# print listSortedTFIDF
	
	return listSortedTFIDF[:k]


# Question 2.2 a)
def get_mi_top ( bg_terms, topic_terms, k ):
	" Function to get list of k terms with highest MI values"
	dictTempMI = {}
	lenTopic_Terms = float(len(topic_terms))
	lenBG_Terms = float(len(bg_terms))
	for term in topic_terms:
		" to get MI values of terms in topic_terms "
		if dictTempMI.has_key(term):
                                continue
		if ( bg_terms.count(term) >= 5):
			" run only if word appears more than 5 times in a cluster"
			pTopic = float(topic_terms.count(term))/lenTopic_Terms
			# print "pTopic:",pTopic
			pBG = float(bg_terms.count(term))/lenBG_Terms
			# print "pBG:",pBG
			miTerms = math.log(float(pTopic)/float(pBG))
			# print "miTerms:",miTerms
		
			if( miTerms < 0 ):
				" to change negative values to zero "
				miTerms  = 0
			dictTempMI[term] = miTerms	

	# print dictTempMI
	# print len(dictTempMI)
	 
	# for sorting dictionary based on values
        listSortedMI = []
	# listTest = []
        for key, value in sorted(dictTempMI.iteritems(), key=operator.itemgetter(1)):
                # print key, ':', value
                listSortedMI.append(key)
		# listTest.append(value)

        # for getting list in descending order
        listSortedMI.reverse()
	# listTest.reverse()
	
	# print listTest

	return listSortedMI[:k]

# Question 2.2 b)
def write_mi_weights ( directory,outfilename):
	" Function to write MI values in a file"
	# to get terms in starbucks
	termsStarbucks = load_collection_tokens (directory)
	
	# to get terms in corpus
	termsCorpus = load_collection_tokens ("/home1/c/cis530/hw1/data/corpus")
	
	dictMI = {}
        lenTopic = float(len(termsStarbucks))
        lenCorpus = float(len(termsCorpus))
        for term in termsStarbucks:
                " to get MI values of terms in termsStarbucks "
                if dictMI.has_key(term):
                                continue
		if ( termsCorpus.count(term) >= 5 ):
                        " run only if word appears more than 5 times in a corpus"

	        	pTopic = float(termsStarbucks.count(term))/lenTopic
        	        pCorpus = float(termsCorpus.count(term))/lenCorpus
	
        	        miTerms = math.log(float(pTopic)/float(pCorpus))

                	if( miTerms <= 0 ):
                        	" to remove 0 or  negative values "
                        	continue
                	dictMI[term] = miTerms
	# print dictMI

	file_Starbucks = open(outfilename,"w")
	for keys in dictMI.keys():
		" for writing in file "
		file_Starbucks.write("<" + keys + "\t" + str(dictMI[keys]) + ">" + "\n")
	file_Starbucks.close()
	return 


# Question 2.3

def intersect ( L_1, L_2 ):
	" Function to calculate Intersection of listSortedMI and listSortedTFIDF "
	# print " Intersection "
	# print list( set(L_1) & set(L_2) )
	return list( set(L_1) & set(L_2) )
	 

def get_precision (L_1, L_2):
	"Function to calculate Precision "
	intersectList = intersect ( L_1, L_2 )
	# print intersectList
	lenIntersect = float ( len(intersectList) )
	lenL_1 = float ( len(L_1) )
	precision = 0.0
	# print lenIntersect 
	# print lenL_1
	precision = lenIntersect / lenL_1
	# print precision
	return precision

def get_recall (L_1 , L_2):
	" Function to calcuate Recall "
	intersectList = intersect ( L_1, L_2 )
	# print intersectList
        lenIntersect = float ( len(intersectList) )
        lenL_2 = float ( len(L_2) )
        recall = 0.0
	# print lenIntersect 
	# print lenL_2 
        recall = lenIntersect / lenL_2
	# print recall 
	return recall


def get_fmeasure ( L_1, L_2 ):
	" Function to calculate Fmeasure "
	precision = float (get_precision (L_1, L_2))
	recall = float(get_recall ( L_1, L_2))
	numerator = float ( 2 * precision * recall )
	denominator = float ( precision + recall )
	if( denominator <> 0 ):
		fmeasure = numerator / denominator
	else :
		# print " FMeasure cannot be calculated "
		fmeasure = 0.0
	return fmeasure

# Question 3 a)
def read_brown_cluster():
	" Function to store cluster file as dictionary "
	fileBrownCluster = "/home1/c/cis530/hw1/data/brownwc.txt"
	fileBrown = open (fileBrownCluster , "r")
	dictTempBrownCluster = {}
	countLines = 0
	for lines in fileBrown:
		strReadLine =str (lines)
		# print "New Line:", strReadLine	
		listNewLine = strReadLine.split("	")
		# print listNewLine
		dictTempBrownCluster[str(listNewLine[1])] = str(listNewLine[0])
	fileBrown.close()
	# print dictTempBrownCluster
	# print len(dictTempBrownCluster)
	return dictTempBrownCluster


# Question 3 b)
def load_file_clusters ( filepath , bc_dict ):
	" Function to return list of cluster ids correspond to token in filepath "
	listToken_Cluster = []
	listToken_Cluster = load_file_tokens(filepath)
	listClusterIDs = []
	for keys in bc_dict.keys():
		" For matching only for words in cluster dictionary "
		if ( keys in listToken_Cluster):
			listClusterIDs.append(bc_dict[keys])
	return listClusterIDs


# Question 3 c)
def load_collection_clusters ( directory , bc_dict ):
	" Function to return list of cluster ids correspond to tokens in all files in a directory "
	listDirClusterIDs = []
	
	# to get list in starbucks
        listStarbucks = load_collection_tokens (directory)

	for keys in bc_dict.keys():
		" For matching only for words in cluster dictionary "
		if ( keys in listStarbucks):
			listDirClusterIDs.append(bc_dict[keys])
	return listDirClusterIDs 


# Question 3 d)
def get_idf_clusters ( bc_dict ):
	" Function to get directory of IDF values for each cluster id in all_data "

	# as of now ... calculating on smaller data corpus/starbucks

	directoryAllData = "/home1/c/cis530/hw1/data/corpus/starbucks"

	listAllClusterIDs_2D = []
        # to create 2D list 
	global aakritis_listAllFiles
        aakritis_listAllFiles = []
        aakritis_listAllFiles = get_Files_AllDirectories( directoryAllData )

        for files in aakritis_listAllFiles:
                " To fetch tokens file wise into 2D list based on cluster ids"
                listTemp = load_file_clusters ( files , bc_dict )
                # to create a 2D list - function append
                listAllClusterIDs_2D.append(listTemp)
                listTemp = []
	
	# print listAllClusterIDs_2D
	# print len (listAllClusterIDs_2D)

	# call calculate IDF function to calculate IDF
	dictIDF_Cluster = get_idf(listAllClusterIDs_2D)
	
	return dictIDF_Cluster

# Question 3 e)

def get_tf_clusters ( bc_dict ):
	" Function to get directory of TF values for cluster ids in starbucks "
	
	directoryStarbucks =  "/home1/c/cis530/hw1/data/corpus/starbucks"

        listAllClusterIDs = []
	dictTF_Cluster = {}

        global aakritis_listAllFiles
        aakritis_listAllFiles = []
        aakritis_listAllFiles = get_Files_AllDirectories( directoryStarbucks )

        for files in aakritis_listAllFiles:
                " To fetch tokens file wise into 2D list based on cluster ids"
                listTemp = load_file_clusters ( files , bc_dict )
                listAllClusterIDs.extend(listTemp)
                listTemp = [] 

	dictTF_Cluster = get_tf ( listAllClusterIDs )
	return dictTF_Cluster

def get_tfidf_Clusters( dict1, dict2 ):
        " get list of top k terms with highest tf-idf values "
        # dict1 = dictTF_Cluster_TFIDF
        # dict2 = dictIDF_Cluster_TFIDF
        dictTempTFIDF = {}
        listTermsBasedTFIDF = []
        default = 0.0
        # valueTempTFIDF = 1.0
        for keys in dict1.keys():
                " keys in dictTermNormalizedFrequency "
                valueTempTFIDF = 0.0
                checkLoopFlag = 0
                if(keys in dict2.keys()):
                        " for calculating TF-IDF values "
                        checkLoopFlag = 1
                        valueTempTFIDF = float ( float(dict1[keys]) * float(dict2[keys]))
                        dictTempTFIDF[keys] = valueTempTFIDF
                if(checkLoopFlag == 0):
                        " if key in TF is not in IDF "
                        # valueTempTFIDF = 0.0
                        dictTempTFIDF[keys] = 0.0;
	return dictTempTFIDF


def write_tfidf_weights ( directory, outfilename, bc_dict ) :
	" For writing TF IDF values in outfile "	
	
	dictTFIDF_Cluster = {}
	
	# complete code for below ....
	
	dictTF_Cluster_TFIDF = get_tf_clusters ( bc_dict )
	dictIDF_Cluster_TFIDF = get_idf_clusters ( bc_dict )

	# to calculate TF IDF 
	
	# pass value of k as NA to show that k is not required 
	
	dictTFIDF_Cluster  = get_tfidf_Clusters( dictTF_Cluster_TFIDF, dictIDF_Cluster_TFIDF)
        
	# dict1 = dictTF_Cluster_TFIDF
        # dict2 = dictIDF_Cluster_TFIDF
	
	# print dictTFIDF_Cluster 
	# print len ( dictTFIDF_Cluster )
	
	file_Starbucks_Cluster = open(outfilename,"w")
        for keys in dictTFIDF_Cluster.keys():
                " for writing in file "
                file_Starbucks_Cluster.write("<" + keys + "\t" + str(dictTFIDF_Cluster[keys]) + ">" + "\n")
        file_Starbucks_Cluster.close()

	return

# Question 4.1 a)

def create_feature_space ( list ):
	" Function to create dictionary keys : cluster id and values : vector component "
	dictFeatureSpace = {}
	iVal = 0
	for listVal in list:
		if ( dictFeatureSpace.has_key ( listVal )) : 
			continue
		dictFeatureSpace[listVal ] = iVal
		iVal = iVal + 1
	return dictFeatureSpace 
 
# Question 4.1 b)

def vectorize ( feature_space , lst ):
	" Funcion to return the list of 0's and 1's "
	listVectorSpace = []
	
	# initializing listVectorSpace to 0 
	for iLoop in range (0, len(feature_space)):
		listVectorSpace.append(0)

	for keys in feature_space.keys():
		if ( keys in lst ) :
			listVectorSpace[feature_space[keys]] = 1
		else :
			listVectorSpace[feature_space[keys]] = 0
	return listVectorSpace

# Question 4.2 

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

# Question 4.3 a)
def rank_doc_sim ( rep_file, method, test_path, bc_dict ):
	" Function to return list of tuples ( doc_base_name, similarity ) in decreasing order "
	listDoc_Tuples = []
	listDoc_TuplesSorted = []
	# Step 1 : reading rep_file line wise to create two lists 
	fileRep = open (rep_file , "r")
        # dictTempBrownCluster = {}
	listWordClust_Rep = []
	listValues_X_Rep = []
        countLines = 0
        for lines in fileRep:
		listNewLine = []
                strReadLineTemp =str (lines)
		# remove <> from strReadLine
		lenStr = len (strReadLineTemp)
		strReadLine = strReadLineTemp [1 : (lenStr-2)]
		
		# print strReadLineTemp
		# print strReadLine
		

                # print "New Line:", strReadLine        
                listNewLine = strReadLine.split("\t")
                
		# print listNewLine
		
		listWordClust_Rep.append(listNewLine[0])
		listValues_X_Rep.append(float(listNewLine[1]))
	
	fileRep.close()

	# create feature space
	
	dictFeatureSpace_Rank = create_feature_space ( listWordClust_Rep)
	
	# to get all files from test_path
	
	global aakritis_listAllFiles
        aakritis_listAllFiles = []
        
        # global listAllFiles 
        aakritis_listAllFiles = get_Files_AllDirectories( test_path )
        listTokens_TestPath = []
	for files in aakritis_listAllFiles:
                " To fetch tokens for vectorize function "
		fileName_Test = ""
		if( method == "TF-IDF"):
			listTokens_TestPath = load_file_clusters ( files , bc_dict )
			
		elif ( method == "MI"):                
			listTokens_TestPath = load_file_tokens( files )
        
		# got list of words / clusters to pass to vectorize function
		print listTokens_TestPath 


		listValues_Y = vectorize ( dictFeatureSpace_Rank , listTokens_TestPath )

		# calculate Cosine Similarity 
		floatCosineSim_Test = cosine_similarity ( listValues_X_Rep , listValues_Y )

		print "Cosine Similarity for : ", files 
		print floatCosineSim_Test
		listFName = []
		# split function for fileName 
		# to fetch relative paths
		listFName = files.split("/")
                count = len(listFName)
                fileName_Test = str(listFName[count-1])

		tempTup = ( fileName_Test , float(floatCosineSim_Test))
		
		listDoc_Tuples.append(tempTup)

	# sorting of list based on Cosine Values 

	listDoc_TuplesSorted = sorted(listDoc_Tuples, key=operator.itemgetter(1))
	
	# to sort in decreasing order

	listDoc_TuplesSorted.reverse()
	
	return listDoc_TuplesSorted 


# Question 4.3 b)
def write_result_file ( list_Tuples):
	" Function to write Precision values for MI and TF-IDF"

	# fetch top 100 for numerator 
	list_Tuples_Top = list_Tuples[:100]

	countDocNum = 0
	countDocDenom = 0

	precision = 0.0

	# for loop to count documents for numerator 

	for word,val in list_Tuples_Top :
		if( "starbucks" in word.lower()):
			countDocNum = countDocNum + 1

	# print " Numerator : ", countDocNum 
	
	# for loop to count documents for denominator
	
	for word,val in list_Tuples :
		if ( "starbucks" in word.lower()):
			countDocDenom = countDocDenom + 1

	# print "Denominator : ", countDocDenom

	precision = float(countDocNum)/float(countDocDenom)
	
	# print "Precision : ", precision 
	
	# to write data to result.txt
	# open file in append mode
        file_Result = open("results.txt","a")
        # for writing in file
        file_Result.write("<" + " " + "precision" + "-" + str(precision) + " " + ">" + " " + "\n")
        file_Result.close()

	return 



def main () :
	"implementation of main calling function"

	# Question 1 a)
	listFiles = get_all_files("/home1/c/cis530/hw1/data/corpus")
	# No need for global declaration to read values of listFiles

	# UNCOMMENT
	print "1 a)"
	# print listFiles # 1 a) list of relative file paths for all files in input directory

	
	# Question 1 b)
	# picking random file name from the given list
	listTokens = load_file_tokens("/home1/c/cis530/hw1/data/corpus/qualcomm/3055013.txt")

	# UNCOMMENT
	print "1 b)"
	# print listTokens # b) a list of words (converted to lower-case) in filepath


	# Question 1 c)
	listAllWords = load_collection_tokens ("/home1/c/cis530/hw1/data/corpus")

	# UNCOMMENT
	print "1 c)"
	# print listAllWords # c) a list of all tokens (converted to lower-case) from all files in directories
	# print len(listAllWords)


	# Question 2.1 a)
	dictTermNormalizedFrequency = get_tf(listAllWords)

	# UNCOMMENT
	print "2.1 a)"
	# print dictTermNormalizedFrequency # 2.1 a) get dictionary with normalized term frequency

	# count5 = len(dictTermNormalizedFrequency)
	# print "Normalized Frequency", count5

	# Question 2.1 b)
	listAllWords_2D = create_itemList()


	# print listAllWords_2D # Getting 2D list of items 

	# print len (listAllWords_2D)

	dictInverseDocumentFrequency = get_idf(listAllWords_2D)

	print "2.1 b)"
	# print dictInverseDocumentFrequency # 2.1 b) get dictionary with idf

	# print len (dictInverseDocumentFrequency)


	listSortedTFIDF = get_tfidf_top( dictTermNormalizedFrequency, dictInverseDocumentFrequency, 50) # Behaves as L_2

	# UNCOMMENT
	# print listSortedTFIDF # 2.1 c) get Sorted TF-IDF key list 


	# Question 2.2 a)
	# global listAllFiles 
	# listAllFiles = []
	topic_terms = load_collection_tokens ("/home1/c/cis530/hw1/data/corpus/starbucks")

	# global listAllFiles
	# listAllFiles = []
	bg_terms = load_collection_tokens ("/home1/c/cis530/hw1/data/corpus")

	# print len(topic_terms)
	# print len(bg_terms)

	listSortedMI = get_mi_top (bg_terms,topic_terms,100)	# Behaves as L_1

	# UNCOMMENT
	print "2.2 a)"
	# print listSortedMI # 2.2 a) get Sorted MI key list


	# Question 2.2 b)
	filename = "starbucks_mi_weights.txt"
	directory_path = "/home1/c/cis530/hw1/data/corpus/starbucks"

	write_mi_weights(directory_path,filename)


	# Question 2.3

	# for sorting dictionary based on values # dictTermNormalizedFrequency
	listSortedTemp = []
	# listTest = []
	for key, value in sorted(dictTermNormalizedFrequency.iteritems(), key=operator.itemgetter(1)):
		# print key, ':', value
		listSortedTemp.append(key)
        	# listTest.append(value)

	# for getting list in descending order
	listSortedTemp.reverse()
	# listTest.reverse()

	# print listTest
	listSortedNormalizedFrequency = listSortedTemp[:100] # for fetching 100 top values for List L3


	##  print MI Values
	print "For Mutual Information "
	precision_MI = get_precision ( listSortedMI , listSortedTFIDF )
	print "Precision :", precision_MI

	recall_MI = get_recall ( listSortedMI , listSortedTFIDF )
	print "Recall :",recall_MI

	fmeasure_MI = get_fmeasure ( listSortedMI , listSortedTFIDF )
	# print "FMeasure :",fmeasure_MI


	## print TF Values
	print "For Normalized TF Values "
	precision_TF = get_precision ( listSortedNormalizedFrequency , listSortedTFIDF )
	print "Precision :",precision_TF


	recall_TF = get_recall ( listSortedNormalizedFrequency , listSortedTFIDF )
	print "Recall :",recall_TF

	fmeasure_TF = get_fmeasure ( listSortedNormalizedFrequency , listSortedTFIDF )
	# print "FMeasure :",fmeasure_TF


	## to write data to results.txt
	file_Result = open("results.txt","w")
	# for writing in file
	file_Result.write("<" + " " + "precision" + "-" + str(precision_MI) + " " + ">" + " " +  "," + " " + "<" + " " + "recall" + "-" + str(recall_MI) + " " + ">" + "\n") 
	file_Result.write("<" + " " + "precision" + "-" + str(precision_TF) + " " + ">" + " " +  "," + " " + "<" + " " + "recall" + "-" + str(recall_TF) + " " + ">" + "\n")
	file_Result.close()


	# Brown Cluster Path 
	# Question 3 a)
	
	# fileBrownCluster = "/home1/c/cis530/hw1/data/brownwc.txt"
	# fileBrown = open(fileBrownCluster,"r")
	# print fileBrown.read()
	# fileBrown.close()
	

	dictBrownCluster = read_brown_cluster()
	# UNCOMMENT
	print "3 a)"
	# print dictBrownCluster # 3 a) dictionary with Brown CLuster values
	# print len(dictBrownCluster)


	# Question 3 b)
	filePath = "/home1/c/cis530/hw1/data/corpus/starbucks/3012977.txt"
	# listToken_Cluster = load_file_tokens(filePath)
	if os.path.isfile( filePath ):
		listClusterIDs = load_file_clusters ( filePath , dictBrownCluster )
	else:
		listClusterIDs = []
		# print " File Not Found "

	# UNCOMMENT 
	print "3 b)"
	# print listClusterIDs 	# 3 b) for getting list of cluster ids 
	# print len(listClusterIDs)


	# Question 3 c)
	directoryPath_Cluster = "/home1/c/cis530/hw1/data/corpus/starbucks"
	listDictClusterIDs = load_collection_clusters ( directoryPath_Cluster , dictBrownCluster )

	# UNCOMMENT 
	print "3 c)"
	# print listDictClusterIDs  # 3 c) for getting list of cluster ids for whole directory
	# print len ( listDictClusterIDs )


	# Question 3 d)
	dictIDF_Cluster = get_idf_clusters ( dictBrownCluster )

	# UNCOMMENT 
	print "3 d)"
	# print dictIDF_Cluster  # 3 d) for getting IDF values for cluster ids in all_data 
	# print len( dictIDF_Cluster)



	# Question 3 e)

	filename_Cluster = "starbucks_tfidf_weights.txt"
	directory_ClusterPath = "/home1/c/cis530/hw1/data/corpus/starbucks"

	write_tfidf_weights(directory_ClusterPath,filename_Cluster, dictBrownCluster)

	# Question 4.1 a)

	# recall functions if require different input value 
	dictFeatureSpace = create_feature_space (listDictClusterIDs)
	
	print "4.1 a)"
	# print dictFeatureSpace
	
	# print len (dictFeatureSpace)

	# Question 4.1 b)
	
	# feature space on starbucks 
	# lst on any document from database # recall functions if require different input value 
	listVectorSpace = vectorize ( dictFeatureSpace , listClusterIDs )
	
	print "4.1 b)"
	# print listVectorSpace

	# Question 4.2 
	
	# list of vector spaces 
	# 	1. listVectorSpace
	# 	2. rerun 3 b) with different file name 
	
	filePath_Vector = "/home1/c/cis530/hw1/data/corpus/starbucks/3019993.txt"
	if os.path.isfile( filePath_Vector ):
		# print " cosine similarity "
		listClusterIDs_2 = load_file_clusters ( filePath_Vector , dictBrownCluster )
		listVectorSpace_2 = vectorize ( dictFeatureSpace , listClusterIDs_2 )
		floatCosineSim = cosine_similarity ( listVectorSpace , listVectorSpace_2 )
		
		print "4.2"
		# print floatCosineSim 

	else :
		floatCosineSim = 0.0
		# print " File Not Found "
	
	# Question 4.3 a)

	# rep_file = "/mnt/castor/seas_home/a/aakritis/starbucks_tfidf_weights.txt"  
	# try using only file name
 
	# rep_file = "starbucks_tfidf_weights.txt" 
	# method = "TF-IDF"
	# test_path = "/home1/c/cis530/hw1/data/mixed"
	# bc_dict = dictBrownCluster
	
	# run for TF-IDF values
	listDoc_Tuples_TFIDF = rank_doc_sim ( "starbucks_tfidf_weights.txt", "TF-IDF", "/home1/c/cis530/hw1/data/mixed", dictBrownCluster)
	
	# run for MI values
	listDoc_Tuples_MI = rank_doc_sim ( "starbucks_mi_weights.txt", "MI", "/home1/c/cis530/hw1/data/mixed", dictBrownCluster)

	print "4.3 a)"
	# print listDoc_Tuples_TFIDF

	print listDoc_Tuples_MI

	# Question 4.3 b) 

	print "4.3 b)"
	write_result_file ( listDoc_Tuples_MI )
	
	write_result_file ( listDoc_Tuples_TFIDF )
	
	return 

if __name__ == "__main__":
	main ()

