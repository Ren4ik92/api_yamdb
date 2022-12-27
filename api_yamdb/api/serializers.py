from time import timezone

from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from reviews.models import Genre, Category, Title, Review, Comment
from users.models import User


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')


class NotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True)
    confirmation_code = serializers.CharField(
        required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    score = serializers.IntegerField(max_value=10, min_value=1)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        author = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже написали ревью к этому произведению.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="slug", many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )

    class Meta:
        fields = "__all__"
        model = Title


class TitlesSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField()
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category"
        )

    def validate_year(self, value):
        year_today = timezone.date.today().year
        if value > year_today:
            raise serializers.ValidationError(
                "Год создания произведения указан неверно!"
            )
        elif value < (year_today - 200):
            raise serializers.ValidationError(
                "Год создания произведения указан неверно!"
            )
        return value


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(
        validators=(UnicodeUsernameValidator(),),
        max_length=150
    )

    email = serializers.EmailField(max_length=254)

    def validate_username(self, username):
        if username.lower() == 'me':
            raise serializers.ValidationError('Недопустимое имя пользователя.')
        return username

    def validate_username(self, username):
        if username.lower() == 'me':
            raise serializers.ValidationError('Недопустимое имя пользователя.')
        user = User.objects.filter(username=username).first()
        if user and user.email != self.initial_data.get('email'):
            raise serializers.ValidationError('Данный username занят.')
        return username

    def validate_email(self, email):
        user = User.objects.filter(email=email).first()
        if user and user.username != self.initial_data.get('username'):
            raise serializers.ValidationError('Данный email уже используется.')
        return email
