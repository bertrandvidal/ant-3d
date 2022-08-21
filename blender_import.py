#!/usr/bin/env python
import csv

import bpy

# clean up all objects in the scene
[bpy.data.objects.remove(o) for o in bpy.context.scene.objects]

# add cubes to the scene
with open("/Users/bertvidal/github/ant-3d/export.csv", "r") as f:
    reader = csv.reader(f)
    for line in reader:
        position = tuple(map(int, line))
        # half the scale because blender cubes are built with one of their corner in
        # the given location rather than centered on it
        bpy.ops.mesh.primitive_cube_add(location=position, scale=(0.5, 0.5, 0.5))

# setup context and join cubes to be one sculpture
context = {
    "object": bpy.context.object,
    "active_object": bpy.context.object,
    "selected_objects": bpy.context.scene.objects,
    "selected_editable_objects": bpy.context.scene.objects,
}
bpy.ops.object.join(context)
