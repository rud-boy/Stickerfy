#!/usr/bin/env python

import os

def stickerfy(fname, interpolation = 3, borderColor = "#FFFFFF"):

    sticker = pdb.gimp_image_new(512, 512, 0)
    meme = pdb.gimp_file_load_layer(sticker, fname)
    pdb.gimp_image_insert_layer(sticker, meme, None, 0)

    pdb.gimp_context_set_interpolation(interpolation)
    pdb.gimp_context_set_foreground(borderColor)

    pdb.plug_in_autocrop_layer(sticker, meme)
    width = pdb.gimp_drawable_width(meme) 
    height = pdb.gimp_drawable_height(meme)

    if width >= height:
        scale = 464.0 / width
    else:
        scale = 464.0 / height

    width = width * scale
    height = height * scale
    pdb.gimp_layer_scale(meme, width, height, FALSE)

    offx = (512.0 - width) / 2
    offy = (512.0 - height) / 2
    pdb.gimp_layer_set_offsets(meme, offx, offy)

    pdb.gimp_layer_resize_to_image_size(meme)

    pdb.gimp_image_select_item(sticker, 0, meme)
    pdb.gimp_selection_grow(sticker, 8)

    silhueta = pdb.gimp_layer_new(sticker, 512, 512, 1, "silhueta", 100.0, 0)
    pdb.gimp_image_insert_layer(sticker, silhueta, None, 1)
    pdb.gimp_drawable_edit_fill(silhueta, 0)
    pdb.gimp_selection_none(sticker)
    pdb.script_fu_drop_shadow(sticker, silhueta, 3, 3, 3, "#000000", 50.0, 0)
    mergedLayers = pdb.gimp_image_merge_visible_layers(sticker, 0)

    stickerName = os.path.dirname(fname) + os.path.splitext(os.path.basename(fname))[0] + "-sticker.png"

    pdb.file_png_save_defaults(sticker, mergedLayers, stickerName, stickerName)
    pdb.gimp_image_delete(sticker)
 
# GIMP auto-execution stub
if __name__ == "__main__":
    import sys, subprocess
    if len(sys.argv) < 2:
        print("you must specify a function to execute!")
        sys.exit(-1)
    scrdir = os.path.dirname(os.path.realpath(__file__))
    scrname = os.path.splitext(os.path.basename(__file__))[0]
    shcode = "import sys;sys.path.insert(0, '" + scrdir + "');import " + scrname + ";" + scrname + "." + sys.argv[1] + str(tuple(sys.argv[2:]))
    shcode = "gimp-console-2.10 -dfi --batch-interpreter python-fu-eval -b \"" + shcode + "\" -b \"pdb.gimp_quit(1)\""
    sys.exit(subprocess.call(shcode, shell=True))
else:
    from gimpfu import *
