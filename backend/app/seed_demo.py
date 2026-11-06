from datetime import UTC, datetime, timedelta

from sqlalchemy import select

from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.address import Address
from app.models.category import Category
from app.models.delivery import Delivery, DeliveryTracking
from app.models.enums import DeliveryStatus, OrderStatus, UserRole
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.restaurant import Restaurant
from app.models.user import User

DEMO_PASSWORD = "123456"

RESTAURANTS = [
    {
        "owner_email": "owner@demo.com",
        "owner_name": "Açaiteria Combina Açaí",
        "name": "Combina Açaí",
        "address": "Rua Tenente Manoel Barbosa, 46, Bairro da Cruz, Lorena/SP",
        "latitude": -22.7406991,
        "longitude": -45.1041195,
        "description": "Açaí cremoso, gelatos artesanais, bowls e vitaminas preparados em Lorena/SP.",
        "delivery_fee": 4.5,
        "avg_delivery_time_min": 25,
        "categories": [
            "Açaí 70% Tradicional",
            "Açaí Tradicional Premium 90%",
            "Açaí Grego",
            "Açaí Zero",
            "Combo Box 1l",
            "Gelato Pitaya",
            "Gelato Cappuccino",
        ],
        "products": [
            (
                "70% Tradicional 330ml",
                13.0,
                "Açaí tradicional com aquele gostinho de infância, livre de cristais de gelo.",
                "Açaí 70% Tradicional",
            ),
            (
                "70% Tradicional 440ml",
                15.0,
                "Açaí tradicional com aquele gostinho de infância, livre de cristais de gelo.",
                "Açaí 70% Tradicional",
            ),
            (
                "70% Tradicional 550ml",
                17.0,
                "Açaí tradicional com aquele gostinho de infância, livre de cristais de gelo.",
                "Açaí 70% Tradicional",
            ),
            (
                "70% Tradicional 770ml",
                21.0,
                "Atenção: indicado 2x de complemento. Açaí tradicional livre de cristais de gelo.",
                "Açaí 70% Tradicional",
            ),
            ("70% Açaí Tradicional Box 1l", 27.9, "Box de 1l tradicional 70% puro.", "Açaí 70% Tradicional"),
            (
                "90% Premium Tradicional 330ml",
                15.0,
                "Açaí premium orgânico, consistente e livre de cristais de gelo.",
                "Açaí Tradicional Premium 90%",
            ),
            (
                "90% Premium Tradicional 440ml",
                17.0,
                "Açaí premium orgânico, consistente e livre de cristais de gelo.",
                "Açaí Tradicional Premium 90%",
            ),
            (
                "90% Premium Tradicional 550ml",
                19.0,
                "Açaí premium orgânico, consistente e livre de cristais de gelo.",
                "Açaí Tradicional Premium 90%",
            ),
            (
                "90% Premium Tradicional 770ml",
                23.9,
                "Atenção: indicado colocar 2x de complemento para ir mais recheado.",
                "Açaí Tradicional Premium 90%",
            ),
            (
                "90% Premium Açaí Tradicional Box 1l",
                36.0,
                "Box de 1l tradicional 90% Premium puro.",
                "Açaí Tradicional Premium 90%",
            ),
            ("Açaí Grego Copo 330ml", 15.0, "Açaí com iogurte grego puro.", "Açaí Grego"),
            ("Açaí Grego Copo 440ml", 17.0, "Açaí com iogurte grego puro.", "Açaí Grego"),
            ("Açaí Grego Copo 550ml", 19.0, "Açaí com iogurte grego puro.", "Açaí Grego"),
            ("Açaí Grego Copo 770ml", 23.9, "Atenção: indicado 2x de complemento para ir bem recheado.", "Açaí Grego"),
            ("Açaí Grego Box 1l", 36.0, "Box de 1l grego puro (complementos à parte).", "Açaí Grego"),
            ("Açaí Zero Copo 330ml", 19.0, "Açaí 100% orgânico sem açúcar.", "Açaí Zero"),
            ("Açaí Zero Copo 440ml", 22.0, "Açaí 100% orgânico sem açúcar.", "Açaí Zero"),
            ("Açaí Zero Copo 550ml", 25.0, "Açaí 100% orgânico sem açúcar.", "Açaí Zero"),
            ("Açaí Zero Copo 770ml", 29.0, "Açaí 100% orgânico sem açúcar.", "Açaí Zero"),
            ("Açaí Zero Box 1l", 45.0, "Box de 1l puro, sem açúcar.", "Açaí Zero"),
            ("90% Box Tradicional + 4 Complementos", 41.9, "Açaí 90% com 4 complementos à escolha.", "Combo Box 1l"),
            ("Box Grego + 4 Complementos", 41.9, "Box grego com 4 complementos à escolha.", "Combo Box 1l"),
            ("Box 70% Tradicional + 4 Complementos", 37.9, "Box 70% com 4 complementos à escolha.", "Combo Box 1l"),
            ("Gelato Pitaya Copo 330ml", 16.0, "Gelato à base de água e pitaya orgânica.", "Gelato Pitaya"),
            ("Gelato Pitaya Copo 440ml", 19.0, "Gelato refrescante de pitaya, à base de água.", "Gelato Pitaya"),
            ("Pitaya Copo 550ml", 21.0, "Gelato de pitaya à base de água e fruta orgânica.", "Gelato Pitaya"),
            ("Pitaya Copo 770ml", 26.9, "Gelato de pitaya; recomendado o dobro de complemento.", "Gelato Pitaya"),
            ("Pitaya Box 1l", 38.0, "Box de 1l puro.", "Gelato Pitaya"),
            ("Gelato Cappuccino Copo 330ml", 16.0, "Gelato à base de café e leite.", "Gelato Cappuccino"),
            ("Gelato Cappuccino Copo 440ml", 19.0, "Gelato à base de café e leite.", "Gelato Cappuccino"),
            ("Cappuccino Copo 550ml", 21.0, "Gelato à base de café e leite.", "Gelato Cappuccino"),
            (
                "Cappuccino Copo 770ml",
                26.9,
                "Gelato de café; no copo de 770ml recomenda-se o dobro de complemento.",
                "Gelato Cappuccino",
            ),
            ("Cappuccino Box 1l", 38.0, "Box de 1l puro.", "Gelato Cappuccino"),
        ],
    },
    {
        "owner_email": "massa@demo.com",
        "owner_name": "Massa Express",
        "name": "Massa Express",
        "address": "Rua Comendador Custodio Vieira, 120, Centro, Lorena/SP",
        "latitude": -22.7305,
        "longitude": -45.1235,
        "description": "Massas artesanais, lanches e pratos executivos para o dia a dia.",
        "delivery_fee": 7.5,
        "avg_delivery_time_min": 35,
        "products": [
            ("Lasanha Bolonhesa", 34.9, "Porcao individual com molho artesanal e queijo gratinado."),
            ("Spaghetti ao Molho Branco", 29.9, "Serve 1 pessoa, com parmesao e bacon."),
            ("Hamburguer Artesanal", 27.5, "Pao brioche, blend 180g, queijo cheddar e fritas."),
            ("Fettuccine Alfredo", 32.9, "Massa fresca com creme de leite e parmesao."),
            ("Nhoque ao Sugo", 28.9, "Nhoque de batata com molho de tomate e manjericao."),
        ],
    },
    {
        "owner_email": "burger@demo.com",
        "owner_name": "Burger House",
        "name": "Burger House",
        "address": "Avenida Salesopolis, 900, Vila Nunes, Lorena/SP",
        "latitude": -22.736,
        "longitude": -45.118,
        "description": "Hamburgueres artesanais, batatas rústicas e milkshakes.",
        "delivery_fee": 4.9,
        "avg_delivery_time_min": 25,
        "products": [
            ("Classic Burger", 24.9, "Blend 160g, queijo prato, alface, tomate e molho da casa."),
            ("Bacon Smash", 29.9, "Dois discos de 90g, cheddar, bacon crocante e cebola caramelizada."),
            ("Batata Rustica", 16.9, "Porcao com paprika e maionese temperada."),
            ("Milkshake de Chocolate", 18.9, "500ml com calda de chocolate e chantilly."),
        ],
    },
    {
        "owner_email": "mineiro@demo.com",
        "owner_name": "Sabor Mineiro",
        "name": "Sabor Mineiro",
        "address": "Rua Doutor Rodrigues Alves, 250, Centro, Lorena/SP",
        "latitude": -22.732,
        "longitude": -45.1255,
        "description": "Comida caseira mineira com feijao tropeiro, frango com quiabo e tutu.",
        "delivery_fee": 6.9,
        "avg_delivery_time_min": 40,
        "products": [
            ("Feijao Tropeiro", 31.9, "Acompanha arroz, couve refogada e torresmo."),
            ("Frango com Quiabo", 34.9, "Frango caipira cozido lentamente com quiabo e angu."),
            ("Tutu a Mineira", 28.9, "Tutu de feijao com lombo, couve e arroz."),
            ("Doce de Leite Caseiro", 12.9, "Pote de 250g produzido na regiao."),
        ],
    },
    {
        "owner_email": "pizza@demo.com",
        "owner_name": "Pizza Prime",
        "name": "Pizza Prime",
        "address": "Avenida Targino Vilela Nunes, 1500, Jardim das Acacias, Lorena/SP",
        "latitude": -22.725,
        "longitude": -45.13,
        "description": "Pizzas de fermentacao natural, brotos e ingredientes selecionados.",
        "delivery_fee": 8.9,
        "avg_delivery_time_min": 45,
        "products": [
            ("Pizza Margherita", 49.9, "Molho de tomate, mussarela de bufala e manjericao."),
            ("Pizza Calabresa", 52.9, "Calabresa fatiada, cebola roxa e oregano."),
            ("Pizza Quatro Queijos", 59.9, "Mussarela, provolone, gorgonzola e parmesao."),
            ("Pizza Portuguesa", 56.9, "Presunto, ovos, cebola, azeitona e mussarela."),
        ],
    },
    {
        "owner_email": "baiano@demo.com",
        "owner_name": "Tempero Baiano",
        "name": "Tempero Baiano",
        "address": "Rua Comendador Custodio Vieira, 800, Centro, Lorena/SP",
        "latitude": -22.734,
        "longitude": -45.12,
        "description": "Moqueca, acaraje, vatapa e temperos da Bahia.",
        "delivery_fee": 5.5,
        "avg_delivery_time_min": 35,
        "products": [
            ("Moqueca de Peixe", 44.9, "Serve 2 pessoas, acompanha arroz e pirão."),
            ("Acaraje Completo", 22.9, "Vatapa, caruru, camarao e salada."),
            ("Vatapa com Arroz", 29.9, "Creme de castanha com frango desfiado."),
            ("Cocada Baiana", 9.9, "Doce de coco tradicional."),
        ],
    },
]


def _get_or_create_user(db, *, name: str, email: str, role: UserRole) -> User:
    user = db.scalar(select(User).where(User.email == email))
    if user:
        return user
    user = User(name=name, email=email, role=role, password_hash=get_password_hash(DEMO_PASSWORD))
    db.add(user)
    db.flush()
    return user


def _get_or_create_restaurant(db, data: dict, owner: User) -> Restaurant:
    restaurant = db.scalar(select(Restaurant).where(Restaurant.name == data["name"]))
    if restaurant:
        for field in ("address", "latitude", "longitude"):
            if getattr(restaurant, field) is None:
                setattr(restaurant, field, data.get(field))
        return restaurant

    restaurant = Restaurant(
        owner_user_id=owner.id,
        name=data["name"],
        description=data["description"],
        address=data.get("address"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
        delivery_fee=data["delivery_fee"],
        avg_delivery_time_min=data["avg_delivery_time_min"],
    )
    db.add(restaurant)
    db.flush()
    return restaurant


def _seed_products(
    db,
    restaurant: Restaurant,
    products: list[tuple[str, float, str] | tuple[str, float, str, str]],
    categories: list[str] | None = None,
) -> None:
    category_ids: dict[str, int] = {}
    for order, category_name in enumerate(categories or [], start=1):
        category = db.scalar(
            select(Category).where(
                Category.restaurant_id == restaurant.id,
                Category.name == category_name,
            )
        )
        if not category:
            category = Category(
                restaurant_id=restaurant.id,
                name=category_name,
                display_order=order,
            )
            db.add(category)
            db.flush()
        category_ids[category_name] = category.id

    for item in products:
        if len(item) == 4:
            name, price, description, category_name = item
        else:
            name, price, description = item
            category_name = None

        product = db.scalar(
            select(Product).where(
                Product.restaurant_id == restaurant.id,
                Product.name == name,
            )
        )
        category_id = category_ids.get(category_name) if category_name else None
        if product:
            if product.category_id is None and category_id:
                product.category_id = category_id
            continue

        db.add(
            Product(
                restaurant_id=restaurant.id,
                category_id=category_id,
                name=name,
                description=description,
                price=price,
                is_available=True,
            )
        )


def _seed_orders(db, client: User, courier: User, restaurants: dict[str, Restaurant]) -> None:
    if db.scalar(select(Order).where(Order.client_user_id == client.id)):
        return

    address = db.scalar(select(Address).where(Address.user_id == client.id))
    if not address:
        return

    now = datetime.now(UTC)

    def create_order(restaurant: Restaurant, items: list[tuple[str, int]], status: OrderStatus) -> Order:
        subtotal = 0.0
        resolved = []
        for product_name, quantity in items:
            product = db.scalar(
                select(Product).where(
                    Product.restaurant_id == restaurant.id,
                    Product.name == product_name,
                )
            )
            if not product:
                continue
            subtotal += float(product.price) * quantity
            resolved.append((product, quantity))

        order = Order(
            client_user_id=client.id,
            restaurant_id=restaurant.id,
            delivery_address_id=address.id,
            status=status,
            subtotal=subtotal,
            delivery_fee=restaurant.delivery_fee,
            total=subtotal + float(restaurant.delivery_fee),
            notes=None,
        )
        db.add(order)
        db.flush()

        for product, quantity in resolved:
            db.add(
                OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=product.price,
                )
            )
        return order

    def add_delivery(order: Order, status: DeliveryStatus, minutes_ago: int, delivered: bool = False) -> None:
        delivery = Delivery(
            order_id=order.id,
            courier_user_id=courier.id,
            status=status,
            started_at=now - timedelta(minutes=minutes_ago + 15),
            delivered_at=now - timedelta(minutes=minutes_ago) if delivered else None,
        )
        db.add(delivery)
        db.flush()
        db.add(
            DeliveryTracking(
                delivery_id=delivery.id,
                latitude=-22.7312,
                longitude=-45.1248,
                status=status.value,
                recorded_at=now - timedelta(minutes=minutes_ago),
            )
        )

    combina_delivered = create_order(
        restaurants["Combina Açaí"],
        [("90% Premium Tradicional 550ml", 1), ("Açaí Grego Copo 550ml", 1)],
        OrderStatus.entregue,
    )
    add_delivery(combina_delivered, DeliveryStatus.entregue, 90, delivered=True)

    create_order(
        restaurants["Combina Açaí"],
        [("70% Tradicional 770ml", 2), ("Açaí Zero Copo 550ml", 1)],
        OrderStatus.em_preparo,
    )

    massa_delivered = create_order(
        restaurants["Massa Express"],
        [("Lasanha Bolonhesa", 1), ("Hamburguer Artesanal", 1)],
        OrderStatus.entregue,
    )
    add_delivery(massa_delivered, DeliveryStatus.entregue, 150, delivered=True)

    create_order(
        restaurants["Burger House"],
        [("Bacon Smash", 2), ("Batata Rustica", 1)],
        OrderStatus.em_preparo,
    )

    on_route = create_order(
        restaurants["Sabor Mineiro"],
        [("Frango com Quiabo", 1), ("Doce de Leite Caseiro", 1)],
        OrderStatus.saiu_entrega,
    )
    add_delivery(on_route, DeliveryStatus.em_rota, 5)


def seed_demo_data() -> None:
    db = SessionLocal()
    try:
        client = _get_or_create_user(db, name="Cliente Demo", email="client@demo.com", role=UserRole.cliente)
        courier = _get_or_create_user(db, name="Entregador Demo", email="courier@demo.com", role=UserRole.entregador)
        _get_or_create_user(db, name="Entregador Backup", email="courier2@demo.com", role=UserRole.entregador)

        restaurants: dict[str, Restaurant] = {}
        for data in RESTAURANTS:
            owner = _get_or_create_user(
                db,
                name=data["owner_name"],
                email=data["owner_email"],
                role=UserRole.dono_restaurante,
            )
            restaurant = _get_or_create_restaurant(db, data, owner)
            _seed_products(db, restaurant, data["products"], data.get("categories"))
            restaurants[restaurant.name] = restaurant
        db.flush()

        if not db.scalar(select(Address).where(Address.user_id == client.id)):
            db.add(
                Address(
                    user_id=client.id,
                    street="Avenida Targino Vilela Nunes",
                    number="2000",
                    district="Vila Nunes",
                    city="Lorena",
                    state="SP",
                    zip_code="12600-000",
                    complement="Apto 12",
                    reference="Proximo a praca",
                    latitude=-22.7262654,
                    longitude=-45.1138106,
                )
            )
            db.flush()

        _seed_orders(db, client, courier, restaurants)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_data()
