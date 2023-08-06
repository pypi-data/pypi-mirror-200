# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import logging
import os

from contrast.extern import structlog

from contrast.agent.rewriter import register
from contrast.agent.assess.policy.string_propagation import (
    build_string_propagator_functions,
)


REWRITE_FOR_PYTEST: str = "__CONTRAST_REWRITE_FOR_PYTEST"


def start_runner():
    if os.environ.get(REWRITE_FOR_PYTEST):
        structlog.configure(
            wrapper_class=structlog.make_filtering_bound_logger(logging.ERROR)
        )

        build_string_propagator_functions()
        register(override_settings=True)
        # Short-circuit initialization
        return

    # We need to avoid this import for the REWRITE_FOR_PYTEST case
    from contrast.agent.agent_state import initialize

    initialize(runner=True, name="agent runner")
