# Copyright (C) 2022-2023 Indoc Research
#
# Contact Indoc Research for any questions regarding the use of this source code.

import logging
from logging import DEBUG
from logging import ERROR


class BaseClient:
    """
    Summary:
        The base client for all object storage class that will
        include some basic functions:
            - set logger level to DEBUG
            - set logger level to ERROR
    """

    def __init__(self, client_name: str) -> None:
        self.client_name = client_name

        # the flag to turn on class-wide logs
        self.logger = logging.getLogger('pilot.common')
        # initially only print out error info
        self.logger.setLevel(ERROR)

    async def debug_on(self):
        """
        Summary:
            The funtion will switch the log level to DEBUG
        """
        self.logger.setLevel(DEBUG)

        return

    async def debug_off(self):
        """
        Summary:
            The funtion will switch the log level to ERROR
        """
        self.logger.setLevel(ERROR)

        return
