"""Module for reporting in JSON format."""
import logging
from enum import Enum
from typing import Any, Dict, List, Optional, Union  # for type hinting

from pandas import DataFrame  # for type hinting
from pandas import Series

from .._analysis.analyseraggregator import JsonAnalyserAggregator
from .._analysis.flow_analyser import (  # for type hinting
    AnalysisDetails,
    FlowAnalyser,
)
from .._traffic.flow import Flow  # for type hinting
from .byteblowerreport import ByteBlowerReport

# Type aliases
# Recursive content type:
_Content = Dict[str, Union['_Content', str, int, float, bool]]
_ContentList = List[_Content]


class ByteBlowerJsonReport(ByteBlowerReport):
    """Generate report in JSON format.

    Generates summary information of test status,
    test configuration and results from all flows.

    This report contains:

    * Global test status
    * Port configuration (**to-do**)
    * Correlated results

       * Aggregated results over all flows
         (supporting aggregation of *over time* data (**to-do**)
         and *summary* data)
    * Per-flow results (**to-do**)

       * Flow configuration
       * Results for all Analysers attached to the flow
    """

    _FILE_FORMAT: str = 'json'

    __slots__ = (
        '_analyseraggregator',
        '_config',
        '_summary',
        '_flows',
    )

    def __init__(
        self,
        output_dir: Optional[str] = None,
        filename_prefix: str = 'byteblower',
        filename: Optional[str] = None
    ) -> None:
        """Create a ByteBlower JSON report generator.

        The report is stored under ``<output_dir>``. The default structure
        of the file name is

           ``<prefix>_<timestamp>.json``

        where:

        * ``<output_dir>``:  Configurable via ``output_dir``.
          Defaults to the current working directory.
        * ``<prefix>``: Configurable via ``filename_prefix``
        * ``<timestamp>``: Current time. Defined at construction time of the
          ``ByteBlowerReport`` Python object.

        :param output_dir: Override the directory where
           the report file is stored, defaults to ``None``
           (meaning that the "current directory" will be used)
        :type output_dir: str, optional
        :param filename_prefix: Prefix for the ByteBlower report file name,
           defaults to 'byteblower'
        :type filename_prefix: str, optional
        :param filename: Override the complete filename of the report,
           defaults to ``None``
        :type filename: str, optional
        """
        super().__init__(
            output_dir=output_dir,
            filename_prefix=filename_prefix,
            filename=filename
        )
        self._analyseraggregator = JsonAnalyserAggregator()
        self._reset_content()

    def add_flow(self, flow: Flow) -> None:
        """Add the flow info.

        :param flow: Flow to add the information for
        :type flow: Flow
        """
        self._render_flow(flow)
        aggregated_analyser: Optional[FlowAnalyser] = None
        sorted_analysers = self._analyseraggregator.order_by_support_level(
            flow._analysers
        )
        for analyser in sorted_analysers:
            if not analyser.has_passed:
                self._summary['status']['passed'] = False
            # NOTE - Avoid aggregating twice with the same Flow data
            if not aggregated_analyser:
                logging.debug(
                    'Aggregating supported analyser %s',
                    type(analyser).__name__
                )
                self._analyseraggregator.add_analyser(analyser)
                aggregated_analyser = analyser

    def render(
        self, api_version: str, framework_version: str, port_list: DataFrame
    ) -> None:
        """Render the report.

        :param port_list: Configuration of the ByteBlower Ports.
        :type port_list: DataFrame
        """
        # TODO - Render the config (from port_list)

        correlation_dict = self._summarize_aggregators()
        if correlation_dict:
            self._summary['aggregated'] = correlation_dict

        content = Series(
            data={
                'apiVersion': api_version,
                'testFrameworkVersion': framework_version,
                'config': self._config,
                'summary': self._summary,
                'flows': self._flows,
            }
        )

        content.to_json(
            self.report_url,
            date_format='iso',
            default_handler=_extra_encode_json
        )

    def clear(self) -> None:
        """Start with empty report contents."""
        self._analyseraggregator = JsonAnalyserAggregator()
        self._reset_content()

    def _reset_content(self) -> None:
        self._config: _Content = {}
        self._summary: _Content = {
            'status': {
                'passed': True,
            },
        }
        self._flows: _ContentList = []

    def _summarize_aggregators(self) -> Optional[_Content]:
        # Check if we can do aggregation
        if not self._analyseraggregator.can_render():
            # Get the summary from the aggregator
            return
        return self._analyseraggregator.summarize()

    def _render_flow(self, flow: Flow) -> None:
        has_passed = True
        tests: _ContentList = []

        # Process the analyser results
        analyser: FlowAnalyser
        for analyser in flow._analysers:
            has_passed = has_passed and analyser.has_passed
            tests.append(
                self._render_test(
                    analyser.type, analyser.has_passed, analyser.details()
                )
            )

        # Store the results
        flow_details: _Content = {}
        self._flows.append(flow_details)

        # TODO - Move to Flow or FlowRenderer
        flow_details['name'] = flow.name
        flow_details['type'] = flow.type
        flow_details['source'] = {
            'name': flow.source.name,
        }
        flow_details['destination'] = {
            'name': flow.destination.name,
        }
        flow_details['status'] = {
            'passed': has_passed,
        }
        flow_tests: _ContentList = flow_details.setdefault('analysers', [])
        flow_tests.extend(tests)

    def _render_test(
        self, test_type: str, has_passed: bool,
        result_details: Optional[AnalysisDetails]
    ) -> _Content:
        test_result: _Content = {
            'type': test_type,
            'status': {
                'passed': has_passed,
            },
        }
        if result_details is not None:
            test_result['results'] = result_details

        return test_result


def _extra_encode_json(o: Any) -> Any:
    if isinstance(o, Enum):
        return o.value

    # Let the base class default method raise the TypeError
    # return JSONEncoder.default(self, o)
    raise TypeError(
        f'Object of type {o.__class__.__name__} '
        'is not JSON serializable'
    )
