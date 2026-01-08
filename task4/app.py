from flask import Flask, request, render_template_string
from adapters import start_mappers, create_tables, SqlAlchemyUnitOfWork
from service_layer import MessageBus, HANDLERS, Allocate, CreateProduct, OutOfStock, out_of_stock_handler

app = Flask(__name__)

# --- Bootstrapping ---
# Inicjalizacja bazy i mapowania ORM
start_mappers()
create_tables()

# --- Minimalistic HTML Templates ---
HOME_HTML = """
<h1>Magazyn</h1>
<p><a href="/add_product">Dodaj nowy produkt</a></p>
<p><a href="/allocate">Wydaj towar (Allocate)</a></p>

<h3>Stan Magazynu (Podgląd Debug):</h3>
<ul>
    {% for p in products %}
    <li>SKU: {{ p.sku }} | Ilość: {{ p.quantity }}</li>
    {% endfor %}
</ul>
"""

FORM_HTML = """
<h1>{{ title }}</h1>
<form method="POST">
    SKU: <input type="text" name="sku"><br>
    Ilość: <input type="number" name="qty"><br>
    <button type="submit">Wykonaj</button>
</form>
<a href="/">Powrót</a>
"""

# --- Routes ---

@app.route("/")
def index():
    uow = SqlAlchemyUnitOfWork()
    with uow:
        products = uow.products.list()
    
    return render_template_string(HOME_HTML, products=products)

@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        sku = request.form["sku"]
        qty = int(request.form["qty"])
        
        # ZADANIE 2:
        # 1. Stwórz komendę CreateProduct
        # 2. Stwórz nowy UnitOfWork
        # 3. Stwórz MessageBus z tym UoW
        # 4. Wyślij komendę do busa (bus.handle)
        
        # TODO
        
        return render_template_string("Produkt dodany! <a href='/'>Wróć</a>")
        
    return render_template_string(FORM_HTML, title="Dodaj Produkt")

@app.route("/allocate", methods=["GET", "POST"])
def allocate():
    if request.method == "POST":
        sku = request.form["sku"]
        qty = int(request.form["qty"])

        # ZADANIE 3:
        # 1. Stwórz komendę Allocate
        # 2. Wyślij ją przez MessageBus (analogicznie jak wyżej)
        # Obserwuj konsolę.
        
        # TODO

        return render_template_string("Próba alokacji zakończona. Sprawdź stan. <a href='/'>Wróć</a>")

    return render_template_string(FORM_HTML, title="Wydaj towar")

if __name__ == "__main__":
    app.run(debug=True, port=5000)