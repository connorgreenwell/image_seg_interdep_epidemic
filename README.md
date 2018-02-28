# Modeling Image Segmentation as Epidemic Spread in an Interdependent Network

In this document we propose formulating the problem of image segmentation as simulating the propagation of
information/ownership through an interdependent network where the first layer is a lattice representation of an input image
and the second layer is a (planar) overlay graph where each node has weighted edges to pixels in the lattice. We will design
and evaluate a number of propagation models, primarily based on pixel/region similarity metrics. Finally we will compare our
method against classical and current state-of-the-art methods for image segmentation on a variety of segmentation benchmark
datasets. 

# Project Members

- Emory Hufbauer
- Connor Greenwell

# Possible Experiments

- [ ] segmentation via information "epidemic" model. randomly seed pixels in image with ownership information, then spread
  ownership between pixels and overlay network where pixel-to-pixel transmission probability is related to similarity, and
  other transmission probs are TBD
- [ ] compose multiple, low quality super-pixelizations into a multi-layer I.D. then propagate information through network to
  form a higher quality segmentation.
