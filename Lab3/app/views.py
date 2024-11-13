from django.contrib.auth import authenticate
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .management.commands.fill_db import calc
from .serializers import *


def get_draft_declaration():
    return Declaration.objects.filter(status=1).first()


def get_user():
    return User.objects.filter(is_superuser=False).first()


def get_moderator():
    return User.objects.filter(is_superuser=True).first()


@api_view(["GET"])
def search_items(request):
    item_name = request.GET.get("item_name", "")

    items = Item.objects.filter(status=1)

    if item_name:
        items = items.filter(name__icontains=item_name)

    serializer = ItemsSerializer(items, many=True)
    
    draft_declaration = get_draft_declaration()

    resp = {
        "items": serializer.data,
        "items_count": ItemDeclaration.objects.filter(declaration=draft_declaration).count() if draft_declaration else None,
        "draft_declaration": draft_declaration.pk if draft_declaration else None
    }

    return Response(resp)


@api_view(["GET"])
def get_item_by_id(request, item_id):
    if not Item.objects.filter(pk=item_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = Item.objects.get(pk=item_id)
    serializer = ItemSerializer(item)

    return Response(serializer.data)


@api_view(["PUT"])
def update_item(request, item_id):
    if not Item.objects.filter(pk=item_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = Item.objects.get(pk=item_id)

    serializer = ItemSerializer(item, data=request.data, partial=True)

    if serializer.is_valid(raise_exception=True):
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
def create_item(request):
    serializer = ItemSerializer(data=request.data, partial=False)

    serializer.is_valid(raise_exception=True)

    Item.objects.create(**serializer.validated_data)

    items = Item.objects.filter(status=1)
    serializer = ItemSerializer(items, many=True)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_item(request, item_id):
    if not Item.objects.filter(pk=item_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = Item.objects.get(pk=item_id)
    item.status = 2
    item.save()

    items = Item.objects.filter(status=1)
    serializer = ItemSerializer(items, many=True)

    return Response(serializer.data)


@api_view(["POST"])
def add_item_to_declaration(request, item_id):
    if not Item.objects.filter(pk=item_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = Item.objects.get(pk=item_id)

    draft_declaration = get_draft_declaration()

    if draft_declaration is None:
        draft_declaration = Declaration.objects.create()
        draft_declaration.owner = get_user()
        draft_declaration.date_created = timezone.now()
        draft_declaration.save()

    if ItemDeclaration.objects.filter(declaration=draft_declaration, item=item).exists():
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    item = ItemDeclaration.objects.create()
    item.declaration = draft_declaration
    item.item = item
    item.save()

    serializer = DeclarationSerializer(draft_declaration)
    return Response(serializer.data["items"])


@api_view(["POST"])
def update_item_image(request, item_id):
    if not Item.objects.filter(pk=item_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = Item.objects.get(pk=item_id)

    image = request.data.get("image")
    if image is not None:
        item.image = image
        item.save()

    serializer = ItemSerializer(item)

    return Response(serializer.data)


@api_view(["GET"])
def search_declarations(request):
    status = int(request.GET.get("status", 0))
    date_formation_start = request.GET.get("date_formation_start")
    date_formation_end = request.GET.get("date_formation_end")

    declarations = Declaration.objects.exclude(status__in=[1, 5])

    if status > 0:
        declarations = declarations.filter(status=status)

    if date_formation_start and parse_datetime(date_formation_start):
        declarations = declarations.filter(date_formation__gte=parse_datetime(date_formation_start))

    if date_formation_end and parse_datetime(date_formation_end):
        declarations = declarations.filter(date_formation__lt=parse_datetime(date_formation_end))

    serializer = DeclarationsSerializer(declarations, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_declaration_by_id(request, declaration_id):
    if not Declaration.objects.filter(pk=declaration_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    declaration = Declaration.objects.get(pk=declaration_id)
    serializer = DeclarationSerializer(declaration, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_declaration(request, declaration_id):
    if not Declaration.objects.filter(pk=declaration_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    declaration = Declaration.objects.get(pk=declaration_id)
    serializer = DeclarationSerializer(declaration, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
def update_status_user(request, declaration_id):
    if not Declaration.objects.filter(pk=declaration_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    declaration = Declaration.objects.get(pk=declaration_id)

    if declaration.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    declaration.status = 2
    declaration.date_formation = timezone.now()
    declaration.save()

    serializer = DeclarationSerializer(declaration, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_status_admin(request, declaration_id):
    if not Declaration.objects.filter(pk=declaration_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = int(request.data["status"])

    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    declaration = Declaration.objects.get(pk=declaration_id)

    if declaration.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    if request_status == 3:
        declaration.weight = calc()

    declaration.date_complete = timezone.now()
    declaration.status = request_status
    declaration.moderator = get_moderator()
    declaration.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
def delete_declaration(request, declaration_id):
    if not Declaration.objects.filter(pk=declaration_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    declaration = Declaration.objects.get(pk=declaration_id)

    if declaration.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    declaration.status = 5
    declaration.save()

    serializer = DeclarationSerializer(declaration, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_item_from_declaration(request, declaration_id, item_id):
    if not ItemDeclaration.objects.filter(declaration_id=declaration_id, item_id=item_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = ItemDeclaration.objects.get(declaration_id=declaration_id, item_id=item_id)
    item.delete()

    items = ItemDeclaration.objects.filter(declaration_id=declaration_id)
    data = [ItemItemSerializer(item.item, context={"value": item.value}).data for item in items]

    return Response(data, status=status.HTTP_200_OK)


@api_view(["PUT"])
def update_item_in_declaration(request, declaration_id, item_id):
    if not ItemDeclaration.objects.filter(item_id=item_id, declaration_id=declaration_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = ItemDeclaration.objects.get(item_id=item_id, declaration_id=declaration_id)

    serializer = ItemDeclarationSerializer(item, data=request.data,  partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    user = serializer.save()

    serializer = UserSerializer(user)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def login(request):
    serializer = UserLoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(**serializer.data)
    if user is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    serializer = UserSerializer(user)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def logout(request):
    return Response(status=status.HTTP_200_OK)


@api_view(["PUT"])
def update_user(request, user_id):
    if not User.objects.filter(pk=user_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = User.objects.get(pk=user_id)
    serializer = UserSerializer(user, data=request.data, partial=True)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    serializer.save()

    return Response(serializer.data)