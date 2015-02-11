# This plotter is a tool for discovering locations where there isn't 
# much coverage. It inspects each flight and looks for segments that
# had a longer travel time than we expected. If the duration is above 
# a threshold, we plot the segment.
#
# eg. if you grabbed data every 6 minutes, you'd hope that each segment 
# in a track would be about 6 minutes (plus some for extra for book
# keeping). If a segment was 12 or 18 minutes, you'd suspect that 
# 2 or 3 samples were missing.

import sys
from math import *
from collections import defaultdict
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from numpy import *
import gzip
import bz2

# Globals
crop_region='world' #'usa_main' #sfbay, world, ukraine
color='b'      #Line color. Can also do '-ob' for line w/ points
alpha='0.50'   #How faint to make the line.
resolution='l' #Set level-of-detail on maps: c,l,h
linewidth=1.0  #How thick to make the line
sampleperiod=400 #every 6minutes with some gap

# Parse our wkt (well-known text) format. Technically, I think we're not
# wkt compliant because our individual data values are 
# (lon, lat, alt, seconds_since_epoc). Other parsers seem to choke on
# more than 2 or 3 values, which seems simple-minded to me.
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



# Set up the plt window
fig = plt.figure()
ax=fig.add_axes([0.1,0.1,0.8,0.8])

# Some regions of interest lon1,lat1, lon2,lat2
lims = defaultdict(list)
lims['sfbay']         = [-126.0, 36.0, -119.0, 40.0]
lims['ukraine']       = [  19.0, 42.0,   43.0, 54.0]
lims['mediterranean'] = [ -70.0,  5.0,   75.0, 55.0]
lims['world']         = [-180.0,-60.0,  180.0, 80.0]
lims['nscamerica']    = [-180.0,-60.0,  -30.0, 80.0]
lims['usa_con']       = [-175.0, 24.0,  -40.0, 72.0]
lims['usa_main']      = [-130.0, 23.0,  -62.0, 50.0]

lm = lims[crop_region]
m = Basemap(projection='merc', lat_0 = 0, lon_0 = 0, lat_ts=20.,
            resolution = resolution, area_thresh = 0.1,
            llcrnrlon=lm[0], llcrnrlat=lm[1],
            urcrnrlon=lm[2], urcrnrlat=lm[3])

# Map options
#m.bluemarble() #Use images for backgound. Hard to see routes
m.drawlsmask() #Nice grey outlines
#m.drawcoastlines(linewidth=0.2)  #Unfortunately, has lakes too
m.drawcountries()
#plt.show() #Just to test out



lengths=[]
start_loc=[]
val=0;
toss_count=0




if filename.endswith(".gz"):
    file = gzip.open(filename)
elif filename.endswith(".bz2"):
    file = bz2.BZ2File(filename)
else:
    file = open(filename)


for line in file:
    #print line
    (np,tag,swkt)=line.split('\t');
    (plane,airline,src,dst)=tag.split('|')

               
    #if(np<4):
    #    continue    

    data = parseWkt(swkt)
               
    d=0.0
    dist=[]
    alt=[]
    speed=[]

    for i in range(len(data)):
            
        if (i==0):
            continue           

        lon1=data[i][0]
        lon2=data[i-1][0]
        lat1=data[i][1]
        lat2=data[i-1][1]

        mi = haversine(lon1, lat1, lon2, lat2)
        t=data[i][3]-data[i-1][3]

        #Look for segments that were longer than a certain
        #duration, and were actually in the air
        #if((t>2*sampleperiod) and (t<4*sampleperiod) 
        if((t>3*sampleperiod) 
              and (data[i-1][2]>500.0) and (data[i][2]>500.0)):
            tmpx=(data[i-1][0], data[i][0])
            tmpy=(data[i-1][1], data[i][1])
            mx,my=m(tmpx,tmpy)
            m.plot(mx, my, color, alpha=alpha, lw=linewidth)
            

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

    val=val+1
    #if(val>100):
    #   break



plt.show()
