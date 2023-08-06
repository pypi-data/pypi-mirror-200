from datetime import datetime

from ckan.model.resource import Resource
from sqlalchemy import func

from ckanext.feedback.models.resource_comment import (
    ResourceComment,
    ResourceCommentSummary,
)
from ckanext.feedback.models.session import session


# Get comments of the target package
def get_package_comments(package_id):
    count = (
        session.query(func.sum(ResourceCommentSummary.comment))
        .join(Resource)
        .filter(Resource.package_id == package_id)
        .scalar()
    )
    return count or 0


# Get comments of the target resource
def get_resource_comments(resource_id):
    count = (
        session.query(ResourceCommentSummary.comment)
        .filter(ResourceCommentSummary.resource_id == resource_id)
        .scalar()
    )
    return count or 0


# Get rating of the target package
def get_package_rating(package_id):
    row = (
        session.query(
            func.sum(
                ResourceCommentSummary.rating * ResourceCommentSummary.comment
            ).label('total_rating'),
            func.sum(ResourceCommentSummary.comment).label('total_comment'),
        )
        .join(Resource)
        .filter(Resource.package_id == package_id)
        .first()
    )
    if row and row.total_comment and row.total_comment > 0:
        return row.total_rating / row.total_comment
    else:
        return 0


# Get rating of the target resource
def get_resource_rating(resource_id):
    rating = (
        session.query(ResourceCommentSummary.rating)
        .filter(ResourceCommentSummary.resource_id == resource_id)
        .scalar()
    )
    return rating or 0


# Create new resource summary
def create_resource_summary(resource_id):
    summary = (
        session.query(ResourceCommentSummary)
        .filter(ResourceCommentSummary.resource_id == resource_id)
        .first()
    )
    if summary is None:
        summary = ResourceCommentSummary(
            resource_id=resource_id,
        )
        session.add(summary)


# Recalculate approved ratings and comments related to the resource summary
def refresh_resource_summary(resource_id):
    row = (
        session.query(
            func.sum(ResourceComment.rating).label('total_rating'),
            func.count().label('total_comment'),
        )
        .filter(
            ResourceComment.resource_id == resource_id,
            ResourceComment.approval,
        )
        .first()
    )
    summary = (
        session.query(ResourceCommentSummary)
        .filter(ResourceCommentSummary.resource_id == resource_id)
        .first()
    )
    if summary is None:
        summary = ResourceCommentSummary(
            resource_id=resource_id,
            rating=row.total_rating / row.total_comment,
            comment=row.total_comment,
        )
        session.add(summary)
    else:
        summary.rating = row.total_rating / row.total_comment
        summary.comment = row.total_comment
        summary.updated = datetime.now()
