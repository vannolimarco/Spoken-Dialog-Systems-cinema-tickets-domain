import  sys
sys.path.insert(0,'class_')
from class_ import nlu
from class_  import pathconfig
import argparse

paths = pathconfig.paths()

""" 
This file aims to be runned in order to train the model and make a prediction of intent 
"""

# train the model
def train(path_save_model = paths.MODELS, path_data_csv=paths.DATA_INTENTS):
    intentclassifier = nlu.IntentCalssifier(path_model=path_save_model,path_data=path_data_csv)
    intentclassifier.train_model()

# get intent from moder trained
def prediction_intent(sentence:str):
    intentclassifier = nlu.IntentCalssifier()
    pred = intentclassifier.prediction_intent(sentence=sentence)
    print('intention predicted from the sentence "%s" : {}'.format(pred) %(sentence))


# main to run
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PyTorch on TORCS with Multi-modal')
    parser.add_argument('--mode', default='prediction', type=str, help='support option: training/prediction')
    parser.add_argument('--path_data_csv', default=paths.DATA_INTENTS, type=str, help='support option: paths save model')
    parser.add_argument('--path_save_model', default=paths.MODELS, type=str, help='support option: path data csv for intents')
    parser.add_argument('--sentence_prediction', default='Ciao, vorrei acquistare due biglietti per il cinema per domani 19 febbraio', type=str,help='support option: sentence for prediction')
    args = parser.parse_args()

    if args.mode == 'training':
        train(path_save_model=args.path_save_model,path_data_csv=args.path_data_csv)
    elif args.mode == 'prediction':
        prediction_intent(sentence=args.sentence_prediction)
    else:
        raise RuntimeError('undefined mode {}. mode args can be: training or prediction'.format(args.mode))