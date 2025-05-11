from datetime import (
    datetime,
    timedelta
)

from django.db.models import (
    Q,
    Count
)
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers.agreement import (
    StatsAgreementSerializer
)
from agreements.repositories.agreement import (
    AgreementRepository
)
from ..serializers.common import (
    DashboardReportSerializer
)

class StatsAgreementView(APIView):

    serializer_class = StatsAgreementSerializer

    def get(self, request):
        now = datetime.now()
        in_30_days = now + timedelta(days = 30)

        repository = AgreementRepository()

        data = {
            'total': Count('id'),
            'active': Count('id', filter = Q(status = 'ACTIVO')),
            'inactive': Count('id', filter = Q(status = 'INACTIVO')),
            'expiring_soon': Count('id', filter = Q(end_date__range = (now, in_30_days)))
        }

        stats = repository.aggregate(**data)

        response_data = StatsAgreementSerializer(data = stats)
        response_data.is_valid(raise_exception = True)
        
        return Response(response_data.data)
    
class AgreementStatusView(APIView):

    serializer_class = DashboardReportSerializer

    def get(self, request):
        repository = AgreementRepository()
        status = repository.count_by_status()

        labels = [item['status'].capitalize() for item in status]
        series = [item['total'] for item in status]

        response_data = DashboardReportSerializer(
            data = {
                'labels': labels,
                'series': series
            }
        )
        response_data.is_valid(raise_exception = True)

        return Response(response_data.data)
    
class ExpirationAgreementView(APIView):

    serializer_class = DashboardReportSerializer

    def get(self, request):
        
        repository = AgreementRepository()
        data = repository.get_soon_to_expire()
    
        labels = [str(item['end_date']) for item in data]
        series = [item['total'] for item in data]

        response_data = DashboardReportSerializer(
            data = {
                'labels': labels,
                'series': series
            }
        )
        response_data.is_valid(raise_exception = True)
        return Response(response_data.data)        
    
class AgreementByYearView(APIView):

    serializer_class = DashboardReportSerializer

    def get(self, request):
        repository = AgreementRepository()
        data = repository.get_initial_by_year()

        labels = [item['year'] for item in data]
        series = [item['total'] for item in data]
        
        response_data = DashboardReportSerializer(
            data = {
                'labels': labels,
                'series': series
            }
        )
        response_data.is_valid(raise_exception = True)

        return Response(response_data.data)
    
class AgreementPerProgramView(APIView):

    serializer_class = DashboardReportSerializer

    def get(self, request):
        repository = AgreementRepository()
        data = repository.per_program()

        labels = [item['program__name'] for item in data]
        series = [item['total'] for item in data]

        response_data = DashboardReportSerializer(
            data = {
                'labels': labels,
                'series': series
            }
        )
        response_data.is_valid(raise_exception = True)

        return Response(response_data.data)
    
class AgreementStudentsView(APIView):

    serializer_class = DashboardReportSerializer

    def get(self, request):
        repository = AgreementRepository()
        data = repository.get_total_students()

        labels = [item['name'] for item in data]
        series = [item['total'] for item in data]
        
        response_data = DashboardReportSerializer(
            data = {
                'labels': labels,
                'series': series
            }
        )
        response_data.is_valid(raise_exception = True)

        return Response(response_data.data)