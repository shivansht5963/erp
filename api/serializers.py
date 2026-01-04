# File: api/serializers.py
from rest_framework import serializers
from accounts.models import CustomUser
from faculty.models import Department, Course, Subject, Class, Teacher
from attendance.models import Attendance, AttendanceReport
from fees.models import FeePayment
from exams.models import Marks
from notifications.models import Notification
from students.models import Student, StudentInfo

# ========== USER SERIALIZERS ==========
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'dob', 'role']

# ========== STUDENT SERIALIZERS ==========
class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = Student
        fields = [
            'id', 'roll_number', 'course', 'course_name', 'class_enrolled',
            'semester', 'dob', 'contact_number', 'address', 'category', 'user'
        ]

class StudentDetailSerializer(StudentSerializer):
    class Meta:
        model = Student
        fields = StudentSerializer.Meta.fields

# ========== FACULTY SERIALIZERS ==========
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']

class CourseSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    class Meta:
        model = Course
        fields = ['id', 'name', 'department', 'department_name']

class ClassSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    class Meta:
        model = Class
        fields = ['id', 'department', 'department_name', 'section', 'semester']

class SubjectSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    class Meta:
        model = Subject
        fields = ['id', 'name', 'code', 'semester', 'department', 'department_name', 
                  'course', 'course_name', 'teacher', 'teacher_name']

class TeacherSubjectSerializer(serializers.ModelSerializer):
    subject_code = serializers.CharField(source='code', read_only=True)
    subject_name = serializers.CharField(source='name', read_only=True)
    class Meta:
        model = Subject
        fields = ['id', 'subject_code', 'subject_name', 'semester']

class TeacherDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    departments = DepartmentSerializer(many=True, read_only=True)
    subjects = TeacherSubjectSerializer(source='subject_set', many=True, read_only=True)
    class Meta:
        model = Teacher
        fields = ['id', 'user', 'departments', 'qualification', 'contact_number', 'join_date', 'subjects']

# ========== ATTENDANCE SERIALIZERS ==========
class AttendanceSerializer(serializers.ModelSerializer):
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    subject_code = serializers.CharField(source='subject.code', read_only=True)
    teacher_name = serializers.CharField(source='marked_by.user.get_full_name', read_only=True)
    class Meta:
        model = Attendance
        fields = ['id', 'student', 'student_roll', 'subject', 'subject_code', 
                  'date', 'status', 'classes_held', 'classes_attended', 'marked_by', 'teacher_name']

class AttendanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['student', 'subject', 'date', 'status', 'classes_held', 'classes_attended', 'marked_by']

class StudentAttendanceSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class Meta:
        model = Attendance
        fields = ['id', 'subject', 'subject_name', 'date', 'status', 'classes_attended', 'classes_held']

# ========== FEES SERIALIZERS ==========
class FeePaymentSerializer(serializers.ModelSerializer):
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    class Meta:
        model = FeePayment
        fields = ['id', 'student', 'student_roll', 'student_name', 'amount', 
                  'payment_date', 'payment_method', 'transaction_id', 'status']

class StudentFeeStatusSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    roll_number = serializers.CharField()
    total_due = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_paid = serializers.DecimalField(max_digits=10, decimal_places=2)
    status = serializers.CharField()

class StudentFeePaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeePayment
        fields = ['id', 'amount', 'payment_date', 'payment_method', 'transaction_id', 'status']

# ========== MARKS SERIALIZERS ==========
class MarksSerializer(serializers.ModelSerializer):
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    subject_code = serializers.CharField(source='subject.code', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class Meta:
        model = Marks
        fields = ['id', 'student', 'student_roll', 'subject', 'subject_code', 
                  'subject_name', 'internal_marks', 'semester_marks', 'total_marks']

class StudentMarksSerializer(serializers.ModelSerializer):
    subject_code = serializers.CharField(source='subject.code', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class Meta:
        model = Marks
        fields = ['id', 'subject', 'subject_code', 'subject_name', 
                  'internal_marks', 'semester_marks', 'total_marks']

class SubjectMarksSerializer(serializers.ModelSerializer):
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    class Meta:
        model = Marks
        fields = ['id', 'student', 'student_roll', 'student_name', 
                  'internal_marks', 'semester_marks', 'total_marks']

class ResultCardSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    roll_number = serializers.CharField()
    student_name = serializers.CharField()
    semester = serializers.IntegerField()
    subjects = StudentMarksSerializer(many=True)
    total_marks = serializers.DecimalField(max_digits=10, decimal_places=2)
    percentage = serializers.DecimalField(max_digits=5, decimal_places=2)

# ========== AUTHENTICATION SERIALIZERS ==========
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        """Convert email to username since CustomUser uses email as username field"""
        data['username'] = data['email']
        return data

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone', 'address', 'dob']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

# ========== NOTIFICATION SERIALIZERS ==========
class NotificationSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)
    recipient_roll = serializers.CharField(source='recipient.roll_number', read_only=True)
    class Meta:
        model = Notification
        fields = ['id', 'sender', 'sender_name', 'recipient', 'recipient_roll', 'title', 'message', 'is_read', 'created_at']

class NotificationDetailSerializer(NotificationSerializer):
    class Meta:
        model = Notification
        fields = NotificationSerializer.Meta.fields

class TeacherSendNotificationSerializer(serializers.Serializer):
    target_type = serializers.ChoiceField(choices=[('class', 'Class'), ('student', 'Student')])
    target_id = serializers.IntegerField() 
    title = serializers.CharField(max_length=255)
    message = serializers.CharField()

    def validate(self, data):
        t_type = data.get('target_type')
        t_id = data.get('target_id')
        if t_type == 'class' and not Class.objects.filter(id=t_id).exists():
            raise serializers.ValidationError({"target_id": "Class ID does not exist."})
        if t_type == 'student' and not Student.objects.filter(id=t_id).exists():
            raise serializers.ValidationError({"target_id": "Student ID does not exist."})
        return data