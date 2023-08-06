from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, DefaultDict

from better_translation._babel.lazy_proxy import LazyProxy
from better_translation.types import (
    Locale,
    MessageID,
    TranslatedText,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from better_translation.translator import ITranslator


@dataclass(slots=True)
class BaseTextProvider(ABC):
    @abstractmethod
    def _gettext(
        self,
        message_id: MessageID,
        /,
        *,
        default: TranslatedText | None = None,
        default_plural: TranslatedText | None = None,
        context: Any | None = None,
        locale: Locale | None = None,
        n: int | None = None,
        **extra: Any,
    ) -> str:
        ...

    def gettext(
        self,
        message_id: MessageID,
        /,
        *,
        default: TranslatedText | None = None,
        context: Any | None = None,
        locale: Locale | None = None,
        **extra: Any,
    ) -> str:
        return self._gettext(
            message_id,
            default=default,
            context=context,
            locale=locale,
            **extra,
        )

    def ngettext(
        self,
        message_id: MessageID,
        /,
        *,
        n: int,
        default: TranslatedText | None = None,
        default_plural: TranslatedText | None = None,
        context: Any | None = None,
        locale: Locale | None = None,
        **extra: Any,
    ) -> str:
        return self._gettext(
            message_id,
            default=default,
            default_plural=default_plural,
            context=context,
            locale=locale,
            n=n,
            **extra,
        )

    def lazy_gettext(
        self,
        message_id: MessageID,
        /,
        *,
        default: TranslatedText | None = None,
        context: Any | None = None,
        locale: Locale | None = None,
        **extra: Any,
    ) -> LazyProxy:
        return LazyProxy(
            self.gettext,
            message_id,
            default=default,
            context=context,
            locale=locale,
            **extra,
        )

    def lazy_ngettext(
        self,
        message_id: MessageID,
        /,
        *,
        n: int,
        default: TranslatedText | None = None,
        default_plural: TranslatedText | None = None,
        context: Any | None = None,
        locale: Locale | None = None,
        **extra: Any,
    ) -> LazyProxy:
        return LazyProxy(
            self.ngettext,
            message_id,
            default=default,
            default_plural=default_plural,
            context=context,
            locale=locale,
            n=n,
            **extra,
        )


@dataclass(slots=True)
class TextProvider(BaseTextProvider):
    translators: DefaultDict[Locale, ITranslator]
    locale_getter: Callable[[], Locale] = lambda: Locale("en")  # noqa: E731
    """Function to get current locale in case it is not provided."""

    def _gettext(
        self,
        message_id: MessageID,
        /,
        *,
        default: TranslatedText | None = None,
        default_plural: TranslatedText | None = None,
        context: Any | None = None,  # noqa: ARG002
        locale: Locale | None = None,
        n: int | None = None,
        **_: Any,
    ) -> TranslatedText:
        if locale is None:
            locale = self.locale_getter()

        translator = self.translators[locale]
        return translator.translate(
            message_id=message_id,
            locale=locale,
            default=default,
            default_plural=default_plural,
            n=n,
        )
