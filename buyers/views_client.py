from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView, RetrieveAPIView
from .serializers import UserSerializer, ClientBusinessSerializer, ClientCatalogeSerializer, ClientAddressSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import User, ClientCataloge, ClientAddress, ClientBusiness
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .permissions import IsAdminOrManager, IsAdmin, IsBuyerOnly
from orders.models import Cart


class ListClientView(ListAPIView):
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrManager]


class ClientUserView(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user
        profile = User.objects.get(id=user.id)
        cartItems = Cart.objects.filter(user=user)
        serializer = self.serializer_class(profile)
        data = serializer.data
        data['cartItems'] = len(cartItems)
        return Response(data, status=status.HTTP_200_OK)


class ClientProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_serializer = UserSerializer(user)

        client_address = ClientAddress.objects.get(user=user)
        client_address_serializer = ClientAddressSerializer(client_address)

        client_catalog = ClientCataloge.objects.get(user=user)
        client_catalog_serializer = ClientCatalogeSerializer(
            client_catalog, context={'request': request})

        client_business = ClientBusiness.objects.get(user=user)
        client_business_serializer = ClientBusinessSerializer(client_business)

        response_data = {
            'user': user_serializer.data,
            'address': client_address_serializer.data,
            'catalog': client_catalog_serializer.data,
            'business': client_business_serializer.data
        }

        return Response(response_data)


class ManageClientView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]


class ListClientBusinessView(ListCreateAPIView):
    queryset = ClientBusiness.objects.all()
    serializer_class = ClientBusinessSerializer
    permission_classes = [IsAdminOrManager]


class ListClientCatalogeView(ListCreateAPIView):
    queryset = ClientCataloge.objects.all()
    serializer_class = ClientCatalogeSerializer
    permission_classes = [IsAdminOrManager]


class ListClientAddressView(ListCreateAPIView):
    queryset = ClientAddress.objects.all()
    serializer_class = ClientAddressSerializer
    permission_classes = [IsAdminOrManager]


class ManageClientBusinessView(RetrieveUpdateDestroyAPIView):
    queryset = ClientBusiness.objects.all()
    serializer_class = ClientBusinessSerializer
    permission_classes = [IsAdminOrManager]


class ManageClientCatalogeView(RetrieveUpdateDestroyAPIView):
    queryset = ClientCataloge.objects.all()
    serializer_class = ClientCatalogeSerializer
    permission_classes = [IsAdminOrManager]


class ManageClientAddressView(RetrieveUpdateDestroyAPIView):
    queryset = ClientAddress.objects.all()
    serializer_class = ClientAddressSerializer
    permission_classes = [IsAdminOrManager]


class ClientBusinessView(APIView):
    serializer_class = ClientBusinessSerializer
    permission_classes = [IsAuthenticated, IsBuyerOnly]

    def get(self, request):
        user = self.request.user
        try:
            emp_details = ClientBusiness.objects.get(user=user)
        except:
            raise NotFound(detail="user basic details not found")

        serializer = self.serializer_class(
            emp_details, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def post(self, request):
    #     user = request.user
    #     serializer = self.serializer_class(
    #         data=request.data, context={'request': request})

    #     if (ClientBusiness.objects.filter(user=user).exists()):
    #         return Response({"detail": "user details already exist"}, status=status.HTTP_409_CONFLICT)

    #     if serializer.is_valid():
    #         serializer.save(user=user)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = request.user
        try:
            emp_details = ClientBusiness.objects.get(user=user)
        except ClientBusiness.DoesNotExist:
            raise NotFound(detail="user not found")

        serializer = self.serializer_class(
            emp_details, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request):
    #     user = request.user
    #     try:
    #         emp_details = ClientBusiness.objects.get(user=user)
    #         emp_details.delete()
    #         return Response({"detail": "user details deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    #     except ClientBusiness.DoesNotExist:
    #         raise NotFound(detail="user not found")


class ClientCatalogeView(APIView):
    serializer_class = ClientBusinessSerializer
    permission_classes = [IsAuthenticated, IsBuyerOnly]

    def get(self, request):
        user = self.request.user
        try:
            emp_details = ClientBusiness.objects.get(user=user)
        except:
            raise NotFound(detail="user basic details not found")

        serializer = self.serializer_class(
            emp_details, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def post(self, request):
    #     user = request.user
    #     serializer = self.serializer_class(
    #         data=request.data, context={'request': request})

    #     if (ClientBusiness.objects.filter(user=user).exists()):
    #         return Response({"detail": "user details already exist"}, status=status.HTTP_409_CONFLICT)

    #     if serializer.is_valid():
    #         serializer.save(user=user)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = request.user
        try:
            emp_details = ClientBusiness.objects.get(user=user)
        except ClientBusiness.DoesNotExist:
            raise NotFound(detail="user not found")

        serializer = self.serializer_class(
            emp_details, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request):
    #     user = request.user
    #     try:
    #         emp_details = ClientBusiness.objects.get(user=user)
    #         emp_details.delete()
    #         return Response({"detail": "user details deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    #     except ClientBusiness.DoesNotExist:
    #         raise NotFound(detail="user not found")


class ClientAddressView(APIView):
    serializer_class = ClientAddressSerializer
    permission_classes = [IsAuthenticated, IsBuyerOnly]

    def get(self, request):
        user = self.request.user
        try:
            emp_details = ClientAddress.objects.get(user=user)
        except:
            raise NotFound(detail="Client address details not found")

        serializer = self.serializer_class(
            emp_details, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(
            data=request.data, context={'request': request})

        if (ClientAddress.objects.filter(user=user).exists()):
            return Response({"detail": "Client address details already exist"}, status=status.HTTP_409_CONFLICT)

        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = request.user
        try:
            emp_details = ClientAddress.objects.get(user=user)
        except ClientAddress.DoesNotExist:
            raise NotFound(detail="Client address not found")

        serializer = self.serializer_class(
            emp_details, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        try:
            emp_details = ClientAddress.objects.get(user=user)
            emp_details.delete()
            return Response({"detail": "Client address details deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except ClientAddress.DoesNotExist:
            raise NotFound(detail="Client address not found")
