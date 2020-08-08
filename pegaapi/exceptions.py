class PegaAPIException(Exception):
    def __init__(self, message: str, node: str, service: str):
        self.message = message
        self.node = node
        self.service = service

        super().__init__(self.message)

    def __str__(self):
        return "Node: {}; Service: {}; message: {}".format(
            self.node, self.service, self.message
        )
