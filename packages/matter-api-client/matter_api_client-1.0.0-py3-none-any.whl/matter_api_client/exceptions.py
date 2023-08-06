from matter_exceptions import DetailedException


class APIClientError(DetailedException):
    TOPIC = "API Client Error"
