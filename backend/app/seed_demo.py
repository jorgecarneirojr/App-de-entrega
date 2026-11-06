from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.address import Address
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
        "owner_name": "Massa Express",
        "name": "Massa Express",
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
        "owner_email": "acai@demo.com",
        "owner_name": "Açaí & Cia",
        "name": "Açaí & Cia",
        "description": "Açaí cremoso, bowls, vitaminas e complementos frescos.",
        "delivery_fee": 3.5,
        "avg_delivery_time_min": 20,
        "products": [
            ("Açaí 300ml", 17.9, "Acompanha banana, granola e leite condensado."),
            ("Açaí 500ml", 23.9, "Com morango, granola e mel."),
            ("Bowl Tropical", 27.9, "Açaí, manga, kiwi, coco e granola."),
            ("Vitamina de Açaí", 15.9, "400ml batida com banana e leite."),
        ],
    },
    {
        "owner_email": "pizza@demo.com",
        "owner_name": "Pizza Prime",
        "name": "Pizza Prime",
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
        return restaurant

    restaurant = Restaurant(
        owner_user_id=owner.id,
        name=data["name"],
        description=data["description"],
        delivery_fee=data["delivery_fee"],
        avg_delivery_time_min=data["avg_delivery_time_min"],
    )
    db.add(restaurant)
    db.flush()
    return restaurant


def _seed_products(db, restaurant: Restaurant, products: list[tuple[str, float, str]]) -> None:
    existing = {
        name
        for (name,) in db.execute(select(Product.name).where(Product.restaurant_id == restaurant.id))
    }
    for name, price, description in products:
        if name not in existing:
            db.add(
                Product(
                    restaurant_id=restaurant.id,
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

    now = datetime.now(timezone.utc)

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

    delivered = create_order(
        restaurants["Massa Express"],
        [("Lasanha Bolonhesa", 1), ("Hamburguer Artesanal", 1)],
        OrderStatus.entregue,
    )
    delivered_delivery = Delivery(
        order_id=delivered.id,
        courier_user_id=courier.id,
        status=DeliveryStatus.entregue,
        started_at=now - timedelta(days=2, minutes=40),
        delivered_at=now - timedelta(days=2, minutes=10),
    )
    db.add(delivered_delivery)
    db.flush()
    db.add(
        DeliveryTracking(
            delivery_id=delivered_delivery.id,
            latitude=-23.55052,
            longitude=-46.633308,
            status=DeliveryStatus.entregue.value,
            recorded_at=now - timedelta(days=2, minutes=10),
        )
    )

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
    on_route_delivery = Delivery(
        order_id=on_route.id,
        courier_user_id=courier.id,
        status=DeliveryStatus.em_rota,
        started_at=now - timedelta(minutes=18),
    )
    db.add(on_route_delivery)
    db.flush()
    db.add(
        DeliveryTracking(
            delivery_id=on_route_delivery.id,
            latitude=-23.561414,
            longitude=-46.655881,
            status=DeliveryStatus.em_rota.value,
            recorded_at=now - timedelta(minutes=5),
        )
    )


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
            _seed_products(db, restaurant, data["products"])
            restaurants[restaurant.name] = restaurant
        db.flush()

        if not db.scalar(select(Address).where(Address.user_id == client.id)):
            db.add(
                Address(
                    user_id=client.id,
                    street="Rua das Flores",
                    number="123",
                    district="Centro",
                    city="Sao Paulo",
                    state="SP",
                    zip_code="01000-000",
                    complement="Apto 12",
                    reference="Proximo a praca",
                )
            )
            db.flush()

        _seed_orders(db, client, courier, restaurants)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_data()
