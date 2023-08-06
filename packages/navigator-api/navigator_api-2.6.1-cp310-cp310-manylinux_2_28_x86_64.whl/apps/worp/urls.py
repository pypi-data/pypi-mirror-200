"""Urls.

List of program routes.
"""
from apps.worp.views import PO_Tracker, Tracker, TrackerDefaults
from navigator.routes import path  # always required

df = TrackerDefaults()

urls = [
    path(
        "get", "/api/v1/tracker/defaults", df.get_defaults, name="worp_tracker_defaults"
    ),
    path(
        "post",
        "/api/v1/tracker/defaults",
        df.set_defaults,
        name="worp_tracker_default_set",
    ),
    path("post", "/api/v1/tracker/values", df.get_values, name="worp_tracker_values"),
    path("get", "/api/v1/tracker/list", df.get_trackers, name="worp_tracker_get"),
    path("get", "/api/v1/tracker/current", df.get_current, name="worp_tracker_current"),
    path("", "/api/v1/tracker", Tracker, name="worp_tracker"),
    path("", "/api/v1/tracker/{uid}", Tracker, name="worp_tracker_id"),
    path("", "/api/v1/po_tracker", PO_Tracker, name="worp_po_tracker"),
]
