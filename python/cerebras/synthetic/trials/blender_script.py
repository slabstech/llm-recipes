import bpy
import os
import json
from mathutils import Vector

def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

def setup_scene(objects, environment):
    clear_scene()
    # Load environment (e.g., desert)
    bpy.ops.wm.open_mainfile(filepath=f"models/{environment}.blend")
    
    # Import military assets
    for obj in objects:
        bpy.ops.import_scene.obj(filepath=f"models/{obj}.obj")
    
    # Setup camera
    bpy.ops.object.camera_add(location=(0, -10, 5), rotation=(1.0, 0, 0))
    bpy.context.scene.camera = bpy.context.object

def render_image(output_dir, image_id):
    bpy.context.scene.render.filepath = os.path.join(output_dir, f"image_{image_id}.png")
    bpy.ops.render.render(write_still=True)
    
    # Generate labels (bounding boxes)
    labels = []
    for obj in bpy.data.objects:
        if obj.type == "MESH":
            # Project 3D bounds to 2D
            coords_2d = [bpy.context.scene.camera.matrix_world @ Vector(corner) for corner in obj.bound_box]
            coords_2d = [bpy_extras.object_utils.world_to_camera_view(bpy.context.scene, bpy.context.scene.camera, coord) for coord in coords_2d]
            x_coords = [coord.x * bpy.context.scene.render.resolution_x for coord in coords_2d]
            y_coords = [(1 - coord.y) * bpy.context.scene.render.resolution_y for coord in coords_2d]  # Invert y-axis
            x_min, x_max = min(x_coords), max(x_coords)
            y_min, y_max = min(y_coords), max(y_coords)
            labels.append({
                "category": obj.name,
                "bbox": [x_min, y_min, x_max - x_min, y_max - y_min]
            })
    return labels

def generate_images(objects, environment, num_images, output_dir):
    setup_scene(objects, environment)
    annotations = []
    for i in range(num_images):
        # Randomize object positions, camera angles, etc. (simplified here)
        labels = render_image(output_dir, i)
        annotations.append({"image_id": i, "file_name": f"image_{i}.png", "labels": labels})
    
    with open(os.path.join(output_dir, "annotations.json"), "w") as f:
        json.dump(annotations, f)

if __name__ == "__main__":
    import sys
    objects, env, num, out_dir = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
    generate_images(objects.split(","), env, num, out_dir)