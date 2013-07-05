import numpy
import scipy
from scipy import integrate
from scipy.optimize import leastsq
from pylab import plot, show


def func_yp(y_p, R_p, y):
    if y < 0:
        return 0
    elif y == 0:
        return 0
    else:
        return (R_p**2 - (y_p -y)**2)**0.5/y**0.5 + 1.0

def lcurve(R_p,R_n,b):
    #light curve data
    l_m = []
    for element in y_p:
        #Luminous part of the large disk
        func = lambda y: func_yp(element, R_p, y)
        if element <= - R_p:
            m = 0
        if (element > - R_p and element < R_p):
            m = integrate.quad(func, 0, R_p+element)[0] 
        if element > R_p:
            m = integrate.quad(func, element - R_p, R_p + element)[0]
        #Dark part of the large disk / small disk
        y_n_i = element + b
        func2 = lambda t: func_yp(element+b, R_n, t)
        if element+b <= -R_n:
            n = 0
        if (element+b > - R_n and element+b < R_n ):
            n  = integrate.quad(func2, 0, R_n + element+b)[0]
        if element +b > R_n:
            n = integrate.quad(func2,element +b - R_n, R_n + element +b)[0]
        #Subtracting them
        l_m = l_m +[m-n]
    #Division by surface area
    Area = numpy.pi*R_p**2 - numpy.pi*R_n**2
    l_m = numpy.array(l_m)/Area
    return l_m

def read():
    fil = open('../wambsganss/out_line')
    all = fil.readlines()[175:275]
    x = []
    y = []
    for l in all:
        s = l.split()
        x.append(int(s[0]))
        y.append(float(s[4]))
    return x,y

def resid(params):
    global N,y_p,data
    print params
    ymin,ymax,Rn,b,floor,slope = params
    Rp = 1.
    f = Rn + abs(b)
    if f > 1:
        Rn /= f
        b /= f
    y_p = numpy.linspace(ymin,ymax,len(data))
    return lcurve(Rp,Rn,b) + floor + slope*y_p - data


time,data = read()
trial = (-5.,5.,0.8,-.2,1,0)
fit = trial
fit = leastsq(resid,trial)[0]
model = resid(fit) + data

plot(time,data)
plot(time,model)

show()
