from django.core.management.base import BaseCommand
from minio import Minio

from ...models import *
from .utils import *


def add_users():
    User.objects.create_user("user", "user@user.com", "1234", first_name="user", last_name="user")
    User.objects.create_superuser("root", "root@root.com", "1234", first_name="root", last_name="root")

    for i in range(1, 10):
        User.objects.create_user(f"user{i}", f"user{i}@user.com", "1234", first_name=f"user{i}", last_name=f"user{i}")
        User.objects.create_superuser(f"root{i}", f"root{i}@root.com", "1234", first_name=f"user{i}", last_name=f"user{i}")

    print("Пользователи созданы")


def add_items():
    Item.objects.create(
        name="Молоко",
        description="Один из самых полезных для человека вещей. Оно богато белком, витаминами A и D, кальцием. Недаром с давних пор люди стали не только покупать молоко оптом, но и придумывать рецепты изготовления из него разных вещей.",
        price=100,
        image="1.png"
    )

    Item.objects.create(
        name="Творог",
        description="Он производится из пастеризованного молока, в которое добавляют закваску, после чего через некоторое время из образовавшейся зернистой массы удаляют сыворотку. Творог необычайно богат белком, витаминами группы В и незаменим в диетическом питании.",
        price=80,
        image="2.png"
    )

    Item.objects.create(
        name="Сливки",
        description="Изготавливаются с древнейших времен и представляют собой верхний, самый жирный слой отстоявшегося молока. Они очень калорийны и питательны, насыщены витаминами А, D и Е.",
        price=200,
        image="3.png"
    )

    Item.objects.create(
        name="Сметана",
        description="Получается из сливок путем добавления специальной закваски. Особенно популярна она в кухне славянских народов. Сметана богата белком и жирами, содержит витамины А, Е, В12.",
        price=50,
        image="4.png"
    )

    Item.objects.create(
        name="Кефир",
        description="Производится с помощью особого кефирного грибка. Очень полезен для здоровья, так же как и другие кисломолочные напитки (простокваша, ряженка, варенец, ацидофилин, мацони и т. д.).",
        price=120,
        image="5.png"
    )

    Item.objects.create(
        name="Сыр",
        description="Секрет его изготовления – закваска, содержащая молочнокислые бактерии или особые ферменты. Он очень полезен, богат белком, жиром, витаминами всех групп и кальцием.",
        price=350,
        image="6.png"
    )

    client = Minio("minio:9000", "minio", "minio123", secure=False)
    client.fput_object('images', '1.png', "app/static/images/1.png")
    client.fput_object('images', '2.png', "app/static/images/2.png")
    client.fput_object('images', '3.png', "app/static/images/3.png")
    client.fput_object('images', '4.png', "app/static/images/4.png")
    client.fput_object('images', '5.png', "app/static/images/5.png")
    client.fput_object('images', '6.png', "app/static/images/6.png")
    client.fput_object('images', 'default.png', "app/static/images/default.png")

    print("Услуги добавлены")


def add_declarations():
    users = User.objects.filter(is_staff=False)
    moderators = User.objects.filter(is_staff=True)

    if len(users) == 0 or len(moderators) == 0:
        print("Заявки не могут быть добавлены. Сначала добавьте пользователей с помощью команды add_users")
        return

    items = Item.objects.all()

    for _ in range(30):
        status = random.randint(2, 5)
        owner = random.choice(users)
        add_declaration(status, items, owner, moderators)

    add_declaration(1, items, users[0], moderators)
    add_declaration(2, items, users[0], moderators)

    print("Заявки добавлены")


def add_declaration(status, items, owner, moderators):
    declaration = Declaration.objects.create()
    declaration.status = status

    if status in [3, 4]:
        declaration.moderator = random.choice(moderators)
        declaration.date_complete = random_date()
        declaration.date_formation = declaration.date_complete - random_timedelta()
        declaration.date_created = declaration.date_formation - random_timedelta()
    else:
        declaration.date_formation = random_date()
        declaration.date_created = declaration.date_formation - random_timedelta()

    if status == 3:
        declaration.weight = calc()

    declaration.date = random_date()

    declaration.owner = owner

    for item in random.sample(list(items), 3):
        item = ItemDeclaration(
            declaration=declaration,
            item=item,
            value=random.randint(1, 10)
        )
        item.save()

    declaration.save()


def calc():
    return random.randint(10, 100)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        add_users()
        add_items()
        add_declarations()
