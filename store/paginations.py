from rest_framework.pagination import PageNumberPagination


class ProductPagination(PageNumberPagination):
    """Custom pagination class for product view set

        Default page size is 10, max page size is 100
        Query parameter lookup for page size is 'page_size'
        Query parameter lookup for current page is 'page'

        example: /api/store/products/?page_size=20&page=2
    """
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100
