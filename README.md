easy-graph Background
=====================

easy-graph is a simple graphing utility I wrote to easily plot data that was being printed in the terminal. It started when I needed to plot data that was generated by a c++ script for debugging purposes, but c++ doesn't have any easy graphing libraries. The best approach was to pipe the output to a file and plot the data with python. This script takes care of plotting the data in that file. It parses each line for an x, y, and optional z value, and plots these points with pyplot. There are a variety of options that control how the plot looks.

Data Formatting
===============
The script parses each line looking for floating point numbers (it searches for matches to [+-]?[0-9]`*`\.?[0-9]+' which is any normal floating point number).  If there are two numbers per row, it will plot a 2D scatter plot. If there are three per row, it will present a 3D scatter plot. By default, first column is x data, second column is y data.

Note that while there has to be two (or three) numbers on each row, there can be any other amount of text. For example,

```
x: 12.123 y: 45.456
x: 11.123 y: 46.654
```
and even
```
cat. = -.1234 dog = +.78998
```
are both valid files to plot.

There is currently no functionality to plot data only from certain lines that match a regex, but the the data can easily be filtered as it is acquired by grep.

Commandline Options
===================

filename (required arg)
-------------------------
The name of the input data file.

--output 
-------------
Saves the plot as an image with the given name.

--title
-------
Title of the graph. This just calls pyplot's title function. Any special formatting that pyplot allows (e.g. latex) should work here (although escaping special characters may be a pain).

--xlabel 
-------------
Sets the label for the x axis. Like the --title option, this is just a wrapper for pyplot setting the axis label, so fun things like latex should still work. The same applies for --ylabel and --zlabel.

--invert
--------
Setting this flag means that the first column of the data is the y data and the second column is the x data. z data (if any) remains in the third column.

--alternate
-----------
This flag tells easy graph that the data is formatted with alternating rows of x and y data, e.g.
```
x: 12
y: 90
x: 13
y: 89 
```

-s
---
"silent" mode, does not display the graph.

--fx, --fy, --fz
----------------
Expression to apply to the x data. Input expected to be the body of a lambda expression that will be applied via map to the x data. Must use "x" as the variable.

This can be super useful when trying to see if the data linearizes under a certain relationship (square root, log, etc). Also useful for scaling the graph or multiplying the y values by -1.

--mzx, --mzy, --mzz
-------------------
Stands for "min zero x" which means that the minimum x value will be set to 0 and the minimum y value will be set to zero. Makes it much easier to understand graphs with very large numbers if the relationship between the points is more important than the absolute magnitudes of the axes.

Future Plans
============
I'd like to add the ability to give easy-graph an input stream and make a plot as data is generated, we'll see if that ever happens.

Maintainer's email: aray.york@gmail.com