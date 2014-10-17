import sys
from math import *
import matplotlib.pyplot as plt
from numpy import *


# Globals
color='b'     #Line color. Can also do '-ob' for line w/ points
alpha='0.20'  #How faint to make the line.
linewidth=1.5 #How thick to make the line

# Hardcode airports for now. Code is smart enough to let you
# add more to this list.
airports = ['SFO','ATL','ABQ','CHS']


# parse my wkt format, which is not technically compliant wkt because
# individual vals are (lon,lat,alt,seconds_since_epoc). Other wkt 
# parsers don't like more than 2 or 3 vals.
def parseWkt(s):
    s2 = s.replace("LINESTRING (","").replace(")","");
    vals = s2.split(",")

    array2d = [[float(digit) for digit in line.split()] for line in vals]
    return array2d;


# Computing distance based on coordinates isn't easy. Remember, lon
# gets smaller as you get near the poles. Haversine is the standard
# op people do to convert to angles and map to distance. This version is
# all based at sea level, and doesn't take into account altitude.
def haversine(lon1, lat1, lon2, lat2):
    degree_to_rad = float(pi/180.0)
    
    d_lat = (lat2 - lat1) * degree_to_rad
    d_lon = (lon2 - lon1) * degree_to_rad
    
    a=pow(sin(d_lat/2),2) + cos(lat1 * degree_to_rad) *  cos(lat2 * degree_to_rad) * pow(sin(d_lon/2),2)
    c=2*atan2(sqrt(a),sqrt(1-a))
    mi = 3956 * c
    return mi

# pylab kludge to make labels readable
def fmt_commas(val, pos=None):
    s = '%d' % val
    groups = []
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    return s + ','.join(reversed(groups))



if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = raw_input('Enter data filename: ')




plt.figure(figsize=(20,5))

num_cols = len(airports)
lengths=[]
start_loc=[]
cutoff=6000.0
val=0;
toss_count=0

with open(filename) as text:
    for line in text:
        (np,tag,swkt)=line.split('\t');
        (plane,airline,src,dst)=tag.split('|')


        if not (src in airports):
            continue

        
        if(np<4):
            continue    

        data = parseWkt(swkt)
               
        d=0.0
        dist=[]
        alt=[]
        speed=[]

        if(data[0][2] > cutoff):
            continue
       

        for i in range(len(data)):
            
            if (i==0):
                continue           

            lon1=data[i][0]
            lon2=data[i-1][0]
            lat1=data[i][1]
            lat2=data[i-1][1]

            mi = haversine(lon1, lat1, lon2, lat2)
            t=data[i][3]-data[i-1][3]

            if(t==0):
                print "Bad time at ",i
                t=1

            mph = (3600.0*mi)/t

            d=d+mi
            dmi=d #d*0.000189394;

            dist.append(dmi)
            alt.append(data[i][2]/5280.0)
            speed.append(mph)

        lengths.append(dmi)
        speed_max=max(speed)

        if(dmi>6000):
            print "Long distance", src,dst,dmi,speed_max

        #if(1):
        if(speed_max <3000):
        #if (speed_max < 800):
        #if(dmi>4000) and (dmi<4200):
        
            idx = airports.index(src) + 1

            #print "xx:", src,idx,dst,dmi, speed_max
            
            plt.subplot(num_cols,1,idx)
            plt.plot(dist,alt, color, alpha=alpha,lw=linewidth)
            plt.xlim((0,9000))
            # if you want to see how out of whack speed can get
            #plt.subplot(num_cols,1,num_cols+idx)
            #plt.plot(dist,speed, color, alpha=alpha,lw=linewidth)
            val=val+1
        else:
            toss_count=toss_count+1

        val=val+1
        #if(val>100):
        #   break


print "Toss Count ",toss_count
#plt.subplot(212)
#plt.hist(lengths,100)

for i in range(num_cols):
    print i

    if(i<num_cols-1):
        plt.subplot(num_cols,1,i+1); plt.gca().axes.get_xaxis().set_visible(False); 
    else:
        plt.subplot(num_cols,1,num_cols); plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(fmt_commas))
    ax = plt.gca()
    ax.text(0.99, 0.90, airports[i],
        verticalalignment='top', horizontalalignment='right',
        transform=ax.transAxes,
        color='red', fontsize=24)

plt.show()
