from rest_framework import generics, viewsets
from base_app.models import Filial, Menu, SubMenu, TestModel
from api.serializers import FilialSerializer, MenuSerializer, SubMenuSerializer, TestModelSerializer


class TestViewSet(generics.ListCreateAPIView):
    queryset = TestModel.objects.all()
    serializer_class = TestModelSerializer


class FilialAPIView(generics.ListAPIView):
    queryset = Filial.objects.all()
    serializer_class = FilialSerializer


class MenuAPIView(generics.ListAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_queryset(self):
        filial = self.request.query_params.getlist('slugFilial')
        if filial:
            return Menu.objects.all().filter(filial__slug=filial[0])
        else:

            return Menu.objects.all().filter()


class SubMenuAPIView(generics.ListAPIView):
    queryset = SubMenu.objects.all()
    serializer_class = SubMenuSerializer

    def get_queryset(self):
        menu = self.request.query_params.getlist('slugMenu')
        if menu:
            return SubMenu.objects.all().filter(menu__slug=menu[0])
        else:
            return SubMenu.objects.all()
