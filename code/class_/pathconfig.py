
class paths(object):
    """ This is a class_ with goals to call all data paths from it. It  simplifies and streamlines the code from long paths.
    It is used following this rules:
    - in the file needs to include the file : import pathconfig,
    - create object from class_ : paths = pathconfig.paths()
    - call path from property of class_: for example path_semcor = paths.TRAIN_DATASET
    Change all path in order to set own path and used them in the code.
    I remember that for path mappings the path are the same. So use this class_ to call them.
    Many files were deleted so
    """

    def __init__(self):
        #possible formats of files
        self.JSON = '.json'
        self.CSV = '.csv'
        self.MODEL = '.model'
        self.H5 = '.h5'
        self.PNG = '.png'
        self.MAT = '.mat'

        #Resources path base
        self.BASE_RESOURCES = _BASE_RES_PATH = '../resources/'

        self.DATA_INTENTS = _BASE_RES_PATH + 'data_intents{}'.format(self.CSV)
        self.MODELS = _BASE_RES_PATH + 'model{}'.format(self.H5)
        self.PLOT_ACC = _BASE_RES_PATH + 'plot_int_acc{}'.format(self.PNG)
        self.PLOT_LOSS = _BASE_RES_PATH + 'plot_int_loss{}'.format(self.PNG)




