from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models import db, User, Product, Order

# Inicializa o app e o banco de dados
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafeteria.db'
app.config['SECRET_KEY'] = 'supersecretkey'
db.init_app(app)


# Configuração do login
login_manager = LoginManager()
login_manager.init_app(app)

# Carregar usuário
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rota principal
@app.route('/')
def home():
    return render_template('catalog.html', products=Product.query.all())

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

# Rota de logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# Rota de admin (adicionar produtos)
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        product = Product(name=name, price=price, stock=stock)
        db.session.add(product)
        db.session.commit()
        flash("Product added successfully!")
    return render_template('admin.html', products=Product.query.all())


# Rota de exibição do carrinho
@app.route('/cart')
def cart():
    cart_items = session.get('cart', {})
    products = {int(id): Product.query.get(int(id)) for id in cart_items.keys()}
    total = sum(products[int(id)].price * quantity for id, quantity in cart_items.items())
    return render_template('cart.html', products=products, cart_items=cart_items, total=total)

# Adicionar item ao carrinho
@app.route('/add-to-cart/<int:product_id>')
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart = session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session['cart'] = cart
    flash(f"{product.name} added to cart!")
    return redirect(url_for('home'))

# Rota para checkout do carrinho
@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart_items = session.get('cart', {})
    if not cart_items:
        flash("Your cart is empty!")
        return redirect(url_for('cart'))

    total_price = sum(Product.query.get(int(id)).price * quantity for id, quantity in cart_items.items())
    order = Order(user_id=current_user.id, total_price=total_price)
    db.session.add(order)
    db.session.commit()

    for id, quantity in cart_items.items():
        product = Product.query.get(int(id))
        product.stock -= quantity
        db.session.commit()

    session.pop('cart', None)
    flash("Order placed successfully!")
    return redirect(url_for('home'))

# Rota para exibir o relatório de vendas
@app.route('/sales-report')
@login_required
def sales_report():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    orders = Order.query.all()
    return render_template('sales_report.html', orders=orders)

# Rota de catálogo de produtos
@app.route('/catalog')
def catalog():
    products = Product.query.all()  # Recupera todos os produtos do banco de dados
    return render_template('catalog.html', products=products)


# Rota de cadastro de usuário
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You can now log in.')
            return redirect(url_for('login'))
    return render_template('register.html')

# Inicializa o banco de dados (cria as tabelas)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
