import uuid

import requests
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from restapi.models.collection import Collection, CollectionTest

from restapi.constants.order_status import (
    TestStatus,
    TestType,
)
from restapi.models.agency import Agency
from restapi.models.collection import Collection
from restapi.workflows.order_workflow import (
    transition_test_status,
)


def get_vidai_access_token() -> str:
    response = requests.post(
        settings.EXTERNAL_LOGIN_URL,
        json={
            "username": settings.EXTERNAL_USERNAME,
            "password": settings.EXTERNAL_PASSWORD,
            "force_login": True,
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()["access"]


def fetch_vidai_orders(
    limit=10,
    offset=0,
) -> dict:
    token = get_vidai_access_token()

    response = requests.get(
        settings.ORDERS_URL,
        params={
            "limit": limit,
            "offset": offset,
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def fetch_vidai_order_detail(order_id: int) -> dict:
    token = get_vidai_access_token()

    url = f"{settings.ORDERS_URL}{order_id}/"

    response = requests.get(
        url,
        headers={
            "Authorization": f"Bearer {token}"
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()

def get_invoice_item(
    order_data: dict,
    invoice_item_id: int = None,
    test_service_id: int = None,
) -> dict:
    for item in order_data.get("invoice_items", []):
        if invoice_item_id and item.get("id") == invoice_item_id:
            return item
        if test_service_id and item.get("test_service_id") == test_service_id:
            return item

    raise ValueError(
        f"No invoice item found for "
        f"invoice_item_id={invoice_item_id} "
        f"or test_service_id={test_service_id}"
    )

def resolve_test_from_service_id(service_id: int):
    from restapi.models.test_test import Test
    try:
        return Test.objects.get(
            test_service_id=service_id
        )
    except Test.DoesNotExist:
        return None


def _build_identifier(prefix: str) -> str:
    date_part = timezone.now().strftime("%Y%m%d")
    random_part = uuid.uuid4().hex[:8].upper()
    return f"{prefix}{date_part}{random_part}"


def generate_collection_identifiers() -> dict:
    while True:
        barcode_value = _build_identifier("BC")
        specimen_no = _build_identifier("SP")

        exists = (
            Collection.objects.filter(
                barcode_value=barcode_value
            ).exists()
            or
            Collection.objects.filter(
                specimen_no=specimen_no
            ).exists()
        )

        if not exists:
            return {
                "barcode_value": barcode_value,
                "specimen_no": specimen_no,
            }


@transaction.atomic
def create_collection(
    collection_date,
    collection_time,
    tests: list,
) -> Collection:

    identifiers = generate_collection_identifiers()

    collection = Collection.objects.create(
        collection_date=collection_date,
        collection_time=collection_time,
        status=TestStatus.COLLECTED,
        barcode_value=identifiers["barcode_value"],
        specimen_no=identifiers["specimen_no"],
    )

    for test_data in tests:
        work_order_id = test_data.get("work_order_id")
        invoice_item_id = test_data.get("invoice_item_id")
        test_service_id = test_data.get("test_service_id")

        # Duplicate protection
        existing = CollectionTest.objects.filter(
            work_order_id=work_order_id,
            invoice_item_id=invoice_item_id,
        ).first()

        if existing:
            continue

        # Resolve test from config
        test = resolve_test_from_service_id(test_service_id)

        # Resolve sample from test
        sample = None
        if test:
            test_sample = test.test_samples.filter(
                is_deleted=False
            ).first()
            if test_sample:
                sample = test_sample.sample

        # Resolve agency if outsource
        agency = None
        agency_id = test_data.get("agency")
        if agency_id:
            from restapi.models.agency import Agency
            try:
                agency = Agency.objects.get(id=agency_id)
            except Agency.DoesNotExist:
                pass

        CollectionTest.objects.create(
            collection=collection,
            work_order_id=work_order_id,
            patient_id=test_data.get("patient_id"),
            invoice_item_id=invoice_item_id,
            test_service_id=test_service_id,
            test=test,
            sample=sample,
            agency=agency,
            test_type=test_data.get("test_type", TestType.INHOUSE),
            status=TestStatus.COLLECTED,
        )

    return collection


@transaction.atomic
def update_collection_status(
    collection_id,
    new_status: str,
) -> Collection:

    collection = (
        Collection.objects
        .select_for_update()
        .get(id=collection_id)
    )

    transition_test_status(
        collection.status,
        new_status,
    )

    collection.status = new_status

    collection.save(
        update_fields=[
            "status",
            "updated_at",
        ]
    )

    return collection


@transaction.atomic
def change_collection_agency(
    *,
    collection_id,
    new_agency_id,
    reason: str,
) -> Collection:

    collection = (
        Collection.objects
        .select_for_update()
        .get(id=collection_id)
    )

    if collection.test_type != TestType.OUTSOURCE:
        raise ValueError(
            "Agency can only be changed "
            "for outsourced collections."
        )

    if collection.status not in (
        TestStatus.COLLECTED,
        TestStatus.SHIPPED,
    ):
        raise ValueError(
            "Agency can only be changed "
            "before sample is received."
        )

    agency = Agency.objects.get(id=new_agency_id)

    collection.agency = agency
    collection.agency_change_reason = reason

    collection.save(
        update_fields=[
            "agency",
            "agency_change_reason",
            "updated_at",
        ]
    )

    return collection