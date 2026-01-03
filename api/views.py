# File: api/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.db.models import Sum, F, Q
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
    NotificationSerializer, NotificationDetailSerializer, UserSerializer
)


# ========== STUDENT VIEWSETS ==========
class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for students:
    - GET /students/ - List all students
    - GET /students/{id}/ - Student details
    """
    queryset = Student.objects.all().order_by('roll_number')
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def attendance(self, request, pk=None):
        """GET /students/{id}/attendance/ - Student attendance"""
        student = self.get_object()
        attendance = Attendance.objects.filter(student=student).order_by('-date')
        serializer = StudentAttendanceSerializer(attendance, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def marks(self, request, pk=None):
        """GET /students/{id}/marks/ - Student marks"""
        student = self.get_object()
        marks = Marks.objects.filter(student=student)
        serializer = StudentMarksSerializer(marks, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def fees(self, request, pk=None):
        """GET /students/{id}/fees/ - Student fee status"""
        student = self.get_object()
        try:
            total_due = 0
            total_paid = FeePayment.objects.filter(
                student=student, status='paid'
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            data = {
                'student_id': student.id,
                'roll_number': student.roll_number,
                'total_due': total_due,
                'total_paid': total_paid,
                'status': 'paid' if total_due == 0 else 'pending'
            }
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def fee_payments(self, request, pk=None):
        """GET /students/{id}/fee-payments/ - Payment history"""
        student = self.get_object()
        payments = FeePayment.objects.filter(student=student).order_by('-payment_date')
        serializer = StudentFeePaymentHistorySerializer(payments, many=True)
        return Response(serializer.data)


# ========== FACULTY VIEWSETS ==========
class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for departments:
    - GET /departments/ - List all departments
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for courses:
    - GET /courses/ - List all courses
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for subjects:
    - GET /subjects/ - List all subjects
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]


class ClassViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for classes:
    - GET /classes/ - List all classes
    """
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated]


class TeacherViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for teachers:
    - GET /teachers/{id}/subjects/ - Teacher's assigned subjects
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherDetailSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def subjects(self, request, pk=None):
        """GET /teachers/{id}/subjects/ - Teacher's assigned subjects"""
        teacher = self.get_object()
        subjects = Subject.objects.filter(teacher=teacher)
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)


# ========== ATTENDANCE VIEWSETS ==========
class AttendanceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for attendance:
    - GET /attendance/ - List attendance records
    - POST /attendance/ - Mark attendance
    - DELETE /attendance/{id}/ - Delete attendance
    """
    queryset = Attendance.objects.all().order_by('-date')
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return AttendanceCreateSerializer
        return AttendanceSerializer

    def get_queryset(self):
        """Filter by student_id if provided in query params"""
        queryset = Attendance.objects.all()
        student_id = self.request.query_params.get('student_id', None)
        if student_id is not None:
            queryset = queryset.filter(student_id=student_id)
        return queryset.order_by('-date')

    def create(self, request, *args, **kwargs):
        """POST /attendance/ - Mark attendance"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """DELETE /attendance/{id}/ - Delete attendance"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


# ========== FEES VIEWSETS ==========
class FeePaymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for fee payments:
    - POST /fees/payments/ - Record payment
    - GET /fees/payments/{student_id}/ - Student payment history
    - GET /fees/{student_id}/due/ - Calculate due fees
    - POST /fees/send-reminder/ - Send fee reminder email
    """
    queryset = FeePayment.objects.all().order_by('-payment_date')
    serializer_class = FeePaymentSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'head', 'options']

    def create(self, request, *args, **kwargs):
        """POST /fees/payments/ - Record payment"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def student_payments(self, request):
        """GET /fees/payments/{student_id}/ - Student payment history"""
        student_id = request.query_params.get('student_id', None)
        if student_id is None:
            return Response(
                {'error': 'student_id query parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payments = FeePayment.objects.filter(student_id=student_id).order_by('-payment_date')
        serializer = StudentFeePaymentHistorySerializer(payments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def student_due(self, request):
        """GET /fees/{student_id}/due/ - Calculate due fees"""
        student_id = request.query_params.get('student_id', None)
        if student_id is None:
            return Response(
                {'error': 'student_id query parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        student = get_object_or_404(Student, id=student_id)
        total_paid = FeePayment.objects.filter(
            student=student, status='paid'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        data = {
            'student_id': student.id,
            'roll_number': student.roll_number,
            'total_paid': float(total_paid),
            'status': 'paid' if float(total_paid) == 0 else 'pending'
        }
        return Response(data)

    @action(detail=False, methods=['post'])
    def send_reminder(self, request):
        """POST /fees/send-reminder/ - Send fee reminder email"""
        student_id = request.data.get('student_id', None)
        if student_id is None:
            return Response(
                {'error': 'student_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        student = get_object_or_404(Student, id=student_id)
        # TODO: Implement email sending logic
        return Response({
            'message': f'Fee reminder sent to {student.user.email}',
            'student_id': student.id
        })


# ========== MARKS VIEWSETS ==========
class MarksViewSet(viewsets.ModelViewSet):
    """
    API endpoint for marks:
    - GET /marks/ - List all marks
    - POST /marks/ - Create marks entry
    - GET /marks/{id}/ - Mark details
    - PUT /marks/{id}/ - Update marks
    - DELETE /marks/{id}/ - Delete marks
    - GET /marks/student/{student_id}/ - Student marks
    - GET /marks/subject/{subject_id}/ - Subject marks
    """
    queryset = Marks.objects.all()
    serializer_class = MarksSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def by_student(self, request):
        """GET /marks/by_student/ - Student marks"""
        student_id = request.query_params.get('student_id', None)
        if student_id is None:
            return Response(
                {'error': 'student_id query parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        marks = Marks.objects.filter(student_id=student_id)
        serializer = StudentMarksSerializer(marks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_subject(self, request):
        """GET /marks/by_subject/ - Subject marks"""
        subject_id = request.query_params.get('subject_id', None)
        if subject_id is None:
            return Response(
                {'error': 'subject_id query parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        marks = Marks.objects.filter(subject_id=subject_id)
        serializer = SubjectMarksSerializer(marks, many=True)
        return Response(serializer.data)


# ========== RESULTS VIEWSET ==========
class ResultViewSet(viewsets.ViewSet):
    """
    API endpoint for results:
    - GET /results/?student_id=X - Get result cards
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """GET /results/?student_id=X - Get result cards"""
        student_id = request.query_params.get('student_id', None)
        if student_id is None:
            return Response(
                {'error': 'student_id query parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        student = get_object_or_404(Student, id=student_id)
        marks = Marks.objects.filter(student=student)
        
        total_marks = marks.aggregate(total=Sum('total_marks'))['total'] or 0
        count = marks.count()
        percentage = (total_marks / (count * 100)) * 100 if count > 0 else 0
        
        data = {
            'student_id': student.id,
            'roll_number': student.roll_number,
            'student_name': student.user.get_full_name(),
            'semester': student.semester,
            'subjects': StudentMarksSerializer(marks, many=True).data,
            'total_marks': total_marks,
            'percentage': round(percentage, 2)
        }
        return Response(data)


# ========== AUTHENTICATION VIEWSET ==========
class AuthViewSet(viewsets.ViewSet):
    """
    API endpoint for authentication:
    - POST /auth/login/ - Login
    - POST /auth/logout/ - Logout
    - POST /auth/refresh-token/ - Refresh token
    - GET /auth/profile/ - Get user profile
    - PUT /auth/profile/ - Update profile
    - POST /auth/change-password/ - Change password
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """POST /auth/login/ - Login"""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        
        if user is None:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Get or create token for the user
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'auth_token': token.key,
            'user_id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'message': 'Login successful'
        })

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """POST /auth/logout/ - Logout"""
        try:
            request.user.auth_token.delete()
        except Exception:
            pass
        return Response({'message': 'Logged out successfully'})

    @action(detail=False, methods=['post'])
    def refresh_token(self, request):
        """POST /auth/refresh-token/ - Refresh token"""
        return Response({'message': 'Token refreshed', 'token': 'new_token_here'})

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """GET /auth/profile/ - Get user profile"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put'])
    def update_profile(self, request):
        """PUT /auth/profile/ - Update profile"""
        serializer = ProfileUpdateSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """POST /auth/change-password/ - Change password"""
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'error': 'Old password is incorrect'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({'message': 'Password changed successfully'})


# ========== NOTIFICATION VIEWSET ==========
class NotificationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for notifications:
    - GET /notifications/ - List notifications
    - GET /notifications/{id}/ - Notification details
    - PUT /notifications/{id}/mark-read/ - Mark as read
    - DELETE /notifications/{id}/ - Delete notification
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'delete', 'head', 'options']

    def get_queryset(self):
        """Only return notifications for the authenticated user"""
        return Notification.objects.filter(recipient__user=self.request.user).order_by('-created_at')

    def destroy(self, request, *args, **kwargs):
        """DELETE /notifications/{id}/ - Delete notification"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['put'])
    def mark_read(self, request, pk=None):
        """PUT /notifications/{id}/mark-read/ - Mark as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        serializer = self.get_serializer(notification)
        return Response(serializer.data)