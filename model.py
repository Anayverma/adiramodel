import PyPDF2 as pdf
import numpy as np
import nltk
import string
import random
import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def combine_pdfs(pdf_files):
    combined_text = ""
    for file_path in pdf_files:
        with open(file_path, 'rb') as file:
            pdf_reader = pdf.PdfReader(file)
            for page in pdf_reader.pages:
                text = page.extract_text()
                combined_text += text
    return combined_text

def adira(sentence):
    try:
        f = open('combined_text.txt', encoding='latin-1')  # Specify the encoding
        raw_doc = f.read()
        
        # Preprocessing
        raw_doc = raw_doc.lower()
        nltk.download('punkt')  # tokeniser
        nltk.download('wordnet')  # dictionary
        nltk.download('omw-1.4')
        sentence_tokens = nltk.sent_tokenize(raw_doc)
        word_tokens = nltk.word_tokenize(raw_doc)
        
        # Lemmatization
        lemmer = nltk.stem.WordNetLemmatizer()
        def LemTokens(tokens):
            return [lemmer.lemmatize(token) for token in tokens]
        
        remove_punc_dict = dict((ord(punct), None) for punct in string.punctuation)
        def LemNormalize(text):
            return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punc_dict)))
        
        # Define Greeting functions
        greet_inputs = ('hello', 'hi', 'namaste', 'satsriyakal')
        greet_responses = ('Hi', 'Hey', 'Hey There!', 'Namaste')
        def greet(sentence):
            for word in sentence.split():
                if word in sentence.split():
                    if word.lower() in greet_inputs:
                        return random.choice(greet_responses)
        
        # Generating response
        def response(user_response):
            robol_response = ''
            TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')  
            tfidf = TfidfVec.fit_transform(sentence_tokens)
            vals = cosine_similarity(tfidf[-1], tfidf)
            idx = vals.argsort()[0][-2]
            flat = vals.flatten()
            flat.sort()
            req_tfidf = flat[-2]
            if(req_tfidf == 0):
                robol_response = robol_response + "I am sorry. Unable to understand you!"
                return robol_response
            else:
                robol_response = robol_response + sentence_tokens[idx]
                return robol_response
        
        # Start conversation
        flag = True
        output = ""
        while(flag == True):
            user_response = sentence
            if(user_response != 'bye'):
                if(user_response == 'thank you' or user_response == 'thankyou' or user_response == 'thanks'):
                    flag = False
                    output += "You're welcome"
                else:
                    flag = False
                    if(greet(user_response) != None):
                        output += greet(user_response)
                    else:
                        sentence_tokens.append(user_response)
                        word_tokens = word_tokens + nltk.word_tokenize(user_response)
                        final_words = list(set(word_tokens))
                        response_text = response(user_response)
                        sentence_tokens.remove(user_response)
                        output += response_text
            else:
                flag = False
                output += "Good Bye"
        
        return output
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Call the adira function and store its return value in a variable
output = adira("hi")

# Return the output
print(output)
