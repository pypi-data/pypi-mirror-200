#!/usr/bin/env python
# coding: utf-8

##
# @file
# @brief ZIDS_Preprocessor base class for Preprocess class.

from typing import List, Any
from dsframework.base.common.component import ZIDS_Component
from dsframework.base.pipeline.predictables.predictable import ZIDS_Predictable
from dsframework.base.pipeline.artifacts.shared_artifacts import ZIDS_SharedArtifacts

class ZIDS_Preprocessor(ZIDS_Component):
    """! ZIDS_Preprocessor the base class for Preprocess class.

    This is the first stage of the pipeline and its main goal is to prepare our dataset format to the model.
    """

    def __init__(self, artifacts:ZIDS_SharedArtifacts=None):
        """! ZIDS_Preprocessor initializer

        Args:
            artifacts(ZIDS_SharedArtifacts): Shared artifacts instance.
        """

        ##
        # @hidecallgraph @hidecallergraph
        super().__init__(artifacts)
        self.input = None

    def __call__(self, **kwargs: Any) -> Any:
        """! ZIDS_Preprocessor.preprocess __call__ method. It is called when its instance gets called ().

        Args:
            **kwargs: Data loaded initially to run model on.
        Returns:
            List[ZIDS_Predictable]: Result of execute method with **kwargs as parameter.
        """
        return self.execute(**kwargs)

    def normalize_input(self, **kwargs: Any) -> Any:
        """! ZIDS_Preprocessor.normalize_input base method. Implemented in generatedProjectNamePreprocess class."""
        raise NotImplementedError

    def preprocess(self, raw_input:Any):
        """! ZIDS_Preprocessor.preprocess,
        Override method in generatedProjectNamePreprocess class and return a list of predictable objects.


        Args:
            raw_input: Data loaded initially to run model on.

        Returns:
            List[ZIDS_Predictable] - Not implemented yet.

        Raises:
            NotImplementedError

        """
        raise NotImplementedError
        ## Should return a list of predictable objects

    def execute(self, **kwargs: Any) -> List[ZIDS_Predictable]:
        """! Executes preprocess stage.

        Args:
            **kwargs: Data loaded initially to run model on.
        Returns:
            List[ZIDS_Predictable]: List of predictable objects
        """
        self.input = self.normalize_input(**kwargs)
        return self.preprocess(self.input)

