#!/usr/bin/env python
# coding: utf-8

"""! @brief ZIDS_Pipeline base class for the pipeline."""

from typing import List
from dsframework.base.common.component import ZIDS_Component
from dsframework.base.pipeline.predictables.predictable import ZIDS_Predictable
from dsframework.base.pipeline.artifacts.shared_artifacts import ZIDS_SharedArtifacts


class ZIDS_Pipeline():
    """! ZIDS_Pipeline base class for the pipeline.

    Its main job is to be the base for building the pipeline components.
    """

    def __init__(self):
        """! ZIDS_Pipeline class initializer."""
        self.components:List[ZIDS_Component] = []
        self.predictables:List[ZIDS_Predictable] = []
        self.artifacts = self.get_artifacts()
        self.build_pipeline()
        self.configure_pipeline()
        self.connect_pipeline()

    def get_artifacts(self):
        """! Loads and returns the artifacts and vocabs,

        This method gets overridden by its parent the generatedProjectNamePipeline.get_artifacts() method."""
        return ZIDS_SharedArtifacts()
    
    def build_pipeline(self):
        """! This is the main place where the pipeline gets build with all of its components.

        It gets overridden by a default implementation in generatedProjectNamePipeline.build_pipeline, where its
        four main components gets instantiated:

        - generatedProjectNamePreprocess
        - generatedProjectNamePredictor
        - generatedProjectNameForcer
        - generatedProjectNamePostprocess.
        """
        raise NotImplementedError

    def configure_pipeline(self, **kwargs):
        """! To add configurations that need to take place after the build_pipeline() method.

        Override method generatedProjectNamePipeline.configure_pipeline()
        """
        pass

    def connect_pipeline(self):
        """! This method distributes Artifacts instance to all pipeline components."""
        for c in self.components:
            c.artifacts = self.artifacts

    def preprocess(self, **kwargs) -> List[ZIDS_Predictable]:
        """! Runs in the begining of the pipeline

        It is a base method that need be overridden in generatedProjectNamePipeline.preprocess and
        needs to include all required steps before the Predictor model.

        Args:
            **kwargs: Dataset loaded initially.
        Returns:
            List[ZIDS_Predictable]: List of predictable objects."""
        raise NotImplementedError

    def postprocess(self, predictables):
        """! Runs at the end of the pipeline.

        It is a base method that need be overridden in generatedProjectNamePipeline.postprocess and
        return the list of results.

        Returns:
            List[generatedProjectNameOutputs]: List of results.
        """
        raise NotImplementedError


    def add_component(self, component:ZIDS_Component):
        """! Adds a component to pipeline.

        Two components added by default: Predictor, Forcer.

        In addition to the pre-existing ones the preprocessor and postprocessor.

        Args:
            component: ZIDS_Component, component to add.
        """
        self.components.append(component)

    def __call__(self,  **kwargs):
        """! ZIDS_Pipeline __call__() method, runs the execute() method of this class with specified Args.

        Args:
            **kwargs: Initially loaded dataset.
        """
        return self.execute( **kwargs)

    def execute(self, **kwargs):
        """! Executes the pipeline,

        Runs the execute method for all registered components one after the other,

        Args:
            **kwargs: Initially loaded dataset.
        """
        self.predictables = self.preprocess(**kwargs)
        for c in self.components:
            self.predictables = c.execute(self.predictables)
        return self.postprocess(self.predictables)
