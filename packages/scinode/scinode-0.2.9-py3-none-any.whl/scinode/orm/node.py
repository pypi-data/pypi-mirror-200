from mongoengine import (
    Document,
    EmbeddedDocument,
    StringField,
    IntField,
    DateTimeField,
    ListField,
    MapField,
    ObjectIdField,
    EmbeddedDocumentField,
)


class Meta(EmbeddedDocument):
    daemon_name = StringField(max_length=50)
    identifier = StringField(max_length=50)
    node_type = StringField(max_length=50)
    nodetree_daemon = StringField(max_length=50)
    nodetree_uuid = StringField(max_length=50)
    ref_uuid = StringField(max_length=50)
    copy_uuid = StringField(max_length=50)
    platform = StringField(max_length=50)
    scattered_from = StringField(max_length=50)
    scattered_label = StringField(max_length=50)
    counter = IntField(min_value=0)
    args = ListField()
    kwargs = ListField()
    hash = StringField(max_length=100)


class Executor(EmbeddedDocument):
    path = StringField()
    name = StringField(max_length=50)
    type = StringField(max_length=50)


class Link(EmbeddedDocument):
    from_node = StringField(max_length=50)
    from_socket = StringField(max_length=50)
    from_socket_uuid = StringField(max_length=50)
    to_node = StringField(max_length=50)
    to_socket = StringField(max_length=50)
    to_socket_uuid = StringField(max_length=50)


class Socket(EmbeddedDocument):
    name = StringField(max_length=50)
    type = StringField(max_length=50)
    node_uuid = StringField(max_length=50)
    identifier = StringField(max_length=50)
    uuid = StringField(max_length=50)
    link_limit = IntField(min_value=0)
    serialize = EmbeddedDocumentField(Executor)
    deserialize = EmbeddedDocumentField(Executor)
    links = ListField(EmbeddedDocumentField(Link))


class Property(EmbeddedDocument):
    name = StringField(max_length=50)
    type = StringField(max_length=50)
    type = StringField(max_length=50)
    value = StringField()
    serialize = EmbeddedDocumentField(Executor)
    deserialize = EmbeddedDocumentField(Executor)


class Node(Document):
    meta = {"collection": "node"}

    _id = ObjectIdField()
    uuid = StringField(required=True)
    name = StringField(required=True, max_length=50)
    state = StringField(max_length=50)
    action = StringField(max_length=50)
    version = StringField(max_length=50)
    lastUpdate = DateTimeField()
    created = DateTimeField()
    description = StringField()
    log = StringField()
    error = StringField()
    index = IntField()
    id = IntField()
    metadata = EmbeddedDocumentField(Meta)
    executor = EmbeddedDocumentField(Executor)
    inputs = ListField(EmbeddedDocumentField(Socket))
    outputs = ListField(EmbeddedDocumentField(Socket))
    properties = MapField(EmbeddedDocumentField(Property))
    position = ListField()
    hash = StringField(max_length=100)

    def _init__(self, uuid, name):
        self.uuid = (uuid,)
        self.name = name


if __name__ == "__main__":
    from mongoengine import connect

    connect("scinode_db", host="mongodb://localhost:27017/")
    for n in Node.objects:
        print(n.name)
    n = Node.objects[0]
    n.name += "test"
    n.save()
