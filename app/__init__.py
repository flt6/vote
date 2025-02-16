from flask import Flask,render_template,redirect,render_template_string
from flask_cors import CORS
from app.routes import chain_routes, vote_routes, admin_routes,base

def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.secret_key="hfdl4i3hr5o"
    CORS(app, supports_credentials=True)  # 允许跨域请求携带cookie
    
    app.register_blueprint(chain_routes.bp)
    app.register_blueprint(vote_routes.bp)
    app.register_blueprint(admin_routes.bp)
    app.register_blueprint(base.bp)
    
    @app.route("/")
    def index():
        mode =  base.get_mode()
        if mode=="config":
            return render_template_string("<h1>未配置，请稍后</h1>")
        else:
            return redirect("/"+mode)
            
    
    @app.route('/vote')
    def vote():
        if base.get_mode()!="vote":return index()
        return render_template('vote/select.html')
    @app.route('/vote/confirm')
    def vote_confirm():
        return render_template('vote/confirm.html')
        
    @app.route('/chain')
    def chain():
        if base.get_mode()!="chain":return index()
        return render_template('chain/select.html')
    @app.route('/chain/confirm')
    def chain_confirm():
        return render_template('chain/confirm.html')
    
    @app.route("/admin")
    @app.route('/admin/login')
    def admin_login():
        return render_template('admin/login.html')
    @app.route('/admin/config')
    @admin_routes.login_required
    def admin_config():
        return render_template('admin/config.html')
    @app.route('/admin/dashboard')
    @admin_routes.login_required
    def admin_dashboard():
        return render_template('admin/dashboard.html')
    
    return app