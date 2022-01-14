import numpy, csv, os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook

class DLM_DIAGRAM_GENERATE:
    def __init__(self, location, year):
        self.location = location
        self.year = year
        self.dl_data = []
        self.simu_data = []
        self.save_path = '.\\datasets_pv\\'+str(year)+'\\'
    
    def set_datasets(self):
        import_dl_data = numpy.array(list(csv.reader(open('.\\datasets_pv\\'+str(self.year)+'\\'+str(self.location)+'-kWp.csv', "rt", encoding="utf8"), delimiter=","))).astype(str)
        import_simu_data = numpy.array(list(csv.reader(open('.\\datasets_matlab\\'+str(self.year)+'\\'+str(self.location)+'-kWp.csv', "rt", encoding="utf8"), delimiter=","))).astype(str)
        for v in range(len(import_dl_data)):
            self.dl_data.append(float(import_dl_data[v][0]))
            self.simu_data.append(float(import_simu_data[v][0]))
        return

    def get_diagram_year_in_days(self):
        period = 365
        new_dl_data = []
        new_simu_data = []
        count = 0
        for _ in range(period):
            sum_month_dl = 0
            sum_month_simu = 0
            for _ in range(24):
                sum_month_dl = sum_month_dl + self.dl_data[count]
                sum_month_simu = sum_month_simu + self.simu_data[count]
                count = count + 1
            new_dl_data.append(sum_month_dl)
            new_simu_data.append(sum_month_simu)
        timeline = [y for y in range(period)]
        prt_dl_data = new_dl_data
        prt_simu_data = new_simu_data
        plt.plot(timeline, prt_dl_data, label = "DL-Data")
        plt.plot(timeline, prt_simu_data, label = "SIMU-Data")
        plt.xlabel('Days')
        plt.ylabel('Power in kWp per Day')
        plt.title('PVA-Power - '+str(self.location)+' '+str(self.year))
        plt.legend()
        plt.savefig(str(self.save_path)+'\\year_in_days.png')
        plt.show()

    def get_diagram_month_in_days(self):
        period = 31
        new_dl_data = []
        new_simu_data = []
        count = 0
        for _ in range(58,period+58):
            sum_month_dl = 0
            sum_month_simu = 0
            for _ in range(24):
                sum_month_dl = sum_month_dl + self.dl_data[count]
                sum_month_simu = sum_month_simu + self.simu_data[count]
                count = count + 1
            new_dl_data.append(sum_month_dl)
            new_simu_data.append(sum_month_simu)
        timeline = [y for y in range(period)]
        prt_dl_data = new_dl_data
        prt_simu_data = new_simu_data
        plt.plot(timeline, prt_dl_data, label = "DL-Data")
        plt.plot(timeline, prt_simu_data, label = "SIMU-Data")
        plt.xlabel('Days')
        plt.ylabel('Power in kWp per Day')
        plt.title('PVA-Power - '+str(self.location)+' Februar '+str(self.year))
        plt.legend()
        plt.savefig(str(self.save_path)+'\\month_in_days.png')
        plt.show()

    def get_diagram_day_in_hours(self, starting_day):
        timeline = [y for y in range(starting_day,starting_day+24)]
        prt_dl_data = self.dl_data[starting_day:starting_day+24]
        prt_simu_data = self.simu_data[starting_day:starting_day+24]
        plt.plot(timeline, prt_dl_data, label = "DL-Data")
        plt.plot(timeline, prt_simu_data, label = "SIMU-Data")
        plt.xlabel('Hour')
        plt.ylabel('Power in kWp per Hour')
        plt.title('PVA-Power - '+str(self.location)+' 30.05.2010')
        plt.legend()
        plt.savefig(str(self.save_path)+'\\day_in_hours.png')
        plt.show()

    def print_diagram(self):
        self.set_datasets()
        self.get_diagram_year_in_days()
        self.get_diagram_month_in_days()
        self.get_diagram_day_in_hours(150*24)

PVA = DLM_DIAGRAM_GENERATE('Magdeburg', 2015)
PVA.print_diagram()