import os
import shutil
import zipfile
import urllib.request
import pickle
import numpy as np
from . import functiontest

from pyairtable import Table

# import importlib

# importlib.reload(function_test)

PICKLE_PATH = '.pickle'


class CourseInfo():
    def __init__(self, title, uid, group_id=None, version=1):
        self.info = {
            'title': title, 
            'uid': uid,
            'version': version,
            'group_id': group_id,
        }
    
    def __call__(self, *args, **kwds):
        return self.info


class FileManager():
    def __init__(self, course_info: CourseInfo, user_name, group_id=None, debug=False, pickle_path='.pickle'):
        self.api_token = 'patON4DhGmQLQjdEr.37865a577686d067523f2c914cdfab5e45a9f8f81b32cf8b62fcf7cb163a9dc0'
        self.base_id = 'appLgpuFIEfGhsjhw'
        self.table_name = 'tblUsF3BQhKCpZ6K7'
        self.status_table_name = 'tblndjREiQtdkjd7q'
        
        self.course_info = course_info
        self.debug = debug
        self.pickle_path = pickle_path
        self.user_name = user_name
        self.group_id = group_id
        # 폴더 생성
        if not os.path.isdir(pickle_path):
            os.mkdir(pickle_path)
            
        self.table = Table(self.api_token, self.base_id, self.table_name)
        self.status_table = Table(self.api_token, self.base_id, self.status_table_name)
        
    def save_pickle(self, data, filename, pickle_path='.pickle'):
        # pickle 파일로 저장
        pkl_filename = os.path.join(pickle_path, f"{filename}.pkl")
        with open(pkl_filename,'wb') as f:
            pickle.dump(data, f)
        if self.debug:
            print(pkl_filename, 'Saved.')            
        return pkl_filename

    def load_pickle(self, filename, pickle_path='.pickle'):
        with open(os.path.join(pickle_path, f'{filename}.pkl'),'rb') as f:
             data = pickle.load(f)
        return data
    
    def create_filename(self, question_no: int):
        info = self.course_info()
        return f"{info['title'].lower()}-{info['uid'].lower()}-ver-{info['version']:02d}-question-{question_no:02d}"
    
    def save_answer(self, answer, question_no, type='value'):
        filename = self.create_filename(question_no=question_no)
        self.save_pickle(answer, filename=filename)
        print(f'[SAVED] {filename}')
    
    def load_answer(self, question_no, type='value'):
        filename = self.create_filename(question_no=question_no)
        return self.load_pickle(filename=filename)
    
    def get_download_url(self):
        rows = self.table.all(sort=['id'])
        download_url = None
        info = self.course_info()
        for r in rows:
            fields = r['fields']
            if 'uid' in fields:
                if fields['uid'].lower() == info['uid'].lower():
                    download_url = fields['download_url']
                    break
        return download_url
    
    def download_answers(self):
        url = self.get_download_url()
        if url:
            info = self.course_info()
            filename = f"{info['title'].lower()}-{info['uid'].lower()}-ver-{info['version']:02d}.zip"
            urllib.request.urlretrieve(url, filename)
            zip_ref = zipfile.ZipFile(filename, 'r')
            zip_ref.extractall(self.pickle_path)
            zip_ref.close()

            os.remove(filename)
            return True
        else:
            return False
        
    def update_status(self, q):
        if self.user_name:
            info = self.course_info()
            group_id = info['group_id']
            if group_id:
                self.status_table.create({'name': self.user_name, 'uid': info['uid'].lower(), 'q': q, 'group_id': info['group_id']})
            else:
                self.status_table.create({'name': self.user_name, 'uid': info['uid'].lower(), 'q': q, 'group_id': 'solo'})
    
    def create_answer_zip(self):
        info = self.course_info()
        pickle_files = [f for f in os.listdir(self.pickle_path) if f.endswith('pkl')]
        files = sorted([f for f in pickle_files if info['uid'].lower() in f])

        for f in os.listdir(self.pickle_path):
            if f not in files:
                os.remove(os.path.join(self.pickle_path, f))
                
        shutil.make_archive(f"{info['title'].lower()}-{info['uid'].lower()}-ver-{info['version']:02d}", 'zip', self.pickle_path)
     
    
class Grade():
    def __init__(self):
        pass
    
    # def check_type(self, value):
    #     if type(value) == 
    #     return 'TYPE_VALUE'
    
    def compare_value(self, val1, val2):
        if type(val1) != type(val2):
            return False
        return val1 == val2

    def compare_dataframe(self, df1, df2, sample_case_count=10):
        if df1.shape != df2.shape:
            return False
        else:
            for s in range(sample_case_count):
                row = np.random.randint(df1.shape[0])
                col = np.random.randint(df1.shape[1])
                if df1.iloc[row, col] != df2.iloc[row, col]:
                    return False
                
        return True
    
    def get_python_testcase(self, uid, q):
        test_case = functiontest.get_python_testcase(uid.lower(), q)
        return test_case
    
    def check_testcase(self, func, samples):
        length = len(samples['args'])
        for i in range(length):
            if type(samples['args'][i]) == tuple:
                ret = func(*samples['args'][i])
                if ret != samples['return'][i]:
                    return False
            elif type(samples['args'][i]) == dict:
                ret = func(**samples['args'][i])
                if ret != samples['return'][i]:
                    return False
            else:
                ret = func(samples['args'][i])
                if ret != samples['return'][i]:
                    return False
        return True
        


grade = None
file = None
info = None


def init(title, uid, group_id=None, version=1, mode='quiz'):
    global grade, file, info
    
    while True:
        user_name = input('이름을 입력하세요: ')
        if user_name == '':
            print('[에러] 이름은 공백일 수 없습니다.')
        else:
            break
    
    if group_id is not None:
        group_id = group_id.lower()
        
    print(f'{user_name} 님 반갑습니다😀')
    print(f'그룹ID: {group_id}')
    # print()
    # print('[주의사항]')
    # print('- 비윤리적인 닉네임은 예고없이 삭제될 수 있어요😡')
    # print('- 제출 기록은 아래 주소에서 확인해 주세요😆')
    # print('https://pycodegrade-web.herokuapp.com/')
    # print()
    # print('- 문의/오류제보: teddylee777@gmail.com')
        
    # if not info:
    info = CourseInfo(title=title, uid=uid, group_id=group_id, version=version)
    
    if info:
        file = FileManager(course_info=info, user_name=user_name, group_id=group_id, debug=False)
        if mode == 'quiz':
            file.download_answers()         
        
    grade = Grade()
    

def check_answer(user_ans, question_no, type='value'):
    global grade, file, info
    if grade and file:
        if type == 'value':
            ans = file.load_answer(question_no, type='value')
            if grade.compare_value(user_ans, ans):
                file.update_status(question_no)
                print('Result: [PASS]')
            else:
                print('Result: [FAIL]')
        elif type == 'function':
            info_ = info()
            uid = info_['uid']
            samples = grade.get_python_testcase(uid.lower(), question_no)
            ret = grade.check_testcase(user_ans, samples)
            if ret:
                file.update_status(question_no)
                print('Result: [PASS]')
            else:
                print('Result: [FAIL]')
            
def get_file_manager():
    return file