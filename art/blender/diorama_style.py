"""FrutiCity Diorama: shared palette, toy materials and a reusable light rig.

Importing this module never imports bpy or changes a Blender scene. Call the
helpers explicitly from a generator. The preview runs in its own new scene:

  blender --background --factory-startup --python art/blender/diorama_style.py -- --preview

Existing generators are deliberately not redirected until their phase-2 renders
have been reviewed. Hex colours are sRGB; Blender socket values are scene linear.
"""
from dataclasses import dataclass
from pathlib import Path
import argparse
import colorsys
import json
import math
import sys


PALETTE = {
    "fresi": "E4484D", "pablo": "FFD34A", "nora": "FF9638",
    "pink": "F08CAF", "blue": "399DD1", "turquoise": "40BAA2",
    "deep_teal": "245D68", "fruti_teal": "287F7A", "sky": "A6E2DF",
    "cream": "FFF3D7", "wood_light": "C99665", "wood_dark": "875C3D",
    "terracotta": "D97B50", "coral": "EF6260", "berry": "D84F8A",
    "sun": "FFC94A", "leaf": "65B34E", "leaf_dark": "417E3B",
    "ink": "3C3027",
}


@dataclass(frozen=True)
class MaterialProfile:
    roughness: float
    specular: float
    coat: float = 0.0
    metallic: float = 0.0


MATERIAL_PROFILES = {
    "fruit": MaterialProfile(.37, .31, .02),
    "clothes": MaterialProfile(.53, .235),
    "wood": MaterialProfile(.51, .21),
    "building": MaterialProfile(.52, .21),
}
LIGHT_RATIOS = {"key": 1.0, "fill": .425, "rim": .20}
CONTACT_SHADOW = {"opacity": .24, "offset_y_px": 6, "blur_px": 11,
                  "reference_width_px": 540}
OWNER = "FrutiCity.Diorama.v1"
OWNER_KEY = "fruticity_owner"
ID_KEY = "fruticity_id"


def srgb(color):
    """Return 0..1 sRGB from a palette key or a six-digit hex string."""
    value = PALETTE.get(color, color).lstrip("#")
    if len(value) != 6:
        raise ValueError("Expected a palette key or six-digit hex colour")
    return tuple(int(value[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def linear_color(color, alpha=1.0):
    """IEC sRGB transfer, rather than the approximate gamma-2.2 shortcut."""
    return tuple(c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4
                 for c in srgb(color)) + (alpha,)


def tonal_family(color):
    """The shadow/base/highlight guide in sRGB HSV value space.

    Highlights clip at white; these are art-direction guides, not three bands
    forcibly quantized into the shader. Soft shading keeps rounded toy forms.
    """
    base = srgb(color)
    h, s, v = colorsys.rgb_to_hsv(*base)
    return {"shadow": colorsys.hsv_to_rgb(h, s, v * .80), "base": base,
            "highlight": colorsys.hsv_to_rgb(h, s, min(1.0, v * 1.12))}


def _find_owned(items, logical_id):
    return next((item for item in items
                 if item.get(OWNER_KEY) == OWNER and item.get(ID_KEY) == logical_id), None)


def _mark(item, logical_id):
    item[OWNER_KEY] = OWNER
    item[ID_KEY] = logical_id
    return item


def material(name, color="cream", category="building"):
    """Create/update only our named material. Same-name user materials survive.

    Repeated calls return the same owned datablock. Do not hand-edit materials
    carrying our owner tag: their canonical sockets are reapplied on regeneration.
    """
    import bpy
    profile = MATERIAL_PROFILES[category]
    logical_id = "material:" + name
    mat = _find_owned(bpy.data.materials, logical_id)
    if mat is None:
        mat = _mark(bpy.data.materials.new("Diorama / " + name), logical_id)
        mat.use_nodes = True
    nodes = mat.node_tree.nodes
    shader = nodes.get("Diorama Principled")
    if shader is None:
        shader = nodes.get("Principled BSDF") or nodes.new("ShaderNodeBsdfPrincipled")
        shader.name = "Diorama Principled"
    output = nodes.get("Material Output") or nodes.new("ShaderNodeOutputMaterial")
    mat.node_tree.links.new(shader.outputs["BSDF"], output.inputs["Surface"])
    values = {"Base Color": linear_color(color), "Metallic": profile.metallic,
              "Roughness": profile.roughness, "Specular IOR Level": profile.specular,
              "Coat Weight": profile.coat, "Coat Roughness": .38,
              "Subsurface Weight": 0.0, "Transmission Weight": 0.0}
    for socket, value in values.items():
        if socket not in shader.inputs:
            raise RuntimeError("Unsupported Principled socket: " + socket)
        target = shader.inputs[socket]
        for link in list(target.links):
            mat.node_tree.links.remove(link)
        target.default_value = value
    mat.diffuse_color = linear_color(color)
    mat["fruticity_category"] = category
    mat["fruticity_color_srgb"] = "#" + PALETTE.get(color, color).lstrip("#").upper()
    return mat


def lighting_rig(scene=None, target=(0, 0, 1), scale=1.0, key_energy=650.0, namespace="main"):
    """Ensure three owned AREA lights; do not remove or modify any other light.

    Front faces -Y. Key: 35 degrees lateral, 45 degrees elevated. Equal distance
    and emitter size preserve the energy ratio 1 : .425 : .20. Scale changes
    distances/sizes and energy squared to preserve surface illumination.
    A caller with an existing rig must explicitly decide whether to disable it.
    """
    import bpy
    from mathutils import Vector
    if scale <= 0 or key_energy <= 0:
        raise ValueError("scale and key_energy must be positive")
    scene = scene or bpy.context.scene
    collection_id = "rig:" + namespace
    # Scope collections to this scene, so a second scene never moves the first rig.
    collection = _find_owned(scene.collection.children, collection_id)
    if collection is None:
        collection = _mark(bpy.data.collections.new("Diorama lights / " + namespace), collection_id)
        scene.collection.children.link(collection)
    origin = Vector(target)
    specs = {"key": (-35, 45, "FFF0D5"), "fill": (50, 20, "D0FFF5"),
             "rim": (145, 30, "FFF1D9")}
    lights = {}
    for role, (azimuth, elevation, tint) in specs.items():
        logical_id = collection_id + ":" + role
        obj = _find_owned(collection.objects, logical_id)
        if obj is None:
            data = _mark(bpy.data.lights.new("Diorama " + role, "AREA"), logical_id)
            obj = _mark(bpy.data.objects.new("Diorama " + role, data), logical_id)
            collection.objects.link(obj)
        if obj.type != "LIGHT" or obj.data.get(OWNER_KEY) != OWNER:
            raise RuntimeError("Owned light identity was replaced: " + logical_id)
        a, e = math.radians(azimuth), math.radians(elevation)
        offset = Vector((math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e)))
        obj.location = origin + offset * (6.0 * scale)
        obj.rotation_mode = "QUATERNION"
        obj.rotation_quaternion = (origin - obj.location).to_track_quat("-Z", "Y")
        obj.data.type = "AREA"
        obj.data.shape = "DISK"
        obj.data.size = 4.0 * scale
        obj.data.energy = key_energy * LIGHT_RATIOS[role] * scale * scale
        obj.data.color = linear_color(tint)[:3]
        obj.data.use_shadow = True
        obj["fruticity_ratio"] = LIGHT_RATIOS[role]
        obj["fruticity_azimuth_degrees"] = azimuth
        obj["fruticity_elevation_degrees"] = elevation
        lights[role] = obj
    return lights


def configure_render(scene, samples=48):
    """Explicit opt-in render settings; never called by material() or lighting_rig()."""
    scene.render.engine = "CYCLES"
    scene.cycles.samples = samples
    scene.cycles.use_denoising = True
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"
    scene.view_settings.exposure = 0
    scene.view_settings.gamma = 1
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"


def smoke_preview(output):
    """Render one material board in a new scene and verify non-destructive reuse."""
    import bpy
    from mathutils import Vector
    previous = bpy.context.window.scene
    previous_objects = tuple(previous.objects)
    previous_materials = tuple(bpy.data.materials)
    scene = _mark(bpy.data.scenes.new("FrutiCity Diorama - material preview"), "preview")
    bpy.context.window.scene = scene
    try:
        configure_render(scene)
        scene.render.resolution_x, scene.render.resolution_y = 1500, 1050
        scene.render.resolution_percentage = 100
        world = _mark(bpy.data.worlds.new("Diorama preview world"), "preview-world")
        world.use_nodes = True
        world.node_tree.nodes["Background"].inputs["Color"].default_value = linear_color("cream")
        world.node_tree.nodes["Background"].inputs["Strength"].default_value = .30
        scene.world = world

        def flat(name, color):
            mat = _mark(bpy.data.materials.new("Diorama preview / " + name), "preview-flat:" + name)
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            emission = nodes.new("ShaderNodeEmission")
            emission.inputs["Color"].default_value = linear_color(color)
            mat.node_tree.links.new(emission.outputs[0], nodes["Material Output"].inputs["Surface"])
            return mat

        ink = flat("ink", "ink")
        muted = flat("muted", "deep_teal")
        cream = flat("cream", "cream")
        paper = flat("paper", "FFFAED")

        def cube(name, location, size, mat, bevel=.10):
            bpy.ops.mesh.primitive_cube_add(size=1, location=location)
            obj = _mark(bpy.context.object, "preview:" + name)
            obj.name = name
            obj.scale = size
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            obj.data.materials.append(mat)
            if bevel:
                modifier = obj.modifiers.new("Soft toy edges", "BEVEL")
                modifier.width, modifier.segments = bevel, 5
                obj.modifiers.new("Face normals", "WEIGHTED_NORMAL")
            return obj

        def label(text, x, z, size=.21, mat=ink):
            curve = bpy.data.curves.new("Label " + text, "FONT")
            curve.body, curve.size, curve.align_x = text, size, "CENTER"
            curve.space_character = 1.1
            obj = _mark(bpy.data.objects.new(text, curve), "preview-label:" + text)
            scene.collection.objects.link(obj)
            obj.location = (x, -1.55, z)
            obj.rotation_euler = (math.pi / 2, 0, 0)
            curve.materials.append(mat)

        cube("Cream board", (0, .7, 3.4), (12.6, .2, 8.5), cream, .18)
        label("FRUTICITY DIORAMA", 0, 6.98, .47, muted)
        label("Una familia de color, luz y materiales", 0, 6.51, .23)
        label("CANON PROCEDURAL  /  FASE 1", 0, 6.10, .14, muted)

        centers = (-4.44, -1.48, 1.48, 4.44)
        categories = ("fruit", "clothes", "wood", "building")
        names = ("FRUTA", "ROPA", "MADERA", "EDIFICIOS")
        colors = ("fresi", "turquoise", "wood_light", "cream")
        category_materials = {}
        for x, category, name, color in zip(centers, categories, names, colors):
            cube(name + " card", (x, .42, 4.05), (2.76, .10, 3.28), paper, .15)
            mat = material("preview-" + category, color, category)
            category_materials[category] = mat
            if category == "fruit":
                bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=.83, location=(x, -.38, 4.47))
                obj = _mark(bpy.context.object, "preview:fruit")
                obj.data.materials.append(mat)
                for polygon in obj.data.polygons:
                    polygon.use_smooth = True
            elif category == "clothes":
                obj = cube("Folded soft fabric", (x, -.4, 4.40), (1.50, .65, 1.32), mat, .25)
                obj.rotation_euler = (0, -.16, -.12)
                cube("Fabric fold", (x + .13, -.78, 4.28), (1.33, .20, .20), mat, .075)
            elif category == "wood":
                for i in range(3):
                    plank = cube("Wood plank " + str(i), (x, -.38, 4.02 + i * .43), (1.75, .63, .33), mat, .09)
                    plank.rotation_euler[2] = -.10
            else:
                obj = cube("House volume", (x, -.42, 4.25), (1.45, .73, 1.35), mat, .12)
                roof = material("preview-roof", "terracotta", "building")
                cube("Terracotta roof", (x, -.41, 4.96), (1.72, .95, .28), roof, .09)
                window = material("preview-window", "fruti_teal", "wood")
                cube("Turquoise window", (x, -.83, 4.36), (.50, .16, .57), window, .05)
            profile = MATERIAL_PROFILES[category]
            label(name, x, 3.31, .24, muted)
            label("R %.2f  /  S %.3f" % (profile.roughness, profile.specular), x, 2.96, .16)
            label("Metal 0  /  Coat %.2f" % profile.coat, x, 2.69, .15)

        label("PALETA DEL BARRIO", 0, 1.91, .21, muted)
        chips = ("deep_teal", "fruti_teal", "cream", "wood_light", "terracotta", "leaf", "coral", "sky")
        for i, key in enumerate(chips):
            x = -5.04 + i * 1.44
            cube("Palette " + key, (x, -.20, 1.31), (1.21, .10, .52), flat(key, key), .08)
            label("#" + PALETTE[key], x, .78, .16)
        label("KEY 1.00     FILL 0.425     RIM 0.20     |     KEY 35 lateral / 45 elevada", 0, .19, .17, muted)
        label("Muestras de material. Los personajes y escenarios actuales se migran en fases posteriores.", 0, -.28, .15)

        lights = lighting_rig(scene, (0, -.2, 4.3), key_energy=1150, namespace="preview")
        light_count = len(bpy.data.lights)
        again = lighting_rig(scene, (0, -.2, 4.3), key_energy=1150, namespace="preview")
        assert all(lights[key] is again[key] for key in lights)
        assert len(bpy.data.lights) == light_count, "Rig regeneration duplicated lights"
        assert len(lights) == 3
        values = {}
        for category, mat in category_materials.items():
            count = len(bpy.data.materials)
            assert material("preview-" + category, colors[categories.index(category)], category) is mat
            assert len(bpy.data.materials) == count, "Regeneration duplicated a material"
            inputs = mat.node_tree.nodes["Diorama Principled"].inputs
            profile = MATERIAL_PROFILES[category]
            values[category] = {"roughness": inputs["Roughness"].default_value,
                                "specular": inputs["Specular IOR Level"].default_value,
                                "coat": inputs["Coat Weight"].default_value,
                                "metallic": inputs["Metallic"].default_value}
            for name, expected in (("roughness", profile.roughness), ("specular", profile.specular),
                                   ("coat", profile.coat), ("metallic", profile.metallic)):
                assert abs(values[category][name] - expected) < 1e-6
        assert tuple(previous.objects) == previous_objects, "Caller scene was changed"
        assert all(mat in tuple(bpy.data.materials) for mat in previous_materials)

        camera_data = bpy.data.cameras.new("Diorama preview camera")
        camera = bpy.data.objects.new("Diorama preview camera", camera_data)
        scene.collection.objects.link(camera)
        camera.location = (0, -20, 3.38)
        camera.rotation_euler = (Vector((0, 0, 3.38)) - camera.location).to_track_quat("-Z", "Y").to_euler()
        camera_data.type, camera_data.ortho_scale = "ORTHO", 12.9
        scene.camera = camera
        output = Path(output).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        scene.render.filepath = str(output)
        bpy.ops.render.render(write_still=True, scene=scene.name)
        print("DIORAMA_VALIDATION " + json.dumps({"blender": bpy.app.version_string,
              "materials": values, "light_ratios": {key: obj.data.energy / lights["key"].data.energy for key, obj in lights.items()},
              "idempotent": True, "caller_scene_unchanged": True, "output": str(output)}))
        return output
    finally:
        bpy.context.window.scene = previous


def main():
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview", action="store_true", help="Render and validate one standalone material sheet")
    parser.add_argument("--output", default=str(Path(__file__).resolve().parents[2] /
                        "docs/fruticity-2/screenshots/phase-1/00-material-canon.png"))
    options = parser.parse_args(args)
    if options.preview:
        smoke_preview(options.output)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
