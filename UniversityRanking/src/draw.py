"""
@author: Bolun
@description: Drawings
"""

from pylab import rcParams
import matplotlib.pyplot as plt

class draw_sensitivity:
    def __init__(self):
        """"""
    def run(self):
        x_axis = [i for i in range(51)]
        x_label = [str(i) for i in range(51)]
        
        x_axis_tick = []
        x_label_tick = []
        
        for i in range(len(x_axis)):
            if i%2 == 0:
                x_axis_tick.append(x_axis[i])
                x_label_tick.append(x_label[i])
         
        y_axis = [i for i in range(50)]
        y_label = [] # univ names
         
        lower = []
        upper = []
        bounds = []
         
        f = open("../result/result_top50_cs_newdata_apr09/sensitivity/all/sensitivity_diff_weightedPR_wo_norm+mit1.csv","r")
        f.readline()
        i = 1
        for line in f:
            lines = line.split(",")
            if len(lines) == 2:
                y_label.append(lines[0].strip())
                upper.append(i-int(lines[1].strip()))
            elif len(lines) == 1:
                y_label.append(lines[0].strip())
                upper.append(i)
            else:
                pass
            i += 1
        f.close()
        print "i", i
        f = open("../result/result_top50_cs_newdata_apr09/sensitivity/all/sensitivity_diff_weightedPR_wo_norm-inedge1.csv","r")
        f.readline()
        i = 1
        for line in f:
            lines = line.split(",")
            if len(lines) == 2:
                lower.append(i-int(lines[1].strip()))
            elif len(lines) == 1:
                lower.append(i)
            else:
                pass
            i += 1
        f.close()
        
        for i in range(len(upper)):
            bounds.append(abs(upper[i]-lower[i])+0.25)
        
        print y_label
        print lower
        print upper
        print bounds
        
        rcParams['figure.figsize'] = 36, 16
        plt.bar(y_axis, bounds, bottom = upper, width = 0.8, color = 'b')
        plt.xticks(y_axis,y_label, rotation='vertical', fontsize = 15)
        plt.yticks(x_axis_tick,x_label_tick, fontsize = 15)
        plt.xlabel("Universities")
        plt.ylabel("Rank")
        plt.grid(True)
        plt.title("Rank Variation Bound - PRwonorm", fontsize = 30)
        plt.savefig("../result/result_top50_cs_newdata_apr09/sensitivity/all/figs/sensitivity_weightedPR_wo_norm.png", dpi=50)

class draw_statistics:
    def __init__(self, path):
        self.path = path #"../result/result_top50_cs_newdata_apr09/statistics/year_cdf.csv"
        
    def run(self):
        x = []
        year = []
        freq = []
        cdf = []
        f = open(self.path, "r")
        f.readline()
        i = 0
        for line in f:
            lines = line.split(",")
            x.append(i)
            year.append(int(lines[0].strip()))
            freq.append(int(lines[1].strip()))
            cdf.append(float(lines[2].strip()))
            i += 1
        f.close()
        
        xticks = []
        xlabel = []
        
        for i in range(len(year)):
            if year[i]%5 == 0:
                xticks.append(x[i])
                xlabel.append(str(year[i]))
        
        yticks = []
        ylabel = []
        for i in xrange(0,61,5):
            yticks.append(i)
            ylabel.append(str(i))
        
        rcParams['figure.figsize'] = 36, 16
        plt.bar(x, freq, width = 0.8, color = 'b', alpha = 0.6)
        plt.xticks(xticks,xlabel, fontsize = 20)
        plt.yticks(yticks,ylabel, fontsize = 20)
        plt.xlabel("Year", fontsize = 25)
        plt.ylabel("Frequency-#Faculty", fontsize = 25)
        plt.xlim(0,68)
        plt.ylim(0,50)
        plt.grid(True)
        plt.title("Year Distribution of Faculties - MechEng", fontsize = 30)
        plt.savefig("../result/me/me_year_distribution.png", dpi=50)
        plt.clf()
        
        yticks = []
        ylabel = []
        for i in xrange(0,101,5):
            yticks.append(i/float(100))
            ylabel.append(str(i/float(100)))
        
        plt.bar(x,cdf, width = 1.0, color = 'b', alpha = 0.6)
        plt.xlim(0,68)
        plt.ylim(0,1)
        plt.xticks(xticks,xlabel, fontsize = 20)
        plt.yticks(yticks,ylabel, fontsize = 20)
        plt.xlabel("Year", fontsize = 25)
        plt.ylabel("Percentile", fontsize = 25)
        plt.title("Year CDF - MechEng", fontsize = 30)
        plt.grid(True)
        #plt.arrow(x, y, dx, dy, hold)
        plt.savefig("../result/me/me_year_cdf.png", dpi=50)        
        plt.clf()

dst = draw_statistics("../result/me/year_cdf.csv")
dst.run()


# plt.show()

# import matplotlib
# from pylab import *
# 
# val = 3+10*rand(5)    # the bar lengths
# pos = arange(5)+.5    # the bar centers on the y axis
# print pos
# figure(1)
# barh(pos,val, align='center')
# yticks(pos, ('Tom', 'Dick', 'Harry', 'Slim', 'Jim'))
# xlabel('Performance')
# title('horizontal bar chart using matplotlib')
# grid(True)
# show()
# 
# plt.show()