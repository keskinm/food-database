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
        self.update_status(nodes_to_add=nodes_to_add, extract=None)

    def add_extract(self, extract):
        for (image_id, labels) in extract.items():
            self.images_nodes.setdefault(image_id, []).append(labels)
        self.update_status(extract=extract, nodes_to_add=None)

    def get_extract_status(self):
        return self.images_status

    def update_status(self, extract, nodes_to_add):
        if extract is not None:
            for (image_id, labels) in extract.items():
                self.images_status.setdefault(image_id, self.status_choices['valid'])
                for label in labels:
                    if not (label in list(self.nodes_set)):
                        self.images_status[image_id] = self.status_choices['invalid']
                        break

		# if nodes_to_add is not None:

		if nodes_to_add is not None:
			for (child, parent) in nodes_to_add:
				for (image_id, image_nodes) in self.images_nodes.items():
					if parent in image_nodes[0]:
						self.images_status[image_id] = self.status_choices['granularity_staged']



