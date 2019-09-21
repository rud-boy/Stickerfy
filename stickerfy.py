#!/usr/bin/env python

# Stickerfy pngs

from gimpfu import *

def stickerfy(sticker, meme, interpolation = 3, borderColor = "#FFFFFF"):
    
    pdb.gimp_context_set_interpolation(interpolation)
    pdb.gimp_context_set_foreground(borderColor)

    pdb.plug_in_autocrop(sticker, meme)
    width = pdb.gimp_drawable_width(meme) 
    height = pdb.gimp_drawable_height(meme)

    if width >= height:
        scale = 464.0 / width
    else:
        scale = 464.0 / height

    width = width * scale
    height = height * scale
    pdb.gimp_layer_scale(meme, width, height, FALSE)

    pdb.gimp_image_resize(sticker, 512, 512, 0, 0) 

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

register(
        "python_fu_stickerfy",
        "Convert a png to one that follows Whatsapp/Telegram stickers guidelines",
        "Convert a png to one that follows Whatsapp/Telegram stickers guidelines",
        "Rudah Amaral",
        "Rudah Amaral",
        "2019",
        "<Image>/Filters/Artistic/_Stickerfy...",
        "RGB*, GRAY*",
        [
            (PF_RADIO, "interpolation", "Set interpolation method used to scale the png", 3,
                (
                    ("None", 0),
                    ("Linear", 1),
                    ("Cubic", 2),
                    ("No-Halo", 3),
                    ("Lo-Halo", 4)
                )
            ),
            (PF_COLOR, "borderColor", "The border of the sticker", (255, 255, 255))
        ],
        [],
        stickerfy)

main()
