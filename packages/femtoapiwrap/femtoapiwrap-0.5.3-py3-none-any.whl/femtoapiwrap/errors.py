# Copyright ©2021. Femtonics Ltd. (Femtonics). All Rights Reserved.
# Permission to use, copy, modify this software and its documentation for educational,
# research, and not-for-profit purposes, without fee and without a signed licensing agreement, is
# hereby granted, provided that the above copyright notice, this paragraph and the following two
# paragraphs appear in all copies, modifications, and distributions. Contact info@femtonics.eu
# for commercial licensing opportunities.
#
# IN NO EVENT SHALL FEMTONICS BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
# INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
# THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF FEMTONICS HAS BEEN
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# FEMTONICS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE. THE SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED
# HEREUNDER IS PROVIDED "AS IS". FEMTONICS HAS NO OBLIGATION TO PROVIDE
# MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.


"""
Errors directly raised from this package.

.. versionchanged:: 0.4.0
    Major redesign to help user interfaces; PEP-8 compliant naming.
    Removed :exc:`IOError` and :exc:`TimeoutError` base classes.
"""

import typing as _t


class FemtoApiWrapError(Exception):
    """Base exception for this package.

    .. versionchanged:: 0.4.0
        No longer a subclass of :exc`IOError`.
        Subclasses redesigned to contain error information in fields.
    """

    message = 'Error caught in FemtoAPI wrapper'
    """Generic short message"""

    def __init__(self, message: str = None, **kwargs):
        super().__init__(message or self.message, {**self.__dict__, **kwargs})

    def __str__(self):
        return f'{self.message} {self.__dict__}'


class ApiCommandError(FemtoApiWrapError):
    """Raised when an API command failed and returned with an error code."""

    message = 'FemtoAPI command returned with error'

    def __init__(self, command: str, code: int, text: str):
        """
        :param command: what command failed
        :param code: value of ``APIWebSocketClient.sendJSCommand(...).getResultCode()``
        :param text: value of ``APIWebSocketClient.sendJSCommand(...).getErrorText()``
        """
        self.command = command
        self.code = code
        self.text = text
        super().__init__()


class ApiConnectionError(FemtoApiWrapError):
    """Connection to FemtoAPI web socket failed."""

    message = 'Connection to FemtoAPI web socket failed'

    def __init__(self, url):
        """
        :param url: websocket url of the attempted connection
        """
        self.url = url
        super().__init__()


class ApiLoginError(FemtoApiWrapError):
    """Login to MESc failed"""

    message = 'Login failed'

    def __init__(self, username: str, code: int, text: str):
        """
        :param username: username
        :param code: value of ``APIWebSocketClient.sendJSCommand(...).getResultCode()``
        :param text: value of ``APIWebSocketClient.sendJSCommand(...).getErrorText()``
        """
        self.username = username
        self.code = code
        self.text = text
        super().__init__()


class MeasurementTimeoutError(FemtoApiWrapError):
    """Cannot find microscope in the requested state within the specified time."""

    message = 'Measurement timed out'

    def __init__(self, what: str, time_passed_s, timeout_s):
        """
        :param what: what exactly timed out
        :param time_passed_s: actual time passed in seconds
        :param timeout_s: timeout in seconds
        """
        self.what = what
        self.time_passed_s = time_passed_s
        self.timeout_s = timeout_s
        super().__init__()


class NodeNotFoundError(FemtoApiWrapError):
    """Cannot find a node (file, session, unit, channel) that meets the conditions."""

    message = 'MESc node not found'

    def __init__(self, node_type, condition):
        """
        :param node_type: ``file``/``session``/``unit``/``channel``
        :param condition: search condition
        """
        self.node_type = node_type
        self.condition = condition
        super().__init__()


class MEScFileError(FemtoApiWrapError):
    """Base class for errors during MESc data structure processing."""

    message = 'Failed to process/create API data structure'


class EmptyJsonError(MEScFileError):
    """The raw metadata object is not provided / empty."""

    message = 'Metadata structure is empty'

    def __init__(self, metadata_type: str):
        self.metadata_type = metadata_type
        super().__init__()


class DimensionError(MEScFileError, IndexError):
    """Invalid / out of bounds index or dimension provided."""

    message = 'Dimensions or index out of bounds'

    def __init__(self, name: str, wrong: _t.Any, good: _t.Any):
        """
        :param name: name of the parameter / value
        :param wrong: the bad value
        :param good: the good values
        """
        self.name = name
        self.wrong = wrong
        self.good = good
        super().__init__()
        super(IndexError, self).__init__(wrong)


class PointSeriesKeyError(MEScFileError, KeyError):
    """Got a point series key not supported by MESc"""

    message = 'Point series keys must be in [0; 9]'

    def __init__(self, wrong: _t.Sequence[int]):
        """
        :param wrong: parameter values
        """
        self.wrong = wrong
        super().__init__()
        super(KeyError, self).__init__(wrong)


class JsonVersionError(MEScFileError, NotImplementedError):
    """The version found in the data structure being processed is not
    supported by the current function."""

    message = 'Unsupported JSON format version'

    def __init__(self, metadata_type: str, wrong: _t.Any, supported: _t.Any):
        """
        :param metadata_type: which (sub-)structure is being processed
        :param wrong: the version found
        :param supported: supported version(s)
        """
        self.metadata_type = metadata_type
        self.wrong = wrong
        self.supported = supported
        super().__init__()
        super(NotImplementedError, self).__init__(self.message)
