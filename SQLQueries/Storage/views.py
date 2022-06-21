from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Store, Purchase
from django.db.models import Count, Sum


class StoreAPIView(APIView):

    def get(self, r: Request):
        total_sum_per_store = Purchase.objects.values('store__name').annotate(Sum('price'))
        all_purchases = Purchase.objects.values('store__name', 'name', 'price')
        min_price = 100
        expensive_purchases = Purchase.objects.values('store__name').filter(price__gte=min_price).annotate(
            Count('store__name'))

        total_sum_per_store_sql = Purchase.objects.raw('SELECT Storage_store.id, '
                                                       'Storage_store.name, SUM(Storage_purchase.price) AS total_sum '
                                                       'FROM Storage_purchase INNER JOIN Storage_store '
                                                       'ON (Storage_purchase.store_id = Storage_store.id) '
                                                       'GROUP BY Storage_store.name')

        all_purchases_sql = Purchase.objects.raw('SELECT Storage_store.id, Storage_purchase.id, '
                                                 'Storage_store.name AS store_name, '
                                                 'Storage_purchase.product AS purchase_name, '
                                                 'Storage_purchase.price AS price '
                                                 'FROM Storage_purchase INNER JOIN Storage_store '
                                                 'ON (Storage_purchase.store_id = Storage_store.id)')

        expensive_purchases_sql = Purchase.objects.raw('SELECT Storage_store.id, Storage_purchase.id, '
                                                       'Storage_store.name AS name, COUNT(Storage_purchase.id) AS count '
                                                       'FROM Storage_purchase INNER JOIN Storage_store '
                                                       'ON (Storage_purchase.store_id = Storage_store.id) '
                                                       'WHERE Storage_purchase.price >= %s '
                                                       'GROUP BY Storage_store.id', [min_price])

        list_expensive_purchases = [{'store_name': x.name, 'count_purchases': x.count}
                                    for x in expensive_purchases_sql]
        list_total_sum_per_store = [{'store__name': x.name, 'price__sum': x.total_sum}
                                    for x in total_sum_per_store_sql]
        list_all_purchases = [{'store__name': x.store_name, 'purchase__name': x.purchase_name, 'price': x.price}
                              for x in all_purchases_sql]
        return Response({
            'total_sum_per_store': list(total_sum_per_store),
            'all_purchases': list(all_purchases),
            'expensive_purchases': list(expensive_purchases),
            'total_sum_per_store_sql': list_total_sum_per_store,
            'all_purchases_sql': list_all_purchases,
            'expensive_purchases_sql': list_expensive_purchases,
        })

    def post(self, r: Request):
        print(r.data)
        return Response({'test': 'Test get request'})

# Create your views here.
