#!/usr/bin/env python
import re
import matplotlib.pyplot as plt
import argparse
from mpl_toolkits.mplot3d import Axes3D

parser = argparse.ArgumentParser(description="Plot a scatter plot from data in a file. Assumes that the first column has floats representing x values and the second column has floats representing y values.")
parser.add_argument('filename', help='Name of the input data file')
parser.add_argument('--output', dest='output', help='Name of the output figure')
parser.add_argument('--title', dest='title', help='Title of the Graph')
parser.add_argument('--xlabel', dest='xlab', help='Label for x axis')
parser.add_argument('--ylabel', dest='ylab', help='Label for y axis')
parser.add_argument('--zlabel', dest='zlab', help='Label for z axis')
parser.add_argument('--invert', dest='invert', default=False, action='store_true', help='First data column is Y, second is X. Leaves Z data alone if any is specified.')
parser.add_argument('--alternate', dest='alternate', default=False, action='store_true', help='Will assume data is alternating rows of X and Y. Using invert with this option would assume Y then X.If there are any lines without legitimate data, they must come in pairs, or the script will not work.')
parser.add_argument('-s', dest='silent', default=False, action='store_true', help='Silent mode. Does not display graph.')
parser.add_argument('--fx', dest='fx', help='Expression to apply to the x data. Input expected to be the body of a lambda expression that will be applied via map to the x data. Must use "x" as the variable.')
parser.add_argument('--fy', dest='fy', help='Expression to apply to the y data. Input expected to be the body of a lambda expression that will be applied via map to the y data. Must use "y" as the variable.')
parser.add_argument('--fz', dest='fz', help='Expression to apply to the z data. Input expected to be the body of a lambda expression that will be applied via map to the z data. Must use "z" as the variable.')

parser.add_argument('--mzx', dest='minzerox', default=False, action='store_true', help='If enabled, will make the minimum element of the X list 0. Will add or subract as necessary to preserve relative differences between values. Will be applied *after* any user-defined functions.')
parser.add_argument('--mzy', dest='minzeroy', default=False, action='store_true', help='If enabled, will make the minimum element of the Y list 0. Will add or subract as necessary to preserve relative differences between values. Will be applied *after* any user-defined functions.')
parser.add_argument('--mzz', dest='minzeroz', default=False, action='store_true', help='If enabled, will make the minimum element of the X list 0. Will add or subract as necessary to preserve relative differences between values. Will be applied *after* any user-defined functions.')

args = parser.parse_args()

if not args.title:
  args.title = args.filename
if not args.output:
  args.output = 'OutputFigure.png'
if not args.xlab:
  args.xlab = ''
if not args.ylab:
  args.ylab= ''
if not args.zlab:
  args.zlab= ''

with open(args.filename) as fo:
  text = fo.readlines()

xlist = list()
ylist = list()
zlist = list()
pointset = set() # Accumulate in a set so that we discard duplicates
if not args.alternate:

    for item in text:
        matches = re.findall('[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?', item)
        matches = list(map(float, matches))
        if len(matches) > 0:
            pointset.add(tuple(matches))
else:
    for rowa, rowb in zip(*[iter(text)]*2): # Pairs the rows

        matches1 = list(map(float, re.findall('[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?', rowa)))
        matches2 = list(map(float, re.findall('[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?', rowb)))
        if( (len(matches1) > 0) and (len(matches2) > 0)):
           pointset.add((matches1[0], matches2[0]))


pointlist = list(pointset)
if len(pointlist[0]) == 2:
  ndim = 2
elif len(pointlist[1]) == 3:
  ndim = 3
else:
  raise "Error, unexpected number of columns (dimensions)"

xlist = list(map(lambda x: x[0], pointlist))
ylist = list(map(lambda y: y[1], pointlist))

# This swaps the x and y data if the 'invert' flag was set
if args.invert:
        tmp = xlist
        xlist = list(ylist)
        ylist = list(tmp)
if args.fx:
    x_expr = eval('lambda x: ' + args.fx) #x_expr is now a lambda function
    xlist = list(map(x_expr, xlist))

if args.fy:
    y_expr = eval('lambda y: ' + args.fy) #y_expr is now a lambda function
    ylist = list(map(y_expr, ylist))

if args.minzerox:
    xlist = list(map(lambda x: x - min(xlist), xlist))

if args.minzeroy:
    ylist = list(map(lambda y: y - min(ylist), ylist))


if (ndim == 3):
  zlist = list(map(lambda z: z[2], pointlist))

  if args.fz:
    z_expr = eval('lambda z: ' + args.fz) #z_expr is now a lambda function
    zlist = list(map(z_expr, zlist))
  if args.minzeroz:
    zlist = list(map(lambda z: z - min(z), zlist))
  fig = plt.figure()
  ax3 = fig.add_subplot(111, projection='3d')
  ax3.scatter(xlist, ylist, zlist)
else:
  plt.scatter(xlist, ylist)
  axes = plt.gca()
  axes.set_xlim([min(xlist), max(xlist)])
  axes.set_ylim([min(ylist), max(ylist)])

plt.xlabel(args.xlab)
plt.ylabel(args.ylab)
plt.title(args.title)
plt.savefig(args.output)

if not args.silent:
  plt.show()
