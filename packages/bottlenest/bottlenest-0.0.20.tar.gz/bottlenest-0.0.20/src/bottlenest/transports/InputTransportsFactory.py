class InputTransportsFactory:
    """Factory for InputTransports."""

    def __init__(self, config):
        self.config = config

    def create(self, transport_name):
        """Create a new InputTransport."""
        transport_class = self.config.get('input_transports', transport_name)
        transport = transport_class()
        return transport
