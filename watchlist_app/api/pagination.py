from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class WatchlistPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'p'
    page_size_query_param = 'size'
    max_page_size = 10
    last_page_strings = 'end'


class WatchListLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 20
    limit_query_param = 'limit'
    offset_query_param = 'start'


class WatchListCursorPagination(CursorPagination):
    page_size = 10
    # ordering = '-created'