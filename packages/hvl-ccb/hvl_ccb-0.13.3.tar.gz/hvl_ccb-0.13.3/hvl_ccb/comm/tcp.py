#  Copyright (c) ETH Zurich, SIS ID and HVL D-ITET
#
"""
TCP communication protocol. Makes use of the socket library.
"""

import logging
import socket
from ipaddress import IPv4Address, IPv6Address
from typing import Union

from hvl_ccb.comm import CommunicationProtocol
from hvl_ccb.configuration import configdataclass
from hvl_ccb.utils.validation import validate_and_resolve_host, validate_tcp_port

logger = logging.getLogger(__name__)


@configdataclass
class TcpCommunicationConfig:
    """
    Configuration dataclass for :class:`TcpCommunication`.
    """

    # Host is the IP address of the connected device.
    host: Union[str, IPv4Address, IPv6Address]
    # TCP port
    port: int = 54321
    # TCP receiving buffersize
    bufsize: int = 1024

    def clean_values(self):
        # if necessary, converts host to a valid IP address
        self.force_value("host", validate_and_resolve_host(self.host, logger))
        validate_tcp_port(self.port, logger)
        if self.bufsize < 1:
            raise ValueError("Buffer size has to be >= 1")


class Tcp(CommunicationProtocol):
    """
    Tcp Communication Protocol.
    """

    def __init__(self, configuration):
        """Constructor socket"""
        super().__init__(configuration)

        # create the communication port specified in the configuration
        logger.debug(
            'Create socket TcpClient with host: "{}", Port: "{}"'.format(
                self.config.host,
                self.config.port,
            )
        )
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    @staticmethod
    def config_cls() -> type[TcpCommunicationConfig]:
        return TcpCommunicationConfig

    def write(self, command: str = "") -> None:
        """
        TCP write function
        :param command: command string to be sent
        :return: none
        """
        self.sock.send(bytes(command, "ascii"))
        logger.debug(
            "Sent {command}".format(
                command=command,
            )
        )

    def read(self) -> str:
        """
        TCP read function
        :return: information read from TCP buffer formatted as string
        """
        reply = self.sock.recv(self.config.bufsize)
        reply = reply.decode("ascii")
        logger.debug(
            "Received via TCP: {reply}".format(
                reply=reply,
            )
        )
        return reply

    def open(self) -> None:
        """
        Open TCP connection.
        """

        # open the port
        logger.debug("Open TCP Port.")

        self.sock.connect((self.config.host, self.config.port))

    def close(self) -> None:
        """
        Close TCP connection.
        """

        # close the port
        logger.debug("Close TCP Port.")

        self.sock.close()
