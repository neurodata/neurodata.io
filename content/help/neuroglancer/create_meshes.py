from pathlib import Path

import numpy as np
import tifffile as tiff

import neuroglancer

json_descriptor = '{{"fragments": ["mesh.{}.{}"]}}'

img_path_str = '/mnt/c/Users/ben/Documents/zbrain-project/data/'
img_path = Path(img_path_str)

mesh_list = []
for f in img_path.glob('*.tif'):
    A = tiff.imread(str(f))
    mesh_list.append(A)
mesh = np.dstack(mesh_list)
mesh = np.transpose(mesh, (2, 0, 1))

ids = [int(i) for i in np.unique(mesh[:])]

voxel_size = [798, 798, 2000]

vol = neuroglancer.LocalVolume(
    data=mesh,
    voxel_size=voxel_size,
)

for ID in ids[1:]:
    print(ID)
    mesh_data = vol.get_object_mesh(ID)
    with open(
            str(img_path.parent / 'output' / 'mesh' / '.'.join(
                ('mesh', str(ID), str(ID)))), 'wb') as meshfile:
        meshfile.write(mesh_data)
    with open(
            str(img_path.parent / 'output' / 'mesh' / ''.join(
                (str(ID), ':0'))), 'w') as ff:
        ff.write(json_descriptor.format(ID, ID))

print('ids to insert into URL:')
ids_string = '[\'' + '\'_\''.join([str(i) for i in ids[1:]]) + '\']'
print(ids_string)

print('done')
