from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django import forms
from django.contrib import admin
from django.db import models

from better_translation.integrations.django.models import (
    BaseMessage,
    BaseTranslation,
)

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from django.http import HttpRequest

admin.ModelAdmin.__class_getitem__ = classmethod(  # type: ignore[attr-defined]
    lambda cls, _: cls,
)
admin.TabularInline.__class_getitem__ = classmethod(  # type: ignore[attr-defined]
    lambda cls, _: cls,
)


class BaseMessageAdmin(admin.ModelAdmin[BaseMessage]):
    list_display = ("id", "default", "context", "is_used")
    readonly_fields = ("id", "context", "is_used")
    search_fields = (
        "id",
        "default",
        "default_plural",
        "context",
        "translations__singular",
        "translations__plural",
    )

    def get_fields(
        self,
        request: HttpRequest,  # noqa: ARG002
        obj: BaseMessage | None = None,
    ) -> Sequence[Callable[..., Any] | str]:
        if obj is None:
            return ("id", "default", "default_plural", "context", "is_used")

        fields = ["id", "default"]
        if obj.default_plural and obj.default_plural != obj.default:
            fields.append("default_plural")

        if obj.context:
            fields.append("context")

        fields.append("is_used")

        return fields


class BaseTranslationInline(admin.TabularInline[BaseTranslation]):
    model = BaseTranslation
    extra = 0
    formfield_overrides = {
        models.TextField: {
            "widget": forms.Textarea(attrs={"rows": 6, "cols": 50}),
        },
    }

    # pyright: reportIncompatibleMethodOverride=false
    def get_fields(
        self,
        request: HttpRequest,  # noqa: ARG002
        obj: BaseMessage | None = None,
    ) -> Sequence[Callable[..., Any] | str]:
        if obj is None or obj.has_plural:
            return ("locale", "singular", "plural")

        return ("locale", "singular")
