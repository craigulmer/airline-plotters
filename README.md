airline-plotters
================

Misc scripts for plotting airline tracks

Airport Finder
--------------
This tool walks through a list of routes and tries to figure out what
the coordinates are for all the airports it sees. It does this by
selecting the Source name for flights on the ground and associating
the coordinates with the airport. After walking through the routes,
the coordinates for each airport are averaged together. This of course
won't work well if any of the values are completely wrong. In the future
this should be changed to a majority-wins clustering algorithm.


Cannonball Plot
---------------
This plotter is meant to show how far and high planes travel leaving
from different airports. For simplicity it figures out where a
plane originates from just by using the source tag in the airline
data (not the actual lon/lat). It ignores any flight that doesn't
originate from one of the desired airports, as well as any flight
that begins at an altitude greater than a certain height. This 
program also assumes that flights have already been cut into their
corresponding segments.

Distance for a flight is calculated by summing the Haversine distances
between each point in an airline's track. It does not take into
account altitude.

While writing this I discovered that there are a number of problem
spots in the bigger data set. A number of flights (especially long
ones) are undersampled over the oceans, and therefore distance is 
fuzzy. There were other discrepancies that caused some segments to
have impossible speeds (commercial flights flying faster than the 
speed of sound). Another problem is that some flights don't change
their src/dst values. Therefore you get some ups and downs, or 
unexpectedly long voyages. The current version of this plotter does
some simple hacks to discard bad flights, but this should be looked
into in more detail.

Highway Plot
------------
This plotter just displays a collection of routes on top of a map. It 
has hooks in it to let you crop the routes to a specified region. Routes
are plotted with an Alpha value (ie, transparency) in order to fake
a heat map for different areas (ie, the more routes that fly over something,
the darker the line becomes). 

The annoying thing for this one is splitting up routes that cross the 
international dateline. If you don't do anything, the -180 to 180 lon
change will draw a long, horizontal line across the screen. You can do
two things to fix this: (1) run your dataset through a splitter that
splits routes into different pieces as they cross the line or (2) enable
the built-in splitter that looks for crossings and splits them up before
plotting them. Option (1) is faster, if you're in a situation where you'll
be redrawing the same data a lot. Option (2) takes some time, but is easier
for dealing with stuff.

The basemap package allows you to specify the resolution of the
maps. For quick jobs, use the low-res setting (l). The high-res version
is good for end products, and requires additional map data.

Warning: This plotting can take a long amount of time, as each route may
be comprised of many segments, and a full day may have tens of thousands 
of routes.

Requirements: basemap, basemap-data, basemap-data-hires, geos

On centos6, this can be done via:
 yum install python-basemap python-basemap-data python-basemap-data-hires geos


Gap Plotter
-----------
This plotter takes a look at tracks and plots segments that are longer
than a particular duration. It expects that you're sampling at a known
interval (say 6mins), and that if the time difference between two points
is greater than 2x or 3x the sampling period, the plane was not in
a place where someone could hear it. By plotting all of these undersampled
segments, you can get an idea of where the gaps in coverage are.


