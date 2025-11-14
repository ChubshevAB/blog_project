from django.db import models
from django.core.exceptions import ValidationError
from datetime import date


def validate_title_words(value):
    """
    Валидатор запрещенных слов в заголовке.
    """
    forbidden_words = ["ерунда", "глупость", "чепуха"]
    for word in forbidden_words:
        if word in value.lower():
            raise ValidationError(f'Заголовок содержит запрещенное слово: "{word}"')


class Post(models.Model):
    title = models.CharField(
        max_length=200, validators=[validate_title_words], verbose_name="Заголовок"
    )
    content = models.TextField(verbose_name="Содержание")
    image = models.ImageField(
        upload_to="posts/images/", blank=True, null=True, verbose_name="Изображение"
    )
    author = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.title

    def clean(self):
        """
        Валидация возраста автора при сохранении.
        """
        super().clean()
        if self.author and self.author.birth_date:
            today = date.today()
            age = (
                today.year
                - self.author.birth_date.year
                - (
                    (today.month, today.day)
                    < (self.author.birth_date.month, self.author.birth_date.day)
                )
            )
            if age < 18:
                raise ValidationError({"author": "Автор должен быть старше 18 лет."})

    def save(self, *args, **kwargs):
        """
        Переопределяем save для вызова clean().
        """
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments", verbose_name="Пост"
    )
    author = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    text = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f'Комментарий от {self.author} к "{self.post}"'

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
