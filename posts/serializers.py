from rest_framework import serializers
from .models import Post, Comment
from users.models import CustomUser


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username"]


class CommentSerializer(serializers.ModelSerializer):
    author = UserShortSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "text", "author", "post", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class PostSerializer(serializers.ModelSerializer):
    author = UserShortSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "image",
            "author",
            "comments",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "content", "image"]

    def validate_image(self, value):
        """
        Валидация загружаемого изображения.
        """
        if value:
            # Проверка размера файла (максимум 5MB)
            max_size = 5 * 1024 * 1024  # 5MB
            if value.size > max_size:
                raise serializers.ValidationError(
                    "Размер изображения не должен превышать 5MB."
                )

            # Проверка типа файла
            valid_extensions = ["jpg", "jpeg", "png", "gif", "bmp", "webp"]
            extension = value.name.split(".")[-1].lower()
            if extension not in valid_extensions:
                raise serializers.ValidationError(
                    f"Неподдерживаемый формат изображения. Разрешены: {', '.join(valid_extensions)}"
                )

        return value

    def create(self, validated_data):
        """
        Создание поста с обработкой изображения.
        """
        # Django REST Framework автоматически обработает загрузку изображения
        # и сохранит его в MEDIA_ROOT/posts/images/
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Обновление поста с обработкой изображения.
        """
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)

        # Обработка обновления изображения
        if "image" in validated_data:
            # Если загружено новое изображение, удаляем старое (опционально)
            if instance.image:
                instance.image.delete(save=False)
            instance.image = validated_data["image"]

        instance.save()
        return instance
