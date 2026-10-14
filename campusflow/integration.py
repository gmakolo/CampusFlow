"""Engineer B's adapters for A-owned APIs; no replacement data-layer rules."""

from importlib import import_module


class IntegrationPendingError(ValueError):
    """A documented Engineer A contract has not yet been implemented."""


def integration_api(module_name, function_name):
    qualified = f"campusflow.{module_name}"
    try:
        module = import_module(qualified)
    except ModuleNotFoundError as error:
        if error.name != qualified:
            raise
        raise IntegrationPendingError(
            f"Engineer A's {module_name} API is not integrated yet. "
            "See docs/integration-contracts.md; no substitute backend is used."
        ) from error
    function = getattr(module, function_name, None)
    if not callable(function):
        raise IntegrationPendingError(f"{qualified}.{function_name} is required by the integration contract.")
    return function
