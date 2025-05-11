from datetime import (
    datetime,
    timedelta
)

from django.db.models import (
    Count,
    QuerySet
)
from django.db.models.functions import (
    ExtractYear
)

from core.interfaces.repository import (
    RepositoryInterface
)
from ..models import (
    Agreement,
    AgreementDocumentThrough,
    AgreementStudentThrough,
    AgreementDocumentComment
)

class AgreementRepository(RepositoryInterface[Agreement]):

    def __init__(self):
        super().__init__(Agreement)

    def count_by_status(self, **kwargs) -> QuerySet[Agreement]:
        """
        Devuelve un queryset agrupado por estado con la cantidad de convenios en cada uno.
        """
        return (
            self
            .model
            .objects
            .values('status')
            .order_by('status')
            .annotate(total = Count('id'))
        )
    
    def get_soon_to_expire(self, days: int = 30):
        """
        Retorna una serie de fechas con el número de convenios que vencen por día.
        """
        now = datetime.now()
        future = now + timedelta(days = days)
        return (
            self
            .model
            .objects
            .filter(end_date__range = (now, future))
            .values('end_date')
            .annotate(total = Count('id'))
            .order_by('end_date')
        )
    
    def get_initial_by_year(self):
        """
        Retorna la cantidad de convenios iniciados por año.
        """
        return (
            self
            .model
            .objects
            .annotate(year = ExtractYear('initial_date'))
            .values('year')
            .annotate(total = Count('id'))
            .order_by('year')
        )
    
    def per_program(self):
        """
        Retorna la cantidad de convenios agrupados por programa académico.
        """
        return (
            self
            .model
            .objects
            .values("program__name")
            .annotate(total = Count("id"))
            .order_by("program__name")
        )
    
    def get_total_students(self):
        """
        Devuelve la cantidad de estudiantes por convenio usando la tabla intermedia.
        """
        return (
            self
            .model
            .objects
            .annotate(total = Count('agreementstudentthrough__student', distinct = True))
            .values('id', 'name', 'total')
            .order_by('total')
        )

class AgreementDocumentThroughRepository(RepositoryInterface[AgreementDocumentThrough]):

    def __init__(self):
        super().__init__(AgreementDocumentThrough)

class AgreementStudentThroughRepository(RepositoryInterface[AgreementStudentThrough]):

    def __init__(self):
        super().__init__(AgreementStudentThrough)

class AgreementDocumentCommentRepository(RepositoryInterface[AgreementDocumentComment]):

    def __init__(self):
        super().__init__(AgreementDocumentComment)