#!/usr/bin/env python
# ! ## File: dynSIS.py
# ! Module: use networkx graphs!
# ! ## See README.md for more information and use
# !-----------------------------------------------------------------------------
# ! SIS epidemic model algorithm based on the article
# !           Computer Physics Communications 219C (2017) pp. 303-312
# !           "Optimized Gillespie algorithms for the simulation of 
# !            Markovian epidemic processes on large and heterogeneous networks"
# ! Copyright (C) 2017 Wesley Cota, Silvio C. Ferreira
# ! 
# ! Please cite the above cited paper (available at <http://dx.doi.org/10.1016/j.cpc.2017.06.007> ) 
# ! as reference to our code.
# ! 
# !    This program is free software: you can redistribute it and/or modify
# !    it under the terms of the GNU General Public License as published by
# !    the Free Software Foundation, either version 3 of the License, or
# !    (at your option) any later version.
# !
# !    This program is distributed in the hope that it will be useful,
# !    but WITHOUT ANY WARRANTY; without even the implied warranty of
# !    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# !    GNU General Public License for more details.
# !
# !    You should have received a copy of the GNU General Public License
# !    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# !-----------------------------------------------------------------------------
# ! Author    : Wesley Cota
# ! Email     : wesley.cota@ufv.br
# ! Date      : 27 Mar 2017
# ! Version   : 1.0
# !-----------------------------------------------------------------------------
# ! See README.md for more details
# ! This code is available at <https://github.com/wcota/dynSIS-networkx>
# ! For performance, see <https://github.com/wcota/dynSIS> (Fortran implementation)
# ! For pure Python, see <https://github.com/wcota/dynSIS-py>

import numpy as np
from math import log

def dyn_run(nw, samples, transmission, run_time, init): 

    def weighted_degree(ver):
        return sum(map(lambda e: e[2]['weight'], nw.edges(ver, data=True)))

    n = nw.number_of_nodes()
    max_degree = max([weighted_degree(ver) for ver in nw.nodes()])              # Used in the rejection probability
    nodes = [None]*n                       # list V^I. Any node type is allowed
    
    i = 0

    while i < samples:
        i += 1
        sigma = dict.fromkeys({ i : 0 for i in nw.nodes()}, 0)
        nodes_infected = 0
        edges_infected = 0
        # Sort vertices and apply the initial condition
        for ver in np.random.permutation(nw.nodes()):
            nodes[nodes_infected] = ver
            nodes_infected += 1
            sigma[ver] = 3
            edges_infected += weighted_degree(ver)
            if nodes_infected == init:
                break

        # Run dynamics
        t = 0
        dt = 0.0

        while t < run_time and nodes_infected > 0:
            # Calculate the total rate
            R = nodes_infected + transmission * edges_infected
            # Select the time step
            rnd = max(np.random.uniform(), 1e-12) # Avoid u = 0
            dt = -log(rnd) / R
            # Update the time
            t += dt
            # Probability m to heal
            m = 1.0 * nodes_infected / R
            if 1 < m: # Select a random occupied vertex and heal.
                pos_inf = np.random.randint(0, nodes_infected)
                ver = nodes[pos_inf]
                # Then, heal it
                sigma[ver] = 0
                edges_infected -= weighted_degree(ver)
                nodes_infected -= 1
                nodes[pos_inf] = nodes[nodes_infected]
            else: # If not, try to infect: w = 1 - m
                # Select the infected vertex i with prob. proportional to k_i
                while True:
                    pos_inf = np.random.randint(0, nodes_infected)
                    ver = nodes[pos_inf]
                    if np.random.uniform() < weighted_degree(ver) / (1.0 * max_degree):
                        break
                # Select one of its neighbors
                ver = np.random.choice(list(nw.neighbors(ver)))
                if sigma[ver] == 0: # if not a phantom process, infect
                    sigma[ver] = 1
                    edges_infected += weighted_degree(ver)
                    nodes[nodes_infected] = ver    # Add one element to list
                    nodes_infected += 1             # Increase by 1 the list
        yield sigma
