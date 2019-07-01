from flask import render_template,flash,redirect
from app import app
import os
from flask import request
from excel_operate import *
# import forms


# @app.route('/login',methods=['GET','POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
#         return redirect('/index')
#
#     return render_template('login.html',title='Sign In',form=form,
#                            providers=app.config['OPENID_PROVIDERS']
#                            )
upload_file_names = []

store_keys = []
select_keys = []

@app.route('/')
@app.route('/index',methods=['GET','POST'])
def excel_operat():
    done = False
    
    global store_keys
    global upload_file_names
    global select_keys
    
    if request.method == "POST":
        post_message = request.form
        if post_message.get('insert', None):
            excel_f = request.files.getlist('upload_file',None)
            for up in excel_f:
                file_name = up.filename
                if not file_name:
                    continue
                write_url = os.path.join('static', file_name)
                up.save(write_url)
                up.flush()
                upload_file_names.append(file_name)
                # for sheet in get_visible_names(write_url):
                #     store_keys = store_keys + get_keys(write_url, sheet)
                #     store_keys = list(set(store_keys))
                    # if session_keys:
                    #     session_keys.extend(get_keys(write_url, sheet))
                    # request.session['store_keys']=store_keys
        elif post_message.get('generate', None):
            select_index = post_message.getlist('check_box_list', None)
            tmp_select = [store_keys[int(index)] for index in select_index]
            select_keys.extend(tmp_select)
        elif post_message.get('done', None):
            if select_keys:
                file_url = [os.path.join('static',file_name) for file_name in upload_file_names]
                write_file_by_keys(file_url, select_keys)
                done = True
        elif post_message.get('clear', None):
            for file in os.listdir('static'):
                if '.xlsx' in file:
                    os.remove(os.path.join('static', file))
            upload_file_names.clear()
            store_keys.clear()
            select_keys.clear()
        elif post_message.get('delete',None):
            select_index = post_message.getlist('check_box_list',None)
            select_index = [int(s) for s in select_index]
            upload_file_names = [upload_file_names[i] for i in range(len(upload_file_names)) if i not in select_index]
        elif post_message.get('delete_property',None):
            select_index = post_message.getlist('check_box_list',None)
            select_index = [int(s) for s in select_index]
            select_keys= [select_keys[i] for i in range(len(select_keys)) if i not in select_index]
        elif post_message.get('comfirm_chart',None):
            store_keys = []
            file_url = [os.path.join('static', file_name) for file_name in upload_file_names]
            for file in file_url:
                for sheet in get_visible_names(file):
                    store_keys = store_keys + get_keys(file, sheet)
                    store_keys = list(set(store_keys))
            
            
    
    # if request.method == 'POST' and request.POST.has_key('done'):
    # 第一步解析用户上传的excel的keys
    # 使用context传递信息
    context = dict({'use_keys': select_keys, 'valid_keys': store_keys, 'done': done, 'files': upload_file_names})
    # return render(request, 'index.html', context)
    return render_template('index.html',**context)
