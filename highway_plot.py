# Generic plot of where the planes gly

import sys
import gzip
import bz2
from collections import defaultdict
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from numpy import *



# Parse our wkt (well-known text) format. Technically, I think we're not
# wkt compliant because our individual data values are 
# (lon, lat, alt, seconds_since_epoc). Other parsers seem to choke on
# more than 2 or 3 values, which seems simple-minded to me.
def parseWkt(s):
    s2 = s.replace("LINESTRING (","").replace(")","");
    vals = s2.split(",")

    array2d = [[float(digit) for digit in line.split()] for line in vals]
    return array2d;


# Globals
crop_region='usa_main' #sfbay, world, ukraine
color='b'
alpha='0.6'  #Transparency. 0.6 seems ok
resolution='h' #Set level-of-detail on maps: c,l,h
linewidth=0.06 #Thickness. 0.06 is thin enough
split_datelines = True #T=Accurate,slower, F=bugs, but quicker 



# Grab the simple args
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = raw_input('Enter wkt file: ');

if len(sys.argv) > 2:
    filename_o = sys.argv[2]
else:
    filename_o = ""


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


wrap_count=0
line_count=0

if filename.endswith(".gz"):
    file = gzip.open(filename)
elif filename.endswith(".bz2"):
    file = bz2.BZ2File(filename)
else:
    file = open(filename)


# If we're given data that's had dateline splits
# removed, or we just want to be quicker, set the
# is_split to false, so we always execute the full
# route render
is_split = split_datelines

for line in file:

    (np,tag,swkt)=line.split('\t');
    (plane,airline,src,dst)=tag.split('|')

    data = parseWkt(swkt)
    a = asarray(data)
    x = a[:,0]
    y = a[:,1]

    if (split_datelines):
        # Look for date-line wrap 
        xa = concatenate((x,   [x[len(x)-1]]),1)
        xb = concatenate(([x[0]],x),1)        
        diff = abs(xa-xb)
        indices = nonzero(diff>100) # look for big jumps
        if(size(indices[0])): 

            start=0 #idx of first point
            for spot in indices[0]:
                #Plot each segment that doesn't cross
                mx,my=m(x[start:spot],y[start:spot])
                m.plot(mx, my,color,alpha=alpha,lw=linewidth)
                start=spot
                wrap_count=wrap_count+1
            is_split=True #Make sure don't redraw this

        else:
            is_split=False
        
    #Either not doing splits, or this didn't have one
    if (not is_split):
        # No wrap around, just plot
        mx,my=m(x,y)
        m.plot(mx, my,color,alpha=alpha,lw=linewidth)

    line_count=line_count+1
        
        

print "Done. Number of dateline wraps: "+str(wrap_count)

if (filename_o == ""):
    plt.show()
else:
    plt.savefig(filename_o)

