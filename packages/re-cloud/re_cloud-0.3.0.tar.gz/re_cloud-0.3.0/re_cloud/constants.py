# ---- THIS FILE IS CONTENT IS SHARED BY THE CLI AND THE SERVER ---- #
# ---- IF YOU EDIT IT, MAKE SURE TO UPDATE BOTH FILES! ---- #

from enum import Enum


class UploadTypes(Enum):
    """
    The upload types.
    """

    HTML_FILE = "HTML_FILE"
    HTML_FOLDER = "HTML_FOLDER"
    MARKDOWN = "MARKDOWN"
    DBT_DOCS = "DBT_DOCS"
    GREAT_EXPECTATIONS = "GREAT_EXPECTATIONS"
    ELEMENTARY = "ELEMENTARY"
    JUPYTER_NOTEBOOK = "JUPYTER_NOTEBOOK"
    PANDAS_PROFILING = "PANDAS_PROFILING"
    RE_DATA_OVERVIEW = "RE_DATA_OVERVIEW"


class UploadStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


RE_DATA_ARTEFACTS = [
    "overview.json",
    "metadata.json",
    "index.html",
    "dbt_manifest.json",
    "monitored.json",
    "table_samples.json",
    "tests_history.json",
]

DBT_DOCS_ARTEFACTS = ["index.html", "catalog.json", "manifest.json", "run_results.json"]

ELEMENTARY_ARTEFACTS = ["elementary_report.html"]

PANDAS_PROFILING_ARTEFACTS = ["index.html"]
JUPYTER_NOTEBOOK_ARTEFACTS = ["index.html"]
CUSTOM_ARTEFACTS = ["index.html"]

ARTEFACTS = {
    UploadTypes.RE_DATA_OVERVIEW.value: RE_DATA_ARTEFACTS,
    UploadTypes.DBT_DOCS.value: DBT_DOCS_ARTEFACTS,
    UploadTypes.PANDAS_PROFILING.value: PANDAS_PROFILING_ARTEFACTS,
    UploadTypes.JUPYTER_NOTEBOOK.value: JUPYTER_NOTEBOOK_ARTEFACTS,
    UploadTypes.HTML_FILE.value: CUSTOM_ARTEFACTS,
    UploadTypes.ELEMENTARY.value: ELEMENTARY_ARTEFACTS,
}

# --- THE COPIED FILE CONTENT ENDS --- #
# --- IF YOU EDIT IT, MAKE SURE TO UPDATE BOTH FILES! --- #
