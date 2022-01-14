import os
import sys
import csv
import numpy
import pandas
import time
from copy import deepcopy

class DLM_PVA_DATASET:
    def __init__(self, location, year):
        self.location = location
        self.year = year
        self.pva_angle = 30
        self.pva_direction = 0
        self.check_structure = False
        self.leap_year = False
        self.dataset = []
        self.correction_dataset = []
        self.all_datasets = []
        self.timescala = []
        self.timestamp = []
        self.zenitdataset = []
        self.azimutdataset = []
        self.sunexposure_normal = []
        self.sunexposure_horizontal = []
        self.ambient_temperature = []
        self.air_temperature = []     
        self.humidity = []           
        self.precipitation = []     
        self.cloud_volume = []      
        self.airpressure = []       
        self.windspeed = []         
        self.winddirection = []    
        self.sunexposure_to_pva = []
        self.longitude = []
        self.latitude = []
        self.sunexposure_directly = []
        self.sunexposure_indirectly = []
  
    def func_check_structure(self):
        root = (os.path.abspath('.'))
        pathweater = (str(root)+'\\datasets_weather\\'+str(self.location)+'\\'+str(self.year))
        pathsun = (str(root)+'\\datasets_sun\\'+str(self.location)+'\\'+str(self.year))
        pathcarnot = (str(root)+'\\datasets_matlab\\'+str(self.year)+'\\'+str(self.location))
        pathpv = (str(root)+'\\datasets_pv\\'+str(self.year)+'\\'+str(self.location))
        self.pathweatherDD = (str(pathweater)+'\\data_DD_MN008.csv')
        self.pathweatherFF = (str(pathweater)+'\\data_FF_MN008.csv')
        self.pathweatherN = (str(pathweater)+'\\data_N_MN008.csv')
        self.pathweatherP0 = (str(pathweater)+'\\data_P0_MN008.csv')
        self.pathweatherR1 = (str(pathweater)+'\\data_R1_MN008.csv')
        self.pathweatherRF = (str(pathweater)+'\\data_RF_TU_MN009.csv')
        self.pathweatherTT = (str(pathweater)+'\\data_TT_TU_MN009.csv')
        self.pathsun = (str(pathsun)+'.csv')
        self.pathinputcarnot = (str(pathcarnot)+'.csv')
        self.pathoutputcarnot = (str(pathcarnot)+'-kWp.csv')
        self.pathinputpvmodule = (str(pathpv)+'.csv')
        self.pathoutputpvmodule = (str(pathpv)+'-kWp.csv')
        path_arr = [self.pathweatherDD, self.pathweatherFF, self.pathweatherN, self.pathweatherP0, self.pathweatherR1,
                    self.pathweatherRF, self.pathweatherTT, self.pathsun, self.pathinputcarnot, self.pathoutputcarnot,
                    self.pathinputpvmodule, self.pathoutputpvmodule]
        check_sum = 0
        
        for path in path_arr:
            if os.path.exists(path) == False:
                if path == self.pathinputcarnot or path == self.pathoutputcarnot:
                    check_dir = os.path.exists(str(root)+'\\datasets_matlab\\'+str(self.year))
                    if check_dir == False:
                        os.makedirs(str(root)+'\\datasets_matlab\\'+str(self.year))
                    check_file = os.path.exists(path)
                    if check_file == False:
                        file = open(path,"w")
                        file.close()
                elif path == self.pathinputpvmodule or path == self.pathoutputpvmodule:
                    check_dir = os.path.exists(str(root)+'\\datasets_pv\\'+str(self.year))
                    if check_dir == False:
                        os.makedirs(str(root)+'\\datasets_pv\\'+str(self.year))
                    check_file = os.path.exists(path)
                    if check_file == False:
                        file = open(path,"w")
                        file.close()
                else:    
                    print(str(path)+' source not exists. Please check or import the source file.')
                    check_sum = check_sum + 1
            if check_sum == 0: self.check_structure = True
        return self.check_structure
    
    def func_leap_year(self):
        if self.year % 4 == 0 or self.year % 100 == 0 or self.year % 400 == 0:
            self.leap_year = True      
        return self.leap_year
    
    def func_timestamp(self):
        self.timescala = ['Timescala']
        self.timestamp = ['Timestamp']
        start = str(self.year)+'0101'
        end = str(self.year+1)+'0101'
        rythm = 0
        time_scala = [d.strftime('%Y%m%d%H%M') for d in pandas.date_range(start, end, freq ='1H')]
        for t in time_scala:   
            self.timescala.append(rythm)                 
            self.timestamp.append(t)
            rythm = rythm + 3600
        self.timescala = self.timescala[:-1]
        self.timestamp = self.timestamp[:-1]
        print('-> Timestamp from: '+str(self.timestamp[1])+', to: '+str(self.timestamp[-1])+' are generate.')
        return self.timescala, self.timestamp
    
    def func_sunangle(self):
        sun_dataset = numpy.array(list(csv.reader(open(self.pathsun, "rt", encoding="utf8"), delimiter=";"))).astype("str")
        row = 0
        self.zenitdataset = ['Zenit-Angle']        
        self.azimutdataset = ['Azimuth-Angle']
        daycount = 365
        if self.leap_year == True: daycount=366 
            
        for col in range(daycount):
            for counter in range(24):
                if sun_dataset[1:,1:][col,row] != '--':
                    self.zenitdataset.append((sun_dataset[1:,1:][col,row]).astype("float"))
                    self.azimutdataset.append((sun_dataset[1:,2:][col,row]).astype("float"))
                else:
                    self.zenitdataset.append(0)
                    self.azimutdataset.append(0)
                row = row + 2 
            row = 0
            
        return self.zenitdataset, self.azimutdataset
    
    def func_sunpower(self):
        self.sunexposure_horizontal = ['Sunpower-Horizontal']
        summer_turn = 14774400
        if self.leap_year == False:
            set_zero = 531.453362255845
            set_diff = 0.114168284050691
            set_max = 31536000
            winter_turn = 30542400
        else:
            set_zero = 532.733690083108
            set_diff = 0.113856313332574
            set_max = 31622400
            winter_turn = 30585600
            
        for second in range(0,set_max,3600):
            if second == 0:
                sun_value = set_zero
            elif second < summer_turn:
                sun_value = sun_value + set_diff
            elif second == summer_turn:
                sun_value = 1000
            else:
                if second < winter_turn:
                    sun_value = sun_value - set_diff
                elif second == winter_turn:
                    sun_value = 500
                else:
                    sun_value = sun_value + set_diff      
            self.sunexposure_horizontal.append(sun_value)

        for c in range(0,len(self.sunexposure_horizontal),1):
            if self.zenitdataset[c] == 0:
                self.sunexposure_horizontal[c] = 0

        return self.sunexposure_horizontal
    
    def func_set_pva_angle(self):
        angle_yn = input('\n->  Is 30 degree the correct photovoltaic system angle? [y/n]: ')
        if angle_yn != ('y' or 'yes' or 'Yes' or 'YES'):
            angle = input('---> What for an angle has your photovoltaic system from the ground? Default is 30. Angle:')
            if int(angle) <= 90 and int(angle) >= 0:
                self.pva_angle = int(angle)
            else:
                print('--!! Wrong Input. Angle set on 30 degree.')
        print('-----> Angle set on '+str(self.pva_angle)+' degree.')
            
        direction_yn = input('-> Stand the module directly to the south? [y/n]: ')
        if direction_yn != ('y' or 'yes' or 'Yes' or 'YES'):
            direction = input('---> What is the correct direction? Eeast = -90 degree, south = 0 degree and west = 90 degree. Direction:')
            if int(direction) >= -90 and int(direction) <= 90:
                self.pva_direction = int(direction)
            else:
                print('--!! Wrong Input. The direction must be between -90 an 90 degree.')
        print('-----> Direction set on '+str(self.pva_direction)+' Degree difference to the south.')                
        return self.pva_angle, self.pva_direction
    
    def func_cloudvolume(self):
        cloud_dataset = numpy.array(list(csv.reader(open(self.pathweatherN, "rt", encoding="utf8"), delimiter=","))).astype("str")
        self.cloud_volume = ['Cloud-Volume']
        correction_dataset = []

        for col in cloud_dataset[1:,3]:
            if col == '0': col_data = 0.9
            elif col == '1': col_data = 0.8
            elif col == '2': col_data = 0.7
            elif col == '3': col_data = 0.6
            elif col == '4': col_data = 0.5
            elif col == '5': col_data = 0.4
            elif col == '6': col_data = 0.3
            elif col == '7': col_data = 0.2
            elif col == '8': col_data = 0.1
            else: col_data = 0.0
            self.cloud_volume.append(col_data)
        
        if (len(self.cloud_volume[1:]))!=(len(self.timestamp[1:])):
            quality = (len(self.cloud_volume)/(len(self.timestamp)))*100
            if quality > 100:
                quality = quality - ((len(self.timestamp)-1)*100)
            print('!! Dataset Cloud-Volume quality: '+str("{:.2f}".format(quality))+'% - Correction in progress...',end='')

            for _ in range(len(self.timestamp[1:])):
                correction_dataset.append(403)

            for test in self.timestamp[1:]:            
                test_count = 0
                for col in cloud_dataset[1:,2:4]:
                    if col[0] == test:
                        if col[1] == '0': col_data = 0.9
                        elif col[1] == '1': col_data = 0.8
                        elif col[1] == '2': col_data = 0.7
                        elif col[1] == '3': col_data = 0.6
                        elif col[1] == '4': col_data = 0.5
                        elif col[1] == '5': col_data = 0.4
                        elif col[1] == '6': col_data = 0.3
                        elif col[1] == '7': col_data = 0.2
                        elif col[1] == '8': col_data = 0.1
                        else: col_data = 0.0
                        correction_dataset[test_count] = col_data
                    test_count = test_count + 1

            correction = self.correction(correction_dataset)
            self.cloud_volume = ['Cloud-Volume']
            for c in correction:
                self.cloud_volume.append(c)
        return self.cloud_volume
    
    def func_longitude(self):
        self.longitude = ['Longitude']
        
        for azimut in self.azimutdataset[1:]:
            azimut = float(azimut)
            sunpower_default = (azimut+self.pva_direction)
            if sunpower_default < 0:
                sunpower_default = 360 + sunpower_default
            if sunpower_default >= 360:
                sunpower_default = sunpower_default - 360
            self.longitude.append(sunpower_default)
        return self.longitude
    
    def func_sunexposure(self):
        self.sunexposure_to_pva = ['Sunexposure-Default']
        self.sunexposure_directly = ['Sunexposure-Directly']
        self.sunexposure_indirectly = ['Sunexposure-Indirectly']
        self.latitude = ['Latidude']
        self.sunexposure_directly_simu = ['Sunexposure-Directly-Simu']
        self.sunexposure_indirectly_simu = ['Sunexposure-Indirectly-Simu']
        count = 1
        
        for zenit in self.zenitdataset[1:]:
            zenit = float(zenit)
            if zenit <= 0:
                self.sunexposure_to_pva.append(0)
                self.sunexposure_directly.append(0)
                self.sunexposure_indirectly.append(0)
                self.latitude.append(0)
                self.sunexposure_indirectly_simu.append(0)
                self.sunexposure_directly_simu.append(0)
            elif zenit > 0 and zenit <= (90-self.pva_angle):
                sunpower_default = (zenit+self.pva_angle)         
                self.sunexposure_to_pva.append(sunpower_default)
                self.latitude.append(sunpower_default)
                sunpower_default = (((zenit+self.pva_angle)/90)*(self.sunexposure_horizontal[count]))
                self.sunexposure_directly.append(sunpower_default) 
                sunpower_default = ((((zenit+self.pva_angle)/90)*(self.sunexposure_horizontal[count]))-((((zenit+self.pva_angle)/90)*(self.sunexposure_horizontal[count]))*(float(self.cloud_volume[count]))))
                self.sunexposure_indirectly.append(sunpower_default)
                self.sunexposure_directly_simu.append(self.sunexposure_horizontal[count])
                self.sunexposure_indirectly_simu.append((self.sunexposure_horizontal[count])*(float(self.cloud_volume[count])))
            else:
                sunpower_default = (90-(zenit-(90-self.pva_angle)))                                    
                self.sunexposure_to_pva.append(sunpower_default)
                self.latitude.append(sunpower_default)
                sunpower_default = ((((((zenit+(90-self.pva_angle))/90)-1)*-1)+1)*(self.sunexposure_horizontal[count]))
                self.sunexposure_directly.append(sunpower_default)
                sunpower_default = (((((((zenit+self.pva_angle)/90)-1)*-1)+1)*(self.sunexposure_horizontal[count]))-(((((((zenit+self.pva_angle)/90)-1)*-1)+1)*(self.sunexposure_horizontal[count]))*(float(self.cloud_volume[count]))))
                self.sunexposure_indirectly.append(sunpower_default)     
                self.sunexposure_directly_simu.append(self.sunexposure_horizontal[count])
                self.sunexposure_indirectly_simu.append((self.sunexposure_horizontal[count])*(float(self.cloud_volume[count])))
            count = count+1  
        self.sunexposure_normal = deepcopy(self.sunexposure_directly)
        self.sunexposure_normal[0] = 'Sunexposure-Normal'
        return self.sunexposure_normal, self.sunexposure_to_pva, self.sunexposure_directly, self.sunexposure_indirectly, self.latitude, self.sunexposure_directly_simu, self.sunexposure_indirectly_simu

    def func_temperature(self):
        temp_dataset = numpy.array(list(csv.reader(open(self.pathweatherTT, "rt", encoding="utf8"), delimiter=","))).astype("str")   
        self.ambient_temperature = self.select_data(temp_dataset, 'Ambient Temperature')
        self.ambient_temperature = self.init_correction(self.ambient_temperature, temp_dataset) 
        self.air_temperature = deepcopy(self.ambient_temperature)
        self.air_temperature[0] = 'Air Temperature'
        return self.air_temperature, self.ambient_temperature
    
    def func_airpressur(self):
        air_dataset = numpy.array(list(csv.reader(open(self.pathweatherP0, "rt", encoding="utf8"), delimiter=","))).astype("str")
        self.airpressure = self.select_data(air_dataset, 'Airpressure')
        self.airpressure = self.init_correction(self.airpressure, air_dataset)
        conversion = ['Airpressure']
        for hPa in self.airpressure[1:]:
            Pa = hPa*100
            conversion.append(Pa)
        self.airpressure = conversion    
        return self.airpressure
        
    def func_humidity(self):
        humidity_dataset = numpy.array(list(csv.reader(open(self.pathweatherRF, "rt", encoding="utf8"), delimiter=","))).astype("str")
        self.humidity = self.select_data(humidity_dataset, 'Humidity')
        self.humidity = self.init_correction(self.humidity, humidity_dataset) 
        return self.humidity
    
    def func_precipitation(self):
        precipitation_dataset = numpy.array(list(csv.reader(open(self.pathweatherR1, "rt", encoding="utf8"), delimiter=","))).astype("str")
        self.precipitation = self.select_data(precipitation_dataset, 'Precipitation')
        self.precipitation = self.init_correction(self.precipitation, precipitation_dataset) 
        return self.precipitation
    
    def func_winddirection(self):
        winddirection_dataset = numpy.array(list(csv.reader(open(self.pathweatherDD, "rt", encoding="utf8"), delimiter=","))).astype("str")
        self.winddirection = self.select_data(winddirection_dataset, 'Wind-Direction')
        self.winddirection = self.init_correction(self.winddirection, winddirection_dataset) 
        return self.winddirection
    
    def func_windspeed(self):  
        windspeed_dataset = numpy.array(list(csv.reader(open(self.pathweatherFF, "rt", encoding="utf8"), delimiter=","))).astype("str")
        self.windspeed = self.select_data(windspeed_dataset, 'Wind-Speed')
        self.windspeed = self.init_correction(self.windspeed, windspeed_dataset) 
        return self.windspeed
    
    def select_data(self, result, header):
        dataset=[header]
        for col in result[1:,3]:
            dataset.append(col.astype(float))
        return dataset
    
    def init_correction(self, dataset, result):
        if(len(dataset)!=len(self.timestamp)):
            quality = len(dataset)/len(self.timestamp)*100
            if quality > 100:
                quality = len(self.timestamp)/len(dataset)*100   
            print('!! Dataset '+str(dataset[0])+' quality: '+str("{:.2f}".format(quality))+'% - correction in progress...', end='')

            correctiondataset = []
            for _ in range(len(self.timestamp[1:])):
                correctiondataset.append(403)

            for test in self.timestamp[1:]:
                testcount = 0
                for col in result[1:,2:4]:
                    if col[0] == test:
                        correctiondataset[testcount] = col[1]
                    testcount = testcount + 1
            correction_dataset = self.correction(correctiondataset)
            dataset = [dataset[0]]
            for c in correction_dataset:
                dataset.append(c)
        correction_dataset = dataset
        return correction_dataset
            
    def correction(self, correctiondataset):
        correctioncount = 0
        for data in correctiondataset:
            if data == 403:
                data_m5 = float(correctiondataset[correctioncount-5])
                data_m4 = float(correctiondataset[correctioncount-4])
                data_m3 = float(correctiondataset[correctioncount-3])
                data_m2 = float(correctiondataset[correctioncount-2])
                data_m1 = float(correctiondataset[correctioncount-1])
                data_p1 = self.select_correction(correctioncount, correctiondataset)
                data_p2 = self.select_correction(correctioncount, correctiondataset)
                data_p3 = self.select_correction(correctioncount, correctiondataset)
                data_p4 = self.select_correction(correctioncount, correctiondataset)
                data_p5 = self.select_correction(correctioncount, correctiondataset)
                correction = (data_m1+data_m2+data_m3+data_m4+data_m5+data_p1+data_p2+data_p3+data_p4+data_p5)/10.0
                correctiondataset[correctioncount] = "{:.1f}".format(correction)
            correctioncount = correctioncount + 1
        print(' Quality updated to 100%')
        return correctiondataset
    
    def select_correction(self, correction_count, correction_dataset):
        data_m1 = float(correction_dataset[correction_count-1])
        data_m2 = float(correction_dataset[correction_count-2])
        data_m3 = float(correction_dataset[correction_count-3])
        data_m4 = float(correction_dataset[correction_count-4])
        data_m5 = float(correction_dataset[correction_count-5])
        if (correction_count+1) < len(self.timestamp[1:]):
            dataset = float(correction_dataset[correction_count+1])
            if (dataset == 403):
                dataset = (data_m1+data_m2+data_m3+data_m4+data_m5)/5.0
        else: dataset = (data_m1+data_m2+data_m3+data_m4+data_m5)/5.0
        return dataset
    
    def func_save(self):
        self.all_datasets = [self.timescala, self.timestamp, self.zenitdataset, self.azimutdataset,
                             self.sunexposure_normal, self.sunexposure_horizontal, self.ambient_temperature,
                             self.air_temperature, self.humidity, self.precipitation, self.cloud_volume,
                             self.airpressure, self.windspeed, self.winddirection, self.sunexposure_to_pva,
                             self.longitude, self.latitude, self.sunexposure_directly, self.sunexposure_indirectly, 
                             self.sunexposure_directly_simu, self.sunexposure_indirectly_simu]
        
        function_type = input('\n-> Select the save module for the dataset:\n--->MATLAB press [m/M] or DLM-PVA press [p/P]: ')
        
        if function_type == ('m' or 'M'):
            DS1 = numpy.array(self.all_datasets[0])
            DS2 = numpy.array(self.all_datasets[1])
            DS3 = numpy.array(self.all_datasets[2])
            DS4 = numpy.array(self.all_datasets[3])
            DS5 = numpy.array(self.all_datasets[4])
            DS6 = numpy.array(self.all_datasets[5])
            DS7 = numpy.array(self.all_datasets[6])
            DS8 = numpy.array(self.all_datasets[7])
            DS9 = numpy.array(self.all_datasets[8])
            DS10 = numpy.array(self.all_datasets[9])
            DS11 = numpy.array(self.all_datasets[10])
            DS12 = numpy.array(self.all_datasets[11])
            DS13 = numpy.array(self.all_datasets[12])
            DS14 = numpy.array(self.all_datasets[13])
            DS15 = numpy.array(self.all_datasets[2])
            DS16 = numpy.array(self.all_datasets[15])
            DS17 = numpy.array(self.all_datasets[16])
            DS18 = numpy.array(self.all_datasets[19])
            DS19 = numpy.array(self.all_datasets[20])
            self.dataset = numpy.column_stack((DS1,DS2,DS3,DS4,DS5,DS6,DS7,DS8,DS9,DS10,DS11,DS12,DS13,DS14,DS15,DS16,DS17,DS18,DS19))
            numpy.savetxt('./datasets_matlab/'+str(self.year)+str('/')+str(self.location)+'.csv', self.dataset, delimiter=',', fmt='%s')
            return self.dataset
        
        elif function_type == ('p' or 'P'):
            DS5 = numpy.array(self.all_datasets[6])
            DS4 = numpy.array(self.all_datasets[10])
            DS2 = numpy.array(self.all_datasets[15])
            DS3 = numpy.array(self.all_datasets[16])
            DS1 = numpy.array(self.all_datasets[17])
            DS6 = numpy.array(self.all_datasets[18])
            self.dataset = numpy.column_stack((DS1,DS2,DS3,DS4,DS5,DS6))
            numpy.savetxt('./datasets_pv/'+str(self.year)+str('/')+str(self.location)+'.csv', self.dataset, delimiter=',', fmt='%s')
            return self.dataset
        
        else: print('!! Wrong Input. Select <CLASS-NAME>.func_save\(\) to save Dataset.')
    
    def generate(self):
        self.func_check_structure()
        if self.check_structure == True:
            self.func_set_pva_angle()
            start = time.time()
            self.func_leap_year()
            self.func_timestamp()
            self.func_sunangle()
            self.func_cloudvolume()
            self.func_sunpower()
            self.func_sunexposure()
            self.func_longitude()
            self.func_temperature()
            self.func_airpressur()
            self.func_humidity()
            self.func_precipitation()
            self.func_winddirection()
            self.func_windspeed()  
            ende = time.time()
            self.func_save()
            print('\n-> Berechnungszeit = {:5.3f}s'.format(ende-start))

PVA = DLM_PVA_DATASET('Magdeburg',2015)
PVA.generate()
PVA.func_save()