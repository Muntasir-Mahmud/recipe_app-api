from rest_framework.pagination import LimitOffsetPagination


class CustomPagination(LimitOffsetPagination):
    default_limit = 4
    max_limit = 10
