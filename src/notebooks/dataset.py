import skimage.io as io
from skimage.util import img_as_float
import tqdm
import numpy as np

ROOT = "/u/amo-d0/ugrad/connor/scratch/data/pascal_voc/VOC2012/"
CSV_ROOT = ROOT+"ImageSets/Segmentation/"

train_path = CSV_ROOT+"train.txt"
val_path = CSV_ROOT+"val.txt"

JPEG_PATTERN = ROOT+"JPEGImages/{}.jpg"
ANNO_PATTERN = ROOT+"SegmentationObject/{}.png"

def make_dataset(train=True, limit=None):
    ids = open(train_path).readlines()[:limit]
    ids = list(map(str.strip, ids))
    
    img_paths = map(JPEG_PATTERN.format, ids)
    anno_paths = map(ANNO_PATTERN.format, ids)
    
    imgs = map(io.imread, img_paths)
    imgs = map(img_as_float, imgs)
    
    anno = map(io.imread, anno_paths)
    
    def foo(anno_orig):
        _, anno = np.unique(anno_orig.reshape(-1, 3), axis=0, return_inverse=True)
        return anno.reshape(anno_orig.shape[:2])
    
    anno = map(foo, anno)

    return list(imgs), list(anno)