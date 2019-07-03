from flask import Flask,render_template,flash,redirect,request,session
from flask_uploads import UploadSet,IMAGES,configure_uploads
from excel_operate import *
import os

app = Flask(__name__)
app.config.from_object('config')

#1. 这个东西是用来存储文件的，当用户上传到同名文件的时候，可以自动加后缀
#2. app要配置UPLOADED_FILE_DEST 属性，指出操作文件的目录在哪 其中'FILE' 与下面的'FILE'对应
files_operator = UploadSet('FILE')
# 这个是让files_operator具有操作文件的权限
configure_uploads(app,files_operator)

@app.route('/')
def main_page():
    # dict操作 如果不存在这个key就pop None, 避免报错
    session.pop('upload_files',None)
    session.pop('store_keys',None)
    session.pop('select_keys',None)
    return render_template('index.html')

@app.route('/combine_excel.html',methods=['GET','POST'])
def excel_operat():
    
    store_keys=[]
    select_keys=[]
    fm = file_manager('tmp_files')
    if 'upload_files' in session:
        fm.add(array=session['upload_files'])
    if 'store_keys' in session:
        store_keys = session['store_keys']
    if 'select_keys' in session:
        select_keys = session['select_keys']

    result_url=None
    if request.method == "POST":
        post_message = request.form
        if post_message.get('insert', None):
            for storage in request.files.getlist('upload_file',None):
                save_loc = files_operator.save(storage,'tmp_files')
                fm.add(file=storage.filename,loc=save_loc)
                session['upload_files'] = fm.all()
        elif post_message.get('generate', None):
            select_index = post_message.getlist('check_box_list', None)
            tmp_select = [store_keys[int(index)] for index in select_index]
            select_keys.extend(tmp_select)
            session['select_keys'] = select_keys
        elif post_message.get('done', None):
            if select_keys:
                # file_url = [f[1] for f in upload_files]
                file_url = fm.locs()
                result_file = write_file_by_keys(file_url, select_keys)
                result_url = files_operator.url(result_file)
        elif post_message.get('clear', None):
            for file in os.listdir('static'):
                if '.xlsx' in file:
                    os.remove(os.path.join('tmp_files', file))
            fm.sync()
            store_keys.clear()
            select_keys.clear()
        elif post_message.get('delete',None):
            select_index = post_message.getlist('check_box_list',None)
            select_index = [int(s) for s in select_index]
            fm.rm(select_index)
            
        elif post_message.get('delete_property',None):
            select_index = post_message.getlist('check_box_list',None)
            select_index = [int(s) for s in select_index]
            select_keys= [select_keys[i] for i in range(len(select_keys)) if i not in select_index]
        elif post_message.get('comfirm_chart',None):
            store_keys = []
            file_url = fm.locs()
            for file in file_url:
                for sheet in get_visible_names(file):
                    store_keys = store_keys + get_keys(file, sheet)
                    store_keys = list(set(store_keys))
            session['store_keys'] = store_keys
    
    context = dict({'use_keys': select_keys, 'valid_keys': store_keys, 'files': fm.files(),'result_file':result_url})
    return render_template('combine_excel.html',**context)

class file_manager:
    def __init__(self,folder=None):
        self.upload_files = []
        # 如果指定了folder就看这个下面有哪些文件，文件结构应该与upload_files保持一致
        self.folder = folder
        self.sync()
    def sync(self):
        if self.folder:
            for file in os.listdir(self.folder):
                if '.xlsx' in file and file in self.locs():
                    os.remove(os.path.join(self.folder, file))
            
    def add(self,file=None,loc=None,array=None):
        if file and loc:
            self.upload_files.append([file,loc])
        if array:
            self.upload_files.extend(array)
    def clear(self):
        for f in self.upload_files:
            os.remove(f[1])
        self.upload_files.clear()
    def files(self):
        return [f[0] for f in self.upload_files]
    def locs(self):
        return [f[1] for f in self.upload_files]
    def all(self):
        return self.upload_files
    def rm(self,index):
        self.upload_files = [self.upload_files[i] for i in range(len(self.upload_files)) if i not in index]
        self.sync()
        
if __name__ == '__main__':
    app.run(debug=True)
