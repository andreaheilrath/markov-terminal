# from nltk.tokenize import WhitespaceTokenizer
from collections import Counter
import random
from termcolor import colored
import os
import pickle


class markov_terminal:

    def __init__(self, corpus):
        self.head = ""
        if os.path.exists('trigrams.pkl'):
            self.dump = open("trigrams.pkl", mode="rb")
            self.trigrams = pickle.load(self.dump)
            self.dump.close()

        else:
            self.trigrams = {}
            self.add_trigrams(self.tokens_from_file(corpus))

        self.log = open("log.txt", mode="a")
        self.running = True

    def tokens_from_file(self, file_name="corpus.txt"):
        text_file = open(file_name, mode='tr', encoding="utf-8")
        corpus = text_file.read()
        text_file.close()
        return corpus.split()

    def add_trigrams(self, tokens):
        if self.head:
            tokens.insert(0, self.head.split()[1])
            tokens.insert(0, self.head.split()[0])
        for i in range(len(tokens)-2):
            self.trigrams.setdefault(tokens[i] + " " + tokens[i+1], []).append(tokens[i+2])

    def start_sentence(self):
        max_iterations = 20
        if not self.head in list(self.trigrams.keys()):
            for i in range(max_iterations):
                self.head = random.choice(list(self.trigrams.keys()))
                if self.head[0] == "~":
                    return self.head
            return self.head
        for i in range(max_iterations):
            stats = Counter(self.trigrams[self.head])
            for j in range(max_iterations):
                word = random.choices(list(stats.keys()), list(stats.values()))[0]
                if word[0] == "~":
                    try:
                        stats = Counter(self.trigrams[self.head.split()[1] + " " + word])
                        tail = random.choices(list(stats.keys()), list(stats.values()))[0]
                        return word + " " + tail
                    except:
                        pass
            self.head = self.head.split()[1] + " " + random.choices(list(stats.keys()), list(stats.values()))[0]

    def talk(self, min_words=3, sentences=2):
        if not self.head:
            self.head = random.choice(list(self.trigrams.keys()))

        for s in range(sentences):
            self.head = self.start_sentence()
            sentence = self.head + " "
            word_count = 3
            end_of_sentence = False
            while not end_of_sentence:
                stats = Counter(self.trigrams[self.head])
                tail = random.choices(list(stats.keys()), list(stats.values()))[0]
                if tail[-1] == "~":
                    end_of_sentence = True
                    sentence += tail
                else:
                    sentence += tail + " "
                    word_count += 1
                self.head = " ".join(sentence.split()[-2:])

            self.log.write(sentence+'\n')
            print(colored(sentence[1:-1], 'green'))

    def listen(self):
        user_input = input()
        if user_input == "experimental stage project exit":
            self.running = False
        else:
            if user_input:
                self.log.write(user_input+'\n')
                user_input = "~" + user_input + "~"
                input_list = user_input.split()
                self.add_trigrams(input_list)
                self.head = " ".join(input_list[-2:])
                self.dump = open("trigrams.pkl", mode="wb")
                pickle.dump(self.trigrams, self.dump)
                self.dump.close()


    def conversation(self):
        os.system("stty intr ''")
        while(self.running):
            try:
                self.talk(sentences=1)
            except KeyError:
                pass
            #print(self.head)
            self.listen()
            #print(self.head)
        os.system("stty sane")




# =======================================================================================================================
# GLOBAL VARIABLES

mt = markov_terminal("corpus.txt")

# =======================================================================================================================
# MAIN PROGRAM

mt.conversation()
