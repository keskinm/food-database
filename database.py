#!usr/bin/python
# -*- coding: utf-8 -*-


class Database(object):

    def __init__(self, core):
        self.graph = {core: []}
        self.images_nodes = {}
        self.images_status = {}
        self.status_choices = {'invalid': 'invalid', 'valid': 'valid', 'granularity_staged': 'granularity_staged', 'coverage_staged': 'coverage_staged'}
        self.nodes_set = set([])

    def add_nodes(self, nodes_to_add):
        for (child, parent) in nodes_to_add:
            self.graph.setdefault(parent, []).append(child)
            self.nodes_set.add(child)
        self.update_status(nodes_to_add)

    def add_extract(self, extract):
        for (image_id, labels) in extract.items():
            self.images_nodes.setdefault(image_id, labels)
        self.build_status(extract)

    def build_status(self, extract):
        for (image_id, labels) in extract.items():
            self.images_status.setdefault(image_id, self.status_choices['valid'])
            for label in labels:
                if not (label in list(self.nodes_set)):
                    self.images_status[image_id] = self.status_choices['invalid']
                    break

    def get_extract_status(self):
        return self.images_status

    def update_status(self, nodes_to_add):
        for (child, parent) in nodes_to_add:
            graph_childs = self.graph[parent]
            for (image_id, image_nodes) in self.images_nodes.items():
                if list(set(graph_childs).intersection(image_nodes)):
                    self.images_status[image_id] = self.status_choices['coverage_staged']

                elif parent in image_nodes:
                    self.images_status[image_id] = self.status_choices['granularity_staged']





