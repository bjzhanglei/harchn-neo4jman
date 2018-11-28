from flask import Flask, render_template, flash, session, url_for
from model import User
from flask import json
from flask_httpauth import HTTPBasicAuth
from restfultools import *
from passlib.hash import bcrypt
from flask import redirect
from flask import request
from datetime import timedelta

app = Flask(__name__)
auth = HTTPBasicAuth()
app.secret_key = 'sugarsugar'


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "registeruser" in request.form:
            username = request.form['registeruser']
            password = request.form['password']
            if not username or not password:
                flash('请输入用户名和密码')
            else:
                user = User(username)
                print(user)
                if not user.register(password):
                    flash('一个用户已经存在')
                else:
                    flash('注册成功')
        else:
            username = request.form['username']
            password = request.form['password']
            user = User(username)
            if not username or not password:
                flash('请输入用户名和密码')
            elif not user.verify_pass(password):
                flash('无效登录')
            else:
                session["username"] = user.username
                session['label'] = user.label
                return redirect(url_for("main_view"))
    return render_template('login.html')


@app.route('/login_graph')
def get_login_graph():
    nodes = []
    rels = []
    i = 0
    num = 50
    for node_index in range(140):
        nodes.append({"name": node_index, "label": "node"})
    rels = [{'source': 1, 'target': 0}, {'source': 2, 'target': 0}, {'source': 3, 'target': 0},
            {'source': 4, 'target': 0}, {'source': 5, 'target': 0},
            {'source': 7, 'target': 6}, {'source': 8, 'target': 6}, {'source': 9, 'target': 6},
            {'source': 10, 'target': 6}, {'source': 11, 'target': 6},
            {'source': 3, 'target': 6}, {'source': 13, 'target': 12}, {'source': 14, 'target': 12},
            {'source': 15, 'target': 12}, {'source': 16, 'target': 12},
            {'source': 18, 'target': 17}, {'source': 19, 'target': 17}, {'source': 20, 'target': 17},
            {'source': 21, 'target': 17}, {'source': 22, 'target': 17},
            {'source': 23, 'target': 17}, {'source': 24, 'target': 17}, {'source': 3, 'target': 25},
            {'source': 27, 'target': 26}, {'source': 28, 'target': 26},
            {'source': 29, 'target': 26}, {'source': 30, 'target': 26}, {'source': 16, 'target': 31},
            {'source': 32, 'target': 31}, {'source': 33, 'target': 31},
            {'source': 35, 'target': 34}, {'source': 36, 'target': 34}, {'source': 37, 'target': 34},
            {'source': 8, 'target': 34}, {'source': 3, 'target': 38},
            {'source': 39, 'target': 38}, {'source': 8, 'target': 38}, {'source': 41, 'target': 40},
            {'source': 42, 'target': 40}, {'source': 43, 'target': 40},
            {'source': 16, 'target': 40}, {'source': 45, 'target': 44}, {'source': 46, 'target': 44},
            {'source': 47, 'target': 44}, {'source': 3, 'target': 44},
            {'source': 49, 'target': 48}, {'source': 43, 'target': 48}, {'source': 39, 'target': 48},
            {'source': 3, 'target': 50}, {'source': 8, 'target': 50},
            {'source': 51, 'target': 50}, {'source': 52, 'target': 50}, {'source': 53, 'target': 50},
            {'source': 54, 'target': 50}, {'source': 56, 'target': 55},
            {'source': 7, 'target': 55}, {'source': 24, 'target': 55}, {'source': 57, 'target': 55},
            {'source': 59, 'target': 58}, {'source': 60, 'target': 58},
            {'source': 3, 'target': 58}, {'source': 61, 'target': 58}, {'source': 4, 'target': 58},
            {'source': 62, 'target': 58}, {'source': 63, 'target': 58},
            {'source': 64, 'target': 58}, {'source': 66, 'target': 65}, {'source': 67, 'target': 65},
            {'source': 3, 'target': 65}, {'source': 68, 'target': 65},
            {'source': 53, 'target': 65}, {'source': 5, 'target': 65}, {'source': 70, 'target': 69},
            {'source': 63, 'target': 69}, {'source': 71, 'target': 69},
            {'source': 72, 'target': 69}, {'source': 74, 'target': 73}, {'source': 33, 'target': 73},
            {'source': 3, 'target': 73}, {'source': 47, 'target': 75},
            {'source': 76, 'target': 75}, {'source': 77, 'target': 75}, {'source': 78, 'target': 75},
            {'source': 79, 'target': 75}, {'source': 30, 'target': 80},
            {'source': 81, 'target': 80}, {'source': 82, 'target': 80}, {'source': 9, 'target': 80},
            {'source': 16, 'target': 83}, {'source': 84, 'target': 83},
            {'source': 30, 'target': 83}, {'source': 47, 'target': 85}, {'source': 86, 'target': 85},
            {'source': 87, 'target': 85}, {'source': 16, 'target': 85},
            {'source': 88, 'target': 85}, {'source': 5, 'target': 89}, {'source': 90, 'target': 89},
            {'source': 56, 'target': 89}, {'source': 82, 'target': 89},
            {'source': 86, 'target': 91}, {'source': 16, 'target': 91}, {'source': 47, 'target': 91},
            {'source': 87, 'target': 91}, {'source': 3, 'target': 92},
            {'source': 93, 'target': 92}, {'source': 90, 'target': 92}, {'source': 95, 'target': 94},
            {'source': 22, 'target': 94}, {'source': 96, 'target': 94},
            {'source': 97, 'target': 94}, {'source': 81, 'target': 94}, {'source': 98, 'target': 94},
            {'source': 99, 'target': 94}, {'source': 62, 'target': 94},
            {'source': 100, 'target': 94}, {'source': 102, 'target': 101}, {'source': 72, 'target': 101},
            {'source': 103, 'target': 101}, {'source': 79, 'target': 101},
            {'source': 105, 'target': 104}, {'source': 106, 'target': 104}, {'source': 70, 'target': 104},
            {'source': 49, 'target': 104}, {'source': 81, 'target': 104},
            {'source': 47, 'target': 107}, {'source': 86, 'target': 107}, {'source': 87, 'target': 107},
            {'source': 16, 'target': 107}, {'source': 43, 'target': 108},
            {'source': 109, 'target': 108}, {'source': 110, 'target': 108}, {'source': 112, 'target': 111},
            {'source': 3, 'target': 111}, {'source': 113, 'target': 111}, {'source': 114, 'target': 111},
            {'source': 95, 'target': 115}, {'source': 116, 'target': 115}, {'source': 30, 'target': 115},
            {'source': 2, 'target': 115}, {'source': 23, 'target': 115}, {'source': 117, 'target': 115},
            {'source': 81, 'target': 115}, {'source': 118, 'target': 115}, {'source': 28, 'target': 115},
            {'source': 119, 'target': 115}, {'source': 120, 'target': 115}, {'source': 121, 'target': 115},
            {'source': 123, 'target': 122}, {'source': 124, 'target': 122}, {'source': 61, 'target': 122},
            {'source': 125, 'target': 122}, {'source': 2, 'target': 122}, {'source': 49, 'target': 126},
            {'source': 125, 'target': 126}, {'source': 30, 'target': 127}, {'source': 29, 'target': 127},
            {'source': 82, 'target': 128}, {'source': 3, 'target': 128}, {'source': 8, 'target': 129},
            {'source': 95, 'target': 129}, {'source': 130, 'target': 129}, {'source': 131, 'target': 129},
            {'source': 132, 'target': 129}, {'source': 133, 'target': 129}, {'source': 135, 'target': 134},
            {'source': 136, 'target': 134}, {'source': 79, 'target': 134}, {'source': 103, 'target': 134},
            {'source': 137, 'target': 134}, {'source': 138, 'target': 134}, {'source': 139, 'target': 134}]
    return jsonify({"nodes": nodes, "links": rels})


@app.route('/graph')
def get_graph():
    user = User(session.get('username'))
    datas = user.get_graph()
    return datas


@app.route('/advance_query')
def advance_query():
    return render_template('advance_query.html')


@app.route('/main')
def main_view():
    if not session.get('username'):
        return redirect(url_for("index"))
    return render_template('view.html')


@app.route('/manage')
def data_manage():
    print(len(request.args))
    if not session.get('username'):
        return redirect(url_for("index"))
    return render_template('datamanage.html')


@app.route('/user_graph')
def user_graph():
    if not session.get('username'):
        return redirect(url_for("index"))
    return render_template('userView.html')


@app.route('/user_info')
def user_info():
    if not session.get('username'):
        return redirect(url_for("index"))
    return render_template('user_info.html')


@app.route('/change_password')
def change_password():
    if not session.get('username'):
        return redirect(url_for("index"))
    return render_template('change_password.html')


@app.route('/import_data')
def import_data():
    return render_template('import_data.html')


@app.route('/export_data')
def export_data():
    return render_template('export_data.html')


@app.route('/search_table', methods=["GET", "POST"])
def search_table():
    try:
        q = request.args.get('q', 0)
        limit = request.args.get('limit', 1)
        offset = request.args.get('offset', 2)
        f = request.args.get('f', 3)
    except KeyError:
        return []
    else:
        user = User(session.get("username"))
        results = user.search_table(q, limit, offset, f)
        return results


@app.route('/search_one', methods=['POST'])
def search_one():
    try:
        data = request.get_json()
    except KeyError:
        return []
    else:
        user = User(session.get("username"))
        print(data)
        results = user.search_one(data)
        print(results)
        return results


@app.route('/search')
def get_search():
    try:
        q = request.args.get('q', '')
        f = request.args.get('f', 1)
        print(q)
        print(f)
    except KeyError:
        return []
    else:
        user = User(session.get("username"))
        results = user.search_graph(q, f)
        try:
            data_result_file = "data_result.json"
            with open(data_result_file, 'w') as f:
                data_json = json.loads(results.data)
                json.dump(data_json, f, indent=4)
        except IOError:
            print("文件不存在")
        print(results.data)
        return results


@app.route('/get_advance_query', methods=['POST'])
def get_advance_query():
    try:
        data = request.get_json()
        print(data)
    except KeyError:
        return []
    else:
        user = User(session.get("username"))
        result = user.get_advance_query(data)
        print(len(json.loads(result.data)['nodes']))
        if len(json.loads(result.data)['nodes']) <= 0:
            return "查询结果为空"
        if data['save_path'] != '':
            try:
                data_result_file = "data_result.json"
                save_path = data['save_path'] + "/" + data_result_file
                with open(save_path, 'w') as f:
                    data_json = json.loads(result.data)
                    json.dump(data_json, f, indent=4)
            except IOError:
                print("文件不存在")
        return result


@app.route('/search_user')
def get_search_user():
    try:
        q = request.args.get('q', 0)
        f = request.args.get('f', 1)
        print(q)
        print(f)
    except KeyError:
        return []
    else:
        user = User(session.get("username"))
        results = user.search_user_graph(q, f)
        return results


@app.route('/insert', methods=['POST'])
def get_insert():
    try:
        data = request.get_json()
    except KeyError:
        return []
    else:
        user = User(session.get("username"))
        start_node_first = {}
        start_node_second = {}
        end_node = {}
        start_node_first['name'] = data['fa_name_first']
        start_node_first['label'] = data['fa_label_first']
        flag = data['flag']
        relation = data['relation']
        data.pop('flag')
        data.pop('fa_name_first')
        data.pop('fa_label_first')
        data.pop('relation')
        if flag:
            start_node_second['name'] = data['fa_name_second']
            start_node_second['label'] = data['fa_label_second']
            data.pop('fa_name_second')
            data.pop('fa_label_second')
        for key in data.keys():
            end_node[key] = data[key]
        if flag:
            results = user.insert_into_table(start_node_first, start_node_second, relation, end_node)
        else:
            results = user.insert_table(start_node_first, relation, end_node)
        return results


@app.route('/update', methods=['POST'])
def get_update():
    try:
        data = request.get_json()
    except KeyError:
        return []
    else:
        user = User(session.get("username"))
        updated_node = {}
        node = {}
        updated_node['name'] = data['ori_name']
        updated_node['label'] = data['ori_label']
        # relation = data['relation']
        data.pop('ori_name')
        data.pop('ori_label')
        # data.pop('relation')
        for key in data.keys():
            node[key] = data[key]
        print(node)
        results = user.get_update(updated_node, node)
        return results


@app.route('/delete', methods=['POST'])
def get_delete():
    try:
        data = request.get_json()
    except KeyError:
        return []
    else:
        user = User(session.get("username"))
        print(data)
        result = user.get_delete(data)
        return result


@app.route('/get_user_graph')
def get_user_graph():
    user = User(session.get('username'))
    datas = user.get_user_graph()
    return datas


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('已注销')
    return redirect(url_for('index'))


@app.route('/search_user_table')
def search_user_table():
    try:
        q = request.args.get('q', 0)
        limit = request.args.get('limit', 1)
        offset = request.args.get('offset', 2)
        print(q)
    except KeyError:
        return []
    else:
        user = User(session.get("username"))
        results = user.search_user_table(q, limit, offset)
        return results


@app.route('/insert_user', methods=['POST'])
def get_insert_user():
    try:
        data = request.get_json()
    except KeyError:
        return []
    else:
        print(data)
        user = User(session.get("username"))
        end_node = {}
        relation = data['relation']
        data.pop('relation')
        for key in data.keys():
            if key == "password":
                data[key] = bcrypt.encrypt(data[key])
            end_node[key] = data[key]
        print(end_node)
        results = user.insert_user_table(relation, end_node)
        return results


@app.route('/delete_user', methods=['POST'])
def get_delete_user():
    try:
        data = request.get_json()
    except KeyError:
        return []
    else:
        user = User(session.get("username"))
        print(data)
        result = user.get_delete_user(data)
        return result


@app.route('/update_password', methods=['POST'])
def get_update_password():
    try:
        data = request.get_json()
        print(data)
    except KeyError:
        return []
    else:
        data['username'] = session.get("username")
        print(data)
        user = User(session.get("username"))
        result = user.update_password(data)
        if result == "修改成功":
            session.pop('username', None)
        return result


@app.route('/db_operate', methods=['POST'])
def get_db_operate():
        return "执行失败"


@app.route('/upload_file', methods=['POST'])
def upload_file():
    try:
        file = request.files.get('userfile')
        save_file_name = file.filename
        file.save(save_file_name)
    except KeyError:
        return []
    else:
        return jsonify({'info': "上传成功"})


@app.route('/batch_insert', methods=['POST'])
def batch_insert():
    try:
        data = request.get_json()
        print(data)
    except KeyError:
        return []
    else:
        start_node = {'name': data['name'], 'label': data['label']}
        user = User(session.get("username"))
        result = user.batch_insert(start_node, data['filename'])
        return result


@auth.verify_password
def get_password(username, password):
    if username:
        user = User(username)
        return user.verify_pass(password)
    return False


@auth.error_handler
def unauthorized():
    return statusResponse(R403_FORBIDDEN)


@app.route('/api/v1.0/info/all', methods=['GET'])
@auth.login_required
def getAll():
    user = User(session.get('username'))
    datas = user.get_graph()
    return datas


@app.route('/api/v1.0/info/search/relation/<string:condition>', methods=['GET'])
@auth.login_required
def get_relation(condition):
    print(condition)
    user = User(session.get('username'))
    datas = user.search_graph(condition, False)
    print(len(json.loads(datas.data)['nodes']))
    if len(json.loads(datas.data)['nodes']) == 0:
        return statusResponse(R404_NOTFOUND)
    return datas


@app.route('/api/v1.0/info/search/source/<string:condition>', methods=['GET'])
@auth.login_required
def get_source(condition):
    user = User(session.get('username'))
    datas = user.search_graph(condition, "true")
    if len(json.loads(datas.data)['nodes']) == 0:
        return statusResponse(R404_NOTFOUND)
    return datas


@app.route('/api/v1.0/info/advance/search/child/<string:level>/<string:condition>', methods=['GET'])
@auth.login_required
def get_advance_child(level, condition):
    user = User(session.get('username'))
    data = {'query_way': '子节点查询', 'query_condition': condition,
            'query_level': level}
    print(data)
    results = user.get_advance_query(data)
    if len(json.loads(results.data)['nodes']) == 0:
        return statusResponse(R404_NOTFOUND)
    return results


@app.route('/api/v1.0/info/advance/search/source/<string:level>/<string:condition>', methods=['GET'])
@auth.login_required
def get_advance_source(level, condition):
    user = User(session.get('username'))
    data = {'query_way': '溯源查询', 'query_condition': condition,
            'query_level': level}
    print(data)
    results = user.get_advance_query(data)
    if len(json.loads(results.data)['nodes']) == 0:
        return statusResponse(R404_NOTFOUND)
    return results


if __name__ == '__main__':
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
    app.run(host='0.0.0.0', debug=True)
