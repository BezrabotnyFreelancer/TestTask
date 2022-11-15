from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import filters
# Create your views here.
from .serializers import ProfileSerializer, CategorySerializer, TransactionSerializer, ReplenishmentSerializer
from .permissions import IsOwner
from main.models import Category, Profile, Transaction


class ProfileDetailAPIView(RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, IsOwner, )
    queryset = Profile.objects.all()


class ReplenishmentCreateAPIView(CreateAPIView):
    serializer_class = ReplenishmentSerializer
    permission_classes = (IsAuthenticated, )


class TransactionListCreateAPIView(ListCreateAPIView):
    serializer_class = TransactionSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['total_sum', 'category', 'time']

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            transaction = Transaction()
            transaction.user = self.request.user
            transaction.total_sum = float(serializer.validated_data['total_sum'])
            transaction.time = serializer.validated_data['time']
            transaction.category = serializer.validated_data['category']
            transaction.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryListCreateAPIView(ListCreateAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            category = Category()
            category.user = self.request.user
            category.name = serializer.validated_data['name']
            category.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDeleteUpdateAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = (IsOwner, IsAuthenticated, )
    queryset = Category.objects.all()
