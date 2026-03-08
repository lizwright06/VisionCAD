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
        
