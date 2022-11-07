class SerializerByMethodMixin:
    serializers = None

    def get_serializer_class(self):
        assert (
            self.serializers is not None
        ), f"'{self.__class__.__name__}' should include a `serializers` attribute,"
        return self.serializers.get(self.request.method)
