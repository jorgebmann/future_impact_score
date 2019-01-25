"""
Prediction of new test data:
    1. load test data
    2. clean data
    3. load tokenizer
    4. apply tokenizer and padding to test data
    5. load model and weihts
    6. predict
"""

from numpy.random import seed
seed(1)
from tensorflow import set_random_seed
set_random_seed(2)
import pandas as pd
from string import punctuation
from nltk.corpus import stopwords
from keras.models import model_from_json
from keras.preprocessing.sequence import pad_sequences
from keras import backend as K
import pickle

#import os
#os.chdir('/mnt/hdd/fis/P/api/pred')

#test_data = pd.read_csv('/mnt/hdd/fis/data/test_reg_long_epubdate01-03_2016.csv').fillna(" ")
#test_data = test_data.iloc[[1]]
#test_data['abstract'] = test_data['abstract'].fillna(' ')
#test_data['abstract'] = test_data['abstract'].str.lower()

#test_data = ['aim aim study explore describe experiences healthcare needs displaced women osire refugee camp namibia namibia country displaced people african countries seek refuge result countrys political instability displaced people hosted osire camp highly protected area women men camp health often compromised descriptive phenomenological study natural dimension experiences participants healthcare needs explored depth interviews reflected upon transcendental processes formulate phenomenological dimension thereof findings essence displaced womens healthcare needs need restoration hope human dignity needs refer measures enhance autonomy freedom skills training certainty future security aid distribution protection stigmatization due human immunodeficiency virus infection protection abuse participation reproductive health care discussion displaced women admitted camp lose freedom make decisions everyday functioning future thus develop feelings insecurity vulnerability participants referred several factors detrimental well essence needs need restoration hope human dignity could achieved needs addressed implications nursing nurses close contact displaced women refugee camps negotiate opportunities women discuss concerns camp officials implications health social development policy policies make provision involvement displaced people aspects relate everyday future living arrangements']
#test_data = pd.DataFrame(['We previously reported that ceramide synthase 6 (CerS6) is elevated in response to folate stress in cancer cells, leading to enhanced production of C16-ceramide and apoptosis. Antifolate methotrexate (MTX), a drug commonly used in chemotherapy of several types of cancer, is a strong inhibitor of folate metabolism. Here we investigated whether this drug targets CerS6. We observed that CerS6 protein was markedly elevated in several cancer cell lines treated with MTX. In agreement with the enzyme elevation, its product C16-ceramide was also strongly elevated, so as several other ceramide species. The increase in C16-ceramide, however, was eliminated in MTX-treated cells lacking CerS6 through siRNA silencing, while the increase in other ceramides sustained. Furthermore, the siRNA silencing of CerS6 robustly protected A549 lung adenocarcinoma cells from MTX toxicity, while the silencing of another ceramide synthase, CerS4, which was also responsive to folate stress in our previous study, did not interfere with the MTX effect. The rescue effect of CerS6 silencing upon MTX treatment was further confirmed in HCT116 and HepG2 cell lines. Interestingly, CerS6 itself, but not CerS4, induced strong antiproliferative effect in several cancer cell lines if elevated by transient transfection. The effect of MTX on CerS6 elevation was likely p53 dependent, which is in agreement with the hypothesis that the protein is a transcriptional target of p53. In line with this notion, lometrexol, the antifolate inducing cytotoxicity through the p53-independent mechanism, did not affect CerS6 levels. We have also found that MTX induces the formation of ER aggregates, enriched with CerS6 protein. We further demonstrated that such aggregation requires CerS6 and suggests that it is an indication of ER stress. Overall, our study identified CerS6 and ceramide pathways as a novel MTX target.'])
#test_data.columns = ['abstract']
#test_data['abstract'] = test_data['abstract'].fillna(' ')
#test_data['abstract'] = test_data['abstract'].str.lower()

def mk_prediction(test_data):

    # turn a doc into clean tokens
    def clean_doc(doc):
        # split into tokens by white space
        tokens = doc.split()
        # remove punctuation from each token
        table = str.maketrans('', '', punctuation)
        tokens = [w.translate(table) for w in tokens]
        # remove remaining tokens that are not alphabetic
        tokens = [word for word in tokens if word.isalpha()]
        # filter out stop words
        stop_words = set(stopwords.words('english'))
        tokens = [w for w in tokens if not w in stop_words]
        # filter out short tokens
        tokens = [word for word in tokens if len(word) > 1]
        tokens = ' '.join(tokens)
        return tokens

    
    test_x = list()
    #test_y = list()
    test_data = pd.DataFrame([test_data], index = ['abstract'])
    test_data.columns = ['abstract']
    test_data['abstract'] = test_data['abstract'].fillna(' ')
    test_data['abstract'] = test_data['abstract'].str.lower()

    #pd.Series.tolist(test_data)
    #pd.DataFrame(eval(['adsf adsf asd dd']))
    #pd.read_csv('asdfasdf')
    #pd.read_table('asd fas df adsf')
    for j in range(len(test_data)):
        #test_x[i] = clean_doc(test_x[i])
        if len(test_data.abstract[j].split()) < 500:
            tokens = clean_doc(test_data.abstract[j])
            # add to list
            test_x.append(tokens)
            #test_y.append(test_data.citations[j])

    # encode a list of lines
    def encode_text(tokenizer, lines, length):
        # integer encode
        encoded = tokenizer.texts_to_sequences(lines)
        # pad encoded sequences
        padded = pad_sequences(encoded, maxlen=length, padding='post')
        return padded

    # loading tokenizer
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    length = 382
    testX = encode_text(tokenizer, test_x, length)
    
    
    # when repeating query, it gives an error message
    # solution K.clear_session() after prediction
    # load json and create model
    json_file = open('pred_model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    #delete_module('keras.models')
    #tf.keras.backend.clear_session()
    # load weights into new model
    loaded_model.load_weights("pred_model.h5")
    
    batch_size = 512 #256

    # evaluate loaded model on test data
    loaded_model.compile(loss='mean_squared_error', optimizer='rmsprop', metrics=['mse'])
    loaded_predictions = loaded_model.predict([testX,testX,testX], batch_size=batch_size, verbose=1)
    if loaded_predictions[0] <= 2:
        fis = 'very low'
    elif (loaded_predictions[0] > 2) and (loaded_predictions[0] <= 5):
        fis = 'low'
    elif (loaded_predictions[0] > 5) and (loaded_predictions[0] <= 10):      
        fis = 'intermediate'
    elif (loaded_predictions[0] > 10) and (loaded_predictions[0] <= 20):      
        fis = 'high'
    elif loaded_predictions[0] > 20:
        fis = 'very high'
    #print(fis)
    #loaded_df = pd.DataFrame(loaded_predictions)
    
    #loaded_df.to_csv('/mnt/hdd/fis/data/predictions/predictions_reg_epubdate01-03_2016_3xconv_embed_long_lr_new1.csv', index=False)
    K.clear_session()

    return fis

#mk_prediction(test_data)
