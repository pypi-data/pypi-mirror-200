"""
@anchor pydoc:grizzly.tasks.until Until
This task calls the `request` method of a `grizzly.users` implementation, until condition matches the
payload returned for the request.

## Step implementations

* {@pylink grizzly.steps.scenario.tasks.step_task_request_with_name_endpoint_until}

* {@pylink grizzly.steps.scenario.tasks.step_task_client_get_endpoint_until}

## Statistics

Executions of this task will be visible in `locust` request statistics with request type `UNTL` indicating how
long time it took to finish the task. `name` will be suffixed with ` r=<retries>, w=<wait>, em=<expected_matches>`.

The request task that is being repeated until `condition` is true will have it's own entry in the statistics as an
ordinary {@pylink grizzly.tasks.request} or {@pylink grizzly.tasks.clients} task.

## Arguments

* `request` _{@pylink grizzly.tasks.request} / {@pylink grizzly.tasks.clients}_ - request that is going to be repeated

* `condition` _str_ - condition expression that specifies how `request` should be repeated

## Format

### `condition`

``` plain
<expression> [| [retries=<retries>][, wait=<wait>][, expected_matches=<expected_matches>]]
```

* `expression` _str_ - JSON- or Xpath expression

* `retries` _int_ (optional) - maximum number of times to repeat the request if `condition` is not met (default `3`)

* `wait` _float_ (optional) - number of seconds to wait between retries (default `1.0`)

* `expected_matches` _int_ (optional): number of matches that the expression should match (default `1`)

"""
import json
import logging

from typing import TYPE_CHECKING, Callable, Any, Type, List, Optional, Generator, Dict, cast
from time import perf_counter
from contextlib import contextmanager

from jinja2 import Template
from gevent import sleep as gsleep
from grizzly_extras.transformer import Transformer, TransformerContentType, TransformerError, transformer
from grizzly_extras.arguments import get_unsupported_arguments, parse_arguments, split_value

from grizzly.types.locust import Environment
from grizzly.types import RequestType

from . import GrizzlyTask, GrizzlyMetaRequestTask, template, grizzlytask

if TYPE_CHECKING:  # pragma: no cover
    from grizzly.context import GrizzlyContextScenario, GrizzlyContext
    from grizzly.scenarios import GrizzlyScenario


logger = logging.getLogger(__name__)


def no_error_handler(environment: Environment) -> Callable[..., None]:
    def no_error_handler_wrapper(request_type: str, name: str, response_time: int, response_length: int, exception: Optional[Exception] = None, **_kwargs: Dict[str, Any]) -> None:
        environment.stats.log_request(request_type, name, response_time, response_length)

        if exception is not None:
            logger.error(f'{request_type} {name}: {response_time=}, {response_length=}, {exception=}')
            environment.stats.total.log_error(None)
            environment.stats.get(name, request_type).log_error(None)

    return no_error_handler_wrapper


@contextmanager
def suppress(environment: Environment) -> Generator[None, None, None]:
    original_handlers = environment.events.request._handlers.copy()
    environment.events.request._handlers = [no_error_handler(environment)]

    try:
        yield
    finally:
        environment.events.request._handlers = original_handlers


@template('condition', 'request')
class UntilRequestTask(GrizzlyTask):
    request: GrizzlyMetaRequestTask
    condition: str

    transform: Optional[Type[Transformer]]
    matcher: Callable[[Any], List[str]]

    retries: int
    wait: float
    expected_matches: int

    def __init__(self, grizzly: 'GrizzlyContext', request: GrizzlyMetaRequestTask, condition: str, scenario: Optional['GrizzlyContextScenario'] = None) -> None:
        super().__init__(scenario)

        self.request = request
        self.condition = condition
        self.retries = 3
        self.wait = 1.0
        self.expected_matches = 1

        if self.request.content_type == TransformerContentType.UNDEFINED:
            raise ValueError('content type must be specified for request')

        self.transform = transformer.available.get(self.request.content_type, None)

        if '|' in self.condition:
            self.condition, until_arguments = split_value(self.condition)

            if '{{' in until_arguments and '}}' in until_arguments:
                until_arguments = Template(until_arguments).render(**grizzly.state.variables)

            arguments = parse_arguments(until_arguments)

            unsupported_arguments = get_unsupported_arguments(['retries', 'wait', 'expected_matches'], arguments)

            if len(unsupported_arguments) > 0:
                raise ValueError(f'unsupported arguments {", ".join(unsupported_arguments)}')

            self.retries = int(arguments.get('retries', self.retries))
            self.wait = float(arguments.get('wait', self.wait))
            self.expected_matches = int(arguments.get('expected_matches', '1'))

            if self.retries < 1:
                raise ValueError('retries argument cannot be less than 1')

            if self.wait < 0.1:
                raise ValueError('wait argument cannot be less than 0.1 seconds')

    def __call__(self) -> grizzlytask:
        if self.transform is None:
            raise TypeError(f'could not find a transformer for {self.request.content_type.name}')

        transform = cast(Transformer, self.transform)

        @grizzlytask
        def task(parent: 'GrizzlyScenario') -> Any:
            task_name = f'{self.scenario.identifier} {self.request.name}, w={self.wait}s, r={self.retries}, em={self.expected_matches}'
            condition_rendered = parent.render(self.condition)
            endpoint_rendered = parent.render(self.request.endpoint)

            if not transform.validate(condition_rendered):
                raise RuntimeError(f'{condition_rendered} is not a valid expression for {self.request.content_type.name}')

            parser = transform.parser(condition_rendered)
            number_of_matches = 0
            retry = 0
            exception: Optional[Exception] = None
            response_length = 0

            start = perf_counter()

            try:
                while retry < self.retries:
                    number_of_matches = 0

                    try:
                        gsleep(self.wait)

                        with suppress(parent.user.environment):
                            _, payload = self.request.execute(parent)

                        if payload is not None:
                            transformed = transform.transform(payload)
                            response_length += len(payload)
                        else:
                            raise TransformerError('response payload was not set')

                        matches = parser(transformed)
                        parent.logger.debug(f'{payload=}, condition={condition_rendered}, {matches=}')
                        number_of_matches = len(matches)
                    except Exception as e:
                        parent.logger.error(f'{task_name}: retry={retry}, endpoint={endpoint_rendered}, exception={str(e)}')
                        if exception is None:
                            exception = e
                        number_of_matches = 0
                    finally:
                        if number_of_matches == self.expected_matches:
                            break
                        else:
                            retry += 1
            except Exception as e:
                parent.logger.error(f'{task_name}: error retry={retry}', exc_info=True)
                if exception is None:
                    exception = e
            finally:
                response_time = int((perf_counter() - start) * 1000)

                if number_of_matches == self.expected_matches:
                    exception = None
                elif exception is None and number_of_matches != self.expected_matches:
                    exception = RuntimeError((
                        f'found {number_of_matches} matching values for {condition_rendered} in payload'
                    ))
                    try:
                        payload_formatted = json.dumps(json.loads(payload or ''), indent=2)
                    except Exception:  # pragma: no cover
                        payload_formatted = payload or ''
                    parent.logger.error(
                        f'{task_name}: endpoint={endpoint_rendered}, {number_of_matches=}, condition={condition_rendered}, {retry=}, {response_time=} payload=\n{payload_formatted}'
                    )

                parent.user.environment.events.request.fire(
                    request_type=RequestType.UNTIL(),
                    name=task_name,
                    response_time=response_time,
                    response_length=response_length,
                    context=parent.user._context,
                    exception=exception,
                )

                if exception is not None and self.scenario.failure_exception is not None:
                    raise self.scenario.failure_exception()

        return task
