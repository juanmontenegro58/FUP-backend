from django.db import transaction

from core.interfaces.controller import (
    ControllerMultiRepositoryInterface
)
from ..validators.defense import (
    DefenseStatusValidator,
    DefenseNewDateValidator
)
from ..enums import (
    DefenseStatusEnum
)
from ..models import (
    Defense
)

class RescheduleDefenseController(ControllerMultiRepositoryInterface):

    """
    Controlador para reprogramar una sustentación.

    Aplica validaciones antes de actualizar el estado de la sustentación a `REPROGRAMADA`
    y registra un comentario asociado a la reprogramación.

    Attributes:
        validations (list): Lista de validaciones a aplicar antes de ejecutar la reprogramación.
    """
    
    validations = [
        DefenseStatusValidator,
        DefenseNewDateValidator,
    ]

    def update_status(self):
        """
        Actualiza el estado de la sustentación a `REPROGRAMADA` y guarda los cambios.
        """

        defense: Defense = self.raw_data['defense']
        defense.status = DefenseStatusEnum.REPROGRAMADA.value
        defense.save()
    
    def create_comment(self):
        """
        Crea un comentario asociado a la reprogramación de la sustentación.

        Registra el comentario del usuario con la referencia a la sustentación.
        """

        
        data = {
            'comment': self.raw_data['comment'],
            'defense': self.raw_data['defense'],
            'created_by': self.raw_data['user'],
            'previous_date': self.raw_data['defense'].scheduled_date,
            'new_date': self.raw_data['new_scheduled_date']
        }
        self.repositories['defense_comment'].create(**data)

    def preload_data(self):
        """
        Precarga los datos necesarios para la ejecución.

        Obtiene y almacena en `self.raw_data` la información de la sustentación basada en su ID.
        """
        
        self.raw_data['defense'] = self.repositories['defense'].get_by_id(
            obj_id = self.raw_data['defense_id']
        )

    @transaction.atomic
    def execute(self):
        """
        Ejecuta el proceso de reprogramación de una sustentación.

        - Precarga los datos requeridos.
        - Valida la información utilizando las reglas definidas.
        - Actualiza el estado de la sustentación a `REPROGRAMADA`.
        - Crea un comentario sobre la reprogramación.
        """
        self.preload_data()
        self.validator.add_rules(rules = self.validations)
        self.validator.validate(data = self.raw_data)
        self.update_status()
        self.create_comment()