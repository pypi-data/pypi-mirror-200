# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['archaea', 'archaea.earcut', 'archaea.geometry', 'archaea.writer']

package_data = \
{'': ['*']}

install_requires = \
['numpy-stl>=3.0.0,<4.0.0', 'numpy>=1.24.2,<2.0.0']

setup_kwargs = {
    'name': 'archaea',
    'version': '1.1.15',
    'description': 'Playground for geometry.',
    'long_description': '# Archaea\n\nArchaea is a base geometric library that includes basic geometric objects\nto create meshes and triangulated exports of meshes.\n\nMotivation of creating this library is started with master thesis, departments of Computational\nScience and Engineering and Architecture at Istanbul Technical University. \nAim of thesis is to create geometric definitions for different environmental\nsolvers like EnergyPlus and OpenFOAM to run them parallely on Linux environment.\n\nArchaea is a geometrical playground for now, most important functionality of library\nis executing earcut algorithm on 3D coordinate system by plane (u, v) transformations.\nShortly library can create triangulations with holes on 3D.\n\n\n## Supported Objects\n\n- CoordinateArray: Base object for vectoral operations on Vector and Point objects.\n- Vector, Vector2d, Vector3d: Vector operations like Dot and Cross Product, also\nserves transformations of other geometrical objects.\n- Point, Point2d, Point3d: Position object to construct other geometric objects\nlike LineSegment, Polyline, Mesh..\n- LineSegment: Construct with start and end point.\n- Polyline: List of consecutive LineSegments\n- Loop: Closed polyline definition.\n- Face: Face is a loop definition that might have holes with inner loops.\n- Mesh: Polygon and vertex list definition for exporting.\n\n\n## Supported Operations\n\n- Move: Objects can be moved by creating copy of source object.\n- Reverse: LineSegment, Polyline, Loop and Face can be reversed.\n- Offset: Loops and Faces can be offseted.\n- Extrude: Faces can be extruded that creates list of Faces. Holes also covered.\n',
    'author': 'Oğuzhan Koral',
    'author_email': 'oguzhankoral@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/archaeans/archaea',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
