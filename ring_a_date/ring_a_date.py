import bpy
import math

# -----------------------------
# SAFE SCENE CLEAR
# -----------------------------
if bpy.context.object:
    bpy.ops.object.mode_set(mode='OBJECT')

# Delete all objects
for obj in bpy.data.objects:
    obj.select_set(True)
bpy.ops.object.delete()

# -----------------------------
# SETTINGS
# -----------------------------
WIDTH = 0.8
HEIGHT = 0.9
PEG_RADIUS = 0.028
PEG_HEIGHT = 0.025
TEXT_OFFSET = 0.002     # slight distance above peg
TEXT_EXTRUDE = 0.001    # tiny height for visibility

# -----------------------------
# MATERIALS
# -----------------------------


# Generic material creator
def create_material(name, color):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = color + (1.0,)
    return mat

# Create base and peg materials
base_mat = create_material("BaseMat", (0.0, 0.6, 0.3))
peg_mat  = create_material("PegMat", (0.0, 0.7, 0.3))

# Create black text material with custom properties
text_mat = bpy.data.materials.new(name="TextMat")
text_mat.use_nodes = True
bsdf = text_mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs['Base Color'].default_value = (0,0,0,1)  # black
bsdf.inputs['Metallic'].default_value = 0.0           # matte
bsdf.inputs['Roughness'].default_value = 0.6          # some gloss
# -----------------------------
# BASE
# -----------------------------
bpy.ops.mesh.primitive_cube_add(size=1, location=(0,0,0))
base = bpy.context.object
base.scale = (WIDTH, HEIGHT, 0.01)
base.name = "Base"
base.data.materials.append(base_mat)
bpy.ops.object.shade_smooth()

# -----------------------------
# WEEKDAYS
# -----------------------------
weekdays = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
wd_x = -0.32
wd_y = 0.32
wd_spacing = 0.108

for i, day in enumerate(weekdays):
    # Peg
    bpy.ops.mesh.primitive_cylinder_add(radius=PEG_RADIUS, depth=PEG_HEIGHT, location=(wd_x + i*wd_spacing, wd_y, PEG_HEIGHT/2))
    peg = bpy.context.object
    peg.name = f"WD_{day}"
    peg.data.materials.append(peg_mat)
    
    # Flat text
    bpy.ops.object.text_add(location=(wd_x + i*wd_spacing, wd_y, PEG_HEIGHT + TEXT_OFFSET))
    txt = bpy.context.object
    txt.data.body = day.upper()[:3]
    txt.data.size = 0.03  # increased size for visibility
    txt.data.align_x = 'CENTER'
    txt.data.align_y = 'CENTER'
    txt.rotation_euler = (0,0,0)  # flat
    txt.data.extrude = TEXT_EXTRUDE
    txt.data.bevel_depth = 0
    txt.data.materials.append(text_mat)

# -----------------------------
# DATE PEGS 1-31
# -----------------------------
row_y = 0.18
date_text_objects = []

for row in range(5):
    for col in range(7):
        day_num = row*7 + col + 1
        if day_num > 31: continue
        x = -0.32 + col * wd_spacing
        y = row_y - row * 0.085

        # Peg
        bpy.ops.mesh.primitive_cylinder_add(radius=PEG_RADIUS, depth=PEG_HEIGHT, location=(x, y, PEG_HEIGHT/2))
        peg = bpy.context.object
        peg.name = f"Day_{day_num}"
        peg.data.materials.append(peg_mat)

        # Flat text
        bpy.ops.object.text_add(location=(x, y, PEG_HEIGHT + TEXT_OFFSET))
        txt = bpy.context.object
        txt.data.body = str(day_num)
        txt.data.size = 0.05   # largest text
        txt.data.align_x = 'CENTER'
        txt.data.align_y = 'CENTER'
        txt.rotation_euler = (0,0,0)
        txt.data.extrude = TEXT_EXTRUDE
        txt.data.bevel_depth = 0
        txt.data.materials.append(text_mat)

        date_text_objects.append(txt)

# -----------------------------
# MONTHS
# -----------------------------
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
month_x = wd_x
month_y_start = -0.28
month_row_gap = 0.10
month_spacing = 0.115

for i, m in enumerate(months):
    row = i // 6
    col = i % 6
    x = month_x + col * month_spacing
    y = month_y_start - row * month_row_gap

    # Peg
    bpy.ops.mesh.primitive_cylinder_add(radius=PEG_RADIUS, depth=PEG_HEIGHT, location=(x, y, PEG_HEIGHT/2))
    peg = bpy.context.object
    peg.name = f"Month_{m}"
    peg.data.materials.append(peg_mat)

    # Flat text
    bpy.ops.object.text_add(location=(x, y, PEG_HEIGHT + TEXT_OFFSET))
    txt = bpy.context.object
    txt.data.body = m
    txt.data.size = 0.03
    txt.data.align_x = 'CENTER'
    txt.data.align_y = 'CENTER'
    txt.rotation_euler = (0,0,0)
    txt.data.extrude = TEXT_EXTRUDE
    txt.data.bevel_depth = 0
    txt.data.materials.append(text_mat)

print("✅ Ring-A-Date scene ready and visible!")