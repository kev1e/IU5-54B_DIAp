from django.conf import settings
from django.core.management.base import BaseCommand
from minio import Minio

from .utils import *
from app.models import *


def add_users():
    User.objects.create_user("user", "user@user.com", "1234", first_name="user", last_name="user")
    User.objects.create_superuser("root", "root@root.com", "1234", first_name="root", last_name="root")

    for i in range(1, 10):
        User.objects.create_user(f"user{i}", f"user{i}@user.com", "1234", first_name=f"user{i}", last_name=f"user{i}")
        User.objects.create_superuser(f"root{i}", f"root{i}@root.com", "1234", first_name=f"user{i}", last_name=f"user{i}")


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

    client = Minio(settings.MINIO_ENDPOINT,
                   settings.MINIO_ACCESS_KEY,
                   settings.MINIO_SECRET_KEY,
                   secure=settings.MINIO_USE_HTTPS)

    for i in range(1, 7):
        client.fput_object(settings.MINIO_MEDIA_FILES_BUCKET, f'{i}.png', f"app/static/images/{i}.png")

    client.fput_object(settings.MINIO_MEDIA_FILES_BUCKET, 'default.png', "app/static/images/default.png")


def add_declarations():
    users = User.objects.filter(is_staff=False)
    moderators = User.objects.filter(is_staff=True)
    items = Item.objects.all()

    for _ in range(30):
        status = random.randint(2, 5)
        owner = random.choice(users)
        add_declaration(status, items, owner, moderators)

    add_declaration(1, items, users[0], moderators)
    add_declaration(2, items, users[0], moderators)
    add_declaration(3, items, users[0], moderators)
    add_declaration(4, items, users[0], moderators)
    add_declaration(5, items, users[0], moderators)


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
        declaration.weight = random.randint(10, 100)

    declaration.date = random_date()

    declaration.owner = owner

    for item in random.sample(list(items), 3):
        item = ItemDeclaration(
            declaration=declaration,
            item=item,
            count=random.randint(1, 10)
        )
        item.save()

    declaration.save()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        add_users()
        add_items()
        add_declarations()
