from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shoppingatlas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Category(db.Model):
    cid = db.Column(db.Integer, primary_key=True)
    cname = db.Column(db.String(100), nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.cname


class Product(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    pname = db.Column(db.String(100), nullable=False)
    pprice = db.Column(db.Integer, nullable=False)
    pimage = db.Column(db.String(100))
    c_id = db.Column(db.Integer, db.ForeignKey('category.cid'))

    def __str__(self):
        return self.pname


class Users(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(100), unique=True)
    uemail = db.Column(db.String(100), unique=True)
    upwd = db.Column(db.String(80))


class Cart(db.Model):
    cartid = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.Integer, db.ForeignKey('users.uid'))
    p_id = db.Column(db.Integer, db.ForeignKey('product.pid'))
    addDate = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/admin')
def admin():

    c1 = Category(cname="Home Furnishing")
    c2 = Category(cname="Fashion")
    c3 = Category(cname="Electronics")

    p1 = Product(pid=1, pname="Sofa Set", pprice=5500,
                 pimage="pic11.jpg", category=c1)
    p2 = Product(pid=2, pname="Photo Frames", pprice=2100,
                 pimage="pic15.jpg", category=c1)
    p3 = Product(pid=3, pname="Cushion Chair", pprice=800,
                 pimage="pic19.jpg", category=c1)
    p4 = Product(pid=4, pname="Dining Table & Chairs",
                 pprice=3000, pimage="pic10.jpg", category=c1)
    p5 = Product(pid=5, pname="Dressing Table", pprice=3000,
                 pimage="pic20.jpg", category=c1)
    p6 = Product(pid=6, pname="Chairs", pprice=1000,
                 pimage="pic13.jpg", category=c1)

    p7 = Product(pid=7, pname="Puffer Hooded Jacket",
                 pprice=1500, pimage="pic1.jpg", category=c2)
    p8 = Product(pid=8, pname="Tokyo Talkies", pprice=3200,
                 pimage="pic2.jpg", category=c2)
    p9 = Product(pid=9, pname="Goggles", pprice=200,
                 pimage="pic26.jpg", category=c2)
    p10 = Product(pid=10, pname="Handbag", pprice=2000,
                  pimage="pic27.jpg", category=c2)
    p11 = Product(pid=11, pname="Eye Shadow Palatte",
                  pprice=300, pimage="pic29.jpg", category=c2)
    p12 = Product(pid=12, pname="Makeup Brushes", pprice=600,
                  pimage="pic32.jpg", category=c2)

    p13 = Product(pid=13, pname="Iphone 7 pro", pprice=6000,
                  pimage="pic24.jpg", category=c3)
    p14 = Product(pid=14, pname="HP Laptop", pprice=10000,
                  pimage="pic5.jpg", category=c3)
    p15 = Product(pid=15, pname="Iphone 12 pro", pprice=9000,
                  pimage="pic7.jpg", category=c3)
    p16 = Product(pid=16, pname="Iphone 12", pprice=8000,
                  pimage="pic9.jpg", category=c3)
    p17 = Product(pid=17, pname="MacBook", pprice=12000,
                  pimage="pic21.jpg", category=c3)
    p18 = Product(pid=18, pname="Apple iMac", pprice=15000,
                  pimage="pic23.jpg", category=c3)

    db.session.add(p1)
    db.session.add(p2)
    db.session.add(p3)
    db.session.add(p4)
    db.session.add(p5)
    db.session.add(p6)
    db.session.add(p7)
    db.session.add(p8)
    db.session.add(p9)
    db.session.add(p10)
    db.session.add(p11)
    db.session.add(p12)
    db.session.add(p13)
    db.session.add(p14)
    db.session.add(p15)
    db.session.add(p16)
    db.session.add(p17)
    db.session.add(p18)
    db.session.commit()
    return redirect('/')


@app.route('/')
def ShoppingAtlasHome():

    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == "POST":

        Email = request.form["email"]
        Pwd = request.form["password"]
        ud = Users.query.filter_by(uemail=Email, upwd=Pwd).first()

        if(ud is not None):
            session["user"] = ud.uname
            print(ud.uname)
            return render_template("categories.html", ud=ud)

        else:
            return render_template("login.html", message="Invalid Username or Password")
    if 'user' in session:
        return redirect('/categories')

    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form["dname"]
        email = request.form["demail"]
        pwd = request.form["dpassword"]

        ud = Users(uname=name, uemail=email, upwd=pwd)
        db.session.add(ud)
        db.session.commit()
        return redirect("/login")
    else:
        return render_template("login.html")


@app.route('/categories')
def ShoppingAtlasCategories():
    if 'user' in session:
        uname = session["user"]
        ud = Users.query.filter_by(uname=uname).first()
        return render_template("categories.html", ud=ud)
    else:
        return redirect('/login')


@app.route('/cart')
def ShoppingAtlasCart():
    if 'user' in session:
        uname = session["user"]
        u = Users.query.filter_by(uname=uname).first()
        c = Cart.query.filter_by(u_id=u.uid).all()
        p = [i.p_id for i in c]
        plist = []
        for id in p:
            plist.append(Product.query.filter_by(pid=id).first())
        print(plist)

        return render_template("cart.html", uname=uname, plist=plist)
    else:
        return redirect('/login')



@app.route('/<name>/addtocart/<int:pid>')
def ShoppingAtlasAddtoCart(name, pid):

    u = Users.query.filter_by(uname=name).first()
    c = Cart(u_id=u.uid, p_id=pid)

    db.session.add(c)
    db.session.commit()

    if pid <= 6:
        return redirect("/homefurnishing")
    if pid > 6 and pid <= 12:
        return redirect("/fashion")
    else:
        return redirect("/electronics")

@app.route('/delete/<int:pid>',methods=["GET","POST"])
def DeleteCart(pid):
    pd=Cart.query.filter_by(p_id=pid).first()
    db.session.delete(pd)
    db.session.commit()
    return redirect("/cart")


@app.route('/fashion')
def ShoppingAtlasFashion():
    if 'user' in session:
        cid = 2
        hf = Product.query.filter_by(c_id=cid).all()
        uname = session["user"]
        return render_template("fashion.html", hf=hf, uname=uname)
    else:
        return redirect('/login')


@app.route('/homefurnishing')
def ShoppingAtlasHomeFurnishing():
    if 'user' in session:
        cid = 1
        hf = Product.query.filter_by(c_id=cid).all()
        uname = session["user"]
        return render_template("homefurnishing.html", hf=hf, uname=uname)
    else:
        return redirect('/login')



@app.route('/electronics')
def ShoppingAtlasElectronics():
    if 'user' in session:
        cid = 3
        hf = Product.query.filter_by(c_id=cid).all()
        uname = session["user"]
        return render_template("electronics.html", hf=hf, uname=uname)
    else:
        return redirect('/login')



@app.route('/logout')
def ShoppingAtlasLogout():
    session.pop('user')
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
