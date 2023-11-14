from rest_framework.viewsets import ModelViewSet

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination

# При наследовании от ModelViewSet нет необходимости создавать отдельные методы
# (list, update, destroy и т.д.) как если бы мы наследовались от ViewSet
class ProductViewSet(ModelViewSet):
    # Модель из которой будем брать все данные
    queryset = Product.objects.all()
    # Используемый сериализатор для конвертации в JSON и обратно
    serializer_class = ProductSerializer

    # при необходимости добавьте параметры фильтрации

    # Явное указание ВьюСету какие фильтры использовать
    filter_backends = [DjangoFilterBackend, SearchFilter]

    # filterset_fields - Поиск по параметрам.
    # Передаются в GET запросе после урла "атрибут="
    # (GET {{baseUrl}}/products/?id=1)
    filterset_fields = ['id', 'title']  # Атрибуты по которым можно искать.

    # search_fields - Поиск по тексту
    # Передаются в GET запросе после урла при помощи ключевого слова search
    # (GET {{baseUrl}}/products/?search=помидоры)
    # Ключевое слово можно изменить в настройках REST_FRAMEWORK файла settings.py
    search_fields = ['title', 'description']  # Поля по которым можно искать.

    # ordering_fields - Упорядочивание отображения
    # Передаются в GET запросе после при помощи ключевого слова ordering
    # (GET {{baseUrl}}/products/?ordering=id)
    # Ключевое слово можно изменить в настройках REST_FRAMEWORK файла settings.py
    # Для обратного направления сортировки нужно поставить минус перед значением
    # (GET {{baseUrl}}/products/?ordering=-id)
    # можно вторым параметром после фильтрации, например:
    # (GET {{baseUrl}}/products/?id=1&ordering=title)
    # также можно указывать несколько условий фильтрации
    # (GET {{baseUrl}}/products/?ordering=-id,title)
    ordering_fields = ['id', 'title']


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    # при необходимости добавьте параметры фильтрации
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['address']
    filterset_fields = ['products']

    # Явное указание ВьюСету использовать пагинацию
    # требует при GET запрросе указать один или два параметра
    # limit и offset
    # (GET {{baseUrl}}/products/?limit=2) - отобразятся 2 элемента от начала
    # (GET {{baseUrl}}/products/?limit=2&offset=4) - отобразятся 2 элемента начиная с четвертого
    # При включенной пагинации она будет применяться всегда, полного списка вывода уже не получить
    pagination_class = LimitOffsetPagination
