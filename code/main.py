import speech_recognition as sr
import sys
sys.path.insert(0,'class_')
from class_ import tts, nlu,dm,data_collection
import sys
import re
language_list = ['en-GB','it-IT']
language = language_list[1]

# initialization of tts class, nlu for slot filling, intent classfier and the data collection
TTS = tts.Tts()  # tts
TTS.set_property_voice()  #property of tts
slots = nlu.Nlu()   # nlu for slot filling
datacollection = data_collection.DataCollection()   # the data collection class
intentclassifier = nlu.IntentCalssifier()  # the intent classifier

# close robot from dialogue
def close_robot():
    sys.exit("Robot Gina Chiuso")

# method to confront two list. It is used to confront if two list have same element (positive answers)
def confront_lists(list1, list2):
    result = False
    word = None
    for x in list1:
        for y in list2:
            if x.lower() == y.lower():
                result = True
                word = x
                return result,word
    return result,word

# start dialogue
def start_dialogue(text_robot = ''):
    with sr.Microphone() as source:
        # all slots for slot filling
        what_film = None
        what_time = None
        number_tickets = None
        when = None
        location = None
        gen_info = None
        choice_gen = None
        check_repeat = False
        if(text_robot != ''):
            ASR = sr.Recognizer()                  # Crea una istanza del recognizer
            print('Gina : {}'.format(text_robot))
            TTS.robot_speak("{}".format(text_robot))
            audio = ASR.listen(source)
            text_first = ''
            try:
                text_first = ASR.recognize_google(audio, language="it-IT")
                print('You : {}'.format(text_first))
                if (text_first == 'Chiudi'):
                    close_robot()
            except:
                if(text_first != 'Chiudi'):
                   start_dialogue(text_robot="Non ti riesco a capire, ripeti per favore.")
                else:
                    close_robot()
        else:
            ASR = sr.Recognizer()                 # instance for recognizer
            audio = ASR.listen(source)            # listen asr
            try:
                text_first = ASR.recognize_google(audio, language="it-IT")
                print('You : {}'.format(text_first))
                if (text_first  == datacollection.close):  # if user says "Chiudi" then chiudi
                    close_robot()
            except:
                if (text_first != datacollection.close):   # if robot doesnt understand
                    start_dialogue(text_robot="Non ti riesco a capire, ripeti per favore.")
                else:
                    close_robot()                          # if user says "Chiudi" then chiudi
        intent = intentclassifier.prediction_intent(sentence=text_first)
        slot_filling = slots.get_entity_from_sent(sent=text_first)
        print('intent understanded :{}'.format(intent))

        # start slot filling at fisrt
        for i in slot_filling:
            if((i[1] == 'DATE' or i[1] == 'TIME') and when == None):
                when = i[0]
            if(i[1] == 'CARDINAL' and number_tickets == None):
                number_tickets = i[0]
            if(i[1] == 'TIME' and what_time == None):
                    num = re.findall(r'\d+', i[0])
                    if(num != [] ):
                       what_time = i[0]
                    else:
                        what_time = None

        # slot filling for geners of films
        for i in datacollection.geners:
            gen = i.lower()
            word = re.search(gen, text_first)
            if (word != None):
                gen = text_first[word.span()[0]:word.span()[1]]
                choice_gen = gen
                break;

        # loop for dialogue
        while (True):
            # instance of dialogue managment
            mangane_act = dm.DM(what_film=what_film, when=when, number_of_tikets=number_tickets, what_time=what_time,location=location,gen_info=gen_info,choice_gen=choice_gen)

            # check if the must repeat or not
            if(check_repeat == False):
                response,response_robot = mangane_act.manage_first_action(intent=intent)
            else:
                response = mangane_act.manage_repeat_action(intent=intent)

            # start the check of slots
            # if dm return stop. Robot must return information about purchase tickets
            if (response == datacollection.stop):
                audio = ASR.listen(source)
                try:
                    text = ASR.recognize_google(audio, language="it-IT")
                    print('You : {}'.format(text))
                    list_confirm = text.split()
                    check_answer_conf,word = confront_lists(list_confirm, datacollection.confirm_expression)
                    check_answer_not_conf,word = confront_lists(list_confirm, datacollection.not_confirm_expression)
                    if(check_answer_conf):
                        text_robot = "Grazie per la prenotazione."
                        print('Gina : {}'.format(text_robot))
                        TTS.robot_speak(text_robot)
                        start_dialogue(text_robot='Come ti posso aiutare ancora?')
                        check_repeat = False
                    elif(check_answer_not_conf):
                        start_dialogue('Acquisto annullato,come ti posso aiutare?')
                        check_repeat = False
                    else:
                        check_repeat = True
                        continue;
                except:
                      check_repeat = True
                      continue;

            # if dm return continue. The robot must contiue with dialogue
            elif(response == datacollection.continue_):
                      start_dialogue('Come ti posso aiutare ancora?')

            # if dm return help. The robot replied the user if how it can help him
            elif(response == datacollection.help):
                      start_dialogue()

            # if dm return the what film slot. The robot asked to user what film he want to know
            elif(response == datacollection.what_film):
                audio = ASR.listen(source)
                try:
                    text_first = ASR.recognize_google(audio, language="it-IT")
                    print('You : {}'.format(text_first))
                    what_film = text_first
                    check_repeat = False
                except:
                    check_repeat = True
                    continue;

            #  if dm return the number tickets slot.The robot asked to user how many number tickets he want to buy
            elif (response == datacollection.number_tickets):
                audio = ASR.listen(source)
                try:
                    text_first = ASR.recognize_google(audio, language="it-IT")
                    number = slots.get_word_by_entity(sent=text_first, ent='CARDINAL')
                    print('You : {}'.format(text_first))
                    if (number != ''):
                        number_tickets = number
                        check_repeat = False
                    else:
                        check_repeat = True
                        continue;
                except:
                    check_repeat = True
                    continue;

            #if dm return the what_time slot.The robot asked to user what time he intends
            elif (response == datacollection.what_time):
                audio = ASR.listen(source)
                try:
                    text_first = ASR.recognize_google(audio, language="it-IT")
                    number = slots.get_word_by_entity(sent=text_first,ent='CARDINAL')
                    number_time = slots.get_word_by_entity(sent=text_first, ent='TIME')
                    print('You : {}'.format(text_first))
                    num_find = re.findall(r'\d+', text_first)
                    # num = re.findall(r'\d+', number_time)
                    # if(number != '' and number_time == ''):
                    #     what_time = number
                    #     check_repeat = False
                    # elif(number == '' and number_time != '' and num != []):
                    #     what_time = number_time
                    #     check_repeat = False
                    # elif(number != '' and number_time != ''):
                    #     if(num != []):
                    #         what_time = number_time
                    #         check_repeat = False
                    #     else:
                    #         what_time = number
                    #         check_repeat = False
                    if(num_find != [] and len(num_find) <= 2):
                        if(len(num_find) == 2):
                            time = num_find[0]+':'+num_find[1]
                            check_time,number_ = confront_lists([time],response_robot)
                            if(check_time):
                                what_time = number_
                                check_repeat = False
                            else:
                                text_robot_time = 'l\'orario %s non è disponibile' % (time)
                                print('Gina : {}'.format(text_robot_time))
                                TTS.robot_speak('{}'.format(text_robot_time))
                                check_repeat = True
                        else:
                            time = num_find[0] + ':00'
                            check_time, number_ = confront_lists([time], response_robot)
                            if (check_time):
                                what_time = number_
                                check_repeat = False
                            else:
                                text_robot_time = 'l\'orario %s non è disponibile' % (time)
                                print('Gina : {}'.format(text_robot_time))
                                TTS.robot_speak('{}'.format(text_robot_time))
                                check_repeat = True
                    else:
                        check_repeat = True
                        continue;
                except:

                    check_repeat = True
                    continue;

            # if dm return the when slot.The robot asked to user the date which user intends
            elif (response == datacollection.when):
                audio = ASR.listen(source)
                try:
                    text_first = ASR.recognize_google(audio, language="it-IT")
                    print('You : {}'.format(text_first))
                    date = slots.get_word_by_entity(sent=text_first, ent='DATE')
                    if (date != ''):
                        when = date
                        check_repeat = False
                    else:
                        check_repeat = True
                        continue;
                except:

                    check_repeat = True
                    continue;

            # if dm return the location slot.The robot asked to user the location which user intends
            elif (response == datacollection.location):
                audio = ASR.listen(source)
                try:
                    text_first = ASR.recognize_google(audio, language="it-IT")
                    print('You : {}'.format(text_first))
                    location = text_first
                    check_repeat = False
                except:
                    check_repeat = True
                    continue;

            # if dm return the gener info or the choice of gener slot.The robot asked to user if he want to filter for gener or it
            # asked him what gener he want to choice
            elif (response == datacollection.gen_info or response == datacollection.choice_gen):
                audio = ASR.listen(source)
                if(response == datacollection.gen_info):
                    try:
                        text = ASR.recognize_google(audio, language="it-IT")
                        print('You : {}'.format(text))
                        list_confirm = text.split()
                        check_answer_conf,word = confront_lists(list_confirm, datacollection.confirm_expression)
                        check_answer_not_conf,word = confront_lists(list_confirm, datacollection.not_confirm_expression)
                        if(check_answer_conf):
                            gen_info = 'sì'
                            check_repeat = False
                        elif(check_answer_not_conf):
                            gen_info = 'no'
                            check_repeat = False
                        else:
                            check_repeat = True
                            continue;
                    except:
                        check_repeat = True
                        continue;
                elif(response == datacollection.choice_gen):
                    try:
                        text = ASR.recognize_google(audio, language="it-IT")
                        print('You : {}'.format(text))
                        check_gen,word = confront_lists(text.split(),datacollection.geners)
                        if(check_gen):
                           choice_gen = word
                           check_repeat = False
                        else:
                           check_repeat = True
                           continue;
                    except:
                        check_repeat = True
                        continue;
                else:
                    print('ERRORE: valore di risposta dal dm errato! ci scusiamo per l\'inconveniente...dire "Chiudi"')


# main run
if __name__ == '__main__':
    import  random
    # start dialogue with Gina
    initial_text = 'Ciao, io sono Gina e ti aiuterò a prenotare dei biglietti per qualsiasi film in qualsiasi cinema in italia e avere informazioni generali sui film, come ti posso aiutare?'
    start_dialogue(text_robot=initial_text)
