Longhaul Tracking
=================

Scripts to help extract a specific set of planes from a dataset and
plot their routes over a long period of time.

I store my track archives in a simple format. Each day is written to a file,
in which a plane appears once (with a long wkt track for all the locations
where it was reported). These files make it easy to grep out things you
care about. Often I want to follow one or more specific planes from
day to day. Because I seem to do this a good bit, I wrote this script
to grep out each plane to its own file.

plane_extractor.sh
------------------
This script looks at a dump directory and then greps for specific flights
on each day. Each plane's daily results are gathered up in a 
file in the results directory.

The script can take command line input, but it asks for specifics
when it runs. 

note: this can take a long time to run, as it rereads each dump file
multiple times to pull out each flight.
