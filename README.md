# Social Human Robot Interaction

The origin of HRI(Human Robot Interaction) as a discrete problem was stated by 20th-century author Isaac Asimov in 1941, in his novel I, Robot. He states the Three Laws of Robotics as:
- A robot may not injure a human being or, through inaction, allow a human being
to come to harm.
- A robot must obey any orders given to it by human beings, except where such
orders would conflict with the First Law.
- A robot must protect its own existence as long as such protection does not conflict
with the First or Second Law.
In this project an agent will take orders from an human through his voice and it will be able to answer his questions, it will be similar to a dialog between two people.

- Youtube: https://www.youtube.com/watch?v=9mpuaswQAcI

The adopted programming language is Python 3.7.6, with the help of some libraries such Speech Recognition, StanfordCoreNLP and System. The interaction
between the human and the agent has been the Spoken Interaction. The latter is based on a task-oriented dialog: the teacher can establish a real time conversation with the simulated agent, who is always listening. The human specifies all the needed requests and questions to the agent, able to understand the sentences, analyze them and perform the task. The first operation is the listening using the SpeechRecognition library; it uses the laptop microphone as input recognizer and translate the vocal message into a text message. It is implemented into the function audioToText which can return two messages: the possible correct translation of the sentence, or an error when can not recognize the sentence.The translation is possible thanks to the Automatic Speech Recognition engine,there are some of them: CMU Sphinx (works offline), Google Speech Recognition,Google Cloud Speech API. Wit.ai, Microsoft Bing Voice Recognition,Houndify API, IBM Speech to Text, Snowboy Hotword Detection (works offline), I tried some of them and I realized that the best for performance and reliability is Google Speech Recognition, even if it is clearly not perfect. After the implementation of this tool, a syntactic and semantic analysis on the words sequences has been performed by a dependency parser called Stanford CoreNLP, provided by a teamof Stanford University. This helps to achieve a useful representation of the sentence. Through functions, such as wordtokenize, pos, or dependencyparse, the agent is able to understand better the human sentences. The method that I used are:

- tokenize (tokenizes the text): This splits the text into roughly “words”, using
rules or methods suitable for the language being processed. Sometimes the tokens
split up surface words in ways suitable for further NLP-processing, for example
“isn’t” becomes “is” and “n’t”. The tokenizer saves the beginning and end char-
acter offsets of each token in the input text;

- ssplit: Splits a sequence of tokens into sentences;

- pos: Labels tokens with their POS tag;

- lemma: Generates the word lemmas for all tokens in the corpus.


<p align="center">
  <img src="https://user-images.githubusercontent.com/114728905/200168346-a5e9fbe1-e7b0-4a5b-8886-94308e31f4fc.png" width="600" />
  <img src="https://user-images.githubusercontent.com/114728905/200168342-110f0af8-9daf-4fcd-8396-ccca0b5dbee3.png" width="600" />
  <img src="https://user-images.githubusercontent.com/114728905/200168347-c7956999-adad-4901-a8e2-b4800a3e9329.png" width="600" />
</p>



Dialog Example:

Agent: Tell me something

Human: go to position 1, 1

Agent: Now I am in position 1, 1

Human: there is a table

Agent: Tell me the right orientation

Human: down

Agent: There is a table in position 2, 1

Human: go to position 6, 2

Agent: Now I am in position 6, 2

Human: there is a box

Agent: Tell me the right orientation

Human: down

Agent: There is a box in position 7, 2

Human: go to position 5, 2

Agent: Now I am in position 5, 2

Human: there is a painting

Agent: Tell me the right orientation

Human: left

Agent: There is a painting in position 5, 1

Human: go to position 7, 6

Agent: Now I am in position 7, 6

Human: there is a bike

Agent: Tell me the right orientation

Human: right

Agent: There is a bike in position 7, 7

Human: how many objects do you know

Agent: I know 4 objects

Human: which object do you know

Agent: I do not understand, please ask me something else

Human: which objects do you know

Agent: I know :['table', 'box', 'painting', 'bike']

Human: where is the table

Agent: There is a table in position 2, 1

Human: how do you feel

Agent: When I talk to someone I am always fine

Human: goodbye

Agent: See you later, bye,bye 
