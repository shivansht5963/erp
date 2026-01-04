# File: api/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.db.models import Sum
from django.utils import timezone

from students.models import Student, StudentInfo
from accounts.models import CustomUser
from faculty.models import Department, Course, Subject, Class, Teacher
from attendance.models import Attendance, AttendanceReport
from fees.models import FeePayment, FeeStructure, FeeCategoryAmount
from exams.models import Marks
from notifications.models import Notification

from .serializers import (
    StudentSerializer, StudentDetailSerializer, DepartmentSerializer,
    CourseSerializer, ClassSerializer, SubjectSerializer, TeacherDetailSerializer,
    AttendanceSerializer, AttendanceCreateSerializer, StudentAttendanceSerializer,
    FeePaymentSerializer, StudentFeeStatusSerializer, StudentFeePaymentHistorySerializer,
    MarksSerializer, StudentMarksSerializer, SubjectMarksSerializer, ResultCardSerializer,
    LoginSerializer, ProfileUpdateSerializer, ChangePasswordSerializer,
    NotificationSerializer, NotificationDetailSerializer, UserSerializer,
    TeacherSendNotificationSerializer
)

class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Student.objects.all().order_by('roll_number')
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def attendance(self, request, pk=None):
        student = self.get_object()
        attendance = Attendance.objects.filter(student=student).order_by('-date')
        return Response(StudentAttendanceSerializer(attendance, many=True).data)

    @action(detail=True, methods=['get'])
    def marks(self, request, pk=None):
        student = self.get_object()
        marks = Marks.objects.filter(student=student)
        return Response(StudentMarksSerializer(marks, many=True).data)

class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

class ClassViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated]

class TeacherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherDetailSerializer
    permission_classes = [IsAuthenticated]

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all().order_by('-date')
    permission_classes = [IsAuthenticated]
    def get_serializer_class(self):
        return AttendanceCreateSerializer if self.action == 'create' else AttendanceSerializer

class FeePaymentViewSet(viewsets.ModelViewSet):
    queryset = FeePayment.objects.all().order_by('-payment_date')
    serializer_class = FeePaymentSerializer
    http_method_names = ['get', 'post']
    permission_classes = [IsAuthenticated]

class MarksViewSet(viewsets.ModelViewSet):
    queryset = Marks.objects.all()
    serializer_class = MarksSerializer
    permission_classes = [IsAuthenticated]

class ResultViewSet(viewsets.ViewSet):
    def list(self, request):
        sid = request.query_params.get('student_id')
        if not sid: return Response({'error': 'student_id required'}, status=400)
        student = get_object_or_404(Student, id=sid)
        marks = Marks.objects.filter(student=student)
        total = marks.aggregate(total=Sum('total_marks'))['total'] or 0
        perc = (total / (marks.count() * 100)) * 100 if marks.count() > 0 else 0
        return Response({'student': student.roll_number, 'total': total, 'percentage': perc})

class AuthViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        ser = LoginSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = authenticate(username=ser.validated_data['username'], password=ser.validated_data['password'])
        if not user: return Response({'error': 'Invalid credentials'}, status=401)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'auth_token': token.key, 'role': user.role})

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        """Get authenticated user's profile"""
        user = request.user
        return Response({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'phone': user.phone,
            'address': user.address,
            'dob': user.dob,
        })

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """Logout by deleting the user's token."""
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
        except Token.DoesNotExist:
            pass
        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        """Update authenticated user's profile"""
        ser = ProfileUpdateSerializer(request.user, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Change user's password"""
        ser = ChangePasswordSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(ser.validated_data['old_password']):
            return Response({'error': 'Old password is incorrect'}, status=400)
        user.set_password(ser.validated_data['new_password'])
        user.save()
        # Delete all existing tokens to force re-login
        Token.objects.filter(user=user).delete()
        return Response({'detail': 'Password changed successfully. Please login again.'})

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def debug_auth(self, request):
        """Debug endpoint: echo the Authorization header and parsed request.auth."""
        auth_header = request.META.get('HTTP_AUTHORIZATION', 'NOT_SET')
        request_auth = str(request.auth) if request.auth else 'None'
        return Response({
            'HTTP_AUTHORIZATION_header': auth_header,
            'request.auth': request_auth,
            'request.user': str(request.user),
            'is_authenticated': request.user.is_authenticated
        })

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student' and hasattr(user, 'student'):
            return Notification.objects.filter(recipient=user.student).order_by('-created_at')
        return Notification.objects.filter(sender=user).order_by('-created_at')

    @action(detail=False, methods=['post'], url_path='send-announcement')
    def send_announcement(self, request):
        # Allow users with role 'faculty' or 'admin', superusers,
        # or users who have an associated Teacher profile.
        # Use an explicit query to avoid attribute errors and ensure DB-backed check.
        is_teacher_profile = Teacher.objects.filter(user=request.user).exists()
        if request.user.role not in ['faculty', 'admin'] and not request.user.is_superuser and not is_teacher_profile:
            return Response({'error': 'Unauthorized'}, status=403)
        ser = TeacherSendNotificationSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        t_type, t_id = ser.validated_data['target_type'], ser.validated_data['target_id']
        
        recipients = []
        if t_type == 'class':
            recipients = Student.objects.filter(class_enrolled_id=t_id)
        else:
            recipients = [get_object_or_404(Student, id=t_id)]

        Notification.objects.bulk_create([
            Notification(sender=request.user, recipient=s, title=ser.validated_data['title'], message=ser.validated_data['message'])
            for s in recipients
        ])
        return Response({'status': 'sent', 'count': len(recipients)})

    @action(detail=True, methods=['put'])
    def mark_read(self, request, pk=None):
        notif = self.get_object()
        notif.is_read = True
        notif.save()
        return Response({'status': 'read'})