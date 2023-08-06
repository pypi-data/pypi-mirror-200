from __future__ import annotations

from typing import Optional

from .custom_sample_data import CustomSampleData
from .local_custom_sample import LocalCustomSample
from ..network_sample import NetworkSample


class CustomSample(NetworkSample[CustomSampleData], LocalCustomSample):

    """
        Represents the custom Sample object from Coretex.ai
    """

    def __init__(self) -> None:
        NetworkSample.__init__(self)

    @classmethod
    def createCustomSample(cls, name: str, datasetId: int, filePath: str) -> Optional[CustomSample]:
        """
            Creates a new sample with the provided name and path

            Parameters:
            name: str -> sample name
            datasetId: int -> id of dataset to which the sample will be added
            filePath: str -> path to the sample

            Returns:
            The created sample object or None if creation failed
        """

        parameters = {
            "name": name,
            "dataset_id": datasetId
        }

        return cls._genericSampleImport("custom-item-import", parameters, filePath)
