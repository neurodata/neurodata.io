import argparse
import numpy as np
from cloudvolume import CloudVolume
import tifffile as tf
from joblib import Parallel


def create_image_layer(destination, num_resolutions):
	info = CloudVolume.create_new_info(
		num_channels 	= 1,
		layer_type	= 'image',
		data_type	= 'uint8',
		encoding	= 'raw',
		resolution	= [1,1,1],
		voxel_offset	= [0, 0, 0],
		chunk_size	= [5, 5, 5],
		volume_size	= [10, 10, 10]
	)

	vol = CloudVolume(destination, compress=False, info=info, parallel=True)
	print(vol.info)
	vol.commit_info()
	return vol

# python upload.py **source** **destination**
# python upload.py ./test/ precomputed://file://test_output
def main():
	parser = argparse.ArgumentParser('Convert a folder of tif files to neuroglancer format')
	parser.add_argument('destination', help='Destination path for precomputed files, pre-pended with precomputed://file://, e.g. precomputed://file://**path** will write the files to ./**path**')
	num_resolutions = 1

	args = parser.parse_args()

	im = np.random.randint(0, 256, size=[10, 10, 10], dtype=np.uint8)
	tf.imsave('test.tif', im)
	im = tf.imread('test.tif')
	
	vol = create_image_layer(args.destination, num_resolutions)

	vol[:,:,:] = im

if __name__ == "__main__":
	main()
