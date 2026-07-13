# TODO: Validate
"""Rebuilds Naphki models."""

import logging

from good_ass_pydantic_integrator.utils import rebuild_models

import naphki

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    rebuild_models(naphki)
