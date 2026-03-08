from drawShapes import drawCube, drawSquareBasedPyramid, drawSphere, drawCylinder, drawRectangularPrism, drawCone, drawTriangleBasedPyramid
from pathlib import Path
import cadquery as cq

"""
example input:

[{'shape': 'cube', 'size': 10, 'position': [0, 0, 0]}, {'shape': 'square based pyramid', 'base_size': 10, 'height': 6, 'position': [0, 5, 0]}, {'shape': 'sphere', 'radius': 6, 'position': [0, 17, 0]}]

"""

def parse(shape):
    if 'position' not in shape:
        raise ValueError(f"Missing 'position' for shape: {shape}")
    if 'shape' not in shape:
        raise ValueError(f"Missing 'shape' type for shape: {shape}")
    
    
    position = shape['position']
    position = [position[0], 0, position[1]]  # Ensure it's a list of 3 values
    print(position)
    name = shape['shape'].lower()
    
    if name == "sphere":
        if 'radius' not in shape:
            raise ValueError(f"Missing 'radius' for sphere: {shape}")
        return drawSphere(shape['radius'], position)

    elif name == 'cylinder':
        if 'radius' not in shape or 'height' not in shape:
            raise ValueError(f"Missing 'radius' or 'height' for cylinder: {shape}")
        return drawCylinder(shape['radius'], shape['height'], position)

    elif name == 'cube':
        if 'size' not in shape:
            raise ValueError(f"Missing 'size' or 'position' for cube: {shape}")
        return drawCube(shape['size'], position)
    
    elif name == 'rectangular prism':
        if 'width' not in shape or 'depth' not in shape or 'height' not in shape:
            raise ValueError(f"Missing 'width', 'depth', or 'height' for rectangular prism: {shape}")
        return drawRectangularPrism(shape['width'], shape['depth'], shape['height'], position)
        
    elif name == 'cone':
        if 'radius' not in shape or 'height' not in shape:
            raise ValueError(f"Missing 'radius' or 'height' for cone: {shape}")
        return drawCone(shape['radius'], shape['height'], position)
        
    elif name == 'square based pyramid':
        if 'base_size' not in shape or 'height' not in shape:
            raise ValueError(f"Missing 'base_size' or 'height' for square based pyramid: {shape}")
        return drawSquareBasedPyramid(shape['base_size'], shape['height'], position)

    elif name == 'triangle based pyramid':
        if 'base_size' not in shape or 'height' not in shape:
            raise ValueError(f"Missing 'base_size' or 'height' for triangle based pyramid: {shape}")
        return drawTriangleBasedPyramid(shape['base_size'], shape['height'], position)
    else:
        print(f"Unknown shape type: {name}")




def save_shape(shape_obj, output_dir="outputfiles", filename="model2.step"):
    output_path = Path(__file__).resolve().parent / output_dir
    output_path.mkdir(parents=True, exist_ok=True)
    file_path = output_path / filename
    cq.exporters.export(shape_obj, str(file_path))
    return file_path


def generateCad(shapes):

    result_arr = []

    for shape in shapes:
        try:
            result = parse(shape)
            result_arr.append(result)
            print(f"Generated shape for: {shape['shape']}")
        except ValueError as e:
            print(f"Error parsing shape: {e}")

    if not result_arr:
        raise ValueError("No valid shapes generated")

    # Combine all shapes
    output_object = result_arr[0]

    for shape in result_arr[1:]:
        output_object = output_object.union(shape)

    save_shape(output_object)
    print("CAD model generated and saved successfully.")
            
if __name__ == "__main__":

    # shapes = [{'shape': 'rectangular prism', 'width': 12, 'depth': 8, 'height': 6, 'position': [0, 3]}, {'shape': 'square based pyramid', 'base_size': 12, 'height': 8, 'position': [0, 6]}, {'shape': 'sphere', 'radius': 5, 'position': [0, 19]}]
    shapes =[{'shape': 'cylinder', 'radius': 6, 'height': 15, 'position': [0, 0]}, {'shape': 'cone', 'radius': 6, 'height': 9, 'position': [0, 15]}]

    
    try:
        generateCad(shapes)
    except ValueError as e:
        print(f"Error parsing shape: {e}")
        
import cadquery as cq
from pathlib import Path
from open_step_file import open_step_file

# example input:
"""    
    {
  "operations": [
    {
      "type": "extrude",
      "polygon": [[0,0],[2,0],[2,2],[0,2]],
      "height": 2,
      "name": "cube1"
    },
    {
      "type": "loft",
      "base_polygon": [[0,0],[2,0],[2,2],[0,2]],
      "apex": [1,1,4],
      "name": "pyramid1"
    },
    {
      "type": "union",
      "objects": ["cube1","pyramid1"]
    }
  ]
}
"""

def should_have_fields(operation, required_fields):
    missing = [field for field in required_fields if field not in operation]
    if missing:
        raise ValueError(f"Missing fields for {operation.get('type')}: {missing}")


def compileShapes(operations):
    if not isinstance(operations, list) or len(operations) == 0:
        raise ValueError("operations must be a non-empty list")

    shapes = {}
    last_shape = None

    for operation in operations:
        op_type = operation.get("type")

        if op_type == "extrude":
            should_have_fields(operation, ["name", "polygon", "height"])
            name = operation["name"]
            polygon = operation["polygon"]
            height = operation["height"]

            shape_obj = cq.Workplane("XY").polyline(polygon).close().extrude(height)
            shapes[name] = shape_obj
            last_shape = shape_obj

        elif op_type == "loft":
            should_have_fields(operation, ["name", "base_polygon", "apex"])
            name = operation["name"]
            base_polygon = operation["base_polygon"]
            apex = operation["apex"]

            if type(apex) != list  or len(apex) != 3:
                raise ValueError("apex must be a list with 3 inputs")

            apex_x = apex[0]
            apex_y = apex[1]
            apex_z = apex[2]
            epsilon = 1e-3 # turns out need a small offset to prevent cq from freaking out when the top profile is a single point
            top_profile = [
                [apex_x - epsilon, apex_y - epsilon],
                [apex_x + epsilon, apex_y - epsilon],
                [apex_x + epsilon, apex_y + epsilon],
                [apex_x - epsilon, apex_y + epsilon],
            ]

            shape_obj = (
                cq.Workplane("XY")
                .polyline(base_polygon)
                .close()
                .workplane(offset=apex_z)
                .polyline(top_profile)
                .close()
                .loft(combine=True)
            )
            shapes[name] = shape_obj
            last_shape = shape_obj

        elif op_type == "union":
            should_have_fields(operation, ["objects"])
            object_names = operation["objects"]

            if type(object_names) != list or len(object_names) == 0:
                raise ValueError("union objects must be a non-empty list")


            missing = []
            for shape_name in object_names:
                if shape_name not in shapes:
                    missing.append(shape_name)
            if missing:
                raise ValueError(f"Cannot union unknown shapes: {missing}")
            

            output = shapes[object_names[0]]
            for shape_name in object_names[1:]:
                output = output.union(shapes[shape_name])

            shapes["final"] = output
            last_shape = output

        else:
            raise ValueError(f"Unsupported operation type: {op_type}")

    if last_shape is None:
        raise ValueError("No shapes were generated from operations")

    return last_shape


def save_shape(shape_obj, output_dir="outputfiles", filename="model.step"):
    output_path = Path(__file__).resolve().parent / output_dir
    output_path.mkdir(parents=True, exist_ok=True)
    file_path = output_path / filename
    cq.exporters.export(shape_obj, str(file_path))
    return file_path


if __name__ == "__main__":
    example_operations = [
        {
            "type": "extrude",
            "name": "cube1",
            "polygon": [[0, 0], [2, 0], [2, 2], [0, 2]],
            "height": 2,
        },
        {
            "type": "loft",
            "name": "pyramid1",
            "base_polygon": [[0, 0], [2, 0], [2, 2], [0, 2]],
            "apex": [1, 1, 4],
        },
        {
            "type": "union",
            "objects": ["cube1", "pyramid1"],
        },
    ]

    model = compileShapes(example_operations)
    saved_path = save_shape(model, output_dir="generated_step_files", filename="model.step")
    print(f"Saved CAD file to: {saved_path}")
