import torch


class State(dict):
    """
    A state in the temporal state buffer.
    Extends dict to allow for arbitrary state data.

    Methods
    -------
    encode()
        Encodes the state to another state.
    decode()
        Decodes the state to another state.
    tensor()
        Returns the state as a tensor.

    TODO
    ----
    - Provide a mapping as part of the _flatten method to reconstruct the state
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def encode(self) -> str:
        """
        Encodes the state to another state.
        """
        raise NotImplementedError("Haven't developed this yet")

    def decode(self) -> dict:
        """
        Decodes the state to another state.
        """
        raise NotImplementedError("Haven't developed this yet")

    def _flatten(self) -> list[float]:
        """
        Flattens the state to a list of floats.
        """
        return [value for value in self.values()]

    def tensor(self) -> torch.Tensor:
        """
        Returns the state as a tensor.
        """
        # Take the contents of the dict and flatten to a single tensor
        return torch.tensor(self._flatten(), dtype=torch.float32)
