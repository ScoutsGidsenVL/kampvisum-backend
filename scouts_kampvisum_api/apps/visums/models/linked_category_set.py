from django.db import connections, models

from apps.visums.models import CampVisum
from apps.visums.models.enums import CheckState
from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.fields import DefaultCharField


class LinkedCategorySetQuerySet(models.QuerySet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def count_unchecked_checks(self, pk):
        with connections['default'].cursor() as cursor:
            cursor.execute(
                f"select count(1) from visums_linkedcategory vl where vl.category_set_id = '{pk}' and vl.check_state = 'UNCHECKED'"
            )
            return cursor.fetchone()[0]

        return 1


class LinkedCategorySetManager(models.Manager):
    def get_queryset(self):
        return LinkedCategorySetQuerySet(self.model, using=self._db).prefetch_related('categories')

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        visum = kwargs.get("visum", None)
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except Exception:
                pass

        if visum:
            try:
                return self.get_queryset().get(visum=visum)
            except Exception:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate CampVisum instance(s) with the provided params: (id: {})".format(
                    pk,
                )
            )

        return None

    def has_unchecked_checks(self, pk):
        return True if self.get_queryset().count_unchecked_checks(pk=pk) == 0 else False


class LinkedCategorySet(AbstractBaseModel):

    objects = LinkedCategorySetManager()

    visum = models.OneToOneField(
        CampVisum, on_delete=models.CASCADE, related_name="category_set"
    )
    check_state = DefaultCharField(
        choices=CheckState.choices,
        default=CheckState.UNCHECKED,
        max_length=32
    )

    class Meta:
        indexes = [
            models.Index(fields=['visum'], name='visum_idx'),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['visum'], name='unique_visum_for_set')
        ]

    def is_checked(self) -> CheckState:
        categories = self.categories.all()
        for category in categories:
            if not category.is_checked():
                return CheckState.UNCHECKED
        return CheckState.CHECKED

    @property
    def readable_name(self):
        return "{} {}".format(
            self.visum.year.year,
            ",".join(
                camp_type.camp_type for camp_type in self.visum.camp_types.all()),
        )
