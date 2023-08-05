""" This module implement tasks functionality  """
import json
from typing import Dict
from typing import List

import pandas as pd
from pandas import DataFrame
from requests import Response

from superwise.controller.base import BaseController
from superwise.models.notification import Notification
from superwise.resources.superwise_enums import NotifyUpon
from superwise.resources.superwise_enums import ScheduleCron


class PolicyController(BaseController):
    """Class ModelController - responsible for task functionality"""

    def __init__(self, client, sw):
        """

        ### Args:

        `client`: superwise client object

        `sw`: superwise  object

        """
        super().__init__(client, sw)
        self.path = "monitor/v1/policy"
        self.model_name = "Policy"
