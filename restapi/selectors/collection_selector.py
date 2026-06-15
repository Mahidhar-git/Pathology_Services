from restapi.models.collection import Collection, CollectionTest


def get_collections(
    *,
    work_order_id=None,
    patient_id=None,
    test_type=None,
    status=None,
    agency_id=None,
    date_from=None,
    date_to=None,
):
    queryset = Collection.objects.prefetch_related(
        "collection_tests__test",
        "collection_tests__sample",
        "collection_tests__agency",
    )

    if date_from:
        queryset = queryset.filter(collection_date__gte=date_from)

    if date_to:
        queryset = queryset.filter(collection_date__lte=date_to)

    if status:
        queryset = queryset.filter(status=status)

    if work_order_id:
        queryset = queryset.filter(
            collection_tests__work_order_id=work_order_id
        ).distinct()

    if patient_id:
        queryset = queryset.filter(
            collection_tests__patient_id=patient_id
        ).distinct()

    return queryset


def get_collection_by_id(collection_id) -> Collection:
    return Collection.objects.prefetch_related(
        "collection_tests__test",
        "collection_tests__sample",
        "collection_tests__agency",
    ).get(id=collection_id)