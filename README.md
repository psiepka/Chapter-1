<h3>DRF - Exam sheet example</h3>
<p>An example Django REST framework application.</p>

<strong><small>Required python 3.7.0+</small></strong>

<hr>
<h5>API Endpoints</h5>

<b>Users:</b>
<ul>
    <li>
        <b>/auth/login/</b> - login to app
        <small>Users avaialbe after load fixtures:
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
        <b>/exams/</b> - list of all not archives exams in app
    </li>
    <li>
        <b>/exams/archives/</b> - list of all archives exams in app
    </li>
    <li>
        <b>/exams/results/</b> - list of all results of users exams in app
    </li>
    <li>
        <b>/exams/<pk>/</b> - detail of exam (only author of exam can access)
    </li>
    <li>
        <b>/exams/<pk>/test/</b> - test of exam for students (student can access only when exam.avaiable == True)
    </li>
    <li>
        <b>/exams/<pk>/assesment</b> - assesment of students exams answers (only author of exam can access)
    </li>
    <li>
        <b>/exams/<pk>/results</b> - list of results students assesments (only author of exam can access)
    </li>
    <li>
        <b>/exams/<pk>/result</b> - student result with details (student can access only when exam.judged == True)
    </li>
</ul>

<hr>
<h5>Install: </h5>
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
        <code>python manage.py loaddata db.json</code>
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
<h5>DOCKER</h5>
<a href="https://hub.docker.com/r/patrykeo/exams">Image</a>
<hr>

<h5>Test Case Scenarios</h5>
<ul>
    <li>Test permisions app</li>
    <li>Test create, update, delete exam</li>
    <li>Test create, update question</li>
    <li>Test create, update assesment</li>
    <li>Test create, update result</li>
    <li>Test create, update result</li>
    <li>Test bad requests in app</li>
</ul>


<h5>Intro:</h5>
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
