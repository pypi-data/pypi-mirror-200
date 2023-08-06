from .augmentations import *
from .augmentations import augmentation_lookup
from .deployment import *
from .deployment import lookup as deployment_lookup
from .models import *
from .models import models_lookup
from .tasks import *
from .tasks import lookup as tasks_lookup
from .utils import *
from .utils import lookup as utils_lookup

lookup = {
    **augmentation_lookup,
    **models_lookup,
    **deployment_lookup,
    **tasks_lookup,
    **utils_lookup,
}
