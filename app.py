from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from utils.document_generator import generate_document
from utils.improvement_suggester import suggest_improvements
import os
import json
from werkzeug.utils import secure_filename

# Import feature modules
from utils.pdf_extractor import extract_text
from utils.summarizer import summarize_contract
from utils.clause_detector import detect_clauses
from utils.risk_analyzer import analyze_risk
from utils.chatbot import ask_question
from utils.report_generator import generate_report

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# ---------------- DATABASE MODELS ----------------

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    documents = db.relationship('Document', backref='owner', lazy=True)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200))
    content = db.Column(db.Text)
    summary = db.Column(db.Text)
    clauses = db.Column(db.Text)
    risks = db.Column(db.Text)
    improvements = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
def get_user_doc(doc_id):
    return Document.query.filter_by(id=doc_id, user_id=current_user.id).first_or_404()

with app.app_context():
    db.create_all()

# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return render_template("home.html")

# ---------- ABOUT ----------
@app.route("/about")
def about():
    return render_template("about.html")

# ---------- SIGNUP ----------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        if User.query.filter_by(username=username).first():
            flash("Username already exists")
            return redirect(url_for("signup"))

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        flash("Account created successfully")
        return redirect(url_for("login"))

    return render_template("signup.html")

# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials")

    return render_template("login.html")

# ---------- DASHBOARD ----------
@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():

    if request.method == "POST":
        file = request.files.get("file")

        if not file or file.filename == "":
            flash("No file selected.")
            return redirect(url_for("dashboard"))

        if not allowed_file(file.filename):
            flash("Only PDF files allowed.")
            return redirect(url_for("dashboard"))

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        text = extract_text(filepath)

        new_doc = Document(
            filename=filename,
            content=text,
            user_id=current_user.id
        )

        db.session.add(new_doc)
        db.session.commit()

        flash("Document uploaded successfully.")
        return redirect(url_for("dashboard"))

    documents = Document.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", documents=documents)

# ---------- SUMMARY ----------
@app.route("/generate_summary/<int:doc_id>")
@login_required
def generate_summary_route(doc_id):

    doc = get_user_doc(doc_id)

    doc.summary = summarize_contract(doc.content)
    db.session.commit()

    return render_template("summary.html", summary=doc.summary)

# ---------- CLAUSES ----------
@app.route("/detect_clauses/<int:doc_id>")
@login_required
def detect_clauses_route(doc_id):

    doc = get_user_doc(doc_id)

    clauses_text = detect_clauses(doc.content)

    doc.clauses = clauses_text
    db.session.commit()

    return render_template("clauses.html", clauses=clauses_text)

# ---------- RISK ----------
@app.route("/analyze_risk/<int:doc_id>")
@login_required
def analyze_risk_route(doc_id):

    doc = get_user_doc(doc_id)

    risks_dict = analyze_risk(doc.content)

    doc.risks = json.dumps(risks_dict)
    db.session.commit()

    return render_template("risks.html", risks=risks_dict)

# ---------- IMPROVEMENTS ----------
@app.route("/improvements/<int:doc_id>")
@login_required
def improvements(doc_id):

    doc = get_user_doc(doc_id)

    suggestions = suggest_improvements(doc.content)

    doc.improvements = suggestions
    db.session.commit()

    return render_template("improvements.html", suggestions=suggestions)

# ---------- CHAT ----------
@app.route("/chat/<int:doc_id>", methods=["GET", "POST"])
@login_required
def chat(doc_id):

    doc = get_user_doc(doc_id)

    session_key = f"chat_history_{doc_id}"

    if session_key not in session:
        session[session_key] = []

    if request.method == "POST":
        question = request.form["question"]
        answer = ask_question(doc.content, question)

        session[session_key].append({
            "question": question,
            "answer": answer
        })

        session.modified = True

    chat_history = session.get(session_key, [])

    return render_template("chat.html", chat_history=chat_history)

# ---------- REPORT ----------
@app.route("/generate_report/<int:doc_id>")
@login_required
def generate_report_route(doc_id):

    doc = get_user_doc(doc_id)

    summary = doc.summary or "Summary not generated yet."
    clauses = doc.clauses or "Clauses not generated yet."
    risks = json.loads(doc.risks) if doc.risks else {}
    improvements = doc.improvements or suggest_improvements(doc.content)

    file_path = generate_report(summary, clauses, risks, improvements)

    return send_file(file_path, as_attachment=True)

# ---------- GENERATE PAGE ----------
@app.route("/generate")
@login_required
def generate_page():
    return render_template("generate.html")


# ---------- GENERATE DOCUMENT ----------
@app.route("/generate-document", methods=["POST"])
@login_required
def generate_document_route():

    doc_type = request.form.get("doc_type")
    details = request.form.get("details")

    if not doc_type or not details:
        flash("Please fill all fields.")
        return redirect(url_for("generate_page"))

    file_stream = generate_document(doc_type, details)

    return send_file(
        file_stream,
        as_attachment=True,
        download_name=f"{doc_type}.pdf",
        mimetype="application/pdf"
    )

# ---------- LOGOUT ----------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)