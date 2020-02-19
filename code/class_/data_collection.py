class DataCollection:
    """
    This is a class about data which contains all data needed for dialogue. It contains the name of
    returns from dm and all name of slots.
    """
    def __init__(self):
            self.films = {'La fabbrica di cioccolato':'Fantasy',
                          'Figli':'Drammatico',
                          'Il diritto di opporsi':'Drammatico',
                          'Judy':'Commedia',
                          'Parasite':'Biografico',
                          'Piccole donne':'Romantico',
                          'Joker':'Animazione',
                          'Tolo Tolo':'Comico',
                          'Alice e il sindaco':'Commedia',
                          'Fight Club':'Avventura',
                          'Toro scatenato':'Animazione',
                          'Lunar city':'Documentario',
                          'Il commissario Montalbano':'Drammatico',
                          'Hammamet':'Drammatico',
                          'Dolittle':'Fantasy',
                          'Odio l\'estate':'Commedia',
                          'Sonic il film':'Animazione',
                          'Bad Boys for life':'Azione',
                          'Gli anni piu belli':'Drammatico',
                          'L\'appartamento':'Drammatico',
                          'Chinatown':'Commedia',
                          'C\'era una volta il West':'Western',
                          'Il cavaliere oscuro':'Animazione',
                          '2001: Odissea nello spazio':'Avventura',
                          'Taxi Driver':'Thriller',
                          'Casablanca':'Documentario/Animazione',
                          'Il padrino - Parte due':'Animazione',
                          'Blade Runner':'Fantascienza',
                          'Il terzo uomo':'Drammatico',
                          'Guerre stellari':'Animazione',
                          'Fantasy island':'Thriller',
                          '1917':'Drammatico',
                          'Ritorno al futuro':'Avventura',
                          'Il Signore degli Anelli - La Compagnia dell\'Anello':'Avventura/Animazione',
                          'Il buono, il brutto, il cattivo':'Western',
                          'Il dottor Stranamore':'Commedia',
                          'A qualcuno piace caldo':'Commedia'}
            self.prize = ['5 euro', '6 euro', '8 euro', '9 euro', '10 euro']
            self.actors = ['Stefano Accorsi', 'Alessandro Borghi', 'Luca Marinelli', 'Pierfrancesco Favino',
                           'Elio Germano',
                           'Toni Servillo',
                           'Marco Giallini',
                           'Valerio Mastandrea',
                           'Aidan Gallagher', 'Antonio Banderas', 'Anthony Hopkins', 'Brad Pitt', 'Bruce Willis',
                           'Colin Firth', 'Colin Farrell', 'Chris Evans', 'Cuba Gooding j.', 'David Carradine',
                           'Denzel Washington',
                           'George Clooney', 'Hugh Laurie',
                           'Iain Glen',
                           'ack Nicholson',
                           'Javier Bardem',
                           'Jim Carrey',
                           'Johnny Depp',
                           'Jude Law',
                           'Kevin Costner',
                           'Kevin Spacey',
                           'Keanu Reeves',
                           'Leonardo Di Caprio',
                           'Matthew Mcconaughey',
                           'Matt Damon',
                           'Michael Caine',
                           'Nicolas Cage',
                           'Orlando Bloom',
                           'Patrick Dempsey',
                           'Richard Gere',
                           'Will Smith',
                           'Ryan Gosling',
                           'Ryan Reynolds',
                           'Robert Pattinson'
                           ]
            self.geners = ['Animazione',
                           'Animazioni',
                           'Avventura',
                           'Azione',
                           'Biografico',
                           'Biografici',
                           'Commedia',
                           'Documentario',
                           'Documentari',
                           'Drammatico',
                           'Drammatici',
                           'Erotico',
                           'Erotici',
                           'Romantico',
                           'Romantici',
                           'Fantascienza',
                           'Fantasy',
                           'Fantastico',
                           'Guerra',
                           'Horror',
                           'Musical',
                           'Storico',
                           'Storici',
                           'Thriller',
                           'Western',
                           'Catastrofico',
                           'Catastrofici',
                           'Comico',
                           'Comici',
                           'Epico',
                           'Epici',
                           'Giallo',
                           'Grottesco',
                           'Grotteschi',
                           'Mitologico',
                           'Mitologici',
                           'Noir',
                           'Politico',
                           'Politici',
                           'Poliziesco',
                           'Polizieschi',
                           'Religioso',
                           'Religiosi',
                           'Sentimentale',
                           'Sentimentali',
                           'Spionaggio',
                           'Sportivo',
                           'Sportivi',
                           'Space Opera'
                           ]
            self.geners_single = ['Animazione',
                           'Avventura',
                           'Azione',
                           'Biografico',
                           'Commedia',
                           'Documentario',
                           'Drammatico',
                           'Erotico',
                           'Romantico',
                           'Fantascienza',
                           'Fantasy',
                           'Fantastico',
                           'Guerra',
                           'Horror',
                           'Musical',
                           'Storico',
                           'Thriller',
                           'Western',
                           'Catastrofico',
                           'Comico',
                           'Epico',
                           'Giallo',
                           'Grottesco',
                           'Mitologico',
                           'Noir',
                           'Politico',
                           'Poliziesco',
                           'Religioso',
                           'Sentimentale',
                           'Spionaggio',
                           'Sportivo',
                           'Space Opera'
                           ]
            self.sit_tickets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                                't', 'u', 'v', 'z', 'k', 'j']
            self.numbers = [item for item in range(1, 15)]
            self.direction = ['sinistra', 'destra']
            self.score_film = ['zero stelle', '1 stella', 'due stelle', 'tre stelle', 'quattro stelle', 'cinque stelle']
            self.takings = ['1 milioni', '2 milioni', '3 milioni', '4 milioni', '5 milioni', '6 milioni', '7 milioni',
                            '8 milioni', '9 milioni', '10 milioni']
            self.confirm_expression = ['sì','esatto','giusto','sì questo','intendo dire questo','si','confermo','certo','sisi','sìsì']
            self.not_confirm_expression = ['no', 'no grazie', 'non confermo', 'assolutamente no','nono']
            self.what_time = 'what_time'
            self.what_film = 'what_film'
            self.close = 'Chiudi'
            self.stop = 'stop'
            self.continue_ = 'continue'
            self.help = 'help'
            self.number_tickets = 'number_tickets'
            self.when = 'when'
            self.location = 'location'
            self.gen_info = 'gen_info'
            self.choice_gen = 'choice_gen'
            self.tags = {'PERSON People', 'including fictional'
                         'NORP', 'Nationalities or religious or political groups'
                         'FACILITY', 'Buildings, airports, highways, bridges, etc.'
                         'ORGANIZATION', 'Companies, agencies, institutions, etc.'
                         'GPE', 'Countries, cities, states'
                         'LOCATION',
                         'Non-GPE locations, mountain ranges, bodies of water'
                         'PRODUCT', 'Vehicles, weapons, foods, etc. (Not services)'
                         'WORK_OF_ART', 'Titles of books, songs, etc.'
                         'EVENT', 'Named hurricanes, battles, wars, sports events, etc.'
                         'WORK', 'OF ART Titles of books, songs, etc.'
                         'LAW', 'Named documents made into laws'
                         'LANGUAGE', 'Any named language'
                         'DATE',
                         'Absolute or relative dates or periods'
                         'TIME', 'Times smaller than a day'
                         'PERCENT', 'Percentage (including “%”)'
                         'MONEY', 'Monetary values, including unit'
                         'MISC',
                         'Miscellaneous entities, e.g. events, nationalities, products or works of art.'
                         'QUANTITY', 'Measurements, as of weight or distance'
                         'ORDINAL', '“first”, “second”'
                         'CARDINAL', 'Numerals that do not fall under another typ'}
            self.times_ava = ['10:00','10:30','11:00','11:15','11:30','12:00','12:30','14:00','14:15','15:00','15:30','16:00',
                          '16:15','16:30','17:15','17:00','17:30','18:00','18:15','18:30','19:00','19:15','19:30','20:00','20:15'
                          ,'20:30','21:00','21:15','21:30','22:00','22:15','22:30','23:00','23:15','23:30']