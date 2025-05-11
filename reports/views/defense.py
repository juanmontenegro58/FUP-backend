from django.db.models import (
    Count
)
from django.db.models.functions import (
    ExtractYear
)
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers.common import (
    DashboardReportSerializer
)
from evaluations.models import (
    Defense
)


class DefenseDashboardView(APIView):

    def get(self, request):
        queryset = Defense.objects.exclude(result='')

        data = (
            queryset.annotate(year = ExtractYear("scheduled_date"))
            .values("year", "status", "result")
            .annotate(count=Count("id"))
            .order_by("year")
        )
        
        grouped_data = {}
        years_set = set()

        for item in data:
            year = item["year"]
            key = f"{item['status']} - {item['result']}"
            years_set.add(year)
            if key not in grouped_data:
                grouped_data[key] = {}
            grouped_data[key][year] = item["count"]

        years_sorted = sorted(years_set)
        chart_series = []

        for key, year_counts in grouped_data.items():
            series_data = [year_counts.get(y, 0) for y in years_sorted]
            chart_series.append({
                "name": key,
                "data": series_data
            })

        return Response({
            "series": chart_series,
            "labels": years_sorted
        })
