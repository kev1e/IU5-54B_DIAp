from django.shortcuts import render

products = [
    {
        "id": 1,
        "name": "Декларирование товаров",
        "description": "Декларация на товары - это документ, оформляемый на груз при перемещении его через таможенную границу. Содержит сведения о грузе и его таможенной стоимости, транспорте, осуществляющем доставку, условиях пoставки, отправителе.",
        "price": 3000,
        "image": "http://localhost:9000/images/1.png"
    },
    {
        "id": 2,
        "name": "Декларирование ценностей",
        "description": "Перемещение культурных ценностей физическими лицами через таможенную границу Перечень культурных ценностей, документов национальных архивных фондов и оригиналов архивных документов, подлежащих контролю при перемещении через таможенную границу Российской Федерации.",
        "price": 100000,
        "image": "http://localhost:9000/images/2.png"
    },
    {
        "id": 3,
        "name": "Декларирование валют",
        "description": "Со 2 марта 2022 года временно запрещено вывозить валюту свыше 10 тыс. долл. США. Соответствующий Указ Президента РФ опубликован 1 марта 2022 года. Согласно документу со 2 марта 2022 года запрещено вывозить из РФ наличную иностранную валюту и денежные инструменты в иностранной валюте в сумме.",
        "price": 2000,
        "image": "http://localhost:9000/images/3.png"
    },
    {
        "id": 4,
        "name": "Декларирование транспортных средств",
        "description": "Согласно ст. 260 ТК ЕАЭС транспортные средства для личного пользования (за исключением ТС, зарегистрированных в странах ЕАЭС), перемещаемые через таможенную границу ЕАЭС любым способом, для целей выпуска в свободное обращение.",
        "price": 3000,
        "image": "http://localhost:9000/images/4.png"
    },
    {
        "id": 5,
        "name": "Декларирование медицинских товаров",
        "description": "Декларирование медицинских средств – это комплекс мероприятий, направленных на подтверждение безопасности препаратов, а также их соответствия требованиям утвержденных стандартов качества.",
        "price": 3000,
        "image": "http://localhost:9000/images/5.png"
    },
    {
        "id": 6,
        "name": "Декларирование документов",
        "description": "Декларирование документов — официальный государственный документ, содержащий основополагающие принципы внешней или внутренней политики государства, основы деятельности международных организаций или выражающий их позицию по какому-либо вопрос.",
        "price": 4500,
        "image": "http://localhost:9000/images/6.png"
    }
]

draft_declaration = {
    "id": 123,
    "status": "Черновик",
    "date_created": "12 сентября 2024г",
    "date": "15 октября 2024г",
    "products": [
        {
            "id": 1,
            "value": 2
        },
        {
            "id": 2,
            "value": 4
        },
        {
            "id": 3,
            "value": 1
        }
    ]
}


def getProductById(product_id):
    for product in products:
        if product["id"] == product_id:
            return product


def getProducts():
    return products


def searchProducts(product_name):
    res = []

    for product in products:
        if product_name.lower() in product["name"].lower():
            res.append(product)

    return res


def getDraftDeclaration():
    return draft_declaration


def getDeclarationById(declaration_id):
    return draft_declaration


def index(request):
    product_name = request.GET.get("product_name", "")
    products = searchProducts(product_name) if product_name else getProducts()
    draft_declaration = getDraftDeclaration()

    context = {
        "products": products,
        "product_name": product_name,
        "products_count": len(draft_declaration["products"]),
        "draft_declaration": draft_declaration
    }

    return render(request, "products_page.html", context)


def product(request, product_id):
    context = {
        "id": product_id,
        "product": getProductById(product_id),
    }

    return render(request, "product_page.html", context)


def declaration(request, declaration_id):
    declaration = getDeclarationById(declaration_id)
    products = [
        {**getProductById(product["id"]), "value": product["value"]}
        for product in declaration["products"]
    ]

    context = {
        "declaration": declaration,
        "products": products
    }

    return render(request, "declaration_page.html", context)
