import json

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Order, OrderProduct

from django.http import JsonResponse
from django.templatetags.static import static


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })

@api_view(['POST'])
def register_order(request):
    data = request.data

    try:
        order_products = data.get('products', [])
        if not isinstance(order_products, list):
            return Response({'error': 'Products must be provided as a list'}, status=400)
        if not order_products:
            return Response({'error': 'No products provided'}, status=400)
        morder = Order.objects.create(
            firstname=data['firstname'],
            lastname=data['lastname'],
            phonenumber=data['phonenumber'],
            address=data['address'],
        )

        products_str = data.get('products', '')
        if products_str:
            products_list = json.loads(products_str)
            for product in products_list:
                product_id = product.get('product')
                quantity = product.get('quantity')
                if product_id:
                    product_obj = Product.objects.get(pk=product_id)
                    OrderProduct.objects.create(order=morder, product=product_obj, quantity=quantity)

        return Response({'message': 'Order created successfully'}, status=201)
    except json.JSONDecodeError:
        return Response({'error': 'products key not presented or not list'}, status=400)
    except KeyError:
        return Response({'error': 'Incomplete data in request'}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
