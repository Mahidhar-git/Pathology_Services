from django.shortcuts import render, get_object_or_404
from requests import request 
from django.db.models import Q
from restapi.pagination import StandardPagination
from restapi.models.sample import Sample        
from rest_framework import viewsets, status
from rest_framework.response import Response
from restapi.serializers.sample import SampleSerializer
from restapi.services import sample_service
from rest_framework.viewsets import ViewSet
from restapi.models import Tube
from restapi.models.receive_model import ReceiveSample
from restapi.serializers.tube import TubeSerializer
from restapi.services import tube_service
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from restapi.serializers.agency import AgencySerializer
from restapi.services.agency_service import AgencyService
from rest_framework.viewsets import ModelViewSet
from restapi.serializers.machine import MachineSerializer
from restapi.services.machine_service import MachineService
from restapi.serializers.pathology_profile import (PathologyProfileSerializer)
from restapi.services.pathology_profile_service import (PathologyProfileService)
from restapi.models.test_category import Category
from restapi.serializers.test_category import CategorySerializer
from restapi.models.test_template import (Template)
from restapi.serializers.test_template import (TemplateSerializer)
from restapi.services.test_template_service import (TemplateService)
from rest_framework.views import APIView
from rest_framework.response import Response

from restapi.models import Collection
from django.utils.timezone import now
from restapi.models.receive_model import ReceiveSample
from restapi.models.result_entry_model import ResultEntry
from restapi.serializers.result_entry_serializer import ResultEntrySerializer

# ==================================
# Sample_(Master)_ViewSet
# ==================================

class SampleViewSet(viewsets.ViewSet):

    def list(self, request):

        search = request.GET.get("search")
        samples = sample_service.get_all_samples()
        if search:
            samples = samples.filter(
            Q(sample_code__icontains=search) |
            Q(sample_name__icontains=search)
         )
        paginator = StandardPagination()

        page = paginator.paginate_queryset(
        samples,
        request
     )

        serializer = SampleSerializer(
        page,
        many=True
     )

        return paginator.get_paginated_response(
        serializer.data
    )

    def create(self, request):
        serializer = SampleSerializer(data=request.data)
        if serializer.is_valid():
            sample = sample_service.create_sample(serializer.validated_data)
            return Response(SampleSerializer(sample).data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        sample = get_object_or_404(Sample, id=pk)
        serializer = SampleSerializer(sample)
        return Response(serializer.data)

    def update(self, request, pk=None):
        sample = sample_service.get_sample(pk)
        serializer = SampleSerializer(sample, data=request.data)
        if serializer.is_valid():
            updated = sample_service.update_sample(sample, serializer.validated_data)
            return Response(SampleSerializer(updated).data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        sample = sample_service.get_sample(pk)
        sample_service.delete_sample(sample)
        return Response(status=204)
    
# ==================================
# Tube_(Master)_ViewSet
# ==================================

class TubeViewSet(ViewSet):

    
    def list(self, request):
      search = request.GET.get("search")

      tubes = tube_service.get_all_tubes()

      if search:
        tubes = tubes.filter(
        Q(tube_code__icontains=search) |
        Q(tube_name__icontains=search)
        )  
      paginator = StandardPagination()

      page = paginator.paginate_queryset(
        tubes,
        request
     )

      serializer = TubeSerializer(
        page,
        many=True
     )

      return paginator.get_paginated_response(
        serializer.data
     )

    def retrieve(self, request, pk=None):
        tube = get_object_or_404(Tube, pk=pk)
        serializer = TubeSerializer(tube)
        return Response(serializer.data)

    def create(self, request):
        serializer = TubeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        tube = get_object_or_404(Tube, pk=pk)
        serializer = TubeSerializer(tube, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        tube = get_object_or_404(Tube, pk=pk)
        tube.delete()
        return Response(status=204)
    

#--------------------------------------------------------

from rest_framework import viewsets
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from restapi.models import (
    Parameter,
    ParameterReferenceRange
)

from restapi.serializers.test_parameter import (
    ParameterSerializer,
    ParameterReferenceRangeSerializer
)

from restapi.services import test_parameter_service

# ==================================
# Parameter_(Master)_ViewSet
# ==================================

from restapi.services import test_parameter_service

class ParameterViewSet(viewsets.ViewSet):

    def list(self, request):

        search = request.GET.get("search")

        parameters = (
        test_parameter_service.get_all_parameters()
     )

        if search:
            parameters = parameters.filter(
            Q(parameter_code__icontains=search) |
            Q(parameter_name__icontains=search) |
            Q(parameter_print_name__icontains=search) |
            Q(unit__icontains=search)
    )

        paginator = StandardPagination()

        page = paginator.paginate_queryset(
        parameters,
        request
     )

        serializer = ParameterSerializer(
        page,
        many=True
     )
     
        return paginator.get_paginated_response(
        serializer.data
     )

    def retrieve(self, request, pk=None):

        parameter = get_object_or_404(
            Parameter,
            pk=pk
        )

        serializer = ParameterSerializer(parameter)

        return Response(serializer.data)

    def create(self, request): 

        serializer = ParameterSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=201
            )

        return Response(
            serializer.errors,
            status=400
        )

    def update(self, request, pk=None):

        parameter = get_object_or_404(
            Parameter,
            pk=pk
        )

        serializer = ParameterSerializer(
            parameter,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=400
        )

    def destroy(self, request, pk=None):

        parameter = get_object_or_404(
            Parameter,
            pk=pk
        )

        parameter.delete()

        return Response(status=204)


# ==================================
# Template_Master_ViewSet
# ==================================

class TemplateViewSet(ViewSet):

    def list(self, request):

        queryset = TemplateService.get_all()

        search = request.GET.get("search")

        if search:
            queryset = queryset.filter(
            Q(template_name__icontains=search)
        )
            
        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")
        template_for = request.GET.get("template_for")
        gender = request.GET.get("gender")
        user_type = request.GET.get("user_type")
        template_format = request.GET.get("template_format")

        if from_date:
            queryset = queryset.filter(
            created_at__date__gte=from_date
        )

        if to_date:
            queryset = queryset.filter(
            created_at__date__lte=to_date
        )

        if template_for:
            queryset = queryset.filter(
            template_for=template_for
        )

        if gender:
            queryset = queryset.filter(
            gender=gender
        )

        if user_type:
            queryset = queryset.filter(
            user_type=user_type
        )

        if template_format:
            queryset = queryset.filter(
            template_format=template_format
        )

        paginator = StandardPagination()

        page = paginator.paginate_queryset(
        queryset,
        request
        )

        serializer = TemplateSerializer(
        page,
        many=True
        )

        return paginator.get_paginated_response(
        serializer.data
        )

    def retrieve(self, request, pk=None):

        instance = TemplateService.get_by_id(pk)

        if not instance:
            return Response(
                {"error": "Template not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TemplateSerializer(instance)

        return Response(serializer.data)

    def create(self, request):

        serializer = TemplateSerializer(data=request.data)

        if serializer.is_valid():

            instance = TemplateService.create(
                serializer.validated_data
            )

            response_serializer = TemplateSerializer(instance)

            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, pk=None):

        instance = TemplateService.get_by_id(pk)

        if not instance:
            return Response(
                {"error": "Template not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TemplateSerializer(
            instance,
            data=request.data
        )

        if serializer.is_valid():

            updated_instance = TemplateService.update(
                instance,
                serializer.validated_data
            )

            response_serializer = TemplateSerializer(updated_instance)

            return Response(response_serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, pk=None):

        instance = TemplateService.get_by_id(pk)

        if not instance:
            return Response(
                {"error": "Template not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        TemplateService.soft_delete(instance)

        return Response(
            {"message": "Template deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


# ==================================
# Test_ViewSet
# ==================================
    
from restapi.serializers.test_test import TestSerializer
from restapi.services.test_test_service import TestService

class TestViewSet(ViewSet):

    def list(self, request):

        search = request.GET.get("search")

        queryset = TestService.get_all_tests()

        if search:
            queryset = queryset.filter(
            Q(test_code__icontains=search) |
            Q(test_name__icontains=search) |
            Q(print_name__icontains=search)
        )

        paginator = StandardPagination()

        page = paginator.paginate_queryset(
        queryset,
        request
        )

        serializer = TestSerializer(
        page,
        many=True
        )

        return paginator.get_paginated_response(
        serializer.data
        )

    def retrieve(self, request, pk=None):

        instance = TestService.get_test_by_id(pk)

        if not instance:
            return Response(
                {"error": "Test not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TestSerializer(instance)

        return Response(serializer.data)

    def create(self, request):

        serializer = TestSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, pk=None):

        instance = TestService.get_test_by_id(pk)

        if not instance:
            return Response(
                {"error": "Test not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TestSerializer(
            instance,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk=None):

        instance = TestService.get_test_by_id(pk)

        if not instance:
            return Response(
                {"error": "Test not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        TestService.delete_test(instance)

        return Response(
            {"message": "Test deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
    
class CategoryViewSet(ModelViewSet):

    serializer_class = CategorySerializer
    pagination_class = StandardPagination

    def get_queryset(self):

        queryset = Category.objects.all().order_by('-id')

        search = self.request.GET.get("search")

        if search:

            queryset = queryset.filter(
                Q(category_code__icontains=search) |
                Q(category_name__icontains=search)
            )

        return queryset


# ==================================
# Profile_Master_ViewSet
# ==================================

class PathologyProfileViewSet(ViewSet):

    def list(self, request):

        search = request.GET.get("search")

        queryset = PathologyProfileService.get_all_profiles()

        if search:
            queryset = queryset.filter(
            Q(service_name__icontains=search)
        )

        paginator = StandardPagination()

        page = paginator.paginate_queryset(
        queryset,
        request
    )

        serializer = PathologyProfileSerializer(
        page,
        many=True
    )

        return paginator.get_paginated_response(
        serializer.data
    )

    def retrieve(self, request, pk=None):

        instance = PathologyProfileService.get_profile_by_id(pk)

        if not instance:
            return Response(
                {"error": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = PathologyProfileSerializer(instance)

        return Response(serializer.data)

    def create(self, request):

        serializer = PathologyProfileSerializer(
            data=request.data
        )

        if serializer.is_valid():

            instance = PathologyProfileService.create_profile(
                serializer.validated_data
            )

            response_serializer = PathologyProfileSerializer(
                instance
            )

            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, pk=None):

        instance = PathologyProfileService.get_profile_by_id(pk)

        if not instance:
            return Response(
                {"error": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = PathologyProfileSerializer(
            instance,
            data=request.data
        )

        if serializer.is_valid():

            updated_instance = (
                PathologyProfileService.update_profile(
                    instance,
                    serializer.validated_data
                )
            )

            response_serializer = (
                PathologyProfileSerializer(
                    updated_instance
                )
            )

            return Response(response_serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, pk=None):

        instance = PathologyProfileService.get_profile_by_id(pk)

        if not instance:
            return Response(
                {"error": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        PathologyProfileService.delete_profile(instance)

        return Response(
            {"message": "Profile deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
    
# ==================================
# Machine_(Master)_ViewSet
# ==================================    

class MachineViewSet(ViewSet):

    def list(self, request):

        queryset = MachineService.get_all_machines()

        search = request.GET.get("search")

        if search:

            queryset = queryset.filter(
            Q(machine_code__icontains=search) |
            Q(machine_name__icontains=search)
        )
        
        paginator = StandardPagination()

        page = paginator.paginate_queryset(
        queryset,
        request
    )

        serializer = MachineSerializer(
        page,
        many=True
    )

        return paginator.get_paginated_response(
        serializer.data
    )

    def retrieve(self, request, pk=None):

        instance = MachineService.get_machine_by_id(pk)

        if not instance:
            return Response(
                {"error": "Machine not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MachineSerializer(instance)

        return Response(serializer.data)

    def create(self, request):

        serializer = MachineSerializer(
            data=request.data
        )

        if serializer.is_valid():

            instance = MachineService.create_machine(
                serializer.validated_data
            )

            response_serializer = MachineSerializer(
                instance
            )

            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, pk=None):

        instance = MachineService.get_machine_by_id(pk)

        if not instance:
            return Response(
                {"error": "Machine not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MachineSerializer(
            instance,
            data=request.data
        )

        if serializer.is_valid():

            updated_instance = (
                MachineService.update_machine(
                    instance,
                    serializer.validated_data
                )
            )

            response_serializer = MachineSerializer(
                updated_instance
            )

            return Response(response_serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, pk=None):

        instance = MachineService.get_machine_by_id(pk)

        if not instance:
            return Response(
                {"error": "Machine not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        MachineService.delete_machine(instance)

        return Response(
            {"message": "Machine deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
    
# ==================================
# Machine_Parameter_ViewSet
# ==================================

from restapi.serializers.machine_parameter import (MachineParameterSerializer)
from restapi.services.machine_parameter_service import (MachineParameterService)

class MachineParameterViewSet(ViewSet):

    def list(self, request):

        queryset = (MachineParameterService.get_all_machine_parameters())
       
        search = request.GET.get("search")
        
        if search:
            queryset = queryset.filter(
            Q(machine_parameter_code__icontains=search) |
            Q(machine_parameter_name__icontains=search)
        )

        paginator = StandardPagination()

        page = paginator.paginate_queryset(queryset,request)

        serializer = MachineParameterSerializer(page,many=True)

        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):

        instance = (
            MachineParameterService
            .get_machine_parameter_by_id(pk)
        )

        if not instance:
            return Response(
                {"error": "Record not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MachineParameterSerializer(
            instance
        )

        return Response(serializer.data)

    def create(self, request):

        serializer = MachineParameterSerializer(
            data=request.data
        )

        if serializer.is_valid():

            instance = (
                MachineParameterService
                .create_machine_parameter(
                    serializer.validated_data
                )
            )

            response_serializer = (
                MachineParameterSerializer(
                    instance
                )
            )

            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, pk=None):

        instance = (
            MachineParameterService
            .get_machine_parameter_by_id(pk)
        )

        if not instance:
            return Response(
                {"error": "Record not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MachineParameterSerializer(
            instance,
            data=request.data
        )

        if serializer.is_valid():

            updated_instance = (
                MachineParameterService
                .update_machine_parameter(
                    instance,
                    serializer.validated_data
                )
            )

            response_serializer = (
                MachineParameterSerializer(
                    updated_instance
                )
            )

            return Response(
                response_serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, pk=None):

        instance = (
            MachineParameterService
            .get_machine_parameter_by_id(pk)
        )

        if not instance:
            return Response(
                {"error": "Record not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        MachineParameterService.delete_machine_parameter(
            instance
        )

        return Response(
            {"message": "Deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
    

# ==================================
# CLinic (Master)_ViewSet
# ==================================

from restapi.serializers.clinic import ClinicSerializer
from restapi.services.clinic_service import ClinicService

class ClinicViewSet(ViewSet):

    def list(self, request):

        queryset = ClinicService.get_all_clinics()

        paginator = StandardPagination()

        page = paginator.paginate_queryset(
        queryset,
        request
    )

        serializer = ClinicSerializer(
        page,
        many=True
    )

        return paginator.get_paginated_response(
        serializer.data
    )

    def retrieve(self, request, pk=None):

        instance = ClinicService.get_clinic_by_id(pk)

        if not instance:

            return Response(
                {"error": "Clinic not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ClinicSerializer(instance)

        return Response(serializer.data)

    def create(self, request):

        serializer = ClinicSerializer(
            data=request.data
        )

        if serializer.is_valid():

            instance = ClinicService.create_clinic(
                serializer.validated_data
            )

            response_serializer = ClinicSerializer(
                instance
            )

            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, pk=None):

        instance = ClinicService.get_clinic_by_id(pk)

        if not instance:

            return Response(
                {"error": "Clinic not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ClinicSerializer(
            instance,
            data=request.data
        )

        if serializer.is_valid():

            updated_instance = (
                ClinicService.update_clinic(
                    instance,
                    serializer.validated_data
                )
            )

            response_serializer = ClinicSerializer(
                updated_instance
            )

            return Response(
                response_serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, pk=None):

        instance = ClinicService.get_clinic_by_id(pk)

        if not instance:

            return Response(
                {"error": "Clinic not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        ClinicService.delete_clinic(instance)

        return Response(
            {"message": "Deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
    

# ==================================
# Agency (Master)_ViewSet
# ==================================
    
from restapi.serializers.agency_clinic import (AgencyClinicSerializer)
from restapi.services.agency_clinic_service import (AgencyClinicService)


class AgencyViewSet(ViewSet):

    def list(self, request):

        queryset = AgencyService.get_all_agencies()
        
        search = request.GET.get("search")

        if search:

            queryset = queryset.filter(
            Q(agency_code__icontains=search) |
            Q(agency_name__icontains=search)
        )
            
        paginator = StandardPagination()

        page = paginator.paginate_queryset(
        queryset,
        request
    )

        serializer = AgencySerializer(
        page,
        many=True
    )

        return paginator.get_paginated_response(
        serializer.data
    )

    def retrieve(self, request, pk=None):

        instance = AgencyService.get_agency_by_id(pk)

        if not instance:
            return Response(
                {"error": "Agency not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AgencySerializer(instance)

        return Response(serializer.data)

    def create(self, request):

        serializer = AgencySerializer(
            data=request.data
        )

        if serializer.is_valid():

            instance = serializer.save()

            response_serializer = AgencySerializer(
                instance
            )

            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, pk=None):

        instance = AgencyService.get_agency_by_id(pk)

        if not instance:
            return Response(
                {"error": "Agency not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AgencySerializer(
            instance,
            data=request.data
        )

        if serializer.is_valid():

            updated_instance = serializer.save()

            response_serializer = AgencySerializer(
                updated_instance
            )

            return Response(response_serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, pk=None):

        instance = AgencyService.get_agency_by_id(pk)

        if not instance:
            return Response(
                {"error": "Agency not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        AgencyService.delete_agency(instance)

        return Response(
            {"message": "Agency deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


class AgencyClinicViewSet(ViewSet):

    def list(self, request):

        queryset = (AgencyClinicService.get_all())

        search = request.GET.get("search")

        if search:
            queryset = queryset.filter(
            Q(clinic__clinic_name__icontains=search)
        )

        paginator = StandardPagination()

        page = paginator.paginate_queryset(
        queryset,
        request
    )

        serializer = AgencyClinicSerializer(
        page,
        many=True
    )

        return paginator.get_paginated_response(
        serializer.data
    )

    def retrieve(self, request, pk=None):

        instance = (
            AgencyClinicService.get_by_id(pk)
        )

        if not instance:

            return Response(
                {"error": "Not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = (
            AgencyClinicSerializer(instance)
        )

        return Response(serializer.data)

    def create(self, request):

        serializer = (
            AgencyClinicSerializer(
                data=request.data
            )
        )

        if serializer.is_valid():

            instance = (
                AgencyClinicService.create(
                    serializer.validated_data
                )
            )

            response_serializer = (
                AgencyClinicSerializer(instance)
            )

            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, pk=None):

        instance = (
            AgencyClinicService.get_by_id(pk)
        )

        if not instance:

            return Response(
                {"error": "Not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = (
            AgencyClinicSerializer(
                instance,
                data=request.data
            )
        )

        if serializer.is_valid():

            updated_instance = (
                AgencyClinicService.update(
                    instance,
                    serializer.validated_data
                )
            )

            response_serializer = (
                AgencyClinicSerializer(
                    updated_instance
                )
            )

            return Response(
                response_serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, pk=None):

        instance = (
            AgencyClinicService.get_by_id(pk)
        )

        if not instance:

            return Response(
                {"error": "Not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        AgencyClinicService.delete(instance)

        return Response(
            {"message": "Deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


# ==================================
# Agency_Service_ViewSet
# ==================================

from restapi.serializers.agency_service import (AgencyServiceSerializer)
from restapi.services.agency_service_service import (AgencyServiceService)

class AgencyServiceViewSet(ViewSet):

    def list(self, request):

        queryset = (AgencyServiceService.get_all_agency_services())

        search = request.GET.get("search")

        if search:

            queryset = queryset.filter(
            Q(service__service_name__icontains=search)
        )

        paginator = StandardPagination()

        page = paginator.paginate_queryset(
        queryset,
        request
    )

        serializer = AgencyServiceSerializer(
        page,
        many=True
    )

        return paginator.get_paginated_response(
        serializer.data
    )

    def retrieve(self, request, pk=None):

        instance = (
            AgencyServiceService
            .get_agency_service_by_id(pk)
        )

        if not instance:
            return Response(
                {"error": "Record not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AgencyServiceSerializer(
            instance
        )

        return Response(serializer.data)

    def create(self, request):

        serializer = AgencyServiceSerializer(
            data=request.data
        )

        if serializer.is_valid():

            instance = (
                AgencyServiceService
                .create_agency_service(
                    serializer.validated_data
                )
            )

            response_serializer = (
                AgencyServiceSerializer(
                    instance
                )
            )

            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, pk=None):

        instance = (
            AgencyServiceService
            .get_agency_service_by_id(pk)
        )

        if not instance:
            return Response(
                {"error": "Record not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AgencyServiceSerializer(
            instance,
            data=request.data
        )

        if serializer.is_valid():

            updated_instance = (
                AgencyServiceService
                .update_agency_service(
                    instance,
                    serializer.validated_data
                )
            )

            response_serializer = (
                AgencyServiceSerializer(
                    updated_instance
                )
            )

            return Response(
                response_serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, pk=None):

        instance = (
            AgencyServiceService
            .get_agency_service_by_id(pk)
        )

        if not instance:
            return Response(
                {"error": "Record not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        AgencyServiceService.delete_agency_service(
            instance
        )

        return Response(
            {"message": "Deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
    

# ==================================
# Test_Parameter_Link_ViewSet
# ==================================

from restapi.serializers.test_parameter_link import (
    TestParameterLinkSerializer
)

from restapi.services.test_parameter_link_service import (
    TestParameterLinkService
)

class TestParameterLinkViewSet(ViewSet):

    def list(self, request):

        queryset = (
        TestParameterLinkService.get_all()
    )

        paginator = StandardPagination()

        page = paginator.paginate_queryset(
        queryset,
        request
    )

        serializer = TestParameterLinkSerializer(
        page,
        many=True
    )

        return paginator.get_paginated_response(
        serializer.data
    )

    def retrieve(self, request, pk=None):

        instance = (
            TestParameterLinkService.get_by_id(pk)
        )

        if not instance:

            return Response(
                {"error": "Not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = (
            TestParameterLinkSerializer(instance)
        )

        return Response(serializer.data)

    def create(self, request):

        serializer = (
            TestParameterLinkSerializer(
                data=request.data
            )
        )

        if serializer.is_valid():

            instance = (
                TestParameterLinkService.create(
                    serializer.validated_data
                )
            )

            response_serializer = (
                TestParameterLinkSerializer(
                    instance
                )
            )

            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, pk=None):

        instance = (
            TestParameterLinkService.get_by_id(pk)
        )

        if not instance:

            return Response(
                {"error": "Not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = (
            TestParameterLinkSerializer(
                instance,
                data=request.data
            )
        )

        if serializer.is_valid():

            updated_instance = (
                TestParameterLinkService.update(
                    instance,
                    serializer.validated_data
                )
            )

            response_serializer = (
                TestParameterLinkSerializer(
                    updated_instance
                )
            )

            return Response(
                response_serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, pk=None):

        instance = (
            TestParameterLinkService.get_by_id(pk)
        )

        if not instance:

            return Response(
                {"error": "Not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        TestParameterLinkService.delete(
            instance
        )

        return Response(
            {"message": "Deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

# ==================================
# Test_Sample_Link_ViewSet
# ==================================    

from restapi.serializers.test_sample_link import (
    TestSampleLinkSerializer
)

from restapi.services.test_sample_link_service import (
    TestSampleLinkService
)

class TestSampleLinkViewSet(ViewSet):

    def list(self, request):

        queryset = (
        TestSampleLinkService.get_all()
    )

        paginator = StandardPagination()

        page = paginator.paginate_queryset(
        queryset,
        request
    )

        serializer = TestSampleLinkSerializer(
        page,
        many=True
    )

        return paginator.get_paginated_response(
        serializer.data
    )

    def retrieve(self, request, pk=None):

        instance = (
            TestSampleLinkService.get_by_id(pk)
        )

        if not instance:

            return Response(
                {"error": "Not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = (
            TestSampleLinkSerializer(instance)
        )

        return Response(serializer.data)

    def create(self, request):

        serializer = (
            TestSampleLinkSerializer(
                data=request.data
            )
        )

        if serializer.is_valid():

            instance = (
                TestSampleLinkService.create(
                    serializer.validated_data
                )
            )

            response_serializer = (
                TestSampleLinkSerializer(
                    instance
                )
            )

            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, pk=None):

        instance = (
            TestSampleLinkService.get_by_id(pk)
        )

        if not instance:

            return Response(
                {"error": "Not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = (
            TestSampleLinkSerializer(
                instance,
                data=request.data
            )
        )

        if serializer.is_valid():

            updated_instance = (
                TestSampleLinkService.update(
                    instance,
                    serializer.validated_data
                )
            )

            response_serializer = (
                TestSampleLinkSerializer(
                    updated_instance
                )
            )

            return Response(
                response_serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, pk=None):

        instance = (
            TestSampleLinkService.get_by_id(pk)
        )

        if not instance:

            return Response(
                {"error": "Not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        TestSampleLinkService.delete(
            instance
        )

        return Response(
            {"message": "Deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
# ==================================
# Test_Template_Link_ViewSet
# ================================== 

from restapi.serializers.test_template_link import (
    TestTemplateLinkSerializer
)

from restapi.services.test_template_link_service import (
    TestTemplateLinkService
)

class TestTemplateLinkViewSet(ViewSet):

    def list(self, request):

        queryset = (
        TestTemplateLinkService.get_all()
    )

        paginator = StandardPagination()

        page = paginator.paginate_queryset(
        queryset,
        request
    )

        serializer = TestTemplateLinkSerializer(
        page,
        many=True
    )

        return paginator.get_paginated_response(
        serializer.data
    )

    def retrieve(self, request, pk=None):

        instance = (
            TestTemplateLinkService.get_by_id(pk)
        )

        if not instance:

            return Response(
                {"error": "Not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = (
            TestTemplateLinkSerializer(instance)
        )

        return Response(serializer.data)

    def create(self, request):

        serializer = (
            TestTemplateLinkSerializer(
                data=request.data
            )
        )

        if serializer.is_valid():

            instance = (
                TestTemplateLinkService.create(
                    serializer.validated_data
                )
            )

            response_serializer = (
                TestTemplateLinkSerializer(
                    instance
                )
            )

            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, pk=None):

        instance = (
            TestTemplateLinkService.get_by_id(pk)
        )

        if not instance:

            return Response(
                {"error": "Not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = (
            TestTemplateLinkSerializer(
                instance,
                data=request.data
            )
        )

        if serializer.is_valid():

            updated_instance = (
                TestTemplateLinkService.update(
                    instance,
                    serializer.validated_data
                )
            )

            response_serializer = (
                TestTemplateLinkSerializer(
                    updated_instance
                )
            )

            return Response(
                response_serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, pk=None):

        instance = (
            TestTemplateLinkService.get_by_id(pk)
        )

        if not instance:

            return Response(
                {"error": "Not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        TestTemplateLinkService.delete(
            instance
        )

        return Response(
            {"message": "Deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from restapi.services.shipment_services import (
    create_patient,
    get_all_patients,
    create_pending_shipment,
    get_all_pending_shipments,
    create_schedule_shipping,
    get_all_schedule_shipping,
    move_to_shipped,
    get_all_shipped_shipments,
    move_to_received,
    get_all_received_shipments,
    get_all_activity_logs,
)

# =========================================
# PATIENT VIEW
# =========================================

class PatientView(APIView):

    def get(self, request):
        patients = get_all_patients()

        data = []
        for patient in patients:
            data.append({
                "id": patient.id,
                "patient_name": patient.patient_name,
                "age": patient.age,
                "sex": patient.sex,
                "mrn": patient.mrn,
                "cycle_id": patient.cycle_id
            })

        return Response(data)

    def post(self, request):

        patient = create_patient(request.data)

        return Response(
            {
                "message": "Patient created successfully",
                "id": patient.id
            },
            status=status.HTTP_201_CREATED
        )


# =========================================
# PENDING SHIPMENT VIEW
# =========================================
class PendingShipmentAPIView(APIView):

    def get(self, request):

        from restapi.models import ShipmentShipped as ShipmentShippedModel
        # Get IDs of pending shipments already moved to shipped
        shipped_pending_ids = set(
            ShipmentShippedModel.objects.values_list('pending_shipment_id', flat=True)
        )

        shipments = get_all_pending_shipments()

        response = []

        for item in shipments:
            # Skip items already shipped
            if item.id in shipped_pending_ids:
                continue
            patient = item.patient
            response.append({
                "status": item.status,
                "id": item.id,
                "order_date": str(item.order_date) if item.order_date else None,
                "sample_no": item.sample_no,
                "sample_type": item.sample_type,
                "test_code": item.test_code,
                "test_name": item.test_name,
                "service_name": item.service_name,
                "patient": {
                    "id": patient.id,
                    "name": patient.patient_name,
                    "age": patient.age,
                    "patient_code": patient.mrn,
                    "gender": patient.sex,
                } if patient else None,
                "created_at": str(item.created_at) if hasattr(item, 'created_at') else None,
            })

        return Response(response)

    def post(self, request):

        shipment = create_pending_shipment(request.data)

        return Response(
            {
                "message": "Pending shipment created successfully",
                "id": shipment.id
            },
            status=status.HTTP_201_CREATED
        )


# =========================================
# SCHEDULE SHIPPING VIEW
# =========================================

class ScheduleShippingView(APIView):

    def get(self, request):

        schedules = get_all_schedule_shipping()

        data = []

        for item in schedules:
            data.append({
                "id": item.id,
                "pending_id": item.pending.id,
                "sample_no": item.pending.sample_no,
                "patient": item.pending.patient.patient_name,
                "ship_date": item.ship_date,
                "ship_time": item.ship_time,
                "dispatched_by": item.dispatched_by,
                "ship_to": item.ship_to
            })

        return Response(data)

    def post(self, request):

        schedule = create_schedule_shipping(request.data)

        return Response(
            {
                "message": "Schedule shipping created successfully",
                "id": schedule.id,
            },
            status=status.HTTP_201_CREATED
        )


# =========================================
# MOVE TO SHIPPED VIEW
# =========================================

class MoveToShippedView(APIView):

    def post(self, request):

        pending_id = request.data.get("pending_id")
        ship_to = request.data.get("ship_to")
        ship_by = request.data.get("ship_by")

        shipped = move_to_shipped(
            pending_id,
            ship_to,
            ship_by
        )

        return Response(
            {
                "message": "Shipment moved to shipped",
                "shipment_no": shipped.shipment_no
            },
            status=status.HTTP_201_CREATED
        )


# =========================================
# SHIPPED SHIPMENT VIEW
# =========================================

class ShipmentShippedView(APIView):

    def get(self, request):

        shipments = get_all_shipped_shipments()

        data = []

        for item in shipments:
            pending = item.pending_shipment
            patient = pending.patient if pending else None
            data.append({
                "id": item.id,
                "shipment_no": item.shipment_no,
                "ship_date": str(item.ship_date) if item.ship_date else None,
                "ship_to": item.ship_to,
                "pending_shipment": {
                    "sample_no": pending.sample_no if pending else None,
                    "sample_type": pending.sample_type if pending else None,
                    "test_code": pending.test_code if pending else None,
                    "test_name": pending.test_name if pending else None,
                    "service_name": pending.service_name if pending else None,
                    "patient": {
                        "name": patient.patient_name,
                        "age": patient.age,
                        "patient_code": patient.mrn,
                        "gender": patient.sex,
                    } if patient else None,
                } if pending else None,
            })

        return Response(data)


# =========================================
# MOVE TO RECEIVED VIEW
# =========================================

class MoveToReceivedView(APIView):

    def post(self, request):

        shipped_id = request.data.get("shipped_id")
        status_value = request.data.get("status")
        result_value = request.data.get("result")

        received = move_to_received(
            shipped_id,
            status_value,
            result_value
        )

        return Response(
            {
                "message": "Shipment moved to received",
                "received_no": received.received_no
            },
            status=status.HTTP_201_CREATED
        )


# =========================================
# RECEIVED SHIPMENT VIEW
# =========================================

class ShipmentReceivedView(APIView):

    def get(self, request):

        received_shipments = get_all_received_shipments()

        data = []

        for item in received_shipments:
            data.append({
                "id": item.id,
                "received_no": item.received_no,
                "receive_date": item.receive_date,
               "shipment_no": item.shipped_shipment.shipment_no if item.shipped_shipment else None,
                "status": item.status,
                "result": item.result
            })

        return Response(data)


# =========================================
# ACTIVITY LOGS VIEW
# =========================================

class ActivityLogsView(APIView):

    def get(self, request):

        logs = get_all_activity_logs()

        data = []

        for log in logs:
            data.append({
                "id": log.id,
                "shipment_no": log.shipped_shipment.shipment_no if log.shipped_shipment else None,
                "ship_from": log.ship_from,
                "ship_to": log.ship_to,
                "ship_by": log.ship_by,
                "ship_date_time": log.ship_date_time
            })

        return Response(data)

    

# =========================================
# FormulaValidation VIEW
# =========================================

# =====================================================
# RECEIVE MODULE IMPORTS
# =====================================================

import logging
import traceback

from rest_framework.exceptions import ValidationError

from django.utils.timezone import now
from django.forms.models import model_to_dict

from restapi.models.receive_model import ReceiveSample
from restapi.serializers.receive_serializer import ReceiveSampleSerializer
from restapi.models.shipment import ShipmentShipped, ShipmentReceived


logger = logging.getLogger(__name__)


def get_receive_sample_or_404(sample_id):
    return get_object_or_404(ReceiveSample, id=sample_id)


# =====================================================
# CREATE SAMPLE API
# =====================================================

class ReceiveSampleCreateAPIView(APIView):

    def post(self, request):
        try:
            serializer = ReceiveSampleSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            sample = serializer.save(status="Shipped")

            return Response(
                {
                    "message": "Sample created successfully",
                    "data": ReceiveSampleSerializer(sample).data
                },
                status=status.HTTP_201_CREATED
            )

        except ValidationError as ve:
            return Response(
                {"error": ve.detail},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception:
            logger.error(traceback.format_exc())
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# =====================================================
# LIST + SEARCH API
# =====================================================

class ReceiveSampleListAPIView(APIView):

    def get(self, request):
        try:
            search = request.GET.get("search", "")
            status_value = request.GET.get("status")

            queryset = ReceiveSample.objects.filter(is_deleted=False)

            if status_value:
                queryset = queryset.filter(status=status_value)

            if search:
                queryset = queryset.filter(
                    Q(patient_name__icontains=search) |
                    Q(specimen_no__icontains=search) |
                    Q(shipment_no__icontains=search) |
                    Q(test_name__icontains=search)
                )

            serializer = ReceiveSampleSerializer(queryset, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception:
            logger.error(traceback.format_exc())
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# =====================================================
# RECEIVE SAMPLE API
# =====================================================

class ReceiveSampleAPIView(APIView):

    def post(self, request, sample_id):
        try:
            sample = get_receive_sample_or_404(sample_id)

            sample.receive_date = request.data.get("receive_date")
            sample.receive_time = request.data.get("receive_time")
            sample.accepted_by = request.data.get("accepted_by")
            sample.remark = request.data.get("remark")
            sample.sub_optimal = request.data.get("sub_optimal", False)
            sample.shipment_id = request.data.get("shipment")
            sample.status = "Received"

            sample.save()

            serializer = ReceiveSampleSerializer(sample)

            return Response(
                {
                    "message": "Sample received successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception:
            logger.error(traceback.format_exc())
            return Response(
                {"error": "Sample not found or Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# =====================================================
# REJECT SAMPLE API
# =====================================================

class RejectSampleAPIView(APIView):

    def post(self, request, sample_id):
        try:
            sample = get_receive_sample_or_404(sample_id)

            sample.receive_date = request.data.get("receive_date")
            sample.receive_time = request.data.get("receive_time")
            sample.accepted_by = None
            sample.rejected_by = request.data.get("rejected_by")
            sample.remark = request.data.get("remark")
            sample.resend_new_sample = request.data.get("resend_new_sample", False)
            sample.sub_optimal = False
            sample.status = "Rejected"

            sample.save()

            serializer = ReceiveSampleSerializer(sample)

            return Response(
                {
                    "message": "Sample rejected successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception:
            logger.error(traceback.format_exc())
            return Response(
                {"error": "Sample not found or Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# =====================================================
# ACTIVITY LOGS API
# =====================================================

class ReceiveActivityLogsAPIView(APIView):

    def get(self, request):
        try:
            queryset = ReceiveSample.objects.filter(
                status__in=["Received", "Rejected"]
            ).order_by("-id")

            serializer = ReceiveSampleSerializer(queryset, many=True)

            return Response(
                {
                    "message": "Activity logs fetched successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception:
            logger.error(traceback.format_exc())
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# =====================================================
# SOFT DELETE SAMPLE API
# =====================================================

class DeleteSampleAPIView(APIView):

    def delete(self, request, sample_id):
        try:
            sample = get_receive_sample_or_404(sample_id)

            sample.is_deleted = True
            sample.deleted_at = now()
            sample.save()

            return Response(
                {"message": "Sample deleted successfully"},
                status=status.HTTP_200_OK
            )

        except Exception:
            logger.error(traceback.format_exc())
            return Response(
                {"error": "Sample not found or Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# =====================================================
# ACTIVE SAMPLES API
# =====================================================

class ActiveSamplesAPIView(APIView):

    def get(self, request):
        try:
            queryset = ReceiveSample.objects.filter(
                is_deleted=False
            ).order_by("-id")

            serializer = ReceiveSampleSerializer(queryset, many=True)

            return Response(
                {
                    "message": "Active samples fetched successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception:
            logger.error(traceback.format_exc())
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# =====================================================
# DELETED SAMPLES API
# =====================================================

class DeletedSamplesAPIView(APIView):

    def get(self, request):
        try:
            queryset = ReceiveSample.objects.filter(
                is_deleted=True
            ).order_by("-id")

            serializer = ReceiveSampleSerializer(queryset, many=True)

            return Response(
                {
                    "message": "Deleted samples fetched successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception:
            logger.error(traceback.format_exc())
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# =====================================================
# CREATE SHIPMENT RECEIVED API
# =====================================================

class ShipmentReceivedCreateAPIView(APIView):

    def post(self, request):
        try:
            shipment = ShipmentReceived.objects.create(
                receive_date=request.data.get("receive_date"),
                received_no=request.data.get("received_no"),
                status=request.data.get("status"),
                result=request.data.get("result")
            )

            return Response(
                {
                    "message": "Shipment received created successfully",
                    "data": model_to_dict(shipment)
                },
                status=status.HTTP_201_CREATED
            )

        except Exception:
            logger.error(traceback.format_exc())
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
# =====================================================
# SHIPPED TAB API
# =====================================================

class ReceiveShippedTabAPIView(APIView):

    def get(self, request):
        try:
            queryset = ShipmentShipped.objects.filter(
                pending_shipment__status="Completed",
                received_records__isnull=True
            ).order_by("-id")

            data = []

            for item in queryset:
                pending = item.pending_shipment

                data.append({
                    "id": item.id,
                    "shipment_no": item.shipment_no,
                    "ship_date": item.ship_date,
                    "ship_to": item.ship_to,
                    "sample_no": pending.sample_no if pending else None,
                    "sample_type": pending.sample_type if pending else None,
                    "test_code": pending.test_code if pending else None,
                    "test_name": pending.test_name if pending else None,
                    "service_name": pending.service_name if pending else None,
                    "status": "Completed"
                })

            return Response({
                "message": "Shipped samples fetched successfully",
                "data": data
            }, status=status.HTTP_200_OK)

        except Exception:
            logger.error(traceback.format_exc())
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# =====================================================
# CONVERT SHIPPED TO RECEIVED API
# =====================================================

class ConvertShippedToReceivedAPIView(APIView):

    def post(self, request, shipment_id):
        try:
            shipment = get_object_or_404(
                ShipmentShipped,
                id=shipment_id
            )

            if shipment.received_records.exists():
                shipment_received = shipment.received_records.first()
                receive_sample = shipment_received.receive_samples.filter(is_deleted=False).first()
                if receive_sample:
                    serializer = ReceiveSampleSerializer(receive_sample)
                    return Response({
                        "message": "Shipment already converted to received",
                        "data": serializer.data
                    }, status=status.HTTP_200_OK)

            pending = shipment.pending_shipment
            patient = pending.patient if pending and pending.patient else None

            shipment_received = ShipmentReceived.objects.create(
                shipped_shipment=shipment,
                receive_date=now(),
                received_no=f"REC-{shipment.id}",
                status="Accepted",
                result="Done"
            )

            receive_sample = ReceiveSample.objects.create(
    shipment=shipment_received,
    ship_date=shipment.ship_date.date() if shipment.ship_date else None,
    ship_time=shipment.ship_date.time() if shipment.ship_date else None,
    shipment_no=shipment.shipment_no,
    specimen_no=pending.sample_no if pending else "",
    specimen_type=pending.sample_type if pending else "",
    test_code=pending.test_code if pending else "",
    test_name=pending.test_name if pending else "",
    service_name=pending.service_name if pending else "",
    patient_name=patient.patient_name if patient else "",
    patient_age=patient.age if patient else 0,
    patient_gender=patient.sex if patient else "",
    patient_code=patient.mrn if patient else "",
    receive_date=now().date(),
    receive_time=now().time(),
    status="Shipped"
)

            serializer = ReceiveSampleSerializer(receive_sample)
            return Response({
                "message": "Sample moved to received successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception:
            logger.error(traceback.format_exc())
            return Response(
                {"error": "Shipment not found or Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
# RESULT API IN RECEIVE MODULE
class ReceiveToResultEntryAPIView(APIView):

    def get(self, request):
        try:
            queryset = ReceiveSample.objects.filter(
                status="Shipped",
                is_deleted=False
            ).order_by("-id")[:4]

            data = []

            for item in queryset:
                data.append({
                    "id": item.id,
                    "shipment_no": item.shipment_no,
                    "specimen_no": item.specimen_no,
                    "specimen_type": item.specimen_type,
                    "test_code": item.test_code,
                    "test_name": item.test_name,
                    "service_name": item.service_name,
                    "patient_name": item.patient_name,
                    "patient_age": item.patient_age,
                    "patient_gender": item.patient_gender,
                    "patient_code": item.patient_code,
                    "status": item.status,
                })

            return Response({
                "message": "Received samples fetched for Result Entry successfully",
                "data": data
            }, status=status.HTTP_200_OK)

        except Exception:
            logger.error(traceback.format_exc())
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
# Added Receive section views

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from restapi.services.pathology_order_service import PathologyOrderService

class PathologyOrdersAPIView(APIView):

    def get(self, request):

        try:

            data = PathologyOrderService.get_orders()

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:

            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

from rest_framework.views import APIView
from rest_framework.response import Response

from restapi.services.laboratory_test_service import (
    LaboratoryTestService
)


class LaboratoryTestAPIView(APIView):

    def get(self, request):

        data = LaboratoryTestService.get_laboratory_tests(
            request.query_params
        )

        return Response(data)



#Result Entry 
class ResultEntryPendingSamplesAPIView(APIView):
    def get(self, request):
        samples = ReceiveSample.objects.filter(status="Received", is_deleted=False)
        data = []

        for item in samples:
            data.append({
                "id": item.id,
                "shipment_no": item.shipment_no,
                "specimen_no": item.specimen_no,
                "patient_name": item.patient_name,
                "test_name": item.test_name,
                "status": item.status
            })

        return Response(data)


class ResultEntryCreateAPIView(APIView):
    def post(self, request):
        serializer = ResultEntrySerializer(data=request.data)

        if serializer.is_valid():
            result = serializer.save()
            return Response({
                "message": "Result entry created successfully",
                "data": ResultEntrySerializer(result).data
            }, status=201)

        return Response(serializer.errors, status=400)


class ResultEntryListAPIView(APIView):
    def get(self, request):

        receive_samples = ReceiveSample.objects.filter(
            status="Shipped",
            is_deleted=False
        ).order_by("-id")[:4]

        for sample in receive_samples:
            ResultEntry.objects.get_or_create(
                receive_sample=sample,
                defaults={
                    "parameter_name": sample.test_name,
                    "result_value": "",
                    "remarks": "",
                    "entered_by": "",
                    "result_status": "Pending"
                }
            )

        results = ResultEntry.objects.filter(
            is_deleted=False
        ).order_by("-id")

        serializer = ResultEntrySerializer(results, many=True)
        return Response(serializer.data)


class ResultEntryUpdateAPIView(APIView):
    def _update(self, request, result_id):
        try:
            result = ResultEntry.objects.get(id=result_id, is_deleted=False)
        except ResultEntry.DoesNotExist:
            return Response({"message": "Result entry not found"}, status=404)

        serializer = ResultEntrySerializer(result, data=request.data, partial=True)
        if serializer.is_valid():
            updated = serializer.save()
            return Response({
                "message": "Result entry updated successfully",
                "data": ResultEntrySerializer(updated).data,
            }, status=200)

        return Response(serializer.errors, status=400)

    def patch(self, request, result_id):
        return self._update(request, result_id)

    def put(self, request, result_id):
        return self._update(request, result_id)

    # Backward compatible route if frontend posts to /update/.
    def post(self, request, result_id):
        return self._update(request, result_id)


class ResultEntryCompleteAPIView(APIView):
    def post(self, request, result_id):
        result = ResultEntry.objects.get(id=result_id, is_deleted=False)
        result.result_status = "Completed"
        result.save()

        return Response({
            "message": "Result completed successfully",
            "data": ResultEntrySerializer(result).data
        })
    
class ResultEntryUpdateAPIView(APIView):
    def put(self, request, result_id):
        try:
            result = ResultEntry.objects.get(id=result_id, is_deleted=False)
        except ResultEntry.DoesNotExist:
            return Response({"error": "Result entry not found"}, status=404)

        serializer = ResultEntrySerializer(result, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Result entry updated successfully",
                "data": serializer.data
            }, status=200)

        return Response(serializer.errors, status=400)
    
class AuthorizationPendingResultsAPIView(APIView):

    def get(self, request):

        results = ResultEntry.objects.filter(
            result_status="Completed",
            is_deleted=False
        ).order_by("-id")

        serializer = ResultEntrySerializer(results, many=True)

        return Response({
            "message": "Completed results fetched successfully",
            "data": serializer.data
        }, status=200)
#above are the resukt entry apis  
    
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from restapi.models.collection import Collection

from restapi.selectors.collection_selector import (
    get_collection_by_id,
    get_collections,
)

from restapi.serializers.collection_serializer import (
    ChangeCollectionAgencySerializer,
    CollectionSerializer,
    CreateCollectionSerializer,
    GenerateCollectionBarcodeSerializer,
    UpdateCollectionStatusSerializer,
)

from restapi.services.collection_service import (
    change_collection_agency,
    create_collection,
    generate_collection_identifiers,
    update_collection_status,
)

from restapi.workflows.order_workflow import (
    InvalidStatusTransitionError,
)

import requests
from django.conf import settings

class VidaiOrdersView(APIView):

    def get(self, request):
        try:
            from restapi.services.collection_service import fetch_vidai_orders
            data = fetch_vidai_orders(
                limit=request.query_params.get("limit", 10),
                offset=request.query_params.get("offset", 0),
            )
        except Exception as error:
            return Response(
                {"detail": f"Failed to fetch orders from Vidai. {str(error)}"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response(
            data,
            status=status.HTTP_200_OK,
        )


class VidaiOrderDetailView(APIView):

    def get(self, request, order_id):
        try:
            from restapi.services.collection_service import fetch_vidai_order_detail
            data = fetch_vidai_order_detail(order_id=order_id)
        except Exception as error:
            return Response(
                {"detail": f"Failed to fetch order from Vidai. {str(error)}"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        # Enrich each invoice_item with pathology collection data
        for item in data.get("invoice_items", []):
            service_id = item.get("test_service_id")

            # Get collection record if exists
            collection = Collection.objects.filter(
                work_order_id=order_id,
                test_service_id=service_id,
            ).first()

            if collection:
                item["specimen_no"] = collection.specimen_no
                item["barcode_value"] = collection.barcode_value
                item["collection_status"] = collection.status
                item["collection_date"] = collection.collection_date
                item["collection_time"] = str(collection.collection_time) if collection.collection_time else None
                item["test_type"] = collection.test_type
                item["agency_name"] = collection.agency.agency_name if collection.agency else None
            else:
                item["specimen_no"] = None
                item["barcode_value"] = None
                item["collection_status"] = "PENDING"
                item["collection_date"] = None
                item["collection_time"] = None
                item["test_type"] = None
                item["agency_name"] = None

            # Enrich with config data from Test model
            from restapi.services.collection_service import resolve_test_from_service_id
            test = resolve_test_from_service_id(service_id) if service_id else None

            if test:
                item["test_code"] = test.test_code
                item["service_name"] = test.service_name
                

                item["tube_type"] = test.tube_name.tube_name if test.tube_name else None
                item["sample_type"] = (
                    test.test_samples.filter(is_deleted=False)
                    .first()
                    .sample.sample_name
            if test.test_samples.filter(is_deleted=False).exists()
            else None
    )
            else:
                item["test_code"] = None
                item["service_name"] = None
                item["tube_type"] = None
                item["sample_type"] = None

        return Response(data, status=status.HTTP_200_OK)
    
class CollectionListCreateView(APIView):
    def get(self, request):
        collections = get_collections(
            work_order_id=request.query_params.get("work_order_id"),
            patient_id=request.query_params.get("patient_id"),
            test_type=request.query_params.get("test_type"),
            status=request.query_params.get("status"),
            agency_id=request.query_params.get("agency_id"),
            date_from=request.query_params.get("date_from"),
            date_to=request.query_params.get("date_to"),
        )
        serializer = CollectionSerializer(collections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CreateCollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        collection = create_collection(
            collection_date=serializer.validated_data["collection_date"],
            collection_time=serializer.validated_data["collection_time"],
            tests=serializer.validated_data["tests"],
    )

        return Response(
            CollectionSerializer(collection).data,
            status=status.HTTP_201_CREATED,
    )


class CollectionDetailView(APIView):
    def get(self, request, collection_id):
        try:
            collection = get_collection_by_id(collection_id)
        except Collection.DoesNotExist:
            return Response(
                {"detail": "Collection not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            CollectionSerializer(collection).data,
            status=status.HTTP_200_OK,
        )


class GenerateCollectionBarcodeView(APIView):
    def post(self, request):
        serializer = GenerateCollectionBarcodeSerializer(
            generate_collection_identifiers()
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateCollectionStatusView(APIView):
    def patch(self, request, collection_id):
        serializer = UpdateCollectionStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            collection = update_collection_status(
                collection_id=collection_id,
                new_status=serializer.validated_data["new_status"],
            )
        except Collection.DoesNotExist:
            return Response(
                {"detail": "Collection not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except InvalidStatusTransitionError as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            CollectionSerializer(collection).data,
            status=status.HTTP_200_OK,
        )


class ChangeCollectionAgencyView(APIView):
    def patch(self, request, collection_id):
        serializer = ChangeCollectionAgencySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            collection = change_collection_agency(
                collection_id=collection_id,
                new_agency_id=serializer.validated_data["new_agency_id"],
                reason=serializer.validated_data["reason"],
            )
        except Collection.DoesNotExist:
            return Response(
                {"detail": "Collection not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except ObjectDoesNotExist:
            return Response(
                {"detail": "Agency not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except ValueError as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            CollectionSerializer(collection).data,
            status=status.HTTP_200_OK,
        )

# ==================================
# Parameter Reference Range Views
# ==================================

class ReferenceRangeListCreateView(APIView):

    def post(self, request, parameter_id):
        parameter = get_object_or_404(Parameter, pk=parameter_id)
        serializer = ParameterReferenceRangeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(parameter=parameter)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReferenceRangeDetailView(APIView):

    def put(self, request, parameter_id, pk):
        instance = get_object_or_404(
            ParameterReferenceRange, pk=pk, parameter=parameter_id
        )
        serializer = ParameterReferenceRangeSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, parameter_id, pk):
        instance = get_object_or_404(
            ParameterReferenceRange, pk=pk, parameter=parameter_id
        )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#Authorization views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.utils import timezone
from datetime import date, datetime

from restapi.models.authorization_models import Authorization
from restapi.serializers.authorization_serializers import AuthorizationSerializer


@api_view(['DELETE'])
def delete_result_api(request, result_id):
    try:
        result = ResultEntry.objects.get(id=result_id)

        result.is_deleted = True
        result.deleted_at = timezone.now()
        result.save()

        return Response({
            "message": "Result Deleted Successfully"
        })

    except ResultEntry.DoesNotExist:
        return Response(
            {"message": "Result not found"},
            status=status.HTTP_404_NOT_FOUND
        )


class AuthorizationListAPIView(APIView):

    def get(self, request):

        search = request.GET.get("search")
        status_filter = request.GET.get("status")

        data = Authorization.objects.filter(
            is_deleted=False
        )

        if status_filter:
            data = data.filter(
                authorization_status=status_filter
            )

        if search:
            data = data.filter(
                patient_name__icontains=search
            )

        serializer = AuthorizationSerializer(
            data,
            many=True
        )

        return Response(serializer.data)


class AuthorizationCreateAPIView(APIView):

    def post(self, request):

        result_entry_id = request.data.get("result_entry")

        try:
            result_entry = ResultEntry.objects.get(
                id=result_entry_id
            )

        except ResultEntry.DoesNotExist:
            return Response(
                {"message": "Result Entry Not Found"},
                status=404
            )

        authorization = Authorization.objects.create(

            result_entry=result_entry,

            order_date=date.today(),
            order_time=datetime.now().time(),

            patient_name=result_entry.receive_sample.patient_name,
            patient_age=result_entry.receive_sample.patient_age,
            patient_gender=result_entry.receive_sample.patient_gender,
            patient_code=result_entry.receive_sample.patient_code,

            patient_type="OP",
            doctor_name="Doctor",
            bill_no=f"BILL-{result_entry.id}",

            no_of_orders=1,

            test_name=result_entry.parameter_name,

            result_status=result_entry.result_status,

            authorization_status="Pending"
        )

        serializer = AuthorizationSerializer(
            authorization
        )

        return Response(
            serializer.data,
            status=201
        )


class ApproveResultAPIView(APIView):

    def post(self, request, pk):

        try:

            obj = Authorization.objects.get(id=pk)

            obj.authorization_status = "APPROVED"
            obj.authorized_date = timezone.now()

            obj.save()

            return Response({
                "message": "Authorization Approved"
            })

        except Authorization.DoesNotExist:

            return Response(
                {
                    "message": "Authorization Not Found"
                },
                status=404
            )


class RejectAuthorizationAPIView(APIView):

    def post(self, request, pk):

        try:

            obj = Authorization.objects.get(id=pk)

            obj.authorization_status = "REJECTED"
            obj.remark = request.data.get("remark")
            obj.authorized_date = timezone.now()

            obj.save()

            return Response({
                "message": "Authorization Rejected Successfully"
            })

        except Authorization.DoesNotExist:

            return Response(
                {
                    "message": "Authorization Not Found"
                },
                status=404
            )


class DeleteAuthorizationAPIView(APIView):

    def delete(self, request, pk):

        try:

            obj = Authorization.objects.get(
                id=pk,
                is_deleted=False
            )

            obj.is_deleted = True
            obj.deleted_at = timezone.now()

            obj.save()

            return Response({
                "message": "Authorization Deleted Successfully"
            })

        except Authorization.DoesNotExist:

            return Response(
                {
                    "message": "Authorization Not Found"
                },
                status=404
            )


class AuthorizationLogsAPIView(APIView):

    def get(self, request):

        data = Authorization.objects.filter(
            authorization_status__in=["APPROVED", "REJECTED"],
            is_deleted=False
        )

        serializer = AuthorizationSerializer(
            data,
            many=True
        )

        return Response(serializer.data)


class DeletedAuthorizationAPIView(APIView):

    def get(self, request):

        data = Authorization.objects.filter(
            is_deleted=True
        )

        serializer = AuthorizationSerializer(
            data,
            many=True
        )

        return Response(serializer.data)
