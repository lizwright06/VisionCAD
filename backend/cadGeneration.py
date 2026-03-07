import cadquery as cq
from pathlib import Path

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
    saved_path = save_shape(model, output_dir="outputfiles", filename="model.step")
    print(f"Saved CAD file to: {saved_path}")