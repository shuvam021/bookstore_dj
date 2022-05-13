from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from api.serializers import BookSerializer, CartSerializer, UserSerializer

from .models import Book, Cart, User


# Create your views here.
class RegisterViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
