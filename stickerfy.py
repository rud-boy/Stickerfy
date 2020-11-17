#!/usr/bin/env python

from gimpfu import *

def stickerfy(image, stickerLayer, interpolation, borderColor):

    if pdb.gimp_drawable_is_indexed(stickerLayer):
        pdb.gimp_image_convert_rgb(image)
    pdb.plug_in_autocrop(image, stickerLayer)
    stickerWidth = pdb.gimp_drawable_width(stickerLayer) 
    stickerHeight = pdb.gimp_drawable_height(stickerLayer)
    if stickerWidth >= stickerHeight:
        scale = 464.0 / stickerWidth
    else:
        scale = 464.0 / stickerHeight
    stickerWidth *= scale
    stickerHeight *= scale
    pdb.gimp_context_set_interpolation(interpolation)
    pdb.gimp_layer_scale(stickerLayer, stickerWidth, stickerHeight, FALSE)
    pdb.gimp_image_resize(image, 512, 512, 0, 0) 
    offsetX = (512.0 - stickerWidth) / 2
    offsetY = (512.0 - stickerHeight) / 2
    pdb.gimp_layer_set_offsets(stickerLayer, offsetX, offsetY)
    pdb.gimp_layer_resize_to_image_size(stickerLayer)

    border = pdb.gimp_layer_new(image, 512, 512, 1, "Border", 100.0, 0)
    pdb.gimp_image_insert_layer(image, border, None, 1)
    pdb.gimp_context_set_foreground(borderColor)
    pdb.gimp_image_select_item(image, 0, stickerLayer)
    pdb.gimp_selection_grow(image, 8)
    pdb.gimp_drawable_edit_fill(border, 0)
    pdb.gimp_selection_none(image)

    pdb.script_fu_drop_shadow(image, border, 3, 3, 3, "black", 50.0, 0)

if __name__ == "__main__":
    register(
        "stickerfy",
        "Transform a png into a Whatsapp/Telegram sticker.",
        "Scale to 512x512, add margins, border and dropshadow.",
        "rud___boy",
        "rud___boy",
        "2019",
        "<Image>/Filters/Plug-ins/_Stickerfy...",
        "RGB*, GRAY*",
        [
            (PF_RADIO, "interpolation", "Set interpolation method", 3,
                (
                    ("None (for pixelart)", 0),
                    ("LoHalo", 3),
                    ("NoHalo", 4)
                )
            ),
            (PF_COLOR, "borderColor", "Set the border color", (255, 255, 255))
        ],
        [],
        stickerfy)
    main()
