airline-plotters
================

Misc scripts for plotting airline tracks


Cannonball Plots
----------------
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

