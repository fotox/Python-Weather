# Import Python Libaries
import csv, numpy, sys, os
from numba import cuda
from sklearn.preprocessing import MinMaxScaler 

# Import Tensorflow and Keras Libaries
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow 
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras import initializers

# Generate Deep Learning Class
class DLM_PVA_GENERATE:
    def __init__ (self, location, year):
        # Basic Settings
        self.location = location
        self.year = year
        self.check_structure = False
        self.check_save_model = False
        self.leap_year = False
        self.train_dataset = []
        self.test_dataset = []
        self.simu_power = []
        self.dl_power = []
        
        # Neuronal Network Setting
        self.optimize_level = 'adam'     
        self.active_first = 'relu'
        self.active_second = 'sigmoid'
        self.loss_level = 'mean_squared_error'
        self.input_neurons = 6
        self.hidden_layer = 9
        self.hidden_neurons = 2
        self.output_neurons = 1
        self.epochs_size = 10
        self.batch_size = 8
        self.verbose_size = 0
        
    def func_check_structure(self):
        root = (os.path.abspath('.'))
        # Traindatasets Input
        train_path_in = (str(root)+'\\datasets_pv\\'+str(self.year)+'\\'+str(self.location))
        self.path_train_dataset = (str(train_path_in)+'.csv')
        # Traindatasets Input
        train_path_out = (str(root)+'\\datasets_matlab\\'+str(self.year)+'\\'+str(self.location))
        self.path_simu_power = (str(train_path_out)+'-kWp.csv')
        # Testdatasets
        test_path = (str(root)+'\\datasets_pv\\'+str(self.year)+'\\'+str(self.location))
        self.path_test_dataset = (str(test_path)+'.csv')
        self.path_dl_power = (str(test_path)+'-kWp.csv')
        # Saving-Files
        self.path_save = (str(root)+'\\dl_model\\')
        self.path_diagram = (str(test_path)+'_diagram')
        # Check Structure
        check_sum = 0
        path_arr = [self.path_train_dataset, self.path_simu_power, self.path_test_dataset,
                    self.path_dl_power, self.path_save]
        for path in path_arr:
            if path == (self.path_train_dataset or self.path_test_dataset or self.path_simu_power): 
                if os.path.getsize(path) == 0:
                    print('!! Please start at first generate_weatherdata.py')
                    check_sum = check_sum + 1
            elif path == self.path_dl_power:
                if os.path.exists(path) == False:
                    file = open(path,"w")
                    file.close()
            else:
                if os.path.exists(path) == False:
                    os.makedirs(path)
                    
            if check_sum == 0: self.check_structure = True
        return self.check_structure
    
    def func_leap_year(self):
        if self.year % 4 == 0 or self.year % 100 == 0 or self.year % 400 == 0:
            self.leap_year = True      
        return self.leap_year
    
    def func_scaling(self, dataset, set_off=None):
        inputdataset = numpy.array(list(csv.reader(open(dataset, "rt", encoding="utf8"), delimiter=","))).astype(str)
        self.scalerinput = MinMaxScaler()
        if dataset == (self.path_train_dataset or self.path_test_dataset):
            self.scalerinput.fit(inputdataset[1:])
            self.scalinputdataset = self.scalerinput.transform(inputdataset[1:])
            return self.scalinputdataset
        elif dataset == self.path_simu_power:
            self.scalerinput.fit(inputdataset)
            self.scalinputdataset = self.scalerinput.transform(inputdataset)
            return self.scalinputdataset
        elif set_off == True: 
            self.scalerinput.fit(inputdataset)
            return self.scalerinput
    
    def func_train_model(self, train_dataset, train_power):
        model = Sequential()
        model.add(Dense(self.hidden_neurons, input_dim=self.input_neurons, activation=self.active_first))
        for _ in range(self.hidden_layer-1):
            model.add(Dense(self.hidden_layer, activation=self.active_first))
        model.add(Dense(self.output_neurons, activation=self.active_first))
        model.compile(loss=self.loss_level, optimizer=self.optimize_level)
        model.fit(train_dataset, train_power, batch_size=self.batch_size, epochs=self.epochs_size, verbose=self.verbose_size)
        return model
    
    def func_save_model(self, model, save_type=None, path_save=None):
        save_type = input('-> Which data type should be stored?\nKeras [k/K], Json [j/J]: ')
        if save_type == ('j' or 'J' or 'json' or 'Json'):
            print('---> Save Type set on Json.')
            path_save = (str(self.path_save)+'json')
            json_config = model.to_json()
            with open(path_save, 'w+') as json_file:
                json_file.write(json_config)
        else:
            print('---> Save Type set on Keras.')
            path_save = (str(self.path_save)+'keras')
            model.save(path_save)
        print('-> Deep Learning Model has be saves.')     
    
    def func_test_model(self, test_dataset, model=None):
        model = tensorflow.keras.models.load_model(str(self.path_save)+'keras')
        name = "-> Location: {}, Year: {}".format(self.location, self.year)        
        testing = self.scalerinput.inverse_transform(model.predict(test_dataset))
        # Delete Anomalies
        dl_power = []
        for data in testing:
            if(data[0]) < 0.005:
                data[0] = 0.0
            dl_power.append(data[0])
        
        power = float(sum(dl_power))    
        numpy.savetxt(self.path_dl_power, dl_power, delimiter=',', fmt='%s')                                          
        print(str(name)+', calculated power per year: '+str("{:.3f}".format(power))+' kWp.')
        return dl_power
    
    def generate(self):
        self.func_check_structure()
        self.check_save_model = True   # Uncomment after first test
        if self.check_structure == True:
            self.scaled_train_dataset = self.func_scaling(self.path_train_dataset)
            self.scaled_simu_power = self.func_scaling(self.path_simu_power)
            if self.check_save_model == False:
                self.train_model = self.func_train_model(self.scaled_train_dataset, self.scaled_simu_power)
                self.func_save_model(self.train_model)
            self.scaled_test_dataset = self.func_scaling(self.path_test_dataset)
            self.func_scaling(self.path_simu_power, True)
            self.dl_power = self.func_test_model(self.scaled_test_dataset)

PVA = DLM_PVA_GENERATE('Magdeburg',2015)
PVA.generate()