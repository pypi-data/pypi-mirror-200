from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

from better_translation.storage import StorageMessage

if TYPE_CHECKING:
    from better_translation.storage import IStorage
    from better_translation.types import (
        Locale,
        MessageID,
        TranslatedText,
    )


logger = logging.getLogger(__name__)


class ITranslator(ABC):
    @abstractmethod
    def translate(  # noqa: PLR0913
        self,
        message_id: MessageID,
        locale: Locale,
        default: TranslatedText | None = None,
        default_plural: TranslatedText | None = None,
        n: int | None = None,
    ) -> TranslatedText:
        ...


@dataclass(slots=True)
class DefaultTranslator(ITranslator):
    storage: IStorage

    def translate(  # noqa: PLR0913
        self,
        message_id: MessageID,
        locale: Locale,
        default: TranslatedText | None = None,
        default_plural: TranslatedText | None = None,
        n: int | None = None,
    ) -> TranslatedText:
        if n is None:
            return self._translate_singular(
                message_id=message_id,
                locale=locale,
                default=default,
            )

        return self._translate_plural(
            message_id=message_id,
            locale=locale,
            n=n,
            default=default,
            default_plural=default_plural,
        )

    def _translate_singular(
        self,
        message_id: MessageID,
        locale: Locale,
        default: TranslatedText | None = None,
    ) -> TranslatedText:
        message = self._get_message(
            message_id=message_id,
            default=default,
        )

        translation = message.translations.get(locale)
        if translation is not None:
            return translation.singular

        return message.default

    def _translate_plural(  # noqa: PLR0913
        self,
        message_id: MessageID,
        locale: Locale,
        n: int,
        default: TranslatedText | None = None,
        default_plural: str | None = None,
    ) -> TranslatedText:
        message = self._get_message(
            message_id=message_id,
            default=default,
            default_plural=default_plural,
        )

        translation = message.translations.get(locale)
        if translation is not None:
            singular, plural = translation.singular, translation.plural
        else:
            singular, plural = message.default, message.default_plural

        return self._get_singular_or_plural(n, singular, plural)

    def _get_message(
        self,
        message_id: MessageID,
        default: TranslatedText | None = None,
        default_plural: TranslatedText | None = None,
    ) -> StorageMessage:
        message = self.storage.get_message(message_id=message_id)
        if message is not None:
            return message

        default = default or message_id
        default_plural = default_plural or message_id

        logger.warning(
            "No message found for '%s'. Using the default values: '%s', '%s'",
            message_id,
            default,
            default_plural,
        )

        return StorageMessage(
            id=message_id,
            default=default,
            default_plural=default_plural,
            translations={},
            context="<no context>",
            has_plural=False,
        )

    def _get_singular_or_plural(
        self,
        n: int,
        singular: TranslatedText,
        plural: TranslatedText,
    ) -> TranslatedText:
        if n == 1:
            return singular

        return plural
