---
title: "CS 687 Project Update"
author: "Connor Greenwell, Emory Hufbauer"
date: "Tuesday, March 13, 2018"

classoption:
  - twocolumn

geometry:
  - margin=1in
  - bottom=1.5in

---

\begin{abstract}
In this document we propose formulating the problem of image segmentation as simulating the propagation of
information/ownership through an interdependent network where the first layer is a lattice representation of an input image
and the second layer is a (planar) overlay graph where each node has weighted edges to pixels in the lattice. We will design
and evaluate a number of propagation models, primarily based on pixel/region similarity metrics. Finally we will compare our
method against classical and current state-of-the-art methods for image segmentation on a variety of segmentation benchmark
datasets. 
\end{abstract}

# Related Work

[@pei2014saliency] use a Markov-Random-Field on precomputed super pixels to perform image segmentation.

# Objective

We will first create an interdependent network model of an image. The weights of edges between adjacent pixels in the lattice
will represent their degree of similarity to each other. The weights of edges between nodes in the overlay graph will
represent their overlap and estimated potential to belong to the same object. The weights of edges between the overlay and
lattice will represent ownership of pixels by superpixels.

We will then perform a simultaneous, competitive propagation of multiple phenomena through this network using a variety of
models, with the ultimate goal of developing a propagation model with property that, after propagation has completed, the
regions of the lattice affected by each phenomena correspond well to the segments of the image.

# Evaluation

The goal of this project is mostly to explore the space and point to future research possibilities. Although the results will
be compared with those of existing algorithms, they are not expected to be competitive with the state of the art. To that end
we will evaluate our performance on a variety of classic image segmentation benchmark datasets, including PASCAL VOC and
MS-COCO, as well as compare our results against existing state-of-the-art segmentation methods. 

# Progress

A dataset has been found, and a system has been put into place for easily loading up pairs of images and annotations from the
PASCAL VOC dataset [@Everingham10]. 

A number of evaluation metrics have been explored for performance on the task of image segmentation. We have chosen the
Adjusted Rand Score from [@unnikrishnan2005measure]  Some other metrics to consider are Mutual Information, FMI, and
Homogeneity scores. These may be included in the final paper if they tell an interesting story but our primary focus will be
on evluating against Hebert's ARS score.

A naive baseline method has been developed for us to compare our actual method against. It is based on using DBSCAN
[@ester1996density] to cluster and merge superpixels produced by SLIC [@achanta2010slic].

Mechanisms for performing hyperparameter optimization have been developed and tested on the naive baseline. This will be
necessary because our final method will likely have a number of tunable hyperparameters and it will be useful to automatically
find the optimal settings for our task.

# References
