# -*- coding: utf-8 -*-

#---------------------------------------------------------------------#
#   FLApy:A Calculator of Illumination factor within Understory       #
#   IA:Illumination factors calculator/interpolation/change analysis  #
#   Virsion: 1.0                                                      #
#   Developer: Wang Bin (Yunnan University, Kunming, China)           #
#   Latest modification time: 2022-4-1                                #
#---------------------------------------------------------------------#

import pyvista as pv

def vis_pointCloud(inPoints):    #xyz

    pc = pv.PolyData(inPoints)

    value = inPoints[:, -1]

    pc['Elevation'] = value

    return pc.plot(render_points_as_spheres=False, show_grid=True)



