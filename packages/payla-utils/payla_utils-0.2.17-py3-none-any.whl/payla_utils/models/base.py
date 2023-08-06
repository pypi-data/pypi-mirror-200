from __future__ import annotations

from functools import lru_cache
from typing import Any

from django.contrib.admin.sites import all_sites
from django.core.checks import Error
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class PaylaQuerySet(models.QuerySet):
    """
    This custom QuerySet with get_or_none method
    """

    def get_or_none(self, *args: Any, **kwargs: Any) -> PaylaModel | None:
        """
        Use this instead of Queryset.get to either get an object if it exists or
        None if it doesn't. This is a shortcut to avoid having to catch DoesNotExist
        exceptions.

        Returns:
            PaylaModel | None: Either the model if it exists or None if it doesn't.
        """
        try:
            return self.get(*args, **kwargs)
        except self.model.DoesNotExist:
            return None

    def update(self, *args, **kwargs) -> int:
        """
        Override Queryset.update to make sure that modified_at is also updated when
        performing multi-row updates.

        Returns:
            int: number of rows updated
        """
        if 'modified_at' not in kwargs:
            kwargs['modified_at'] = now()
        return super().update(*args, **kwargs)


class PaylaModel(models.Model):
    created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name=_('Last modified'), auto_now=True)

    objects = PaylaQuerySet.as_manager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Overriding the save method in order to make sure that
        modified field is updated even if it is not given as
        a parameter to the update field argument.
        """
        update_fields = kwargs.get('update_fields', None)
        if update_fields:
            kwargs['update_fields'] = set(update_fields).union({'modified_at'})

        super().save(*args, **kwargs)

    @classmethod
    @lru_cache(maxsize=1)
    def get_registered_models(cls) -> set[models.Model]:
        registered_models = set()
        for admin_site in all_sites:
            for model, admin in admin_site._registry.items():
                registered_models.add(model)
                for inline in admin.inlines:
                    registered_models.add(inline.model)
        return registered_models

    @classmethod
    def check(cls, **kwargs):
        errors = super().check(**kwargs)
        if hasattr(cls, 'objects') and not issubclass(cls.objects._queryset_class, PaylaQuerySet):
            errors.append(
                Error(
                    f'Model {cls.__name__} objects must be a subclass of PaylaQuerySet',
                    hint=f'Your custom queryset class for model {cls.__name__} must be extending from PaylaQueryset',
                    obj=cls,
                    id='payla_utils.E001',
                )
            )

        if cls not in cls.get_registered_models():
            errors.append(
                Error(
                    f"Model {cls.__name__} does not have an admin",
                    hint=f"Register the model {cls.__name__} in the admin",
                    obj=cls,
                    id='payla_utils.E002',
                )
            )

        return errors
