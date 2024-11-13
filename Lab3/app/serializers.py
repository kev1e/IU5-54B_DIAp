from rest_framework import serializers

from .models import *


class ItemsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, item):
        if item.image:
            return item.image.url.replace("minio", "localhost", 1)

        return "http://localhost:9000/images/default.png"

    class Meta:
        model = Item
        fields = ("id", "name", "status", "price", "image")


class ItemSerializer(ItemsSerializer):
    class Meta(ItemsSerializer.Meta):
        model = Item
        fields = ItemsSerializer.Meta.fields + ("description", )


class DeclarationsSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    moderator = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Declaration
        fields = "__all__"


class DeclarationSerializer(DeclarationsSerializer):
    items = serializers.SerializerMethodField()
            
    def get_items(self, declaration):
        items = ItemDeclaration.objects.filter(declaration=declaration)
        return [ItemItemSerializer(item.item, context={"value": item.value}).data for item in items]


class ItemItemSerializer(ItemSerializer):
    value = serializers.SerializerMethodField()

    def get_value(self, item):
        return self.context.get("value")

    class Meta(ItemSerializer.Meta):
        fields = "__all__"


class ItemDeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemDeclaration
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username')


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'username')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
