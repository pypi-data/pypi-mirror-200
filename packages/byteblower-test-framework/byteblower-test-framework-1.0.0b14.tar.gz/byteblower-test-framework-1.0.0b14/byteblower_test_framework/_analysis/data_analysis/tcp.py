import pandas

from ..storage.tcp import HttpData
from .data_analyser import DataAnalyser


class HttpDataAnalyser(DataAnalyser):

    __slots__ = (
        '_http_data',
        '_df_dataspeed',
    )

    def __init__(self, http_data: HttpData) -> None:
        super().__init__()
        self._http_data = http_data
        self._df_dataspeed: pandas.DataFrame = None

    def analyse(self) -> None:
        """
        .. note::
           Currently, no pass/fail criteria.
        """
        # Get the data
        df_tcp = self._http_data.df_tcp_client
        self._df_dataspeed = df_tcp[['AVG dataspeed']]
        avg_data_speed = self._http_data.avg_data_speed

        self._set_log(f'Average data speed: {avg_data_speed} Bytes/s')
        self._set_result(True)

    @property
    def http_method(self):
        """Return the configured HTTP Request Method."""
        return self._http_data.http_method

    @property
    def df_http_client(self) -> pandas.DataFrame:
        return self._http_data.df_tcp_client

    @property
    def df_http_server(self) -> pandas.DataFrame:
        return self._http_data.df_tcp_server

    @property
    def df_dataspeed(self) -> pandas.DataFrame:
        return self._df_dataspeed

    @property
    def total_rx_client(self) -> int:
        """Number of received bytes at HTTP Client."""
        return self._http_data.total_rx_client

    @property
    def total_tx_client(self) -> int:
        """Number of transmitted bytes at HTTP Client."""
        return self._http_data.total_tx_client

    @property
    def total_rx_server(self) -> int:
        """Number of received bytes at HTTP Server."""
        return self._http_data.total_rx_server

    @property
    def total_tx_server(self) -> int:
        """Number of transmitted bytes at HTTP Server."""
        return self._http_data.total_tx_server

    @property
    def rx_first_client(self) -> pandas.Timestamp:
        """Time when the first packet was received at the HTTP Client."""
        return self._http_data.ts_rx_first_client

    @property
    def rx_last_client(self) -> pandas.Timestamp:
        """Time when the last packet was received at the HTTP Client."""
        return self._http_data.ts_rx_last_client

    @property
    def tx_first_client(self) -> pandas.Timestamp:
        """Time when the first packet was transmitted at the HTTP Client."""
        return self._http_data.ts_tx_first_client

    @property
    def tx_last_client(self) -> pandas.Timestamp:
        """Time when the last packet was transmitted at the HTTP Client."""
        return self._http_data.ts_tx_last_client

    @property
    def rx_first_server(self) -> pandas.Timestamp:
        """Time when the first packet was received at the HTTP Server."""
        return self._http_data.ts_rx_first_server

    @property
    def rx_last_server(self) -> pandas.Timestamp:
        """Time when the last packet was received at the HTTP Server."""
        return self._http_data.ts_rx_last_server

    @property
    def tx_first_server(self) -> pandas.Timestamp:
        """Time when the first packet was transmitted at the HTTP Server."""
        return self._http_data.ts_tx_first_server

    @property
    def tx_last_server(self) -> pandas.Timestamp:
        """Time when the last packet was transmitted at the HTTP Server."""
        return self._http_data.ts_tx_last_server
