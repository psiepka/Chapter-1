Used python 3.7.0

Instruction of useage:
1. git clone https://github.com/psiepka/Chapter-1.git
2. cd Chapter-1
3. script.sh <br>
<b>Done</b> you should be able to get on http://127.0.0.1:8000/exams/ to check exam prepare sheet app!<br>
<u> If some Error occure: </u>
You must install 'sheets_manager/<b>requirements.txt</b>' after this go to sheets_manager folder and migrate database <python manage.py migrate>, next load fixtures <python manage.py loaddata db.json> and run it <python manage.py runserver>

<hr>

<b> <a href="http://127.0.0.1:8000/auth/login/">LOGIN</a></b>:
You can login in http://127.0.0.1:8000/auth/login/ as:
<br>login : 'User_1'  ; password: 'pass'
<br>login : 'User_2'  ; password: 'pass'
<br>login : 'User_3'  ; password: 'pass'
<br>-to fully check app possibility
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
<br>


<hr>
<br>
<a href="https://hub.docker.com/r/patrykeo/exams">DOCKER IMAGE</a>
<br>
https://hub.docker.com/r/patrykeo/exams
