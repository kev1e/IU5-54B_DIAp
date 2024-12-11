from django.contrib.auth.models import User
from django.db import connection
from django.shortcuts import render, redirect
from django.utils import timezone

from app.models import Item, Declaration, ItemDeclaration


def index(request):
    item_name = request.GET.get("item_name", "")
    items = Item.objects.filter(status=1)

    if item_name:
        items = items.filter(name__icontains=item_name)

    draft_declaration = get_draft_declaration()

    context = {
        "item_name": item_name,
        "items": items
    }

    if draft_declaration:
        context["items_count"] = len(draft_declaration.get_items())
        context["draft_declaration"] = draft_declaration

    return render(request, "items_page.html", context)


def add_item_to_draft_declaration(request, item_id):
    item_name = request.POST.get("item_name")
    redirect_url = f"/?item_name={item_name}" if item_name else "/"

    item = Item.objects.get(pk=item_id)

    draft_declaration = get_draft_declaration()

    if draft_declaration is None:
        draft_declaration = Declaration.objects.create()
        draft_declaration.owner = get_current_user()
        draft_declaration.date_created = timezone.now()
        draft_declaration.save()

    if ItemDeclaration.objects.filter(declaration=draft_declaration, item=item).exists():
        return redirect(redirect_url)

    item = ItemDeclaration(
        declaration=draft_declaration,
        item=item
    )
    item.save()

    return redirect(redirect_url)


def item_details(request, item_id):
    context = {
        "item": Item.objects.get(id=item_id)
    }

    return render(request, "item_page.html", context)


def delete_declaration(request, declaration_id):
    if not Declaration.objects.filter(pk=declaration_id).exists():
        return redirect("/")

    with connection.cursor() as cursor:
        cursor.execute("UPDATE declarations SET status=5 WHERE id = %s", [declaration_id])

    return redirect("/")


def declaration(request, declaration_id):
    if not Declaration.objects.filter(pk=declaration_id).exists():
        return redirect("/")

    declaration = Declaration.objects.get(id=declaration_id)
    if declaration.status == 5:
        return redirect("/")

    context = {
        "declaration": declaration,
    }

    return render(request, "declaration_page.html", context)


def get_draft_declaration():
    return Declaration.objects.filter(status=1).first()


def get_current_user():
    return User.objects.filter(is_superuser=False).first()