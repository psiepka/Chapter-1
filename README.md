<h1>DRF - Exam sheet example</h1>
<p>An example Django REST framework application.</p>

<strong><small>Required python 3.7.0+</small></strong>

<hr>
<h3>API Endpoints</h3>

<b>Users:</b>
<ul>
    <li>
        <b>/auth/login/</b> - login to app <br>
        <small>Users avaiable after load fixtures:
            <ul>
                <li>
                    username:'User_1'<br>
                    password: 'pass'
                </li>
                <li>
                    username:'User_2'<br>
                    password: 'pass'
                </li>
                <li>
                    username:'User_3'<br>
                    password: 'pass'
                </li>
            </ul>
        </small>
    </li>
    <li>
        <b>/auth/logout/</b> - logout from app
    </li>
</ul>

<b>Exams:</b>
<ul>
    <li>
        <b>GET POST /exams/</b> - list of all not archives exams in app
        <ul>
            <li>
                POST (example)
            </li>
            <pre>
                {
                    'title':'Example title exam',
                    'topic':'Example topic exam'
                }
            </pre>
            <li>
                GET (example)
            </li>
            <pre>
                [
                    {
                        "url": "http://127.0.0.1:8000/exams/18/",
                        "id": 18,
                        "examiner": "User_1",
                        "title": "Last exam number 3",
                        "topic": "Building",
                        "created_in": "2019-03-07T08:26:09.620000+01:00",
                        "avaiable": false,
                        "test": "http://127.0.0.1:8000/exams/18/test/",
                        "answered": true,
                        "checking": false,
                        "judged": true,
                        "result": "http://127.0.0.1:8000/exams/18/result/",
                        "archivized": false,
                        "archivized_in": null
                    },
                    {
                        "url": "http://127.0.0.1:8000/exams/19/",
                        "id": 19,
                        "examiner": "User_2",
                        "title": "Exam number 4, still going",
                        "topic": "Personal",
                        "created_in": "2019-03-07T08:20:47.348000+01:00",
                        "avaiable": true,
                        "test": "http://127.0.0.1:8000/exams/19/test/",
                        "answered": true,
                        "checking": false,
                        "judged": false,
                        "result": "http://127.0.0.1:8000/exams/19/result/",
                        "archivized": false,
                        "archivized_in": null
                    },
                ]
            </pre>
        </ul>
    </li>
    <li>
        <b>GET /exams/archives/</b> - list of all archives exams in app
        <ul>
            <li>
                GET (example)
            </li>
            <pre>
                [
                    {
                        "url": "http://127.0.0.1:8000/exams/21/",
                        "id": 21,
                        "examiner": "User_1",
                        "title": "Archivum 002",
                        "topic": "Nothing here",
                        "created_in": "2019-03-07T08:52:58.900000+01:00",
                        "avaiable": false,
                        "test": "http://127.0.0.1:8000/exams/21/test/",
                        "answered": false,
                        "checking": false,
                        "judged": false,
                        "result": "http://127.0.0.1:8000/exams/21/result/",
                        "archivized": true,
                        "archivized_in": "2019-03-07T08:52:12.286000+01:00"
                    },
                    {
                        "url": "http://127.0.0.1:8000/exams/20/",
                        "id": 20,
                        "examiner": "User_2",
                        "title": "Archivum X",
                        "topic": "Secret",
                        "created_in": "2019-03-07T03:00:34.860000+01:00",
                        "avaiable": false,
                        "test": "http://127.0.0.1:8000/exams/20/test/",
                        "answered": false,
                        "checking": false,
                        "judged": false,
                        "result": "http://127.0.0.1:8000/exams/20/result/",
                        "archivized": true,
                        "archivized_in": "2019-03-07T03:00:34.860000+01:00"
                    }
                ]
            </pre>
        </ul>
    </li>
    <li>
        <b>GET /exams/results/</b> - list of all results of users exams in app
        <ul>
            <li>
                GET (example)
            </li>
            <pre>
                [
                    {
                        "exam": "Exam number 2",
                        "student": "User_1",
                        "grade": 2,
                        "exam_id": "http://127.0.0.1:8000/exams/17/result/"
                    },
                    {
                        "exam": "Exam number 2",
                        "student": "User_3",
                        "grade": 5,
                        "exam_id": "http://127.0.0.1:8000/exams/17/result/"
                    },
                ]
            </pre>
        </ul>
    </li>
    <li>
        <b>GET PUT /exams/&lt;pk&gt;/</b> - detail of exam (only author of exam can access)
        <ul>
            <li>
                PUT (example)
            </li>
            <pre>
                {
                    "id": 19,
                    "title": "Exam number 4, still going",
                    "topic": "Personal",
                    "exam_questions": [
                        {
                            "id": 78,
                            "question_text": "Whats your favorite meal?",
                            "max_points": 0.7
                        },
                        {
                            "id": 79,
                            "question_text": "Tomato or potato?",
                            "max_points": 100.0
                        },
                        {
                            "id": 83,
                            "question_text": "Do you like Pepsi light?",
                            "max_points": 20.0
                        }
                    ]
                }
            </pre>
            <li>
                GET (example)
            </li>
            <pre>
                {
                    "url": "http://127.0.0.1:8000/exams/19/",
                    "id": 19,
                    "examiner": "User_2",
                    "title": "Exam number 4, still going",
                    "topic": "Personal",
                    "created_in": "2019-03-07T08:20:47.348000+01:00",
                    "avaiable": true,
                    "test": "http://127.0.0.1:8000/exams/19/test/",
                    "answered": true,
                    "assesments": "http://127.0.0.1:8000/exams/19/assesment/",
                    "checking": false,
                    "set_grades": "http://127.0.0.1:8000/exams/19/results/",
                    "judged": false,
                    "archivized": false,
                    "archivized_in": null,
                    "exam_questions": [
                        {
                            "id": 78,
                            "question_text": "Whats your favorite meal?",
                            "max_points": 0.7
                        },
                        {
                            "id": 79,
                            "question_text": "Tomato or potato?",
                            "max_points": 100.0
                        },
                        {
                            "id": 83,
                            "question_text": "Do you like Pepsi light?",
                            "max_points": 20.0
                        }
                    ]
                }
            </pre>
        </ul>
    </li>
    <li>
        <b>GET PUT /exams/&lt;pk&gt;/test/</b> - test of exam for students (student can access only when exam.avaiable == True)
        <ul>
            <li>
                PUT (example)
            </li>
            <pre>
                {
                    "examiner": "User_2",
                    "title": "Exam number 4, still going",
                    "topic": "Personal",
                    "exam_questions": [
                        {
                            "id": 78,
                            "question_text": "Whats your favorite meal?",
                            "max_points": 0.7,
                            "question_anwsers": [
                                {
                                    "answer_text": "MEAT"
                                }
                            ]
                        },
                    ]
                }
            </pre>
            <li>
                GET (example)
            </li>
            <pre>
                {
                    "examiner": "User_2",
                    "title": "Exam number 4, still going",
                    "topic": "Personal",
                    "exam_questions": [
                        {
                            "id": 78,
                            "question_text": "Whats your favorite meal?",
                            "max_points": 0.7,
                            "question_anwsers": []
                        },
                        {
                            "id": 79,
                            "question_text": "Tomato or potato?",
                            "max_points": 100.0,
                            "question_anwsers": []
                        },
                        {
                            "id": 83,
                            "question_text": "Do you like Pepsi light?",
                            "max_points": 20.0,
                            "question_anwsers": []
                        }
                    ]
                }
            </pre>
        </ul>
    </li>
    <li>
        <b>GET PUT /exams/&lt;pk&gt;/assesment</b> - assesment of students exams answers (only author of exam can access)
        <ul>
            <li>
                PUT (example)
            </li>
            <pre>
                {
                    "url": "http://127.0.0.1:8000/exams/19/",
                    "id": 19,
                    "examiner": "User_2",
                    "title": "Exam number 4, still going",
                    "topic": "Personal",
                    "created_in": "2019-03-07T08:20:47.348000+01:00",
                    "avaiable": true,
                    "answered": true,
                    "checking": false,
                    "judged": false,
                    "archivized": false,
                    "archivized_in": null,
                    "exam_questions": [
                        {
                            "id": 78,
                            "question_text": "Whats your favorite meal?",
                            "max_points": 0.7,
                            "question_anwsers": [
                                {
                                    "id": 21,
                                    "student": 15,
                                    "answer_text": "Pizza",
                                    "answer_assesments": {
                                        "commentary": "Nice one",
                                        "points": 0.7
                                },
                            ]
                        },
                    ]
                }
            </pre>
            <li>
                GET (example)
            </li>
            <pre>
                {
                    "url": "http://127.0.0.1:8000/exams/19/",
                    "id": 19,
                    "examiner": "User_2",
                    "title": "Exam number 4, still going",
                    "topic": "Personal",
                    "created_in": "2019-03-07T08:20:47.348000+01:00",
                    "avaiable": true,
                    "answered": true,
                    "checking": false,
                    "judged": false,
                    "archivized": false,
                    "archivized_in": null,
                    "exam_questions": [
                        {
                            "id": 78,
                            "question_text": "Whats your favorite meal?",
                            "max_points": 0.7,
                            "question_anwsers": [
                                {
                                    "id": 21,
                                    "student": 15,
                                    "answer_text": "Pizza",
                                    "answer_assesments": null
                                },
                                {
                                    "id": 24,
                                    "student": 13,
                                    "answer_text": "Nope",
                                    "answer_assesments": null
                                }
                            ]
                        },
                        {
                            "id": 79,
                            "question_text": "Tomato or potato?",
                            "max_points": 100.0,
                            "question_anwsers": [
                                {
                                    "id": 22,
                                    "student": 15,
                                    "answer_text": "Definitely Potato",
                                    "answer_assesments": null
                                },
                                {
                                    "id": 25,
                                    "student": 13,
                                    "answer_text": "yep",
                                    "answer_assesments": null
                                }
                            ]
                        },
                        {
                            "id": 83,
                            "question_text": "Do you like Pepsi light?",
                            "max_points": 20.0,
                            "question_anwsers": [
                                {
                                    "id": 23,
                                    "student": 13,
                                    "answer_text": "Nope",
                                    "answer_assesments": null
                                }
                            ]
                        }
                    ]
                }
            </pre>
        </ul>
    </li>
    <li>
        <b>GET PUT /exams/&lt;pk&gt;/results</b> - list of results students assesments (only author of exam can access)
        <ul>
            <li>
                PUT (example)
            </li>
            <pre>
                {
                    "id": 19,
                    "results": [
                        {
                            "id": 6,
                            "overall_max_points": 10,
                            "scored_points": 0,
                            "grade": 1,
                            "exam": 19,
                            "student": 13
                        },
                        {
                            "id": 9,
                            "overall_max_points": 10,
                            "scored_points": 10,
                            "grade": 5,
                            "exam": 19,
                            "student": 15
                        }
                    ]
                }
            </pre>
            <li>
                GET (example)
            </li>
            <pre>
                {
                    "id": 19,
                    "title": "Exam number 4, still going",
                    "topic": "Personal",
                    "created_in": "2019-03-07T08:20:47.348000+01:00",
                    "avaiable": true,
                    "answered": true,
                    "judged": false,
                    "archivized": false,
                    "results": [
                        {
                            "id": 6,
                            "overall_max_points": 10,
                            "scored_points": 0,
                            "grade": null,
                            "exam": 19,
                            "student": 13
                        },
                        {
                            "id": 9,
                            "overall_max_points": 10,
                            "scored_points": 10,
                            "grade": null,
                            "exam": 19,
                            "student": 15
                        }
                    ]
                }
            </pre>
        </ul>
    </li>
    <li>
        <b>GET /exams/&lt;pk&gt;/result</b> - student result with details (student can access only when exam.judged == True)
        <ul>
            <li>
                GET (example)
            </li>
            <pre>
                {
                    "id": 18,
                    "examiner": "User_1",
                    "title": "Last exam number 3",
                    "topic": "Building",
                    "created_in": "2019-03-07T08:26:09.620000+01:00",
                    "avaiable": false,
                    "answered": true,
                    "judged": true,
                    "judged_in": "2019-03-07T08:26:09.620000+01:00",
                    "archivized": false,
                    "results": [
                        {
                            "overall_max_points": 40.7,
                            "scored_points": 15.5,
                            "grade": 3
                        }
                    ],
                    "exam_questions": [
                        {
                            "question_text": "Which is more effective accordding to bearing -steel or concrete brigde? Why?",
                            "max_points": 0.7,
                            "question_anwsers": [
                                {
                                    "answer_text": "Concrete, the most important reason why concrete is better than steel is",
                                    "answer_assesments": {
                                        "commentary": "Nice one",
                                        "points": 0.5
                                    }
                                }
                            ]
                        },
                        {
                            "question_text": "Type the biggest benefits of steel bridges ?",
                            "max_points": 20.0,
                            "question_anwsers": [
                                {
                                    "answer_text": "Price",
                                    "answer_assesments": {
                                        "commentary": "Nice one",
                                        "points": 5.0
                                    }
                                }
                            ]
                        },
                        {
                            "question_text": "Type the biggest benefits of steel bridges?",
                            "max_points": 20.0,
                            "question_anwsers": [
                                {
                                    "answer_text": "view",
                                    "answer_assesments": {
                                        "commentary": "Nice one",
                                        "points": 10.0
                                    }
                                }
                            ]
                        }
                    ]
                }
            </pre>
        </ul>
    </li>
</ul>

<hr>
<h3>Install: </h3>
<ol>
    <li>
        <code>git clone https://github.com/psiepka/Chapter-1.git</code>
    </li>
    <li>
        <code>cd Chapter-1</code>
    </li>
    <li>
        <code>script.sh</code>
    </li>
</ol>

<b><u> If some Error occure: </u></b>

<ol>
    <li>
        <code>git clone https://github.com/psiepka/Chapter-1.git</code>
    </li>
    <li>
        <code>cd Chapter-1</code>
    </li>
    <li>
        <code>python3 -m venv exam-venv</code>
    </li>
    <li>
        <code>exam-venv\Scripts\activate</code>
    </li>
    <li>
        <code>pip install -r requirements.txt</code>
    </li>
    <li>
        <code>python manage.py makemigrations</code>
    </li>
    <li>
        <code>python manage.py migrate</code>
    </li>
    <li>
        <code>python manage.py loaddata db.json</code>
    </li>
    <li>
        <code>python manage.py runserver</code>
    </li>
</ol>
<br>

<b>Done</b> you should be able to get on http://127.0.0.1:8000/exams/ to check exam prepare sheet app!<br>
<br>
If you want to check tests
<br>
<code>python manage.py test</code>


<hr>
<h3>DOCKER</h3>
<a href="https://hub.docker.com/r/patrykeo/exams">Image</a>
<hr>

<h3>Test Case Scenarios</h3>
<ul>
    <li>Test permisions app</li>
    <li>Test create, update, delete exam</li>
    <li>Test create, update question</li>
    <li>Test create, update assesment</li>
    <li>Test create, update result</li>
    <li>Test create, update result</li>
    <li>Test bad requests in app</li>
</ul>


<h3>Intro:</h3>
<br>
After you log in go to <a href="http://127.0.0.1:8000/exams/">exams</a> (http://127.0.0.1:8000/exams/)
on this authorized users can create exams sheets - anonymous user can only read elements of exam list.
<br>
<br>
If you create your own exam sheet you can go to detail view of exam by hyperlink 'url'.
In detail view of exam you can edit exam atributs and add related with exam questions.
Only if you set Exam.avaiable to true others will have oportunity to answer in Exam test.
<br>
If some user will participate in Exam (will add related with exam model Answer) atribute answered will change to true.
After you change atribute avaiable again users cant create/update answers on exam questions.
If you view assesment page exam atribute 'checking' will change to True.
If you assess for every students points you shuold go to exam/<pk>/results/ page and assign to students grade for entire exam
(points will sum according to qyestion 'max_points' and assessmet 'points')
After you assign every student grade atribute judged will change to True and students will have permision to view personal and private information in exam/<pk>/result/ url.
<br>
On http://127.0.0.1:8000/exams/archives/ are stored exams when you want to delete them on main exam page( http://127.0.0.1:8000/exams/ ).
After exam is arhcivized and you want to still delete them you can do it, go in exam detail again and chose method DELETE
<br>
On http://127.0.0.1:8000/results/  we can view list of every exisiting result instance in app.
