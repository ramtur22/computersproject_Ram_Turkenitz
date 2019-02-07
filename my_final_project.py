# Python final project

# input file handling:
#this function converts the file to a dictionary with the keys being the axis titles dx,dy,x,y lowercased.
def input_handling(input_file):
    file1=open(input_file,'r')
    lines=file1.readlines()
    data_dict={}
    data_list=[]
    for line in lines:
        line_list=line.strip().split()
        data_list.append(line_list)
    if type(data_list[0][1])==str:
        for x in data_list[0]:
            key= data_list[x].lower()
            data_dict[key]= []
        for item in range(1,(len(data_list)-1)):
            for i in range(0,data_list[item]):
                data_dict[data_list[0][i]].append(data_list[item][i])
    else:
        for i in data_list[0:4]:
            key= i[0].lower()
            data_dict[key]=i[1:]
    X_title= " ".join(data_list[-2][2:])
    Y_title= " ".join(data_list[-1][2:])
    return X_title, Y_title, data_dict

# error checking:
# this function checks for length errors.
def length_errors(dict_of_data):
    listlen=[]
    keys=dict_of_data.keys()
    for key in keys:
        listlen.append(dict_of_data[key])
    if listlen[0]==listlen[1]==listlen[2]==listlen[3]:
        return True
    else:
        return False

#this function checks for uncertainties that are negative.
def uncertainties_errors(dict_of_data):
    for i in dict_of_data[dx]:
        if i<0:
            return False
        else:
            for x in dict_of_data[dy]:
                if x<0:
                    return False
                else:
                    return True

#fitting parameters:
#this function fits the data numbers to the correct variables that are to be used in the algorithms:
from matplotlib import numpy
def fitting_variables_calculating_parameters(dict_of_data):
    x=dict_of_data.get(x)
    dx=dict_of_data.get(dx)
    y=dict_of_data.get(y)
    dy=dict_of_data.get(dy)
    N=len(x)
    x_roof,x_square_roof,x_roof_square,y_roof,xy_roof,xy_square_roof,dy_square_roof,dy_power_minus2=0,0,0,0,0,0,0,0
    
    #now to assign the data to the variables
    for k in range(0,N):
        x_roof=x_roof+(x[k]/(dy[k]**2))
        y_roof=y_roof+(y[k]/(dy[k]**2))
        xy_roof=xy_roof+((x[k]*y[k])/(dy[k]**2))
        x_square_roof+=((x[k]**2)/(dy[k]**2))
        dy_square_roof+=1
        dy_power_minus2+=(dy[k]**(-2))
    x_roof=x_roof/dy_power_minus2
    y_roof=y_roof/dy_power_minus2
    xy_roof=xy_roof/dy_power_minus2
    x_roof_square=x_roof**2
    x_square_roof=x_square_roof/dy_power_minus2
    dy_square_roof=dy_square_roof/dy_power_minus2
    
    #now we calculate the fitting parameters
    A=(xy_roof-(x_roof*y_roof))/(x_square_roof-x_roof_square)
    dA=numpy.sqrt((dy_square_roof)/(N*(x_square_roof-x_roof_square)))
    B=y_roof-(A*x_roof)
    dB=numpy.sqrt((dy_square_roof*x_square_roof)/(N*(x_square_roof-x_roof_square)))
    
    #chi square calculation
    chi_square=0
    for i in range(0,N):
        chi_square+=((y[i]-(A*x[i]+B))/dy[i])**2
    chi_square_red=chi_square/(N-2)
    
    #print and return the parameters calculated:
    print('a =', A, '+-', dA)
    print('b =', B, '+-', dB)
    print('chi2 =', chi_square)
    print('chi2_reduced =', chi_square_red)
    return A,B
    
#ploting the graphs:
import matplotlib.pyplot as pyplot
from matplotlib import numpy as num

def graph_plotting(dict_of_data,A,B,X_title,Y_title):
    x=dict_of_data.get('x')
    dx=dict_of_data.get('dx')
    y=dict_of_data.get('y')
    dy=dict_of_data.get('dy')  
    
    x_array=num.array(x)
    lin_fun=A*x_array+B
    
    #graph plotting with errorbars
    pyplot.plot(x_array,lin_fun,'r')
    pyplot.errorbar(x,y,dx,dy,fmt=none,ecolor='b')
    pyplot.xlabel(x_title)
    pyplot.ylabel(y_title)
    pyplot.show()
    pyplot.savefig('linear_fit.svg')
    
#main function:
def fit_linear(filename):
    
    #first we use the file handking function to transform the file to a dictionary
    x_title,y_title,data_dict= input_handling(filename)
    
    #now the error checking functions will be used to test the data:
    if length_errors(data_dict)==False:
        print('Input file error: Data lists are not the same length.')
        exit()
        
    if uncertainties_errors(data_dict)==False:
        print('Input file error: Not all uncertainties are positive.')
        exit()
    
    #fit and calculate the parameters a,b,chi2 and chi2 reduced:
    a,b=fitting_variables_calculating_parameters(data_dict)
    
    #plot the data into a graph with errors
    graph_plotting(data_dict,a,b,x_title,y_title)
    

print(fit_linear('/inputOutputExamples/input.txt'))
    

    