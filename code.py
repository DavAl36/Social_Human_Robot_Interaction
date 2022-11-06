import speech_recognition as sr
from os import system
from pycorenlp import StanfordCoreNLP
import pprint


def search_dict(where,type,what): #type = pos,lemma,token,...  what = word
    source = where
    length = len(source)
    del output_list[:]
    flag = False
    for indx in range(0, length):
            if(source[indx][type] == what):
                flag = True
                output_list.append(source[indx]['word'].lower())
    return flag 

def audioToText():

    r = sr.Recognizer()
    m = sr.Microphone()
    value = ""
    with m as source:
        r.adjust_for_ambient_noise(m, 1) # listen for 1 second to calibrate the energy threshold for ambient noise levels
        print("······Listening.")
        audio = r.listen(source)
        print("······Found something")
    try:
        Interpretation = r.recognize_google(audio)
        print("······Google Speech Recognition: " + Interpretation.upper())
        file.write("Human: " + Interpretation + "\n") 
    except sr.UnknownValueError:
        Interpretation = "Error I have not understood "
        print("······Google Speech Recognition: " + Interpretation.upper())
        file.write("[ERROR]Google Speech Recognition: " + "I didn't understand the sentence" + "\n") 
    except sr.RequestError as e:
        Interpretation = "Error {0}".format(e)
        print("······Google Speech Recognition: " + Interpretation.upper())
        file.write("[ERROR]Google Speech Recognition: " + "I didn't understand the sentence" + "\n") 
    return Interpretation

def NLP(phrase):
    nlp = StanfordCoreNLP('http://localhost:9000')
    output = nlp.annotate(phrase, properties={
        'annotators': 'tokenize, ssplit, pos, lemma ',
        'pipelineLanguage': 'en',
        'outputFormat': 'json'
    })
    return output



env = range(1,49) 
obstacles = [4,5,7,14,21,18,22,23,24,25,34,39,40,46,8,29,44,49] 
learnedList = []

output_list = [] 
currentPos = 5 # starting position
path = "/home/dav/Scrivania/Shri Project/"
file = open(path + "dialog.txt","w") 
end = False
something = False
objectList = []
currentRow = 1
currentCol = 6
row = 1
col = 6

print("Tell me something")
file.write("Agent: " + "Tell me something" + "\n") 
system('say ' + "Tell me something")


while (end == False):
    text  = audioToText()
    
    output = NLP(text)
    root = output['sentences'][0]['tokens']
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(output)

    if(search_dict(root,'pos','VB') or search_dict(root,'pos','VBZ') or search_dict(root,'pos','VBP')):# Check Verbs POS
        print("Check: VB, VBZ, VBP")
        if( ("walk" in output_list) or ("move" in output_list) or ("go" in output_list)   ):# Check Verbs
            print("----Check: walk,move,go")
            if(search_dict(root,'pos',',') and search_dict(root,'pos','CD') ):# Check Position Numbers POS
                print("--------Check CD")
                currentPos = 7*(int(output_list[0])-1)+ int(output_list[1]) 
                if(currentPos in obstacles):#Check if it is an obstacle 
                    print("------------OBSTACLE!") 
                    system('say ' + "OUCH! There is an obstacle in position " + output_list[0] + ", " + output_list[1] + ", therefore, I will stand still")
                    file.write("Agent: " + "OUCH! There is an obstacle in position " + output_list[0] + ", " + output_list[1] + ", therefore, I will stand still" + "\n") 
                    something = True
                else:
                    currentRow = int(output_list[0])
                    currentCol = int(output_list[1])
                    print("------------Movement OK!") 
                    print("------------Now I am in position " + output_list[0] + ", " + output_list[1] )
                    system('say ' + "Now I am in position " + output_list[0] + ", " + output_list[1])
                    file.write("Agent: " + "Now I am in position " + output_list[0] + ", " + output_list[1] + "\n") 
                    something = True

        if( search_dict(root,'word','are') ):# Check Verbs
            print("----Check: are ")
            if( search_dict(root,'pos','PRP') ):# Check "you"
                print("--------Check: PRP")
                something = True
                print("--------I am in position " + str(currentRow) + ", " + str(currentCol))
                system('say ' + "I am in position " + str(currentRow) + ", " + str(currentCol) )
                file.write("Agent: " + "I am in position " + str(currentRow) + ", " + str(currentCol) + "\n")                 

        if( search_dict(root,'word','is') ):# Check Verbs
            print("----Check: is ")
            if( search_dict(root,'pos','WRB') and search_dict(root,'word','where') ):
                print("--------Check: WRB ")
                if( search_dict(root,'pos','NN') ):
                    print("------------Check: NN ")
                    objectName = output_list[0]
                    print("------------objectName: " + str(objectName) )
                    for element in learnedList:
                        for w in element.strip().split():
                            if(w == objectName):
                                something = True
                                system('say ' + element )
                                file.write("Agent: " + element + "\n") 
        #LEARN BLOCK        
            if( search_dict(root,'pos','EX')):# check there
                print("--------Check EX ")
                if( search_dict(root,'pos','NN')):
                    print("------------Check NN ")
                    objectLearned = output_list[0]
                    objectList.append(objectLearned)
                    flag1 = False
                    while(flag1 == False):
                        system('say ' + "Tell me the right orientation")
                        file.write("Agent: " + "Tell me the right orientation" + "\n") 
                        print("----------------Tell me the right orientation")
                        text  = audioToText()
                        output = NLP(text)
                        root = output['sentences'][0]['tokens']
                        #pp.pprint(output)
                        if(search_dict(root,'pos','RB') or search_dict(root,'pos','NN')):
                            print("--------------------Check: RB,NN ")
                            row = int(currentRow)
                            col = int(currentCol)
                            if( search_dict(root,'word','up') or search_dict(root,'word','top')):
                                print("------------------------Check: up,top")
                                something = True
                                row = int(currentRow)-1
                                system('say ' + "There is a "+ objectLearned + " in position " + str(row) + ", " + str(col))
                                file.write("Agent: " + "There is a "+ objectLearned + " in position " + str(row) + ", " + str(col) + "\n")
                                learnedList.append("There is a "+ objectLearned + " in position " + str(row) + ", " + str(col))
                                flag1 = True
                                break
                            if( search_dict(root,'word','right')):
                                print("------------------------Check: right")
                                something = True
                                col = int(currentCol)+1
                                system('say ' + "There is a "+ objectLearned + " in position " + str(row) + ", " + str(col))
                                file.write("Agent: " + "There is a "+ objectLearned + " in position " + str(row) + ", " + str(col) + "\n")
                                learnedList.append("There is a "+ objectLearned + " in position " + str(row) + ", " + str(col))
                                flag1 = True
                                break
                            if( search_dict(root,'word','left')):
                                print("------------------------Check: left")
                                something = True
                                col = int(currentCol) - 1
                                system('say ' + "There is a "+ objectLearned + " in position " + str(row) + ", " + str(col))
                                file.write("Agent: " + "There is a "+ objectLearned + " in position " + str(row) + ", " + str(col) + "\n")
                                learnedList.append("There is a "+ objectLearned + " in position " + str(row) + ", " + str(col))
                                flag1 = True
                                break
                            if( search_dict(root,'word','bottom') or search_dict(root,'word','down')):
                                print("------------------------Check: bottom,down")
                                something = True
                                row = int(currentRow)+1
                                system('say ' + "There is a "+ objectLearned + " in position " + str(row) + ", " + str(col))
                                file.write("Agent: " + "There is a "+ objectLearned + " in position " + str(row) + ", " + str(col) + "\n")
                                learnedList.append("There is a "+ objectLearned + " in position " + str(row) + ", " + str(col))
                                flag1 = True
                                break


    if( search_dict(root,'pos','WRB') ):# how
        print("Check: WRB ")
        if( search_dict(root,'pos','VB') ): # check verb 
            print("----Check: VB ")
            if(("feel" in output_list)):
                if( search_dict(root,'pos','PRP') ):# Check "you"
                    something = True
                    print("--------Check: PRP")
                    system('say ' + "When I talk to someone I am always fine" )
                    print("--------When I talk to someone I am always fine")
                    file.write("Agent: " + "When I talk to someone I am always fine" + "\n") 

    #REQUEST BLOCK
    if( ( search_dict(root,'pos','WDT') or search_dict(root,'pos','WRB') ) and (search_dict(root,'pos','NN') or search_dict(root,'pos','NNS')) ):# (which or how) and word Objects/ Object
        print("Check: WDT,WRB and NN,NNS ")
        if( search_dict(root,'pos','VB') ): # check verb 
            print("----Check: VB ")
            if(len(learnedList) == 0): # if agen't didn't learn anything
                something = True
                system('say ' + "I have not learned anything yet" )
                print("--------I have not learned anything yet")
                file.write("Agent: " + "I have not learned anything yet" + "\n")
            else:
                if( ("know" in output_list) ): #if previous verb is "know"
                    if( search_dict(root,'pos','JJ') and search_dict(root,'word','many')):#how many object do you know?
                        print("----------------Check: JJ ")
                        something = True
                        nOb = len(learnedList)
                        if( nOb == 1):
                            system('say ' + "I know only 1 object" )
                            print("--------------------I know only 1 object")
                            file.write("Agent: " + "I know only 1 object" + "\n") 
                        else:
                            system('say ' + "I know " + str(nOb) + " objects" )
                            print("--------------------I know " + str(nOb) + " objects")
                            file.write("Agent: " + "I know " + str(nOb) + " objects" + "\n")                                   
                    else:# Which objects do you know
                        something = True
                        system('say ' + "I know :" + str(objectList))
                        print("----------------I know :" + str(objectList))
                        file.write("Agent: " + "I know :" + str(objectList) + "\n")
    
    #CLOSE BLOCK
    if(search_dict(root,'pos','NN') and (search_dict(root,'word','goodbye') ) ): #Close Session
        print("Check: NN ")
        something = True
        end = True
        speechText = "See you later, bye,bye "
        system('say ' + speechText)
        file.write("Agent: " + speechText + "\n")
    if(something == False):
        system('say ' + "I do not understand, please ask me something else")
        print("I do not understand, please ask me something else")
        file.write("Agent: " + "I do not understand, please ask me something else" + "\n")
    something = False



print("End")
print(learnedList)
file.close() 

