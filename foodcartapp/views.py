import json

from rest_framework.decorators import api_view
from rest_framework.response import Response
from phonenumber_field.phonenumber import PhoneNumber
from phonenumber_field.validators import validate_international_phonenumber
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
        
        required_keys = ['firstname', 'lastname', 'phonenumber', 'address']
        missing_fields = []
        invalid_fields = []
        for key in required_keys:
            if key not in data or data[key] == "":
                missing_fields.append(key)
            elif not isinstance(data[key], str):
                invalid_fields.append(key)

        if missing_fields or invalid_fields:
            error_message = ''
            if missing_fields:
                missing_fields_str = ', '.join(missing_fields)
                error_message += f'Missing fields: {missing_fields_str}. '
            if invalid_fields:
                invalid_fields_str = ', '.join(invalid_fields)
                error_message += f'Invalid fields: {invalid_fields_str} must be provided as a string.'
            return Response({'error': error_message}, status=400)

        for product in data['products']:
            product_id = product.get('product')
            if not Product.objects.filter(id=product_id).exists():
                return Response(f'Invalid product id: {product_id}')

        firstname=data['firstname']
        lastname=data['lastname']
        phonenumber=data['phonenumber']
        address=data['address']

        try:
            phone_number = PhoneNumber.from_string(phonenumber)
            validate_international_phonenumber(phone_number)
        except Exception as e:
            return Response({'error': f'Invalid phone number: {phonenumber}'}, status=400)

        order = Order.objects.create(
            firstname=firstname,
            lastname=lastname,
            phonenumber=phonenumber,
            address=address,
        )
        

        products_str = data.get('products', '')
        if products_str:
            products = order_products
            for product in products:
                product_id = product.get('product')
                quantity = product.get('quantity')
                if product_id:
                    product_obj = Product.objects.get(pk=product_id)
                    OrderProduct.objects.create(order=order, product=product_obj, quantity=quantity)

        return Response({'message': 'Order created successfully'}, status=201)
    except json.JSONDecodeError:
        return Response({'error': 'Products key not presented or not list'}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
