from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,)
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from .models import Post

# https://viblo.asia/p/advanced-django-rest-framework-3P0lPkebZox
# Định nghĩa model cần serialize và các trường. ở đây mình để là all.
# Có rất nhiều API class mà rest đã viết sẵn. ở đây mình chỉ dùng 2 class để thao tác CRUD với database.
class PostListSerializer(serializers.ModelSerializer):
    # class Meta:
    #     model = Post
    #     #fields = '__all__'
    #     # ko dùng đến updated và created
    #     fields = ('title', 'content', 'draft', 'read_time',)
    #     # định nghĩa trường chỉ cho phép đọc
    #     read_only_fields = ('draft', 'read_time')

    # khai báo trường custom
    created_formated = serializers.SerializerMethodField(read_only=True)
    # hàm này để get dữ liệu cho trường created_formated
    def get_created_formated(seft,post):
        # return dd-mm-yyyy format
        return post.created.strftime("%d-%m-%Y")

    # Validate Field Title
    def validate_title(self, value):
        """
        Kiểm tra trong tiêu đề có từ django hay không. không có sẽ báo lỗi.
        """
        if 'django' not in value.lower():
            raise serializers.ValidationError("Blog post is not about Django")
        return value

    # Validate Object
    # Trong trường hợp ta muốn validate trên nhiều field cùng lúc. ta có thể dùng hàm validate trong serializer

    start = serializers.DateTimeField()
    finish = serializers.DateTimeField()
    def validate(self, data):
        """
        Kiểm tra nếu start lớn hơn stop.
        """
        if data['start'] > data['finish']:
            raise serializers.ValidationError("finish must occur after start")
        return data

    class Meta:
        model = Post
        fields = ('title', 'content', 'draft', 'read_time', 'created_formated')
        read_only_fields = ('draft', 'read_time')


    # API get detail, update, delete
class PostDetailUpdateAPIView(viewsets.GenericViewSet,  RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    lookup_field = 'id'
    # permission_classes = [IsAuthenticated]


# API get list and create
class PostListCreateAPIView(viewsets.GenericViewSet, ListCreateAPIView):
    serializer_class = PostListSerializer
    queryset = Post.objects.all()