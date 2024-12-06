from rest_framework import pagination, response, filters


class DataTablePagination(pagination.LimitOffsetPagination):

    default_limit = 10
    offset_query_param = 'start'

    def get_paginated_response(self, data):
        return response.Response({
            'data': data,
            'recordsTotal': self.count,
            'recordsFiltered': self.count,
        })


class DataTableSearchFilter(filters.SearchFilter):
    search_param = 'search[value]'
