from SFAP import PublisherItem

class TerminalPublisherItem(PublisherItem):
    def __init__(self, terminal_representation: str):
        super().__init__()
        self.terminal_representation = terminal_representation

    def terminalRepresentation(self) -> str:
        return self.terminal_representation
