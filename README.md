# Blender Curve Merge Segments
Merges overlapping segments in a curve by distance.  Basically remove duplicate verices but for curves.

I ran across an issue where I used a vertex to design a curve for some braids.  After using the array modifier I applied it,
merged many of the vertices but forgot some.  I converted to a curve and used a different beizer curve to shape the braids, 
only to find out at the end I that the strands where not fully connected all the way through.  What I needed was the equivalent
of merge duplicate vertices by distance that you get for a mesh but unfortunately that isn't (as of this writing) a feature
of blender for curves.

So I wrote a simple plugin that gives you a `Merge Segments by Distance` option when you right click on a curve in Edit mode.

To use this, simply copy the python script to the scripting tab and hit run.  Once you have the script you should have the
option under the curve context menu in Edit Mode.  By default it will only merge directly overlapping segments, however,
there is a popup once you have run it to adjust this tolerance.
