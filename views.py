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
upload_files = []
upload_file_names =[]
store_keys = []
select_keys = []

@app.route('/')
@app.route('/index',methods=['GET','POST'])
def excel_operat():
    done = False
    
    global store_keys
    global upload_files
    global upload_file_names
    global select_keys
    
    if request.method == "POST":
        post_message = request.form
        if post_message.get('insert', None):
            excel_f = request.files['upload_file']
            file_name = excel_f.filename
            write_url = os.path.join('static', file_name)
            excel_f.save(write_url)
            excel_f.flush()
            upload_file_names.append(file_name)
            upload_files.append(write_url)
            for sheet in get_visible_names(write_url):
                store_keys = store_keys + get_keys(write_url, sheet)
                store_keys = list(set(store_keys))
                    # if session_keys:
                    #     session_keys.extend(get_keys(write_url, sheet))
                    # request.session['store_keys']=store_keys
        elif post_message.get('generate', None):
            select_index = post_message.getlist('check_box_list', None)
            tmp_select = [store_keys[int(index)] for index in select_index]
            select_keys.extend(tmp_select)
        elif post_message.get('done', None):
            if select_keys:
                write_file_by_keys(upload_files, select_keys)
                done = True
        elif post_message.get('clear', None):
            for file in os.listdir('static'):
                if '.xlsx' in file:
                    os.remove(os.path.join('static', file))
            upload_files.clear()
            upload_file_names.clear()
            store_keys.clear()
            select_keys.clear()
    
    # if request.method == 'POST' and request.POST.has_key('done'):
    # 第一步解析用户上传的excel的keys
    # 使用context传递信息
    context = dict({'use_keys': select_keys, 'valid_keys': store_keys, 'done': done, 'files': upload_file_names})
    # return render(request, 'index.html', context)
    return render_template('index.html',**context)
