from .models import Order, OrderItem
from rest_framework.serializers import ModelSerializer


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = OrderItemSerializer(many=True, allow_empty=False, write_only=True) 
    class Meta:
        model = Order
        fields = ['id', 'firstname', 'lastname', 'phonenumber', 'address', 'products']

    def create(self, validated_data):
        products = validated_data.pop('products')  
        order = Order.objects.create(**validated_data)  
        for product_data in products:
            OrderItem.objects.create(order=order, **product_data)

        return order