"""Register every feature table once for API, scripts, workers and migrations."""

import ppm_api.modules.agents.tables  # noqa: F401
import ppm_api.modules.agents.task_tables  # noqa: F401
import ppm_api.modules.ai.tables  # noqa: F401
import ppm_api.modules.assessments.tables  # noqa: F401
import ppm_api.modules.capacity.tables  # noqa: F401
import ppm_api.modules.command.tables  # noqa: F401
import ppm_api.modules.delivery.tables  # noqa: F401
import ppm_api.modules.documents.tables  # noqa: F401
import ppm_api.modules.identity.tables  # noqa: F401
import ppm_api.modules.integrations.tables  # noqa: F401
import ppm_api.modules.ml.tables  # noqa: F401
import ppm_api.modules.selection.tables  # noqa: F401
import ppm_api.modules.workspace.tables  # noqa: F401
from ppm_api.shared.table_base import TABLES as TABLES
from ppm_api.shared.table_base import metadata as metadata
