from EventManager import EventType
from Repository import Repository
import uuid
import os

class Controller:
    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.repository = Repository()

    def load_node(self, user_id, node_id):
        if node_id is None:
            node_id = self.repository.get_god_node_uuid()

        self.watch_node(user_id, node_id)

        self.watch_children(user_id, node_id, 3)
        self.watch_parents(user_id, node_id, 2)

    def watch_children(self, user_id, node_id, max_level):
        children = self.repository.get_children_ids(node_id)
        for child_id in children:
            self.watch_node(user_id, child_id)
            if max_level > 1:
                self.watch_children(user_id, child_id, max_level - 1)

    def watch_parents(self, user_id, node_id, max_level):
        parents = self.repository.get_parent_ids(node_id)
        for parent_id in parents:
            self.watch_node(user_id, parent_id)
            if max_level > 1:
                self.watch_children(user_id, parent_id, max_level - 1)

    def watch_node(self, user_id, node_id):
        if self.event_manager.watch(user_id, node_id):
            data = self.repository.get_node(node_id)
            self.event_manager.throw_for_client(user_id, EventType.NODE_CHANGED, data)

    def update_new_client(self, user_id):
        self.load_node(user_id, None)

    def add_node(self, user_id, parent_id, sorting):
        node_id = str(uuid.uuid4())
        self.repository.add_node(node_id, parent_id)
        if sorting != -1:
            self.change_sorting(parent_id, node_id, sorting)

        self.load_node(user_id, node_id)
        return node_id

    def change_sorting(self, parent_id, node_id, new_sorting):
        children_to_change = self.repository.change_sorting(parent_id, node_id, new_sorting)
        for child in children_to_change:
            self.node_changed(child)
        self.node_changed(node_id)

    def update_node(self, node_id, data):
        self.repository.update_node(node_id, data)
        self.node_changed(node_id)

    def delete_node(self, node_id):
        self.repository.delete_node(node_id)
        self.event_manager.throw(EventType.NODE_DELETED, {"id": node_id})

    def delete_file(self, node_id):
        file = self.repository.get_node(node_id)["file"]
        if file != "":
            try:
                os.remove("data/uploads/" + file[:file.find("/")])
            except:
                pass
            self.update_node(node_id, {"file": ""})

    def move_node(self, node_id, old_parent, new_parent, sorting):
        self.repository.move_node(node_id, old_parent, new_parent)
        if sorting != -1:
            self.change_sorting(new_parent, node_id, sorting)
        else:
            self.node_changed(node_id)

    def node_changed(self, node_id):
        data = self.repository.get_node(node_id)
        self.event_manager.throw(EventType.NODE_CHANGED, data)