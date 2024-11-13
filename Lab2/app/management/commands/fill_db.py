import random

from django.core.management.base import BaseCommand
from minio import Minio

from ...models import *
from .utils import random_date, random_timedelta


def add_users():
    User.objects.create_user("user", "user@user.com", "1234", first_name="user", last_name="user")
    User.objects.create_superuser("root", "root@root.com", "1234", first_name="root", last_name="root")

    for i in range(1, 10):
        User.objects.create_user(f"user{i}", f"user{i}@user.com", "1234", first_name=f"user{i}", last_name=f"user{i}")
        User.objects.create_superuser(f"root{i}", f"root{i}@root.com", "1234", first_name=f"user{i}", last_name=f"user{i}")

    print("Пользователи созданы")


def add_items():
    Item.objects.create(
        name="Декларирование товаров",
        description="Декларация на товары - это документ, оформляемый на груз при перемещении его через таможенную границу. Содержит сведения о грузе и его таможенной стоимости, транспорте, осуществляющем доставку, условиях пoставки, отправителе.",
        price=3000,
        image="1.png"
    )

    Item.objects.create(
        name="Декларирование ценностей",
        description="Перемещение культурных ценностей физическими лицами через таможенную границу Перечень культурных ценностей, документов национальных архивных фондов и оригиналов архивных документов, подлежащих контролю при перемещении через таможенную границу Российской Федерации.",
        price=100000,
        image="2.png"
    )

    Item.objects.create(
        name="Декларирование валют",
        description="Со 2 марта 2022 года временно запрещено вывозить валюту свыше 10 тыс. долл. США. Соответствующий Указ Президента РФ опубликован 1 марта 2022 года. Согласно документу со 2 марта 2022 года запрещено вывозить из РФ наличную иностранную валюту и денежные инструменты в иностранной валюте в сумме.",
        price=2000,
        image="3.png"
    )

    Item.objects.create(
        name="Декларирование транспортных средств",
        description="Согласно ст. 260 ТК ЕАЭС транспортные средства для личного пользования (за исключением ТС, зарегистрированных в странах ЕАЭС), перемещаемые через таможенную границу ЕАЭС любым способом, для целей выпуска в свободное обращение.",
        price=3000,
        image="4.png"
    )

    Item.objects.create(
        name="Декларирование медицинских товаров",
        description="Декларирование медицинских средств – это комплекс мероприятий, направленных на подтверждение безопасности препаратов, а также их соответствия требованиям утвержденных стандартов качества.",
        price=1200,
        image="5.png"
    )

    Item.objects.create(
        name="Декларирование документов",
        description="Декларирование документов — официальный государственный документ, содержащий основополагающие принципы внешней или внутренней политики государства, основы деятельности международных организаций или выражающий их позицию по какому-либо вопрос.",
        price=4500,
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

    if declaration.status in [3, 4]:
        declaration.date_complete = random_date()
        declaration.date_formation = declaration.date_complete - random_timedelta()
        declaration.date_created = declaration.date_formation - random_timedelta()
    else:
        declaration.date_formation = random_date()
        declaration.date_created = declaration.date_formation - random_timedelta()

    declaration.owner = owner
    declaration.moderator = random.choice(moderators)

    declaration.date = random_date()

    for item in random.sample(list(items), 3):
        item = ItemDeclaration(
            declaration=declaration,
            item=item,
            value=random.randint(1, 10)
        )
        item.save()

    declaration.save()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        add_users()
        add_items()
        add_declarations()
