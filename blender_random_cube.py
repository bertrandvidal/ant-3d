import bpy
from random import randint, shuffle, choice
from time import sleep

[bpy.data.objects.remove(o) for o in bpy.context.scene.objects]

location = (0, 0, 0)
cubes = {location}
bpy.ops.mesh.primitive_cube_add(location=location)

transformations = [
    lambda x, y, z: (x, y + 2, z),
    lambda x, y, z: (x, y + 2, z),
    lambda x, y, z: (x, y - 2, z),
    lambda x, y, z: (x + 2, y, z),
    lambda x, y, z: (x - 2, y, z),
    lambda x, y, z: (x, y, z + 2),
    lambda x, y, z: (x, y, z - 2),
]


def get_neighboring_location(location, cubes):
    new_location = None

    while not new_location:
        shuffle(transformations)
        for transformation in transformations:
            potential_location = transformation(*location)
            if potential_location not in cubes:
                new_location = potential_location
                break
            return get_neighboring_location(choice(list(cubes)), cubes)

    cubes.add(new_location)
    return new_location


for _ in range(500):
    location = get_neighboring_location(location, cubes)
    bpy.ops.mesh.primitive_cube_add(location=location)


c = {}
c["object"] = c["active_object"] = bpy.context.object
c["selected_objects"] = c["selected_editable_objects"] = bpy.context.scene.objects
bpy.ops.object.join(c)

raise Exception("Buuuuuuuuurt")
