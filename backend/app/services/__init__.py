"""
TeeDesign AI — Services Package
"""
from app.services.storage_service import storage_service, StorageService
from app.services.auth_service import (
    authenticate_user,
    create_user,
    get_user_by_email,
    get_user_by_username,
)
from app.services.design_service import (
    create_design,
    get_designs,
    get_design_by_id,
    update_design_status,
    delete_design,
)
from app.services.analytics_service import (
    get_cost_summary,
    get_overview_stats,
    get_performance_data,
)

__all__ = [
    "storage_service",
    "StorageService",
    "authenticate_user",
    "create_user",
    "get_user_by_email",
    "get_user_by_username",
    "create_design",
    "get_designs",
    "get_design_by_id",
    "update_design_status",
    "delete_design",
    "get_cost_summary",
    "get_overview_stats",
    "get_performance_data",
]
