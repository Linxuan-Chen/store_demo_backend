from rest_framework.pagination import PageNumberPagination


class ProductPagination(PageNumberPagination):
    """Custom pagination class for product view set

        Default page size is 10, max page size is 100
        Query parameter lookup for page size is 'page_size'
        Query parameter lookup for current page is 'page'

        example: /api/store/products/?page_size=20&page=2
    """
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class CustomerPagination(PageNumberPagination):
    """Custom pagination class for customer view set

        Default page size is 10, max page size is 100
        Query parameter lookup for page size is 'page_size'
        Query parameter lookup for current page is 'page'

        example: /api/store/customers/?page_size=20&page=2
    """
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class OrderPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 20