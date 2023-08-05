import logging

from typing import TYPE_CHECKING, Optional, Dict, Any, cast
from os import environ

from locust.exception import StopUser
from locust.user.sequential_taskset import SequentialTaskSet
from jinja2 import Template

from grizzly.types import ScenarioState
from grizzly.context import GrizzlyContext
from grizzly.testdata.communication import TestdataConsumer
from grizzly.tasks import GrizzlyTask, grizzlytask

if TYPE_CHECKING:  # pragma: no cover
    from grizzly.users.base import GrizzlyUser


class GrizzlyScenario(SequentialTaskSet):
    consumer: TestdataConsumer
    logger: logging.Logger
    grizzly: GrizzlyContext

    def __init__(self, parent: 'GrizzlyUser') -> None:
        super().__init__(parent=parent)
        self.logger = logging.getLogger(f'{self.__class__.__name__}/{id(self)}')
        self.grizzly = GrizzlyContext()
        self.user.scenario_state = ScenarioState.STOPPED

    @property
    def user(self) -> 'GrizzlyUser':
        return cast('GrizzlyUser', self._user)

    @classmethod
    def populate(cls, task_factory: GrizzlyTask) -> None:
        task = task_factory()

        if callable(getattr(cls, 'pace', None)):
            cls.tasks.insert(-1, task)
        else:  # pragma: no cover
            cls.tasks.append(task)

    def render(self, input: str, variables: Optional[Dict[str, Any]] = None) -> str:
        if variables is None:
            variables = {}

        return Template(input).render(**self.user._context['variables'], **variables)

    def prefetch(self) -> None:
        pass

    def on_start(self) -> None:
        producer_address = environ.get('TESTDATA_PRODUCER_ADDRESS', None)
        if producer_address is not None:
            self.consumer = TestdataConsumer(
                scenario=self,
                address=producer_address,
                identifier=self.__class__.__name__,
            )
            self.user.scenario_state = ScenarioState.RUNNING
        else:
            self.logger.error('no address to testdata producer specified')
            raise StopUser()

        self.prefetch()

        for task in self.tasks:
            if isinstance(task, grizzlytask):
                task.on_start(self)

    def on_stop(self) -> None:
        for task in self.tasks:
            if isinstance(task, grizzlytask):
                task.on_stop(self)

        self.consumer.stop()
        self.user.scenario_state = ScenarioState.STOPPED


from .iterator import IteratorScenario


__all__ = [
    'GrizzlyScenario',
    'IteratorScenario',
]
