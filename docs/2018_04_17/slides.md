---
title: "Modeling Image Segmentation as Info. Spread in an IDN"
author: "Emory Hufbauer, Connor Greenwell"
date: "Tuesday, April 17th, 2018"

classoption:
    - 17pt
    
theme: metropolis
themeoptions:
    - numbering=fraction

header-includes:
    - \setbeamertemplate{caption}{\insertcaption} 


---

# Visual Object Segmentation 

Given an image, label each pixel as belonging to a separete physical object.
(Note: distinct from object classification)

![](res/seg_ex.png)

---

# Method Overview

- Off the shelf super-pixel segmentation
- Compute similarity metrics between neigboring SPs
- overlay networks of neighbor similarity graphs, uniform value links

---

# Method Overview (continued)

- simulate traversal of graph (Markov)
- threshold traversal probabilities
- combine threshold-ed segmentation masks

---

# Similarity Metrics

---

![](res/input.png){width=33%}
![](res/alpha.png){width=33%}
![](res/beta.png){width=33%}

Left: original image. Middle: alpha similarity to starred pixel. Right: beta
similarity to starred pixel.

---

# Method Walkthrough

Divide image into superpixels with off the shelf method (such as SLIC).

![](res/superpixels.png){width=60%}

---

Compute similarity metrics between neigboring SPs;
overlay networks of neighbor similarity graphs, uniform value links.

![Left: alpha. Right: beta.](res/ab_graphs.png)

---

Simple segmentation by cutting edges under some threshold similarity. Left:
alpha only. Right: beta only.

![](res/only_alpha.png){width=50%}
![](res/only_beta.png){width=50%}

---

Simulate traversal of graph by taking the n-th power of the adjacency matrix;
threshold traversal probabilities to create binary segmentation masks.

![](res/single_source.png)

---

Threshold traversals from *all* source superpixels.

![](res/many_sources.png)

---

# Example Combined Segmentations

![](res/example_out.png)

---

# Baseline for Comparison

- use off the shelf superpixel method (SLIC-Zero)
- cluster superpixels based on pixel similarity (k-Means, k=3)

---

![](res/searched.png)

---

# Scoring

Normalized Probabilistic Rand (NPR) index[^npri]:

[^npri]: https://www.cs.cmu.edu/~hebert/segs.htm

---

![](res/ars_demo.png)

---

# Initial Results

Negative values indicate poor segmentation, higher is better.

![](res/bars.png){width=80%}

---

![](res/ours_best.png){width=50%}
![](res/base_best.png){width=50%}

Left: best segmentations w/ our method.
Right: best segmentations w/ baseline method.

---

# TODO

- Full evaluation on PASCAL VOC dataset
- Find optimal threshold
- Explore different traversal horizons
- More!

---

# Questions?

On GitHub: 

\tiny
github.com/connorgreenwell/image_seg_interdep_epidemic
