from rest_framework.routers import DefaultRouter

from logistic.views import ProductViewSet, StockViewSet

# Т.к. в views.py наследовались от ModelViewSet, а он содержит набор обработчиков,
# для регистрации маршрутов используются роутеры.
# Создание стандартного роутера:
router = DefaultRouter()

# Регистрация маршрута:
# router.register('префикс по которому в браузере будет доступ', СамВьюСет)
router.register('products', ProductViewSet)
router.register('stocks', StockViewSet)

urlpatterns = router.urls  # В данном примере стандартные маршруты отсутствуют

"""
Если бы здесь были и стандартные маршруты, помимо лежащих в роутере,
то к ним маршруты роутера можно просто прибавить через конкатенацию:
urlpatterns = [
    path('admin/', admin.site.urls),
] + router.urls
"""
