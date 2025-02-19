from importlib.metadata import version
from typing import Any, Dict

import requests
from robot.api.deco import keyword, library

from .server import MockServer


@library(scope="GLOBAL", auto_keywords=False)
class FastHTTPMock:
    """
    FastHTTPMock is a lightweight HTTP mock server library for Robot Framework powered by FastAPI.

    = Table of Contents =

    - Introduction
    - Installation
    - Examples
    - Keyword Documentation

    = Introduction =

    FastHTTPMock provides an easy way to mock HTTP endpoints in your Robot Framework tests.
    It uses FastAPI and uvicorn to create a high-performance mock server that can be controlled
    through Robot Framework keywords.

    = Installation =

    To install the library, run:
    | ``pip install robotframework-fasthttpmock``

    = Examples =

    == Basic Usage ==

    | *** Settings ***          | | |
    | Library | FastHTTPMock | |
    | Library | RequestsLibrary | |

    | *** Test Cases ***        | | |
    | Mock Simple API Response | | |
    | Start Mock Server | port=8085 | |
    |    ${request}= | Create Dictionary | method=GET | path=/api/users |
    |    ${response}= | Create Dictionary | status=${200} | body={"users": ["user1", "user2"]} |
    |    ${id}= | Add Mock Interaction | ${request} | ${response} |
    |    ${resp}= | GET | http://localhost:8085/api/users |
    | Should Be Equal As Strings | ${resp.status_code} | 200 |
    | Verify Interaction Called | ${id} | 1 |
    |    [Teardown]             | Stop Mock Server | |

    """

    __version__ = version("robotframework-fasthttpmock")
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_VERSION = __version__
    ROBOT_LIBRARY_DOC_FORMAT = "HTML"

    def __init__(self):
        super().__init__()
        self.server = MockServer()
        self.base_url = None

    @keyword
    def start_mock_server(self, host: str = "127.0.0.1", port: int = 8085):
        """Start the mock HTTP server.

        | =Arguments= | =Description= |
        | ``host`` | Host address to bind the server to (default: 127.0.0.1) |
        | ``port`` | Port number to listen on (default: 8085) |

        Example:
        | Start Mock Server | port=8085 |
        """
        self.server.start(host, port)
        self.base_url = f"http://{host}:{port}"

    @keyword
    def stop_mock_server(self):
        """Stop the mock HTTP server.

        This keyword should be called in the test teardown to ensure proper cleanup.

        Example:
        | [Teardown] | Stop Mock Server |
        """
        self.server.stop()

    @keyword
    def add_mock_interaction(
        self, request: Dict[str, Any], response: Dict[str, Any]
    ) -> str:
        """Add a new mock interaction to the server.

        Arguments:
        - ``request`` - Dictionary containing request matching criteria
        - ``response`` - Dictionary containing response details

        Request dictionary can contain:
        - ``method`` - HTTP method (GET, POST, etc.)
        - ``path`` - URL path to match
        - ``headers`` - Headers to match (optional)
        - ``body`` - Body to match (optional)

        Response dictionary can contain:
        - ``status`` - HTTP status code
        - ``body`` - Response body
        - ``headers`` - Response headers (optional)

        Returns:
        - Interaction ID that can be used for verification

        Example:
        | ${request}= | Create Dictionary | method=GET | path=/api/users |
        | ${response}= | Create Dictionary | status=${200} | body={"users": ["user1"]} |
        | ${id}= | Add Mock Interaction | ${request} | ${response} |
        """
        interaction = {"request": request, "response": response}
        resp = requests.post(f"{self.base_url}/mock/interaction", json=interaction)
        return resp.json()["id"]

    @keyword
    def remove_mock_interaction(self, interaction_id: str):
        """Remove a mock interaction from the server.

        Arguments:
        - ``interaction_id`` - ID of the interaction to remove

        Example:
        | Remove Mock Interaction | ${id} |
        """
        requests.delete(f"{self.base_url}/mock/interaction/{interaction_id}")

    @keyword
    def verify_interaction_called(self, interaction_id: str, expected_calls: int):
        """Verify that an interaction was called the expected number of times.

        Arguments:
        - ``interaction_id`` - ID of the interaction to verify
        - ``expected_calls`` - Expected number of calls

        Fails if the actual number of calls doesn't match the expected number.

        Example:
        | Verify Interaction Called | ${id} | 1 |
        """
        resp = requests.get(f"{self.base_url}/mock/interaction/{interaction_id}")
        interaction = resp.json()
        actual_calls = interaction.get("call_count", 0)
        assert (
            actual_calls == expected_calls
        ), f"Expected {expected_calls} calls but got {actual_calls}"

    @keyword
    def clear_all_mock_interactions(self):
        """Clears all mock Interactions.

        Example:
        | Clear All Mock Interactions |
        """
        resp = requests.delete(f"{self.base_url}/mock/interactions")
        assert resp.status_code == 200, f"Expected 200 calls but got {resp.status_code}"
