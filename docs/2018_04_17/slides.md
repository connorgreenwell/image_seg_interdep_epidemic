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
- simulate traversal of graph ala markov
- threshold traversal probabilities
- combine threshold-ed segmentation masks

---

# Similarity Metrics

---

![](res/input.png){width=33%}
![](res/alpha.png){width=33%}
![](res/beta.png){width=33%}

---

# IDN

---

![](res/ab_graphs.png)

---

![](res/only_alpha.png){width=50%}
![](res/only_beta.png){width=50%}

---

![](res/single_source.png)

---

![](res/many_sources.png)

---

# Example Output

![](res/ours_best.png){width=50%}
![](res/base_best.png){width=50%}

---

# Baseline for Comparison

---

![](res/searched.png)

---

# Scoring

Adjusted Rand Score [^npri]:

[^npri]: https://www.cs.cmu.edu/~hebert/segs.htm

---

![](res/ars_demo.png)

---

# Results

![](res/bars.png)

---

# TODO

- foo
- bar
- baz

---

# Questions?
