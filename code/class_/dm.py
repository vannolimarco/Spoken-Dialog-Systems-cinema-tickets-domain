import  sys
sys.path.insert(0,'class_')
import nlu,tts
import random
import data_collection


# initialize the tts and the datacollection class
TTS = tts.Tts()
TTS.set_property_voice()
datacollection = data_collection.DataCollection()

class DM:
        """ This is a class about dialogue management. It aims to manage all slots and intent compoted from nlu
        and then return the answer to user.
        """
        def __init__(self,what_film,number_of_tikets,what_time,when,location,gen_info,choice_gen):
            self.intent_class = nlu.IntentCalssifier()
            self.what_film = what_film
            self.number_of_tikets = number_of_tikets
            self.what_time = what_time
            self.when = when
            self.location = location
            self.gen_info = gen_info
            self.choice_gen = choice_gen
            self.slot_booking_film = [self.what_film,self.number_of_tikets,self.what_time,self.location,self.when]
            self.intents = self.intent_class.intents_class

        # manage al intent for first time. It is called when the user doesn't repeat. Thus the
        # robot has undestand the answer of user
        def manage_first_action(self, intent):
            if(intent == self.intents[10]):     #request.info_robot
                 text_robot = 'Sono il robot Gina che ti aiuterà ad acquistare un biglietto per il cinema.Come ti posso aiutare?'
                 print(('Gina : {}').format(text_robot))
                 TTS.robot_speak('{}'.format(text_robot))
                 return datacollection.help,text_robot
            elif(intent == self.intents[9]):    #request.info_films
                if(self.when == None):
                    text_robot = 'Che periodo intendi?'
                    print(('Gina : {}').format(text_robot))
                    TTS.robot_speak('{}'.format(text_robot))
                    return datacollection.when,text_robot
                elif(self.choice_gen == None):
                    if(self.gen_info == None):
                        text_robot = 'li vuoi filtrare per genere?'
                        print(('Gina : {}').format(text_robot))
                        TTS.robot_speak('{}'.format(text_robot))
                        return datacollection.gen_info, text_robot
                    elif(self.gen_info == 'sì'):
                            if (self.choice_gen == None):
                                random_gen = random.sample(datacollection.geners_single,5)
                                text_robot = ('Per quale genere li vuoi filtrare? ti do dei consigli :%s ' % (
                                    ' '.join([str(elem) for elem in random_gen])))
                                print(('Gina : {}').format(text_robot))
                                TTS.robot_speak(text_robot)
                                return datacollection.choice_gen, text_robot
                            else:
                                films_random = random.sample(list(datacollection.films), 2)
                                text_robot = ('I film con il genere %s che sono proiettati %s sono i seguenti : %s' % (
                                        self.choice_gen, self.when, ' '.join([str(elem) for elem in films_random])))
                                print(('Gina : {}').format(text_robot))
                                TTS.robot_speak(text_robot)
                                return datacollection.continue_, text_robot
                    else:
                        film = random.sample(list(datacollection.films), 3)
                        geners = [datacollection.films[k] for k in film]
                        text_robot = ('I film che sono proiettati %s sono i seguenti : %s con i generi %s' % (
                            self.when, ' , '.join([str(elem) for elem in film]),','.join([str(elem) for elem in geners])))
                        print(('Gina : {}').format(text_robot))
                        TTS.robot_speak(text_robot)
                        return datacollection.continue_,text_robot
                else:
                    films_random = random.sample(list(datacollection.films), 2)
                    text_robot = ('I film con il genere %s che sono proiettati %s sono i seguenti : %s' % (
                        self.choice_gen, self.when, ' e '.join([str(elem) for elem in films_random])))
                    print(('Gina : {}').format(text_robot))
                    TTS.robot_speak(text_robot)
                    return 'continue', text_robot
            elif (intent == self.intents[0]):     #request.booking_film
                if (self.what_film == None):
                     text_robot = 'Quale film vuoi andare a vedere?'
                     print(('Gina : {}').format(text_robot))
                     TTS.robot_speak('{}'.format(text_robot))
                     return datacollection.what_film,text_robot

                elif(self.number_of_tikets == None):
                     text_robot = 'Quanti biglietti vuoi acquistare?'
                     print(('Gina : {}').format(text_robot))
                     TTS.robot_speak('{}'.format(text_robot))
                     return datacollection.number_tickets,text_robot
                elif (self.location == None):
                    text_robot = 'In quale cinema?'
                    print(('Gina : {}').format(text_robot))
                    TTS.robot_speak('{}'.format(text_robot))
                    return datacollection.location, text_robot
                elif (self.when == None):
                     text_robot = 'Quando lo vuoi vedere?'
                     print(('Gina : {}').format(text_robot))
                     TTS.robot_speak('{}'.format(text_robot))
                     return datacollection.when,text_robot
                elif (self.what_time == None):
                     random_times = random.sample(datacollection.times_ava,5)
                     random_times = sorted(random_times)
                     text_robot = 'A che ora vuoi vedere il film? Orari disponibili : %s' %(' , '.join([str(elem) for elem in random_times]))
                     print(('Gina : {}').format(text_robot))
                     TTS.robot_speak('{}'.format(text_robot))
                     return datacollection.what_time,random_times
                else:
                     random_room = random.sample(datacollection.sit_tickets,1)
                     random_sit = random.sample(datacollection.sit_tickets,1)
                     random_number = random.sample(datacollection.numbers, 1)
                     random_direction = random.sample(datacollection.direction, 1)
                     random_prize = random.sample(datacollection.prize,1)
                     info_booking = '\n       Film : '+self.what_film +'\n       Alle ore : '+self.what_time+'\n       Il giorno : '\
                                   +self.when +' \n       Nel cinema : '+self.location
                     info_ticket = '\n       Quantità biglietti : '+self.number_of_tikets +'\n       Sala : '+' '.join([str(elem) for elem in random_room])+'\n       Posti : fila '\
                                   +' '.join([str(elem) for elem in random_sit])+', dal numero '+ ' '.join([str(elem) for elem in random_number])+' scorrendo verso '+' '.join([str(elem) for elem in random_direction])+'\n       costo per biglietto : '+' '.join([str(elem) for elem in random_prize])
                     text_robot =  ('Procedo nell'"'acquisto con le seguenti informazioni che mi hai fornito : {}").format(info_booking)
                     text_robot = text_robot + '\n       INFO DEI BIGLIETTI: {}       \n       Confermi?'.format(info_ticket)
                     print(('Gina : {}').format(text_robot))
                     TTS.robot_speak('{}'.format(text_robot))
                     return datacollection.stop,text_robot
            elif (intent == self.intents[2]):     #request.help
                     text_robot = 'ok, come ti posso aiutare?'
                     print(('Gina : {}').format(text_robot))
                     TTS.robot_speak('{}'.format(text_robot))
                     return datacollection.help,text_robot
            elif (intent == self.intents[1]):      #request.congratulations
                text_robot = 'Grazie molto gentile, anche tu lo sei.'
                print(('Gina : {}').format(text_robot))
                TTS.robot_speak('{}'.format(text_robot))
                return datacollection.continue_, text_robot
            elif (intent == self.intents[4]):      #request.info_film_adv
                if (self.when == None):
                    text_robot = 'In che periodo? così ti consiglio nei migliori dei modi!'
                    print(('Gina : {}').format(text_robot))
                    TTS.robot_speak('{}'.format(text_robot))
                    return datacollection.when, text_robot
                elif (self.choice_gen == None):
                    if (self.gen_info == None):
                        text_robot = 'li vuoi filtrare per genere?'
                        print(('Gina : {}').format(text_robot))
                        TTS.robot_speak('{}'.format(text_robot))
                        return datacollection.gen_info, text_robot
                    elif (self.gen_info == 'sì'):
                        if (self.choice_gen == None):
                            random_gen = random.sample(datacollection.geners_single, 5)
                            text_robot = ('Per quale genere li vuoi filtrare? ti do dei consigli :%s ' % (
                                ','.join([str(elem) for elem in random_gen])))
                            print(('Gina : {}').format(text_robot))
                            TTS.robot_speak(text_robot)
                            return datacollection.choice_gen, text_robot
                        else:
                            films_random = random.sample(list(datacollection.films), 2)
                            text_robot = ('I film con il genere %s che ti consiglio per %s sono i seguenti : %s' % (
                                self.choice_gen,self.when, ' , '.join([str(elem) for elem in films_random])))
                            print(('Gina : {}').format(text_robot))
                            TTS.robot_speak(text_robot)
                            return datacollection.continue_, text_robot
                    elif(self.gen_info == 'no'):
                        film = random.sample(list(datacollection.films), 3)
                        geners = [datacollection.films[k] for k in film]
                        text_robot = ('i film che ti consiglio per %s sono i seguenti : %s con i seguenti generi %s' % (self.when,
                            ','.join([str(elem) for elem in film]),
                            ','.join([str(elem) for elem in geners])))
                        print(('Gina : {}').format(text_robot))
                        TTS.robot_speak('{}'.format(text_robot))
                        return datacollection.continue_, text_robot
                else:
                    films_random = random.sample(list(datacollection.films), 2)
                    text_robot = ('I film con il genere %s che ti consiglio per %s sono : %s' % (
                        self.choice_gen,self.when, ' e '.join([str(elem) for elem in films_random])))
                    print(('Gina : {}').format(text_robot))
                    TTS.robot_speak(text_robot)
                    return datacollection.continue_, text_robot
            elif (intent == self.intents[5]):    #request.info_film_gen
                if (self.what_film == None):
                     text_robot = 'Di quale film vuoi sapere il genere?'
                     print(('Gina : {}').format(text_robot))
                     TTS.robot_speak('{}'.format(text_robot))
                     return datacollection.what_film,text_robot
                else:
                    gen_random = random.sample(datacollection.geners_single,1)
                    text_robot = 'il film %s ha come genere il seguente : %s' % \
                       (self.what_film,','.join([str(elem) for elem in gen_random]))
                    print(('Gina : {}').format(text_robot))
                    TTS.robot_speak('{}'.format(text_robot))
                    return datacollection.continue_, text_robot
            elif (intent == self.intents[6]):    #request.info_film_max_score
                if (self.when == None):
                    text_robot = 'Che periodo intendi?'
                    print(('Gina : {}').format(text_robot))
                    TTS.robot_speak('{}'.format(text_robot))
                    return datacollection.when, text_robot
                elif (self.choice_gen == None):
                    if (self.gen_info == None):
                        text_robot = 'lo vuoi filtrare per genere?'
                        print(('Gina : {}').format(text_robot))
                        TTS.robot_speak('{}'.format(text_robot))
                        return datacollection.gen_info, text_robot
                    elif (self.gen_info == 'sì'):
                        if (self.choice_gen == None):
                            random_gen = random.sample(datacollection.geners_single, 5)
                            text_robot = ('Per quale genere li vuoi filtrare? ti do dei consigli :%s ' % (
                                ','.join([str(elem) for elem in random_gen])))
                            print(('Gina : {}').format(text_robot))
                            TTS.robot_speak(text_robot)
                            return datacollection.choice_gen, text_robot
                        else:
                            films_max_random = random.sample(list(datacollection.films), 1)
                            text_robot = 'il film che ha il massimo punteggio %s è : %s, categorizzato con il genere %s' % (
                            self.when,(' '.join([str(elem) for elem in films_max_random])), self.choice_gen)
                            print(('Gina : {}').format(text_robot))
                            TTS.robot_speak('{}'.format(text_robot))
                            return datacollection.continue_, text_robot
                    else:
                        film = random.sample(list(datacollection.films), 1)
                        geners = [datacollection.films[k] for k in film]
                        text_robot = 'il film che ha il massimo punteggio %s è : %s, categorizzato con il genere %s' % (
                            self.when, (' '.join([str(elem) for elem in film])), (' '.join([str(elem) for elem in geners])))
                        print(('Gina : {}').format(text_robot))
                        TTS.robot_speak('{}'.format(text_robot))
                        return datacollection.continue_, text_robot
                else:
                    films_max_random = random.sample(list(datacollection.films), 1)
                    text_robot = 'il film che ha il massimo punteggio %s è : %s, categorizzato nel genere %s' % (self.when,
                    (' '.join([str(elem) for elem in films_max_random])),self.choice_gen
                    )
                    print(('Gina : {}').format(text_robot))
                    TTS.robot_speak('{}'.format(text_robot))
                    return datacollection.continue_, text_robot
            elif (intent == self.intents[7]):   #request.info_film_max_score_actor
                if (self.when == None):
                    text_robot = 'In che periodo?'
                    print(('Gina : {}').format(text_robot))
                    TTS.robot_speak('{}'.format(text_robot))
                    return datacollection.when, text_robot
                else:
                    film = random.sample(list(datacollection.films), 1)
                    geners = [datacollection.films[k] for k in film]
                    actor_random = random.sample(datacollection.actors,1)
                    text_robot = 'Il film intitolato %s è stato il film di genere %s %s con il quale %s è stato l\'attore piu premiato e valutato' % ((' '.join([str(elem) for elem in film])),(' '.join([str(elem) for elem in geners]))
                    ,self.when,(' '.join([str(elem) for elem in actor_random])))
                    print(('Gina : {}').format(text_robot))
                    TTS.robot_speak('{}'.format(text_robot))
                    return datacollection.continue_, text_robot
            elif (intent == self.intents[3]):   #request.info_film
                if (self.what_film == None):
                     text_robot = 'Di quale film vuoi avere informazioni?'
                     print(('Gina : {}').format(text_robot))
                     TTS.robot_speak('{}'.format(text_robot))
                     return datacollection.what_film,text_robot
                else:
                    actor_random = random.sample(datacollection.actors,2)
                    score_random = random.sample(datacollection.score_film,1)
                    taking_random = random.sample(datacollection.takings,1)
                    gen_random = random.sample(datacollection.geners_single,1)
                    text_robot = 'il film %s ha avuto come attori principali %s e ha ottenuto un punteggio pari a %s con un\'incasso di %s , rientra nel genere %s' % \
                       (self.what_film,(' e '.join([str(elem) for elem in actor_random])),(' '.join([str(elem) for elem in score_random])),(' '.join([str(elem) for elem in taking_random])),(' '.join([str(elem) for elem in gen_random])))
                    print(('Gina : {}').format(text_robot))
                    TTS.robot_speak('{}'.format(text_robot))
                    return datacollection.continue_, text_robot
            elif (intent == self.intents[8]):   #request.info_film_score
                if (self.what_film == None):
                    text_robot = 'Di quale film vuoi sapere il punteggio??'
                    print(('Gina : {}').format(text_robot))
                    TTS.robot_speak('{}'.format(text_robot))
                    return datacollection.what_film, text_robot
                else:
                    score_random = random.sample(datacollection.score_film, 1)
                    text_robot = 'il film %s ha ottenuto un punteggio pari a %s' % (self.what_film,' '.join([str(elem) for elem in score_random]))
                    print(('Gina : {}').format(text_robot))
                    TTS.robot_speak('{}'.format(text_robot))
                    return datacollection.continue_, text_robot
            else:
                     text_robot = 'Scusa non ho capito le tue intenzioni'
                     print(('Gina : {}').format(text_robot))
                     TTS.robot_speak('{}'.format(text_robot))
                     return datacollection.continue_,text_robot

        # manage al intent for repeat time. It is called when the user has to repeat the answer. Thus the
        # robot hasn't undestand the answer of user
        def manage_repeat_action(self, intent):
            if (intent == self.intents[9]):        #request.info_films
                if (self.when == None):
                    text_robot = 'Ripeti il periodo'
                    print(('Gina : {}').format(text_robot))
                    TTS.robot_speak('{}'.format(text_robot))
                    return datacollection.when
                elif (self.choice_gen == None):
                    if (self.gen_info == None):
                        text_robot = 'Ripeti se confermi o no'
                        print(('Gina : {}').format(text_robot))
                        TTS.robot_speak('{}'.format(text_robot))
                        return datacollection.gen_info
                    elif(self.gen_info == 'sì'):
                            if (self.choice_gen == None):
                                text_robot = 'Ripeti il genere'
                                print(('Gina : {}').format(text_robot))
                                TTS.robot_speak('{}'.format(text_robot))
                                return datacollection.choice_gen
                            else:
                                films_random = random.sample(list(datacollection.films), 2)
                                text_robot = (
                                        'I film con il genere %s che sono proiettati %s sono i seguenti : %s' % (
                                    self.choice_gen, self.when, ' e '.join([str(elem) for elem in films_random])))
                                return datacollection.continue_
                    else:
                        film = random.sample(list(datacollection.films), 1)
                        geners = [datacollection.films[k] for k in film]
                        text_robot = ('I film che sono proiettati %s sono i seguenti : %s con i generi %s' % (
                            self.when, ' , '.join([str(elem) for elem in film]),' , '.join([str(elem) for elem in geners])))
                        return datacollection.continue_
                else:
                    text_robot = 'Ripeti il genere'
                    print(('Gina : {}').format(text_robot))
                    TTS.robot_speak('{}'.format(text_robot))
                    return datacollection.choice_gen
            elif(intent == self.intents[6]):   #request.info_films
                if (self.when == None):
                    text_robot = 'Ripeti il periodo'
                    print(('Gina : {}').format(text_robot))
                    TTS.robot_speak('{}'.format(text_robot))
                    return datacollection.when
                elif (self.choice_gen == None):
                    if (self.gen_info == None):
                        text_robot = 'Ripeti se confermi o no'
                        print(('Gina : {}').format(text_robot))
                        TTS.robot_speak('{}'.format(text_robot))
                        return datacollection.gen_info
                    elif (self.gen_info == 'sì'):
                        if (self.choice_gen == None):
                            text_robot = 'Ripeti il genere'
                            print(('Gina : {}').format(text_robot))
                            TTS.robot_speak('{}'.format(text_robot))
                            return datacollection.choice_gen
                        else:
                            film = random.sample(list(datacollection.films), 1)
                            geners = [datacollection.films[k] for k in film]
                            text_robot = 'il film che ha il massimo punteggio %s è : %s, categorizzato con il genere %s' % (
                                self.when, (' '.join([str(elem) for elem in film])), (' '.join([str(elem) for elem in geners])))
                            print(('Gina : {}').format(text_robot))
                            TTS.robot_speak('{}'.format(text_robot))
                            return datacollection.continue_
                    else:
                        film = random.sample(list(datacollection.films), 1)
                        geners = [datacollection.films[k] for k in film]
                        text_robot = 'il film che ha il massimo punteggio %s è : %s, categorizzato con il genere %s' % (
                            self.when, (' '.join([str(elem) for elem in film])), (' '.join([str(elem) for elem in geners])))
                        print(('Gina : {}').format(text_robot))
                        TTS.robot_speak('{}'.format(text_robot))
                        return datacollection.continue_
                else:
                    text_robot = 'Ripeti il genere'
                    print(('Gina : {}').format(text_robot))
                    TTS.robot_speak('{}'.format(text_robot))
                    return datacollection.choice_gen

            elif (intent == self.intents[4]):   #request.info_film_adv
                if (self.when == None):
                    text_robot = 'Ripeti il periodo'
                    print(('Gina : {}').format(text_robot))
                    TTS.robot_speak('{}'.format(text_robot))
                    return datacollection.when
                elif (self.choice_gen == None):
                    if (self.gen_info == None):
                        text_robot = 'Ripeti se confermi o no'
                        print(('Gina : {}').format(text_robot))
                        TTS.robot_speak('{}'.format(text_robot))
                        return datacollection.gen_info
                    elif (self.gen_info == 'sì'):
                        if (self.choice_gen == None):
                            text_robot = 'Ripeti il genere'
                            print(('Gina : {}').format(text_robot))
                            TTS.robot_speak('{}'.format(text_robot))
                            return datacollection.choice_gen
                        else:
                            films_random = random.sample(list(datacollection.films), 2)
                            text_robot = ('I film con il genere %s che ti consiglio sono i seguenti : %s' % (
                                self.choice_gen, ' , '.join([str(elem) for elem in films_random])))
                            print(('Gina : {}').format(text_robot))
                            TTS.robot_speak(text_robot)
                            return datacollection.continue_
                    else:
                        film = random.sample(list(datacollection.films), 3)
                        geners = [datacollection.films[k] for k in film]
                        text_robot = (
                                    'i film che ti consiglio sono i seguenti : %s con i seguenti generi %s' % (
                                ','.join([str(elem) for elem in film]),
                                ','.join([str(elem) for elem in geners])))
                        print(('Gina : {}').format(text_robot))
                        TTS.robot_speak('{}'.format(text_robot))
                        return datacollection.continue_
                else:
                    text_robot = 'Ripeti il genere'
                    print(('Gina : {}').format(text_robot))
                    TTS.robot_speak('{}'.format(text_robot))
                    return datacollection.choice_gen

            elif (intent == self.intents[0]):  # request.booking_film
                if (self.what_film == None):
                    text_robot = 'Ripeti il titolo del film'
                    print(('Gina : {}').format(text_robot))
                    TTS.robot_speak('{}'.format(text_robot))
                    return datacollection.what_film

                elif (self.number_of_tikets == None):
                    text_robot = 'Ripeti la quantità'
                    print(('Gina : {}').format(text_robot))
                    TTS.robot_speak('{}'.format(text_robot))
                    return datacollection.number_of_tikets

                elif (self.location == None):
                    text_robot = 'Ripeti il nome del cinema'
                    print(('Gina : {}').format(text_robot))
                    TTS.robot_speak('{}'.format(text_robot))
                    return datacollection.location

                elif (self.when == None):
                    text_robot = 'Ripeti il giorno'
                    print(('Gina : {}').format(text_robot))
                    TTS.robot_speak('{}'.format(text_robot))
                    return datacollection.when

                elif (self.what_time == None):
                    text_robot = 'Ripeti l\'orario'
                    print(('Gina : {}').format(text_robot))
                    TTS.robot_speak('{}'.format(text_robot))
                    return datacollection.what_time

                else:
                    text_robot = 'Ripeti se confermi o no'
                    print(('Gina : {}').format(text_robot))
                    TTS.robot_speak('{}'.format(text_robot))
                    return datacollection.stop
            elif (intent == self.intents[1] or intent == self.intents[5] or intent == self.intents[2] or intent == self.intents[10]):  # other intents
                text_robot = 'Scusa? Ripeti per favore'
                print(('Gina : {}').format(text_robot))
                TTS.robot_speak('{}'.format(text_robot))
                return datacollection.continue_
            elif(intent == self.intents[7]): #request.info_film_max_score_actor
                if (self.when == None):
                    text_robot = 'Ripeti il periodo'
                    print(('Gina : {}').format(text_robot))
                    TTS.robot_speak('{}'.format(text_robot))
                    return datacollection.when
                else:
                    film = random.sample(list(datacollection.films), 1)
                    geners = [datacollection.films[k] for k in film]
                    actor_random = random.sample(datacollection.actors, 1)
                    text_robot = 'Il film intitolato %s è stato il film di genere %s %s con il quale %s è stato l\'attore piu premiato e valutato' % (
                    (' '.join([str(elem) for elem in film])), (' '.join([str(elem) for elem in geners]))
                    , self.when, (' '.join([str(elem) for elem in actor_random])))
                    print(('Gina : {}').format(text_robot))
                    TTS.robot_speak('{}'.format(text_robot))
                    return datacollection.continue_
            elif (intent == self.intents[3]):  #request.info_film
                if (self.what_film == None):
                    text_robot = 'Ripeti il titolo del film'
                    print(('Gina : {}').format(text_robot))
                    TTS.robot_speak('{}'.format(text_robot))
                    return datacollection.what_film
                else:
                    actor_random = random.sample(datacollection.actors, 2)
                    score_random = random.sample(datacollection.score_film, 1)
                    taking_random = random.sample(datacollection.takings, 1)
                    text_robot = 'il film %s ha avuto come attori principali %s e ha ottenuto un punteggio pari a %s con un\'incasso di %s' % \
                                 (self.what_film, (' '.join([str(elem) for elem in actor_random])),
                                  (' '.join([str(elem) for elem in score_random])),
                                  (' '.join([str(elem) for elem in taking_random])))
                    print(('Gina : {}').format(text_robot))
                    TTS.robot_speak('{}'.format(text_robot))
                    return datacollection.continue_
            elif (intent == self.intents[8]):  #request.info_film_score
                if (self.what_film == None):
                    text_robot = 'Ripeti il titolo del film'
                    print(('Gina : {}').format(text_robot))
                    TTS.robot_speak('{}'.format(text_robot))
                    return datacollection.what_film
                else:
                    score_random = random.sample(datacollection.score_film, 1)
                    text_robot = 'il film %s ha ottenuto un punteggio pari a %s stelle' % (self.what_film, ' '.join([str(elem) for elem in score_random]))
                    print(('Gina : {}').format(text_robot))
                    TTS.robot_speak('{}'.format(text_robot))
                    return datacollection.continue_
            else:
                text_robot = 'Scusa non ho capito le tue intenzioni'
                print(('Gina : {}').format(text_robot))
                TTS.robot_speak('{}'.format(text_robot))
                return datacollection.continue_

