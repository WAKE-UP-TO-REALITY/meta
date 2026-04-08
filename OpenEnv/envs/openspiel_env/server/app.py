# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
FastAPI application for the OpenSpiel Environment.

This module creates an HTTP server that exposes OpenSpiel games
over HTTP and WebSocket endpoints, compatible with EnvClient.

Usage:
    # Development (with auto-reload):
    uvicorn server.app:app --reload --host 0.0.0.0 --port 8000

    # Production:
    uvicorn server.app:app --host 0.0.0.0 --port 8000 --workers 4

    # Or run directly:
    uv run --project . server

Environment variables:
    OPENSPIEL_GAME: Game name to serve (default: "catch")
    OPENSPIEL_AGENT_PLAYER: Agent player ID (default: 0)
    OPENSPIEL_OPPONENT_POLICY: Opponent policy (default: "random")
"""

import os
import sys

# Add the repository root and src directory to sys.path to ensure correct module resolution
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

src_dir = os.path.join(repo_root, "src")
if os.path.exists(src_dir) and src_dir not in sys.path:
    sys.path.insert(0, src_dir)

import os

from openenv.core.env_server import create_app

from envs.openspiel_env.models import OpenSpielAction, OpenSpielObservation
from envs.openspiel_env.server.openspiel_environment import OpenSpielEnvironment

# Get game configuration from environment variables
game_name = os.getenv("OPENSPIEL_GAME", "catch")
agent_player = int(os.getenv("OPENSPIEL_AGENT_PLAYER", "0"))
opponent_policy = os.getenv("OPENSPIEL_OPPONENT_POLICY", "random")


# Factory function to create OpenSpielEnvironment instances
def create_openspiel_environment():
    """Factory function that creates OpenSpielEnvironment with config."""
    return OpenSpielEnvironment(
        game_name=game_name,
        agent_player=agent_player,
        opponent_policy=opponent_policy,
    )


# Create the FastAPI app with web interface and README integration
# Pass the factory function instead of an instance for WebSocket session support
app = create_app(
    create_openspiel_environment,
    OpenSpielAction,
    OpenSpielObservation,
    env_name="openspiel_env",
)


def main(host: str = "0.0.0.0", port: int = 8000):
    """
    Entry point for direct execution via uv run or python -m.

    This function enables running the server without Docker:
        uv run --project . server
        uv run --project . server --port 8001
        python -m openspiel_env.server.app

    Args:
        host: Host address to bind to (default: "0.0.0.0")
        port: Port number to listen on (default: 8000)
    """
    import uvicorn

    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
