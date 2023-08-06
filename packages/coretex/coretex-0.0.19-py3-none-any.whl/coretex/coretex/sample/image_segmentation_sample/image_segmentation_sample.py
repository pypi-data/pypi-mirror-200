from __future__ import annotations

from typing import Optional

from ..image_sample import ImageSample


class ImageSegmentationSample(ImageSample):
    """
        Represents the Image segmentation sample object from Coretex.ai
    """

    @classmethod
    def createImageSegmentationSample(cls, datasetId: int, filePath: str) -> Optional[ImageSegmentationSample]:
        """
            Creates a new sample with the provided name and path

            Parameters:
            datasetId: int -> id of dataset to which sample will be added
            filePath: str -> path to the sample

            Returns:
            The created sample object or None if creation failed
        """

        return cls.createImageSample(datasetId, filePath)
