import os, json
# flask --app hello run
# flask --app flaskr run --debug

# {{ url_for('static', filename='style.css') }}
# {{ url_for('static', filename='script.js') }}

from flask import Flask, render_template, request, g, escape, redirect, url_for
from syllabus_gen import *
from doc_sum import *
from note_gen import *
from utils import *
from test_companion import *


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    app.static_folder = 'static'

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    def get_chatcomp():
        messages = getattr(g, '_chatcompletion', None)
        if messages is None:
            g._chatcompletion = create_chat_object('/Users/zain/Desktop/api_key.txt')

        return g._chatcompletion

    # a simple page that says hello
    @app.route('/notegen')
    def notegen():
        return render_template('notegen.html')
    @app.route('/testgen')
    def testgen():
        return render_template('testgen.html')

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route("/notegen", methods=['POST','GET'])
    def move_forward():
        chatcomp = get_chatcomp()

        if request.method == 'POST':
            print(request.form)

            at_level = request.form['level']
            subject = request.form['subject']
            prompt_req = request.form['prompt_req']

            # formatted_req = indented_string_to_dict(prompt_req)
            prompt_req = json.loads(prompt_req)
            ret = note_generator(chatcomp,
                           prompt_req, at_level, subject)
            # ret = 'hellow how to do'

            # print(prompt_req)
            # print(at_level, subject, prompt_req)

            final_ret = []
            # ind_level = 0

            # print(ret)

            for line in ret.strip().split('\n'):
                if len(line) > 0 and line[-1] == ':':
                    # temp_ind = max(0, ind_level - 1)
                    final_ret.append('<b>' + line + '</b><br/>')
                    # ind_level = 1
                    continue
                print(line)
                final_ret.append('     ' + line + '<br/>')

            final_ret = ' '.join(final_ret)

            print(final_ret)
            
            return final_ret
            # render_template('notegen.html', forward_message=final_ret)
        else:
            return ''
            # render_template('notegen.html')
    
    # @app.route('/docsummarizer')
    # def docummari():
    #     return render_template('docsummarizer.html')

    @app.route("/about", methods=['POST','GET'])
    def about_func():
        return render_template('about.html')

    @app.route("/docsummarizer", methods=['POST','GET'])
    def summarize_doc():
        chatcomp = get_chatcomp()

        if request.method == 'POST':
            prompt = request.form['prompt_req']

            file_content = parse_pdf_from_flask_object(request.files.get('fileUpload'))

            ret = generate_summary(chatcomp, file_content, prompt, 700)

            return render_template('docsummarizer.html', returned=ret)
        else:
            return render_template('docsummarizer.html')
    
    @app.route("/syllabusinfo", methods=['POST','GET'])
    def syllabusinfo():
        chatcomp = get_chatcomp()
        if request.method == 'POST':
            file_content = parse_pdf_from_flask_object(request.files.get('fileUpload'))

            ret = generate_syllabus(chatcomp, file_content)

            final_ret = []

            for line in ret.strip().split('\n'):
                if len(line) > 0 and line[-1] == ':':
                    final_ret.append('<b>' + line + '</b><br/>')
                    continue
                final_ret.append('     ' + line + '<br/>')

            final_ret = ' '.join(final_ret)

            return render_template('syllabusinfo.html', returned=final_ret)
        else:
            return render_template('syllabusinfo.html')
    

    @app.route("/testgen", methods=['POST','GET'])
    def testgenf():
        chatcomp = get_chatcomp()

        if request.method == 'POST':
            at_level = request.form['level']
            diff = request.form['diff']
            subject = request.form['subject']
            topic = request.form['topic']
            num_qs = request.form['numqs']

            ret = generate_questions(chatcomp,
                           at_level, subject, topic, diff, num_qs)

            # at_level = 'College'
            # diff = 'Hard'
            # subject = 'Mathematics'
            # topic = 'FTC'
            # num_qs = '10'

            # ret = {'question1': 'answer1'}
            
            return ret
            # render_template('notegen.html', forward_message=final_ret)
        else:
            return ''
            # render_template('notegen.html')
    

    @app.route("/testgen/grade_answer", methods=['POST','GET'])
    def gradeans():
        chatcomp = get_chatcomp()

        if request.method == 'POST':
            question = request.form['question']
            provided = request.form['myans']
            expected = request.form['expected']

            ret = grade_answer(chatcomp, question, provided, expected)
            
            return ret
            # render_template('notegen.html', forward_message=final_ret)
        else:
            return ''
            # render_template('notegen.html')


    return app
