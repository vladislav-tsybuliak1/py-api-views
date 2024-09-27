from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework import status, generics, mixins

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from cinema.models import Movie, Genre, Actor
from cinema.serializers import (
    GenreSerializer,
    ActorSerializer,

)

class GenreList(APIView):
    def get(self, request: HttpRequest) -> Response:
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest) -> Response:
        serializer = GenreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GenreDetail(APIView):
    def get_object(self, pk: int) -> Genre:
        return get_object_or_404(Genre, pk=pk)

    def get(self, request: HttpRequest, pk: int) -> Response:
        serializer = GenreSerializer(self.get_object(pk=pk))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: HttpRequest, pk: int) -> Response:
        serializer = GenreSerializer(self.get_object(pk=pk), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: HttpRequest, pk: int) -> Response:
        serializer = GenreSerializer(
            self.get_object(pk=pk),
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: HttpRequest, pk: int) -> Response:
        self.get_object(pk=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActorList(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    def get(
        self,
        request: HttpRequest,
        *args: tuple,
        **kwargs: dict
    ) -> Response:
        return self.list(request, *args, **kwargs)

    def post(
        self,
        request: HttpRequest,
        *args: tuple,
        **kwargs: dict
    ) -> Response:
        return self.create(request, *args, **kwargs)


class ActorDetail(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    def get(self,
        request: HttpRequest,
        *args: tuple,
        **kwargs: dict
    ) -> Response:
        return self.retrieve(request, *args, **kwargs)

    def put(
        self,
        request: HttpRequest,
        *args: tuple,
        **kwargs: dict
    ) -> Response:
        return self.update(request, *args, **kwargs)

    def patch(
        self,
        request: HttpRequest,
        *args: tuple,
        **kwargs: dict
    ) -> Response:
        return self.update(request, *args, partial=True, **kwargs)

    def delete(
        self,
        request: HttpRequest,
        *args: tuple,
        **kwargs: dict
    ) -> Response:
        return self.destroy(request, *args, **kwargs)
