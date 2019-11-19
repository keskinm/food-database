#!usr/bin/python
# -*- coding: utf-8 -*-


class Database(object):

    def __init__(self, core):
        self.graph = {core: []}
        self.graph_set = {core}

        self.images_graph = {}
        self.images_status = {}

        self.status_choices = {'invalid': 'invalid', 'valid': 'valid', 'granularity_staged': 'granularity_staged',
                               'coverage_staged': 'coverage_staged'}

    def add_nodes(self, nodes_to_add):
        self._add_nodes(self.graph, nodes_to_add)
        for (child, parent) in nodes_to_add:
            self.graph_set.add(child)
        self.update_status(nodes_to_add)

    def add_extract(self, extract):
        for (image_id, labels) in extract.items():
            self.images_graph.setdefault(image_id, labels)
        self.build_status(extract)

    def build_status(self, extract):
        for (image_id, labels) in extract.items():
            self.images_status.setdefault(image_id, self.status_choices['valid'])
            if len(set(labels).intersection(self.graph_set)) != len(labels):
                self.images_status[image_id] = self.status_choices['invalid']

    def get_extract_status(self):
        return self.images_status

    @staticmethod
    def _add_nodes(graph, nodes_to_add):
        for (child, parent) in nodes_to_add:
            graph.setdefault(parent, []).append(child)
        return graph

    def update_status(self, nodes_to_add):
        candidate_nodes_graph = self._add_nodes(graph={}, nodes_to_add=nodes_to_add)
        current_invalids = self.check_current_invalids(current_invalids=[])

        coverage_stageds = []
        for (image_id, image_nodes) in self.images_graph.items():
            for (candidate_parent, candidate_childs) in candidate_nodes_graph.items():
                graph_childs = self.graph[candidate_parent]
                if set(graph_childs).intersection(image_nodes) and self.images_status[image_id] != self.status_choices['invalid']:
                    self.images_status[image_id] = self.status_choices['coverage_staged']
                    coverage_stageds.append(image_id)

                elif candidate_parent in image_nodes and (not (image_id in coverage_stageds)):
                    if not (image_id in current_invalids):
                        self.images_status[image_id] = self.status_choices['granularity_staged']

    def check_current_invalids(self, current_invalids):
        for (image_id, image_nodes) in self.images_graph.items():
            if len(set(image_nodes).intersection(self.graph_set)) != len(image_nodes):
                current_invalids.append(image_id)
        return current_invalids





