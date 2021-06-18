#!/usr/bin/env python

from gimpfu import *

def stickerfy(image, stickerLayer, interpolation, borderColor):

    pdb.gimp_context_set_interpolation(interpolation)
    pdb.gimp_context_set_foreground(borderColor)
    if pdb.gimp_drawable_is_indexed(currentLayer):
        pdb.gimp_image_convert_rgb(image)

    pdb.gimp_image_undo_group_start(image)
    for layer in image.layers:
        pdb.gimp_image_set_active_layer(image, layer)
        pdb.plug_in_autocrop_layer(image, layer)
    pdb.gimp_image_resize_to_layers(image)
    for layer in image.layers:
        pdb.gimp_layer_resize_to_image_size(layer)
    pdb.gimp_image_undo_group_end(image)

    pdb.gimp_image_undo_group_start(image)
    composedFramesWidth = pdb.gimp_image_width(image)
    composedFramesHeight = pdb.gimp_image_height(image)
    offsetX = (512.0 - composedFramesWidth) / 2
    offsetY = (512.0 - composedFramesHeight) / 2
    pdb.gimp_image_resize(image, 512, 512, offsetX, offsetY)
    if  composedFramesWidth >= composedFramesHeight:
        scaleFactor = 464.0 / composedFramesWidth
    else:
        scaleFactor = 464.0 / composedFramesHeight
    pdb.gimp_image_undo_group_end(image)

    pdb.gimp_image_undo_group_start(image)
    for layer in image.layers:
        layerWidth = pdb.gimp_drawable_width(layer) * scaleFactor
        layerHeight = pdb.gimp_drawable_height(layer) * scaleFactor
        pdb.gimp_layer_scale(layer, layerWidth, layerHeight, True)

        frameName = pdb.gimp_item_get_name(layer)
        border = pdb.gimp_layer_new(image, 512, 512, 1, frameName + "B", 100, 0)
        parentPosition = pdb.gimp_image_get_item_position(image, layer) + 1
        pdb.gimp_image_insert_layer(image, border, None, parentPosition)
        pdb.gimp_image_select_item(image, 2, layer)
        pdb.gimp_selection_grow(image, 8)
        pdb.gimp_drawable_edit_fill(border, 0)
        pdb.gimp_selection_none(image)

        pdb.script_fu_drop_shadow(image, border, 3, 3, 3, "black", 50.0, 0)
        #layer = pdb.gimp_image_merge_down(image, layer, 0)
        #layer = pdb.gimp_image_merge_down(image, layer, 0)
        #pdb.gimp_item_set_name(layer, frameName)
    pdb.gimp_image_undo_group_end(image)

register(
    "stickerfy",
    "Transform a png into a Whatsapp/Telegram sticker.",
    "Scale to 512x512, add margins, border and dropshadow.",
    "rud___boy",
    "rud___boy",
    "2019-2021",
    "<Image>/Filters/Plug-ins/_Stickerfy...",
    "RGB*, GRAY*, INDEXED",
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
    stickerfy
)

main()
