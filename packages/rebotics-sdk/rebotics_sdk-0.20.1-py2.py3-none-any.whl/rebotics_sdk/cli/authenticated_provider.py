import pathlib

try:
    import click
except ImportError:
    raise Exception("To use authenticated role provider you have to install rebotics_sdk[shell]")

from rebotics_sdk.cli.utils import app_dir, ReboticsScriptsConfiguration

from rebotics_sdk.providers import \
    RetailerProvider, CvatProvider, AdminProvider, DatasetProvider, FVMProvider, HawkeyeProvider


PROVIDER_NAME_TO_CLASS = {
    'retailer': RetailerProvider,
    'cvat': CvatProvider,
    'admin': AdminProvider,
    'dataset': DatasetProvider,
    'fvm': FVMProvider,
    'hawkeye': HawkeyeProvider,
}


class AuthenticatedRoleProvider:
    def __init__(self):
        self.app_path = pathlib.Path(app_dir)
        assert self.app_path.exists(), "App path from cli should exist and be available"

    def get_provider(self, provider_name, role):
        config_provider = ReboticsScriptsConfiguration(
            self.app_path / f"{provider_name}.json",
            PROVIDER_NAME_TO_CLASS[provider_name]
        )
        return config_provider.get_provider(role)
