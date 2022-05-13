from rest_framework.serializers import ModelSerializer

from .models import Book, Cart, User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'phone')
        read_only_fields = ('id',)
        extra_kwargs = {'password': {'write_only': True}}


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
        read_only_fields = ('id',)


class CartSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'total_quantity', 'total_price', 'status', 'product', 'user']
        read_only_fields = ('id', 'user')
