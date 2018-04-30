import numpy as np

import skimage.io as skio
import skimage.util as sku
import skimage.segmentation as seg
from skimage.future import graph
import skimage.filters as skf
import skimage.color as skc

from sklearn.neighbors import LocalOutlierFactor as LOF
from sklearn.metrics import adjusted_rand_score

import networkx as nx
import dynSIS
import importlib
importlib.reload(dynSIS)

def hufbauer_alpha(image, labels, connectivity=2, fudge=1e-8):
    rag = graph.RAG(labels, connectivity=connectivity)

    for n in rag:
        rag.node[n].update({'labels': [n],
                            'pixel count': 0,
                            'total color': np.array([0, 0, 0],
                                                    dtype=np.double)})

    for index in np.ndindex(labels.shape):
        current = labels[index]
        rag.node[current]['pixel count'] += 1
        rag.node[current]['total color'] += image[index]

    for n in rag:
        rag.node[n]['mean color'] = (rag.node[n]['total color'] /
                                     rag.node[n]['pixel count'])
        rag.node[n]['alpha'] = np.sum(rag.node[n]['mean color'] ** 2)

    for x, y, d in rag.edges(data=True):
        # TODO: might be wrong, check later
        #d['weight'] = 1 / (fudge + (rag.node[x]['alpha'] - rag.node[y]['alpha']) ** 2)
        d['weight'] = -((rag.node[x]['alpha'] - rag.node[y]['alpha']) ** 2.)
        #d['weight'] = np.log((rag.node[x]['alpha'] - rag.node[y]['alpha']) ** 2.)

    return rag

def hufbauer_beta(image, labels, connectivity=2):
    image = skc.rgb2lab(image)[:, :, [1,2]]
    rag = graph.RAG(labels, connectivity=connectivity)

    for n in rag:
        rag.node[n].update({'labels': [n],
                            'pixel count': 0,
                            'total hue': np.array([0, 0],
                                                    dtype=np.double)})

    for index in np.ndindex(labels.shape):
        current = labels[index]
        rag.node[current]['pixel count'] += 1
        rag.node[current]['total hue'] += image[index]

    for n in rag:
        rag.node[n]['mean hue'] = (rag.node[n]['total hue'] /
                                     rag.node[n]['pixel count'])

    for x, y, d in rag.edges(data=True):
        # TODO: might be wrong, check later
        diff = 1 / (1 + (rag.node[x]['mean hue'] - rag.node[y]['mean hue']) ** 2)
        diff = np.linalg.norm(diff)
        d['weight'] = diff

    return rag

def normalize_graph(g):
    values = []
    for _, _, d in g.edges(data=True):
        values.append(d["weight"])
    values = np.sort(values)
    
    # outlier smoothing
    outliers = LOF().fit_predict(values[:, None])
    values =  values[outliers > 0]
    min_val, max_val = values.min(), values.max() - values.min()
    
    for _, _, d in g.edges(data=True):
        weight = d["weight"]
        
        if weight > max_val: 
            weight = max_val
        if weight < min_val:
            weight = min_val
        weight = (weight - min_val) / max_val
        
        d["weight"] = weight
    
    return g

def sim_to_horizon(adj, N):
    adj = np.matrix(adj)
    for n in range(1, N+1):
        yield adj ** n

def build_adj(img, sps):
    num_sps = sps.max() + 1
    
    rag_a = normalize_graph(hufbauer_alpha(img, sps))
    rag_b = normalize_graph(hufbauer_beta(img, sps))
    
    adj_a = nx.adjacency_matrix(rag_a).todense()
    adj_b = nx.adjacency_matrix(rag_b).todense()

    adj = np.c_[
        np.r_[
            adj_a, 
            np.diag(np.ones(num_sps)) * 0.1,
        ],
        np.r_[
            np.diag(np.ones(num_sps)) * 0.1,
            adj_b,
        ],
    ]
    adj[np.diag_indices_from(adj)] += 1
    
    return adj

def segment_proposals_epidemic(adj, transmission, run_time):
    # Run it through the simulator
    proposals = dynSIS.dyn_run(
        nx.Graph(adj), 
        samples=108, 
        transmission=transmission, 
        run_time=run_time, 
        init=1)
    # Extract the data
    proposals = np.array([
        np.fromiter(prop.values(), dtype=float) 
        for prop in proposals
    ]).T
    # Fold the two layers together
    proposals = sum(np.array(np.split(proposals, 2)), 0).T
    proposals -= proposals.min()
    proposals /= proposals.max()
    
    return proposals

def merge_proposals(proposals, sps, thresh):
    masks = (proposals[sps] > thresh).astype(int)
    
    base = np.zeros_like(masks[:,:,0])
    for mask in np.rollaxis(masks, 2):
        base = seg.join_segmentations(base, mask)
    return base

def epidemic_method(img, horizon, merge_thresh):
    sps = seg.slic(img, slic_zero=True)
    adj = build_adj(img, sps)
    proposals = segment_proposals_epidemic(adj, horizon)
    segmentation = merge_proposals(proposals, sps, merge_thresh)
    return segmentation

if __name__ == "__main__":
    import tqdm
    import dataset
    import itertools as it
    
    print("building dataset...")
    imgs, anno = dataset.make_dataset(limit=20)
    all_sps = [
        seg.slic(img, slic_zero=True)
        for img in tqdm.tqdm(imgs)
    ]
    all_adj = [
        build_adj(img, sps)
        for img, sps in tqdm.tqdm(zip(imgs, all_sps))
    ]
    
    transmission_range = np.linspace(0., 1., 2, endpoint=True)
    run_time_range = np.array([1, 5, 10, 20])
    thresh_range = np.linspace(0.1, 0.5, 2, endpoint=True)
    
    print("making proposals")
    prop_params = list(it.product(
        transmission_range, run_time_range))
    all_props = [
        [
            segment_proposals_epidemic(adj, transmission, run_time)
            for adj, sps in zip(all_adj, all_sps)
        ]
        for transmission, run_time in tqdm.tqdm(prop_params)
    ]
    
    print("finding best params")
    means = [
        np.mean([
            adjusted_rand_score(
                ann.flat,
                merge_proposals(
                    prop,
                    sps, 
                    thresh).flat)
            for prop, sps, ann in zip(props, all_sps, anno)
        ])
        for props, thresh in tqdm.tqdm(it.product(all_props, thresh_range))
    ]
    
    print("Best:", params[np.argmax(means)])
    
    for mean, param in zip(means, params):
        print(mean, param)