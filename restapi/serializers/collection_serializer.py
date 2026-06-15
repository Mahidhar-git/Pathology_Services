from rest_framework import serializers
from restapi.constants.order_status import TestStatus, TestType
from restapi.models.collection import Collection, CollectionTest


class CollectionTestSerializer(serializers.ModelSerializer):

    test_code = serializers.CharField(source="test.test_code", read_only=True)
    test_name = serializers.CharField(source="test.test_name", read_only=True)
    service_name = serializers.CharField(source="test.service_name", read_only=True)
    tube_type = serializers.CharField(source="test.tube_name.tube_name", read_only=True)
    sample_name = serializers.CharField(source="sample.sample_name", read_only=True)
    agency_name = serializers.CharField(source="agency.agency_name", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    test_type_display = serializers.CharField(source="get_test_type_display", read_only=True)

    class Meta:
        model = CollectionTest
        fields = [
            "id",
            "collection",
            "work_order_id",
            "patient_id",
            "invoice_item_id",
            "test_service_id",
            "test",
            "test_code",
            "test_name",
            "service_name",
            "tube_type",
            "sample",
            "sample_name",
            "agency",
            "agency_name",
            "agency_change_reason",
            "test_type",
            "test_type_display",
            "status",
            "status_display",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "agency_change_reason",
            "created_at",
            "updated_at",
        ]


class CollectionSerializer(serializers.ModelSerializer):

    collection_tests = CollectionTestSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Collection
        fields = [
            "id",
            "barcode_value",
            "specimen_no",
            "collection_date",
            "collection_time",
            "status",
            "status_display",
            "collection_tests",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "barcode_value",
            "specimen_no",
            "status",
            "created_at",
            "updated_at",
        ]


class CreateCollectionTestSerializer(serializers.Serializer):
    work_order_id = serializers.IntegerField()
    patient_id = serializers.IntegerField()
    invoice_item_id = serializers.IntegerField()
    test_service_id = serializers.IntegerField()
    test_type = serializers.ChoiceField(choices=TestType.choices)
    agency = serializers.UUIDField(required=False, allow_null=True)

    def validate(self, attrs):
        if attrs.get("test_type") == TestType.OUTSOURCE and not attrs.get("agency"):
            raise serializers.ValidationError(
                {"agency": "Agency is required for outsourced tests."}
            )
        return attrs


class CreateCollectionSerializer(serializers.Serializer):
    collection_date = serializers.DateField()
    collection_time = serializers.TimeField()
    tests = CreateCollectionTestSerializer(many=True)

    def validate_tests(self, tests):
        if not tests:
            raise serializers.ValidationError(
                "At least one test is required."
            )
        return tests


class GenerateCollectionBarcodeSerializer(serializers.Serializer):
    barcode_value = serializers.CharField(read_only=True)
    specimen_no = serializers.CharField(read_only=True)


class UpdateCollectionStatusSerializer(serializers.Serializer):
    new_status = serializers.ChoiceField(choices=TestStatus.choices)


class ChangeCollectionAgencySerializer(serializers.Serializer):
    new_agency_id = serializers.UUIDField()
    reason = serializers.CharField(max_length=500)

    def validate_reason(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Reason cannot be blank.")
        return value