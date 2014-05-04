# -*- coding: utf8 -*-
from Node import Node
import numpy as np

#Define class parameter
r = 0.0001


class Tree(object):
    """docstring for Tree"""
    def getSoftLabel(self, l):
        label = np.zeros(5)
        if l <= 0.2:
            label[0] = 1
        elif 0.2 < l <= 0.4:
            label[1] = 1
        elif 0.4 < l <= 0.6:
            label[2] = 1
        elif 0.6 < l <= 0.8:
            label[3] = 1
        else:
            label[4] = 1
        return label

    def __init__(self, sentence, structure, label=None):
        self.sentence = sentence
        self.structure = structure

        wc = len(sentence)

        self.nodes = []
        self.leaf = []

        for i in range(2*wc-1):
            self.nodes.append(Node())

        for i, w in enumerate(sentence):
            node = self.nodes[i]
            node.word = w
            node.order = i
            self.leaf.append(node)

        parc = {}
        for i, (n, p) in enumerate(zip(self.nodes, structure)):
            n.parent = p-1
            self.nodes[p-1].childrens.append(i)
            l = parc.get(p-1, [])
            l.append(i)
            parc[p-1] = l
        parc.pop(-1)
        self.parcours = parc.items()
        self.parcours.sort()

        if label is not None:
            for n in self.leaf:
                n.y = self.getSoftLabel(label[n.word])

            for p, [a, b] in self.parcours:
                aT = self.nodes[a]
                bT = self.nodes[b]
                pT = self.nodes[p]
                if aT.order < bT.order:
                    pT.word = ' '.join([aT.word, bT.word])
                else:
                    pT.word = ' '.join([bT.word, aT.word])
                pT.y = self.getSoftLabel(label[pT.word])
                pT.order = aT.order
