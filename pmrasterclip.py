#! /usr/bin/env python
# coding: utf-8
import os,ogr,osr


root_dir = '/mnt/mfs/zjh/rspm25/PM25_CIESIN/china'
#dst_dir = '/mnt/mfs/zjh/rspm25/PM25_CIESIN/china'
dst_dir = '/mnt/mfs/zjh/rspm25/PM25_CIESIN/grid75'
shpfolder = "/mnt/mfs/zjh/rspm25/shpdata"

if __name__ == '__main__':
    #china_boundary = os.path.join(shpfolder, 'china.shp')
    prename = "grid75"
    clip_boundary = os.path.join(shpfolder,'grid_75.shp')
    shpdata = ogr.Open(clip_boundary)
    shplayer = shpdata.GetLayer(0)
    xmin, xmax, ymin, ymax = shplayer.GetExtent()

    #return all filenames of the directory in a list
    files = os.listdir(root_dir)
    for name in files:
        if name.endswith(".tif"):
            # define the cliped filename
            dstfile = os.path.join(dst_dir,prename+'_'+ name)
            if os.path.exists(dstfile):
                print "the pm2.5 data of %s: %s already exists.."% (prename,name)
                continue
            filename = os.path.join(root_dir, name)
            cmd = 'gdalwarp -co "COMPRESS=deflate" -co "TILED=YES" -co "BIGTIFF=IF_NEEDED"  -of GTiff -dstnodata none -cutline %s -te %s %s %s %s %s %s' % ( clip_boundary, xmin, ymin, xmax, ymax, filename, dstfile)
            print cmd
            os.system(cmd)

'''
    # clip 2000
    dstfile = dstfolder + str(rid) + "_2000.tif"
    cmd = 'gdalwarp -co "COMPRESS=deflate" -co "TILED=YES" -co "BIGTIFF=IF_NEEDED" -tr 30 30 -of GTiff -dstnodata none -cutline %s -te %s %s %s %s %s %s' % (
        pshpfile, xmin, ymin, xmax, ymax, rst2000file, dstfile)
    print cmd
    os.system(cmd)
'''

