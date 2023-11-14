from rest_framework import serializers
from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    # настройте сериализатор для продукта

    class Meta:
        model = Product  # Указываем таблицу
        fields = ['id', 'title', 'description']  # Столбцы таблицы которые показываем


class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе

    class Meta:
        model = StockProduct  # Указываем таблицу
        fields = ['product', 'quantity', 'price']  # Столбцы таблицы которые показываем


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    # настройте сериализатор для склада
    class Meta:
        model = Stock  # Указываем таблицу
        fields =['id', 'address', 'positions']  # Столбцы таблицы которые показываем

    # Метод создания. validated_data - данные полученные от пользователя:
    def create(self, validated_data):  #
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)

        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for data in positions:
            print(f'data = {data}')
            stock.positions.create(**data)
        return stock


    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for data in positions:
            stock.positions.update_or_create(product=data['product'], defaults={**data})
        return stock
