import os

from typing import Dict, Optional, Any

from core.base import Base, Factory

from .handlers.bistrover import IIDXBistrover
from core.common import Model, VersionConstants
from core.data import Data

MANAGED_VERSION = [
    VersionConstants.IIDX_BISTROVER
]


class IIDXFactory(Factory):
    MANAGED_CLASSES = [
        IIDXBistrover,
    ]

    @classmethod
    def register_all(cls) -> None:
        for game in ['LDJ']:
            Base.register(game, IIDXFactory)

    @classmethod
    def create(cls, data: Data, config: Dict[str, Any], model: Model, parentmodel: Optional[Model] = None) -> Optional[Base]:
        def version_from_date(date: int) -> Optional[int]:
            if date >= 2020102800:
                return VersionConstants.IIDX_BISTROVER
            return None

        if model.game == 'LDJ':
            if model.version is None:
                if parentmodel is None:
                    return None

                # We have no way to tell apart newer versions. However, we can make
                # an educated guess if we happen to be summoned for old profile lookup.
                if parentmodel.game not in ['LDJ']:
                    return None
                parentversion = version_from_date(parentmodel.version)
                if parentversion == VersionConstants.IIDX_BISTROVER:
                    return IIDXBistrover(data, config, model)

                # Unknown older version
                return None

            version = version_from_date(model.version)
            if version == VersionConstants.IIDX_BISTROVER:
                return IIDXBistrover(data, config, model)

        # Unknown game version
        return None
