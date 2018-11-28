import xlrd
from flask import jsonify
from passlib.hash import bcrypt
from py2neo import authenticate, Graph, Node

authenticate("localhost:7474", "neo4j", "1234")
graph = Graph()

class User:
    def __init__(self, username):
        self.username = username
        user_data = self.find()
        #获取登录用户标签
        if user_data:
            self.label = user_data['label']
        else:
            self.label = "User"
    def find(self):
        user = {}
        data_user = graph.find_one("User", "username", self.username)
        if not data_user:
            data_admin = graph.find_one("Admin", "username", self.username)
            if not data_admin:
                return False
            else:
                print(user)
                user['username'] = data_admin['username']
                user['password'] = data_admin['password']
                user['label'] = 'Admin'
        else:
            user['username'] = data_user['username']
            user['password'] = data_user['password']
            user['label'] = 'User'
        return user
    def register(self, password):
        if not self.find():
            user = Node("User", username=self.username, password=bcrypt.encrypt(password))
            graph.create(user)
            cypher = 'MATCH (admin:Admin) MATCH(user:User {username:\'' + self.username + '\'}) CREATE (admin)-[manage:Manage]->(user)'
            graph.cypher.execute(
                'MATCH (admin:Admin) MATCH(user:User {username:\'' + self.username + '\'}) CREATE (admin)-[manage:Manage]->(user)')
            return True
        else:
            return False
    def verify_pass(self, password):
        user = self.find()
        if not user:
            return False
        else:
            return bcrypt.verify(password, user["password"])

    def get_graph(self):
        nodes = []
        rels = []
        i = 0
        query = "MATCH (m)<-[:ACTED_IN]-(a) RETURN properties(m) as start_node, labels(m) as labels," \
                "collect(properties(a)) as cast,collect(labels(a)) as cast_labels"
        results = graph.cypher.execute(query)
        print(query)
        #print(results)
        for start_nodes, labels, cast, cast_labels in results:
            keys = list(start_nodes.keys())
            node = {}
            for key in keys:
                node[key] = start_nodes.get(key)
            node['label'] = labels[0]
            node['name'] = node['title']
            #print(node)
            try:
                target = nodes.index(node)
            except ValueError:
                nodes.append(node)
                target = i
                i += 1
            for end_node, label in zip(cast, cast_labels):
                end_keys = list(end_node.keys())
                end = {}
                for key in end_keys:
                    end[key] = end_node.get(key)
                end['label'] = label[0]
                try:
                    source = nodes.index(end)
                except ValueError:
                    nodes.append(end)
                    source = i
                    i += 1
                rels.append({"source": source, "target": target})

        return jsonify({"nodes": nodes, "links": rels})

    def search_graph(self, condition, flag=False):
        print(flag)
        nodes = []
        rels = []
        i = 0
        query = "MATCH (m)<-[:ACTED_IN]-(a) WHERE m.name CONTAINS \'" + condition + "\' or a.name CONTAINS \'" + condition + \
                "\' RETURN properties(m) as start_node, labels(m) as labels, " \
                "collect(properties(a)) as cast,collect(labels(a)) as cast_labels"
        query_trace = "Match (n) WHERE n.name contains \'" + condition + \
                      "\' MATCH path = shortestPath( (m:Movie)-[:ACTED_IN*..11]-(n) )" \
                      " where n:Person " \
                      " RETURN nodes(path) AS nodes, EXTRACT(node IN nodes(path) | ID(node)) AS ids " \
                      ",EXTRACT(node IN nodes(path) | labels(node)) AS labels"
        #print(query)
        results = graph.cypher.execute(query)
        if flag == "true" and condition:
            nodes_act = []
            rels_act = []
            print(query_trace)
            for node_trace, id_trace, label_trace in graph.cypher.execute(query_trace):
                j = 0
                print(node_trace)
                for node_ori in node_trace:
                    node_act = {}
                    node_ori_dict = dict(node_ori.properties)
                    node_keys = list(node_ori_dict.keys())
                    for key in node_keys:
                        node_act[key] = node_ori_dict.get(key)
                        node_act['name'] = node_ori_dict.get('title')
                    print(label_trace[j])
                    node_act['label'] = label_trace[j][0]
                    try:
                        target_act = nodes_act.index(node_act)
                        j += 1
                    except ValueError:
                        target_act = len(nodes_act)
                        nodes_act.append(node_act)
                        j += 1
                    if j < len(node_trace):
                        try:
                            source_act = nodes_act.index(self.get_node(node_trace[j].properties, label_trace[j]))
                        except ValueError:
                            source_act = len(nodes_act)
                        rels_act.append({"source": source_act, "target": target_act})
                    # node_keys = list(node_ori.keys)
                    # for key in node_keys:
                    #     node_act[key] = node_ori.get(key)
                    # print(label_trace[j])
                    # node_act['label'] = label_trace[j][0]
                    # try:
                    #     target_act = nodes_act.index(node_act)
                    #     j += 1
                    # except ValueError:
                    #     target_act = len(nodes_act)
                    #     nodes_act.append(node_act)
                    #     j += 1
                    # if j < len(node_trace):
                    #     try:
                    #         source_act = nodes_act.index(self.get_node(node_trace[j], label_trace[j]))
                    #     except ValueError:
                    #         source_act = len(nodes_act)
                    #     rels_act.append({"source": source_act, "target": target_act})
            print(nodes_act)
            print(rels_act)
            return jsonify({"nodes": nodes_act, "links": rels_act})

        for start_nodes, start_labels, end_nodes, end_labels in results:
            print("----Start----")
            print(start_nodes)
            print(end_nodes)
            print("---End---")
            keys = list(start_nodes.keys())
            node = {}
            for key in keys:
                node[key] = start_nodes.get(key)
            node['label'] = start_labels[0]
            node['name'] = node['title']
            try:
                target = nodes.index(node)
            except ValueError:
                nodes.append(node)
                target = i
                i += 1
            for end_node, label in zip(end_nodes, end_labels):
                end_keys = list(end_node.keys())
                end = {}
                for key in end_keys:
                    end[key] = end_node.get(key)
                end['label'] = label[0]
                try:
                    source = nodes.index(end)
                except ValueError:
                    nodes.append(end)
                    source = i
                    i += 1
                rels.append({"source": source, "target": target})
        print(nodes)
        print(rels)
        return jsonify({"nodes": nodes, "links": rels})

    # 如需批量更新功能更新这里
    def search_one(self, data):
        query = "MATCH (m) WHERE m.name=\'" + data['name'] + "\' RETURN properties(m) as node"
        results = graph.cypher.execute(query)
        #node_data = {}
        res = list(results)
        if res.__len__() == 0:
            return jsonify([''])
        else:
            for node_ori in results:
                print(node_ori['node'])
                return jsonify(node_ori['node'])

    def search_table(self, condition, limit, offset, flag="false"):
        nodes = []
        act_nodes = []
        query = "MATCH (m) WHERE (m:Movie or m:Person) RETURN m,labels(m)"
                #   "MATCH (m) WHERE m.Name CONTAINS \'" + condition + \
                #"\' and (m:项目 and m:工具 and m:工具软件) RETURN m, labels(m)"
        query_relation = "MATCH (m)<-[:ACTED_IN]-(a) WHERE m.name CONTAINS \'" + condition + "\' or a.name CONTAINS \'" + condition + \
                         "\' RETURN m, labels(m), a, labels(a)"
        print(query)
        print(query_relation)
        if flag == "false":
            results = graph.cypher.execute(query)
            for result, label in results:
                node = {}
                node["name"] = (result["name"] if label[0] == 'Person' else result["title"])
                node["label"] = label[0]
                nodes.append(node)
        elif flag == "true":
            results = graph.cypher.execute(query_relation)
            for result, label, relation, relation_label in results:
                node = {}
                node_relation = {}
                node["name"] = result["name"]
                node["label"] = label[0]
                node_relation["name"] = relation["name"]
                node_relation["label"] = relation_label[0]
                if node not in nodes:
                    nodes.append(node)
                if node_relation not in nodes:
                    nodes.append(node_relation)
        total = len(nodes)
        for i in range(int(offset), int(offset) + int(limit)):
            if i >= len(nodes):
                break
            act_nodes.append(nodes[i])
        print({'total': total, 'rows': nodes})
        return jsonify({'total': total, 'rows': act_nodes})

    def insert_table(self, start_node, relation, end_node):
        end_node_label = end_node['label']
        end_node.pop("label")
        data = ""
        for key in end_node.keys():
            data += key + ":" + "\'" + end_node[key] + "\'" + ","
        data = data.strip(",")
        check_query = "MATCH (m) WHERE m.name=\'" + end_node['name'] + "\'" \
                      + "and m:" + end_node_label + " RETURN m"
        print(check_query)
        insert_query = "MATCH (m) WHERE m.name=\'" + start_node['name'] + "\' or m.title=\'" + start_node['name'] + "\'" \
                       + "and m:" + start_node['label'] + \
                       " CREATE (n:" + end_node_label + "" + "{" + data + "})-" + \
                       "[:" + relation + "]->(m) RETURN n"
        check_result = list(graph.cypher.execute(check_query))
        if len(check_result):
            return "已经存在此节点"
        print(insert_query)
        insert_result = list(graph.cypher.execute(insert_query))
        if len(insert_result):
            return "插入成功"
        return "插入失败"

    def insert_into_table(self, start_node_first, start_node_second, relation, end_node):
        end_node_label = end_node['label']
        end_node.pop("label")
        data = ""
        for key in end_node.keys():
            data += key + ":" + "\'" + end_node[key] + "\'" + ","
        data = data.strip(",")
        check_query = "MATCH (m) WHERE m.name=\'" + end_node['name'] \
                      + "\' and m:" + end_node_label + " RETURN m"

        check_relation_query = "MATCH p = (start:" + start_node_first['label'] + \
                               ")-[r]-(end:" + start_node_second['label'] + \
                               ") WHERE start.name=\'" + start_node_first['name'] \
                               + "\' and end.name=\'" + start_node_second['name'] + "\' RETURN length(p) as length"
        remove_relation = "MATCH p = (start:" + start_node_first['label'] + \
                          ")-[r]-(end:" + start_node_second['label'] + \
                          ") WHERE start.name=\'" + start_node_first['name'] \
                          + "\' and end.name=\'" + start_node_second['name'] + "\' DELETE r"
        insert_query_first = "MATCH (m) WHERE m.name=\'" + start_node_first['name'] \
                             + "\' and m:" + start_node_first['label'] + \
                             " CREATE (n:" + end_node_label + "" + "{" + data + "})-" + \
                             "[:" + relation + "]->(m) RETURN n"
        insert_query_second = "MATCH (m) WHERE m.name=\'" + start_node_second['name'] \
                              + "\' and m:" + start_node_second['label'] + \
                              " MATCH(n) WHERE n.name=\'" + end_node['name'] + "\' and n:" + \
                              end_node_label + " CREATE (n)<-" + "[:" + relation + "]-(m) RETURN n"

        print(check_query)
        print(check_relation_query)
        print("----start---")
        print(remove_relation)
        print(insert_query_first)
        print(insert_query_second)
        print("----end----")
        check_relation_result = list(graph.cypher.execute(check_relation_query))
        if len(check_relation_result) == 0:
            return "选择的父节点之间不存在关系，插入失败"
        check_result = list(graph.cypher.execute(check_query))
        if len(check_result):
            return "已经存在此节点"
        graph.cypher.execute(remove_relation)
        insert_result_first = list(graph.cypher.execute(insert_query_first))
        insert_result_second = list(graph.cypher.execute(insert_query_second))
        if len(insert_result_first) and len(insert_result_second):
            return "插入成功"
        return "插入失败"

    def get_delete(self, deleted_data):
        try:
            for data in deleted_data:
                #print(data['fa_label'])
                delete_query = "MATCH (m) WHERE m.name=\'" + data['fa_name'] + "\'" + " or m.title=\'" + data['fa_name'] + \
                                "\' and m:" + data['fa_label'] + " DETACH DELETE m"
                print(delete_query)
                graph.cypher.execute(delete_query)
            return "删除成功"
        except:
            return "删除失败"

    def get_update(self, updated_node, node):
        data = ""
        remove_data = ""
        i = 0
        query_key = "MATCH (m) WHERE m.name=\'" + updated_node['name'] + "\' RETURN properties(m) as node"
        result_keys = graph.cypher.execute(query_key)

        node_data = {}
        for node_ori in result_keys:
            for delete_key in list(node_ori['node'].keys()):
                remove_data += "m." + delete_key + ","
        remove_data = remove_data.strip(",")
        for key in node.keys():
            if key == "label":
                data += "m:" + node[key] + ","
            else:
                data += "m." + key + "=" + "\'" + node[key] + "\'" + ","
        data = data.strip(",")
        print(data)
        print(remove_data)
        update_query = "MATCH (m)" + " WHERE m.name=\'" + updated_node['name'] + "\' " \
                       + "REMOVE " + remove_data + ",m:" + updated_node['label'] + " SET " + data
        print(update_query)
        try:
            graph.cypher.execute(update_query)
            return "更新成功"
        except:
            return "更新失败"

    def get_node(self, node_ori, label_ori):
        node_act = {}
        node_keys = list(node_ori.keys())
        for key in node_keys:
            node_act[key] = node_ori.get(key)
        node_act['label'] = label_ori[0]
        return node_act

    def get_user_graph(self):
        nodes = []
        rels = []
        i = 0
        query = "MATCH (m)<-[:Manage]-(a) RETURN properties(m) as start_node, labels(m) as labels," \
                "collect(properties(a)) as cast,collect(labels(a)) as cast_labels"
        results = graph.cypher.execute(query)
        for start_nodes, start_labels, end_nodes, end_labels in results:
            keys = list(start_nodes.keys())
            node = {}
            for key in keys:
                node[key] = start_nodes.get(key)
            node['label'] = start_labels[0]
            print(node)
            try:
                target = nodes.index(node)
            except ValueError:
                nodes.append(node)
                target = i
                i += 1
            for end_node, label in zip(end_nodes, end_labels):
                end_keys = list(end_node.keys())
                end = {}
                for key in end_keys:
                    end[key] = end_node.get(key)
                end['label'] = label[0]
                try:
                    source = nodes.index(end)
                except ValueError:
                    nodes.append(end)
                    source = i
                    i += 1
                rels.append({"source": source, "target": target})
        return jsonify({"nodes": nodes, "links": rels})

    def search_user_table(self, condition, limit, offset):
        nodes = []
        act_nodes = []
        print(condition)
        query = "MATCH (m) WHERE m.username CONTAINS \'" + condition + \
                "\' and (m:Admin or m:User) RETURN m, labels(m)"
        results = graph.cypher.execute(query)
        print(query)
        for result, label in results:
            node = {}
            node["username"] = result["username"]
            node["password"] = result["password"]
            node["label"] = label[0]
            nodes.append(node)
        total = len(nodes)
        for i in range(int(offset), int(offset) + int(limit)):
            if i >= len(nodes):
                break
            act_nodes.append(nodes[i])
        print({'total': total, 'rows': nodes})
        return jsonify({'total': total, 'rows': act_nodes})

    def search_user_graph(self, condition, flag=False):
        print(flag)
        nodes = []
        rels = []
        i = 0
        query = "MATCH (m)<-[:Manage]-(a) WHERE m.username CONTAINS \'" + condition + "\' or a.username CONTAINS \'" + condition + \
                "\' RETURN properties(m) as start_node, labels(m) as labels, " \
                "collect(properties(a)) as cast,collect(labels(a)) as cast_labels"
        query_trace = "Match (n) WHERE n.username contains \'" + condition + \
                      "\' MATCH path = shortestPath( (m:Admin)-[:Manage*..5]-(n) )" \
                      " where labels(n)='User'" \
                      " RETURN nodes(path) AS nodes, EXTRACT(node IN nodes(path) | ID(node)) AS ids " \
                      ",EXTRACT(node IN nodes(path) | labels(node)) AS labels"
        results = graph.cypher.execute(query)
        if flag == "true" and condition:
            nodes_act = []
            rels_act = []
            for node_trace, id_trace, label_trace in graph.cypher.execute(query_trace):
                j = 0
                for node_ori in node_trace:
                    node_act = {}
                    node_keys = list(node_ori.keys())
                    for key in node_keys:
                        node_act[key] = node_ori.get(key)
                    node_act['label'] = label_trace[j][0]
                    try:
                        target_act = nodes_act.index(node_act)
                        j += 1
                    except ValueError:
                        target_act = len(nodes_act)
                        nodes_act.append(node_act)
                        j += 1
                    if j < len(node_trace):
                        try:
                            source_act = nodes_act.index(self.get_node(node_trace[j], label_trace[j]))
                        except ValueError:
                            source_act = len(nodes_act)
                        rels_act.append({"source": source_act, "target": target_act})
            print(nodes_act)
            print(rels_act)
            return jsonify({"nodes": nodes_act, "links": rels_act})

        for start_nodes, start_labels, end_nodes, end_labels in results:
            print(start_nodes)
            print(end_nodes)
            keys = list(start_nodes.keys())
            node = {}
            for key in keys:
                node[key] = start_nodes.get(key)
            node['label'] = start_labels[0]
            try:
                target = nodes.index(node)
            except ValueError:
                nodes.append(node)
                target = i
                i += 1
            for end_node, label in zip(end_nodes, end_labels):
                end_keys = list(end_node.keys())
                end = {}
                for key in end_keys:
                    end[key] = end_node.get(key)
                end['label'] = label[0]
                try:
                    source = nodes.index(end)
                except ValueError:
                    nodes.append(end)
                    source = i
                    i += 1
                rels.append({"source": source, "target": target})
        print(nodes)
        return jsonify({"nodes": nodes, "links": rels})

    def insert_user_table(self, relation, end_node):
        end_node_label = end_node['label']
        end_node.pop("label")
        data = ""
        for key in end_node.keys():
            data += key + ":" + "\'" + end_node[key] + "\'" + ","
        data = data.strip(",")
        check_query = "MATCH (m) WHERE m.username=\'" + end_node['username'] \
                      + "\' RETURN m"
        insert_query = " CREATE (n:" + end_node_label + "" + "{" + data + "}) RETURN n"
        user_relation_query = 'MATCH (admin:Admin) MATCH(user:User {username:\'' + \
                              end_node['username'] + '\'}) CREATE (admin)-[manage:Manage]->(user)'
        insert_admin_query = " CREATE (n:" + end_node_label + "" + "{" + data + "}) RETURN n"
        admin_relation_query = 'MATCH (user:User) MATCH(admin:Admin {username:\'' + \
                               end_node['username'] + '\'}) CREATE (admin)-[manage:Manage]->(user)'
        check_result = list(graph.cypher.execute(check_query))
        print(insert_admin_query)
        if len(check_result) :
            return "已经存在此节点"
        if end_node_label == 'Admin':
            insert_admin_result = list(graph.cypher.execute(insert_admin_query))
            graph.cypher.execute(admin_relation_query)
            if len(insert_admin_result):
                return "插入成功"
        else:
            insert_result = list(graph.cypher.execute(insert_query))
            graph.cypher.execute(user_relation_query)
            if len(insert_result):
                return "插入成功"
        return "插入失败"

    def get_delete_user(self, deleted_data):
        try:
            for data in deleted_data:
                print(data['fa_label'])
                delete_query = "MATCH (m) WHERE m.username=\'" + data['fa_name'] \
                               + "\' and m:" + data['fa_label'] + " DETACH DELETE m"
                print(delete_query)
                graph.cypher.execute(delete_query)
            return "删除成功"
        except:
            return "删除失败"

    def update_password(self, data):
        query_user = "MATCH (m) WHERE m.username=\'" + data['username'] \
                     + "\' RETURN m.password as password"
        query_update = "MATCH (m) WHERE m.username=\'" + data['username'] \
                       + "\' SET m.password=\'" + bcrypt.encrypt(data['inpassword']) + "\'"
        print(query_user)
        for i in graph.cypher.execute(query_user):
            if not bcrypt.verify(data['oripassword'], i['password']):
                return "原密码错误"
        try:
            graph.cypher.execute(query_update)
            return "修改成功"
        except:
            return "修改失败"

    def batch_insert(self, start_node, file_name):
        print(file_name)
        print(start_node)
        # 打开文件
        workbook = xlrd.open_workbook(file_name)
        # 获取所有sheet

        # 根据sheet索引或者名称获取sheet内容
        sheet1 = workbook.sheet_by_index(0)  # sheet索引从0开始
        rows = sheet1.nrows
        cols = sheet1.ncols
        try:
            for row in range(rows):
                end_node = {}
                relation = ""
                if row == 0:
                    continue
                for col in range(cols):
                    if sheet1.row(0)[col].value == "relation":
                        relation = sheet1.row(row)[col].value
                    else:
                        if not sheet1.row(row)[col].value == "":
                            end_node[sheet1.row(0)[col].value] = sheet1.row(row)[col].value
                self.insert_table(start_node, relation, end_node)
        except:
            return "执行失败"
        return "执行成功"

    def get_advance_query(self, data):
        query_condition = data['query_condition']
        query_way = data['query_way']
        query_level = data['query_level']
        query = "Match (m) WHERE m.name contains \'" + query_condition + \
                "\' MATCH path = shortestPath( (m)<-[*.." + query_level \
                + "]-(n) ) where n.name <> m.name and (labels(n) = 'Sort' or labels(n) = 'GOODS')" \
                  " RETURN nodes(path) AS nodes, EXTRACT(node IN nodes(path) | ID(node)) AS ids " \
                  ",EXTRACT(node IN nodes(path) | labels(node)) AS labels"
        query_trace = "Match (n) WHERE n.name contains \'" + query_condition + \
                      "\' MATCH path = shortestPath( (m)<-[*.." + query_level \
                      + "]-(n) ) where n.name <> m.name and (labels(m) = 'Sort' or labels(m) = 'Website')" \
                        " RETURN nodes(path) AS nodes, EXTRACT(node IN nodes(path) | ID(node)) AS ids " \
                        ",EXTRACT(node IN nodes(path) | labels(node)) AS labels"
        print(query)
        print(query_trace)
        if query_way == "溯源查询":
            nodes_act = []
            rels_act = []
            for node_trace, id_trace, label_trace in graph.cypher.execute(query_trace):
                j = 0
                print(node_trace)
                for node_ori in node_trace:
                    node_act = {}
                    node_keys = list(node_ori.keys())
                    for key in node_keys:
                        node_act[key] = node_ori.get(key)
                    print(label_trace[j])
                    node_act['label'] = label_trace[j][0]
                    try:
                        target_act = nodes_act.index(node_act)
                        j += 1
                    except ValueError:
                        target_act = len(nodes_act)
                        nodes_act.append(node_act)
                        j += 1
                    if j < len(node_trace):
                        try:
                            source_act = nodes_act.index(self.get_node(node_trace[j], label_trace[j]))
                        except ValueError:
                            source_act = len(nodes_act)
                        rels_act.append({"source": source_act, "target": target_act})
            print(nodes_act)
            print(rels_act)
            return jsonify({"nodes": nodes_act, "links": rels_act})
        elif query_way == "子节点查询":
            nodes = []
            rels = []
            for node_chlid, id_chlid, label_chlid in graph.cypher.execute(query):
                j = 0
                for node_ori in node_chlid:
                    node_act = {}
                    node_keys = list(node_ori.keys())
                    for key in node_keys:
                        node_act[key] = node_ori.get(key)
                    node_act['label'] = label_chlid[j][0]
                    try:
                        target_act = nodes.index(node_act)
                        j += 1
                    except ValueError:
                        target_act = len(nodes)
                        nodes.append(node_act)
                        j += 1
                    if j < len(node_chlid):
                        try:
                            source_act = nodes.index(self.get_node(node_chlid[j], label_chlid[j]))
                        except ValueError:
                            source_act = len(nodes)
                        rels.append({"source": source_act, "target": target_act})
            print(nodes)
            print(rels)
            return jsonify({"nodes": nodes, "links": rels})
