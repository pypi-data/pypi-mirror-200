import enum
from datetime import timedelta, datetime
from typing import Optional, Union, List, Dict, Any

from pydantic import BaseModel


class TestEnvStatus(enum.Enum):
    STARTING = "STARTING"
    # RUNNING says nothing about any active agent(s). Check agents for that.
    RUNNING = "RUNNING"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    # FAILED: Something went wrong. (So it is possible the TestEnv is partially running without agents, etc.)
    FAILED = "FAILED"


class TestEnvDef(BaseModel):
    """
    The TestEnv Definition determines the type of TestEnv by describes the setup used to run tests in

    For example, there can be a separate TestEnvDefs for each of these:
       - A setup with one CSS and 1 client
       - A setup with one CSS and 2 client
       - A setup with 3 CSS's and 4 client
       - A setup with some other server software and a few clients

    Each of these TestEnvDefs specifies how to setup this environment.

    Currently, for each TestEnvDef.id, a specific ESpec to use is hardcoded. (This will be more flexible later)
    """

    id: int
    name: str
    description: str

    # TODO especRepo: repo  # details about ESpec to use
    # fixed parameters for this environment. For example: clientCount, serverCpuCount,
    fixed_parameters: Dict[int, Union[str, int, bool]]  # parameterId to parameterValue


class TestEnv(BaseModel):
    """
    TestEnv describes a running test setup in which tests (= TestFragments) can be run
    """

    id: int
    testenv_def_id: int  # this specifies if the TestEnv is jFed/slice based or something else
    slice_urn: Optional[str]  # optional during init and if not slice based
    # slice_expire*: optional during init and if not slice based
    # slice_expire: Best known slice expired time. Might be known indirectly.
    # slice_expire_confirmed: known directly from wall
    slice_expire: Optional[datetime]
    slice_expire_confirmed: Optional[datetime]
    auth_token: str  # auth token needed by agent running to auth themselves to perftest-server
    status: TestEnvStatus

    # commit_id: the CSS commit currently installed. This can be changed by running tests.
    commit_id: Optional[int]
    # TODO in_use: Optional[int]  # ActiveSweepId  # locked because in use by a certain active TestFragment
