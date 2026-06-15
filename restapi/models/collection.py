import uuid
from django.db import models
from restapi.constants.order_status import TestStatus


class Collection(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    barcode_value = models.CharField(
        max_length=100,
        unique=True,
    )
    specimen_no = models.CharField(
        max_length=100,
        unique=True,
    )

    collection_date = models.DateField()
    collection_time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=TestStatus.choices,
        default=TestStatus.COLLECTED,
        db_index=True,
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "collections"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Collection {self.specimen_no} | {self.status}"


class CollectionTest(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    collection = models.ForeignKey(
        Collection,
        on_delete=models.PROTECT,
        related_name="collection_tests",
    )

    # Vidai references — store IDs only, fetch details when needed
    work_order_id = models.BigIntegerField(db_index=True)
    patient_id = models.BigIntegerField(db_index=True)
    invoice_item_id = models.BigIntegerField(
        null=True,
        blank=True,
        db_index=True,
    )
    test_service_id = models.BigIntegerField(
        null=True,
        blank=True,
        db_index=True,
    )

    # Config FKs
    test = models.ForeignKey(
        "restapi.Test",
        on_delete=models.PROTECT,
        related_name="collection_tests",
        null=True,
        blank=True,
    )
    sample = models.ForeignKey(
        "restapi.Sample",
        on_delete=models.PROTECT,
        related_name="collection_tests",
        null=True,
        blank=True,
    )
    agency = models.ForeignKey(
        "restapi.Agency",
        on_delete=models.PROTECT,
        related_name="collection_tests",
        null=True,
        blank=True,
    )
    agency_change_reason = models.TextField(
        null=True,
        blank=True,
    )

    from restapi.constants.order_status import TestType
    test_type = models.CharField(
        max_length=20,
        choices=TestType.choices,
        default=TestType.INHOUSE,
        db_index=True,
    )

    status = models.CharField(
        max_length=20,
        choices=TestStatus.choices,
        default=TestStatus.COLLECTED,
        db_index=True,
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "collection_tests"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["work_order_id", "invoice_item_id"],
                name="unique_collection_test_per_order_item",
            )
        ]

    def __str__(self):
        return f"CollectionTest {self.id} | {self.status}"