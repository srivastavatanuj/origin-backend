from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from .models import StaffProfile, User
from .serializers import StaffProfileSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .permissions import IsAdmin


class StaffCreateView(CreateAPIView):
    queryset = StaffProfile.objects.all()
    serializer_class = StaffProfileSerializer
    permission_classes = [IsAdmin]


class StaffManageView(RetrieveUpdateDestroyAPIView):
    queryset = StaffProfile.objects.all()
    serializer_class = StaffProfileSerializer
    permission_classes = [IsAdmin]


class StaffListView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request, *args, **kwargs):
        assigned = StaffProfile.objects.all()
        notAssigned = User.objects.filter(is_staff=True, is_superuser=False).exclude(
            id__in=assigned.values_list('user_id', flat=True))
        assigned_serializer = [
            {"id": user.id, "user_id": user.user.id, "user_email": user.user.email, "role": user.role} for user in assigned]
        notAssigned_serializer = [
            {"id": user.id, "email": user.email} for user in notAssigned]
        data = {
            "assigned": assigned_serializer,
            "not_assigned": notAssigned_serializer
        }

        return Response(data)
