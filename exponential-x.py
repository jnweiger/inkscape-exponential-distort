#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys, math
import inkex
import cubicsuperpath
from simpletransform import computeBBox

sys.path.append('/usr/share/inkscape/extensions')
inkex.localize()


class TransformExponentialX(inkex.Effect):
    """
    Apply logarithmic or exponential scale on all x-coordinates.
    """

    def __init__(self):
        """
        Constructor.
        """

        inkex.Effect.__init__(self)

        self.OptionParser.add_option(
            '-x', '--exponent', action='store', type='float',
            dest='exponent', default=float(1.3),
            help='distortion factor. 1=no distortion, default 1.3')

    def x_exp(self, bbox, x):
        xmin = bbox[0]      # maps to 0, 
        w = bbox[1]-xmin    # maps to 1
        x = (x-xmin)/w
        x = x**self.options.exponent
        return x*w + xmin
            

    def computeBBox(self, pts):
        xmin = None
        xmax = None
        ymin = None
        ymax = None
        for p in pts:
          for pp in p:
            for ppp in pp:
              if xmin is None: xmin = ppp[0]
              if xmax is None: xmax = ppp[0]
              if ymin is None: xyin = ppp[1]
              if ymax is None: ymax = ppp[1]

              if xmin > ppp[0]: xmin = ppp[0]
              if xmax < ppp[0]: xmax = ppp[0]
              if ymin > ppp[1]: xyin = ppp[1]
              if ymax < ppp[1]: ymax = ppp[1]
        return (xmin, xmax, ymin, ymax)


    def effect(self):

        if len(self.selected) == 0:
            inkex.errormsg(_("Please select an object to perform the " +
                             "exponential-x transformation on."))
            return

        for id, node in self.selected.items():
            type = node.get("{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}type", "path")
            if node.tag != '{http://www.w3.org/2000/svg}path' or type != 'path':
                inkex.errormsg(node.tag + " is not a path. Type="+type+". Please use 'Path->Object to Path' first.")
            else:
                pts = cubicsuperpath.parsePath(node.get('d'))
                bbox = self.computeBBox(pts)
                ## bbox (60.0, 160.0, 77.0, 197.0)
                ## pts [[[[60.0, 77.0], [60.0, 77.0], [60.0, 77.0]], [[60.0, 197.0], [60.0, 197.0], [60.0, 197.0]], [[70.0, 197.0], ...
                for p in pts:
                  for pp in p:
                    for ppp in pp:
                      ppp[0] = self.x_exp(bbox, ppp[0])

                node.set('d', cubicsuperpath.formatPath(pts))


if __name__ == '__main__':   #pragma: no cover
        e = TransformExponentialX()
        e.affect()

