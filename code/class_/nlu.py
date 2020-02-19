import spacy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from sklearn.preprocessing import OneHotEncoder
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential, load_model
from keras.layers import Dense, Bidirectional, Embedding, Dropout,BatchNormalization,LSTM
from keras.callbacks import ModelCheckpoint
import re
from sklearn.model_selection import train_test_split
from nltk.stem import WordNetLemmatizer
from googletrans import Translator
import pathconfig



paths = pathconfig.paths()
translator = Translator()

class Nlu:
    """
    This is a class with goals to call the natural language understanding. It is composed by
    six methods.
    """
    # get the slots from sentence
    def get_slots(self, sent):
        if self.language == 'en-GB':
            nlp = spacy.load("en_core_web_sm")
        elif self.language == 'it-IT':
            nlp = spacy.load("it_core_news_sm")
        doc = nlp(sent)
        return ([(X.text, [X.label_]) for X in doc.ents])

    #get the words from sentence
    def get_words_pos(self, sent):
        if self.language == 'en-GB':
            nlp = spacy.load("en_core_web_sm")
        elif self.language == 'it-IT':
            nlp = spacy.load("it_core_news_sm")
        doc = nlp(sent)
        list_sent = []
        for token in doc:
            list_text_pos = []
            list_text_pos.append(token.text)
            list_text_pos.append(token.pos_)
            list_sent.append(list_text_pos)
        return list_sent

    # get the word from pos
    def get_word_by_pos(self, sent, pos):
        if self.language == 'en-GB':
            nlp = spacy.load("en_core_web_sm")
        elif self.language == 'it-IT':
            nlp = spacy.load("it_core_news_sm")
        doc = nlp(sent)
        word = ''
        for token in doc:
            if(token.pos_ == pos):
                word = token.text
                break
        return word

    #get the word from entity
    def get_word_by_entity(self, sent, ent):
        sentence = translator.translate(sent, dest='en')
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(sentence.text)
        word = ''
        for entity in doc.ents:
            if(entity.label_ == ent):
                word = translator.translate(entity.text, dest='it')
                word = word.text
        return word

    #get the entity from sentence
    def get_entity_from_sent(self,sent):
        sent = translator.translate(sent, dest='en')
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(sent.text)
        list_entity = []
        for ent in doc.ents:
            list_ = []

            word = translator.translate(ent.text, dest='it')
            list_.append(word.text)
            list_.append(ent.label_)
            list_entity.append(list_)
        return list_entity

    #extract entities from sentence
    def extract_entities(self,sent):
        if self.language == 'en-GB':
            nlp = spacy.load("en_core_web_sm")
        elif self.language == 'it-IT':
            nlp = spacy.load("it_core_news_sm")
        for entity in nlp(sent).ents:
            print("Entity: ", entity.text)
            print("Entity Type: %s | %s" % (entity.label_, spacy.explain(entity.label_)))
            print("Start Offset of the Entity: ", entity.start_char)
            print("End Offset of the Entity: ", entity.end_char)
            print("--")

class IntentCalssifier:
        """
           This is a class with goals to call implement a intents classfier and use it to do a prediction
           about intent. There are all methods needed to make preprocessing, training and prediction
           of intents.
        """
        def __init__(self, path_model=paths.MODELS, path_data=paths.DATA_INTENTS):
            self.path_model = path_model
            self.path_data = path_data
            self.intents_class = ['request.booking_film', 'request.congratulations', 'request.help', 'request.info_film', 'request.info_film_advi', 'request.info_film_gen','request.info_film_max_score', 'request.info_film_max_score_actor','request.info_film_score','request.info_films', 'request.info_robot']

        # load data
        def load_dataset(self,filename):
            df = pd.read_csv(filename, encoding="latin1",names=["Sentence", "Intent"])
            intent = df["Intent"]
            unique_intent = list(set(intent))
            unique_intent_sorted = sorted(unique_intent)
            sentences = list(df["Sentence"])

            return (intent, unique_intent_sorted, sentences)

        # cleaning data
        def cleaning(self,sentences):
            lemmatizer = WordNetLemmatizer()

            words = []
            for s in sentences:
                clean = re.sub(r'[^ a-z A-Z 0-9]', " ", s)
                w = word_tokenize(clean)
                # lemmatizing
                words.append([lemmatizer.lemmatize(i.lower()) for i in w])

            return words

        #create tokenize data
        def create_tokenizer(self,words,filters = '!"#$%&()*+,-./:;<=>?@[\]^_`{|}~'):
          token = Tokenizer(filters = filters)
          token.fit_on_texts(words)
          return token

        # return the max legnght of sentence in the file data
        def max_length(self,words):
          return(len(max(words, key = len)))

        #get the encoding data form words
        def encoding_doc(self,token, words):
          return(token.texts_to_sequences(words))

        #get the data with padding
        def padding_doc(self,encoded_doc, max_length):
          return(pad_sequences(encoded_doc, maxlen = max_length,padding =   "post"))

        # get one data one hot encoding
        def one_hot(self,encode):
          o = OneHotEncoder(sparse = False)
          return(o.fit_transform(encode))

        #create model
        def create_model(self,vocab_size, max_length):
            model = Sequential()

            model.add(Embedding(vocab_size, 128,input_length=max_length, trainable=False))
            model.add(Bidirectional(LSTM(128)))
            model.add(Dense(64, activation="relu"))
            model.add(Dropout(0.10))
            model.add(Dense(64, activation="relu"))
            model.add(Dropout(0.10))
            model.add(BatchNormalization())
            model.add(Dense(len(self.intents_class), activation="softmax"))

            return model

        #perform predictions
        def predictions(self,text,model,cleaned_words):
            intent, unique_intent, sentences = self.load_dataset(self.path_data)
            word_tokenizer = self.create_tokenizer(cleaned_words)
            max_length = self.max_length(cleaned_words)

            clean = re.sub(r'[^ a-z A-Z 0-9]', " ", text)
            test_word = word_tokenize(clean)
            test_word = [w.lower() for w in test_word]
            test_ls = word_tokenizer.texts_to_sequences(test_word)
            # Check for unknown words
            if [] in test_ls:
                test_ls = list(filter(None, test_ls))

            test_ls = np.array(test_ls).reshape(1, len(test_ls))

            x = self.padding_doc(test_ls, max_length)

            pred = model.predict_proba(x)

            return pred,unique_intent

        # get the intent which the hight probability
        def get_final_output(self,pred, classes):
            predictions = pred[0]
            classes = np.array(classes)
            ids = np.argsort(-predictions)
            classes = classes[ids]
            return classes[0]

        # map an integer to a word
        def word_for_id(self,integer, tokenizer):
             for word, index in tokenizer.word_index.items():
              if index == integer:
               return word
             return None

        #load model of intents
        def load_model_intents(self):
            model = load_model(self.path_model)
            return model

        #training
        def train(self,vocab_size,max_length,train_x,train_y,val_x,val_y):
            print('start training of model for intent classification...')
            model = self.create_model(vocab_size, max_length)
            model.compile(loss="categorical_crossentropy", optimizer='adam', metrics=["accuracy"])
            model.summary()
            checkpoint = ModelCheckpoint(self.path_model, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
            hist_model = model.fit(train_x, train_y, epochs=200, batch_size=16, validation_data=(val_x, val_y), callbacks=[checkpoint])
            print('The model has been saved to the path: {}'.format(self.path_model))
            self.plots_acc(history_=hist_model)  # plot accuracy
            self.plots_loss(history_=hist_model) # plot loss function
            return hist_model

        # plot accuracy
        def plots_acc(self, history_):
            pl_acc = plt
            pl_acc.plot(history_.history['acc'])
            pl_acc.plot(history_.history['val_acc'])
            pl_acc.title('model accuracy')
            pl_acc.ylabel('accuracy')
            pl_acc.xlabel('epoch')
            pl_acc.legend(['train', 'test'], loc='upper left')
            pl_acc.savefig(paths.PLOT_ACC)
            print('the plot of accuracy was saved in the file to the path : {}'.format(paths.PLOT_ACC))
            pl_acc.clf()

        # plot loss function
        def plots_loss(selfself,history_):
            pl_loss = plt
            pl_loss.plot(history_.history['loss'])
            pl_loss.plot(history_.history['val_loss'])
            pl_loss.title('model loss')
            pl_loss.ylabel('loss')
            pl_loss.xlabel('epoch')
            pl_loss.legend(['train', 'test'], loc='upper left')
            pl_loss.savefig(paths.PLOT_LOSS)
            print('the plot of loss function was saved in the file to the path : {}'.format(paths.PLOT_LOSS))
            pl_loss.clf()

        # preprocessing process
        def preprocessing(self):
            intent, unique_intent, sentences = self.load_dataset(self.path_data)
            cleaned_words = self.cleaning(sentences)
            word_tokenizer = self.create_tokenizer(cleaned_words)
            vocab_size = len(word_tokenizer.word_index) + 1
            max_length = self.max_length(cleaned_words)
            encoded_doc = self.encoding_doc(word_tokenizer, cleaned_words)
            padded_doc = self.padding_doc(encoded_doc, max_length)
            output_tokenizer = self.create_tokenizer(unique_intent, filters = '!"#$%&()*+,-/:;<=>?@[\]^`{|}~')
            encoded_output = self.encoding_doc(output_tokenizer, intent)
            encoded_output = np.array(encoded_output).reshape(len(encoded_output), 1)
            output_one_hot = self.one_hot(encoded_output)
            train_X, val_X, train_Y, val_Y = train_test_split(padded_doc, output_one_hot, shuffle=True, test_size=0.3)
            return vocab_size,max_length,cleaned_words,train_X, val_X, train_Y, val_Y

        # training model
        def train_model(self):
            vocab_size, max_length, cleaned_words, train_X, val_X, train_Y, val_Y = self.preprocessing()
            self.train(vocab_size, max_length, train_x=train_X, val_x=val_X, train_y=train_Y, val_y=val_Y)

        # prediction of intent from model
        def prediction_intent(self,sentence: str):
            vocab_size, max_length, cleaned_words, train_X, val_X, train_Y, val_Y = self.preprocessing()
            model = self.load_model_intents()
            pred, unique_intent = self.predictions(text=sentence, model=model, cleaned_words=cleaned_words)
            return self.get_final_output(pred, unique_intent)

