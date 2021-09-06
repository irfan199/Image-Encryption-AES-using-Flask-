from flask import Flask, render_template, request, session, redirect, url_for,send_file
from Dbconnection import Db
from des import process_image,dec_process_image




static_path='/Users/mohammedirfan/PycharmProjects/flaskProject3.6/static/'
app = Flask(__name__)
app.secret_key='123'

@app.route('/')
def home_page():
    return render_template("index.html")

@app.route('/login_post',methods=["post"])
def login_post():
    Password = request.form['textfield2']
    Username=request.form['textfield']

    db=Db()
    res=db.selectOne("SELECT * from login WHERE `username`='"+Username+"' AND `password`='"+Password+"'")
    if res is not None:
        utype=res['user_type']
        session['lid']=res['login_id']
        if utype=='admin':
            return redirect(url_for('admin_home'))
        else:
            return redirect((url_for('user_home')))
    else:
        return '<script>alert("invalid username or password");window.location="/"</script>'

@app.route('/admin_home')
def admin_home():
    return render_template('admin/admin_panel.html')

@app.route('/user_home')
def user_home():
    return render_template('user/user_panel.html')

@app.route('/add_staff')
def add_staff():
    return render_template('admin/add staff.html')

@app.route('/add_staff_post',methods=['post'])
def add_staff_post():
    Name=request.form['textfield']
    Gender=request.form['radio']
    Place=request.form['textfield2']
    Post=request.form['textfield3']
    Pin=request.form['textfield4']
    District=request.form.get('select')
    Dob=request.form['textfield7']
    Photo=request.files['fileField']
    Email=request.form['textfield5']
    Phone=request.form['textfield6']
    db=Db()
    lid=db.insert("INSERT INTO `login`(`username`,`password`,`user_type`)VALUES('"+Email+"','"+Phone+"','staff')")
    filename="staff_"+str(lid)+".jpg"
    Photo.save(static_path+"staff_pics/"+filename)
    qq=" INSERT INTO `staff`(`login_id`,`name`,`place`,`pin`,`phone_number`,`email`,`post`,`district`,`dob`,`gender`,`photo`)VALUES('"+str(lid)+"','"+Name+"','"+Place+"','"+Pin+"','"+Phone+"','"+Email+"','"+Post+"','"+District+"','"+Dob+"','"+Gender+"','"+filename+"')"
    db.insert(qq)
    return '<script>alert("registration successful");window.location="/add_staff"</script>'



@app.route('/view_staff')
def view_staff():
    db=Db()
    res=db.select("SELECT * from staff")
    return  render_template('admin/admin view staff.html',data=res)

@app.route('/edit_staff/<id>')
def edit_staff(id):
    session['id']=id
    db=Db()
    res=db.selectOne("SELECT * from staff WHERE login_id='"+str(id)+"'")
    return render_template('admin/edit staff.html',data=res)



@app.route('/edit_staff_post',methods=['post'])
def edit_staff_post():
    Name = request.form['textfield']
    Gender = request.form['radio']
    Place = request.form['textfield2']
    Post = request.form['textfield3']
    Pin = request.form['textfield4']
    District = request.form.get('select')
    Dob = request.form['textfield7']
    Photo = request.files['fileField']
    Phone = request.form['textfield6']
    db=Db()
    lid=session["id"]
    filename = "staff_"+str(lid)+".jpg"
    Photo.save(static_path+"staff_pics/"+filename)
    qq=db.update("UPDATE staff SET `name` ='"+Name+"',`place` = '"+Place+"',`pin` = '"+Pin+"',`phone_number` ='"+Phone+"',`post` ='"+Post+"' ,`district` ='"+District+"' ,`dob` ='"+Dob+"',`gender` ='"+Gender+"' ,`photo` ='"+filename+"' WHERE `login_id` = '"+lid+"'");
    print(qq)
    return '<script>alert("updated successfully");window.location="/view_staff"</script>'

@app.route('/admin_dlt_staff/<id>')
def admin_dlt_staff(id):
    db=Db()
    res=db.delete("DELETE FROM `project`.`staff`WHERE `login_id`='"+str(id)+"';")
    return '<script>alert("deleted successfully");window.location="/view_staff"</script>'


@app.route('/work_assign')
def work_assign():
    db=Db()
    res=db.select("SELECT * from staff ")
    print(res)
    return render_template('admin/work assign.html',data=res)

@app.route('/work_assigned_post',methods=['post'])
def work_assigned_post():
    Staff_name=request.form.get('select')
    Work_assigned=request.form['textfield']
    Description=request.form['textfield2']
    db=Db()
    res=db.insert("INSERT INTO `project`.`work_assigned`(`staff_id`,`work_assigned`,`description`,`date`)VALUES('"+Staff_name+"','"+Work_assigned+"','"+Description+"',curDate())")
    return'<script>alert("work assigned successfully");window.location="/work_assign"</script>'

@app.route('/view_assigned_work')
def view_assigned_work():
    db=Db()
    res=db.select("SELECT `work_assigned`.*,`staff`.name FROM `work_assigned`,`staff` WHERE `work_assigned`.`staff_id`=`staff`.`login_id` ORDER BY 'work_id' DESC ")
    return render_template('admin/view assigned works.html',data=res)

@app.route('/work_status_view/<wid>')
def work_status_view(wid):
    db=Db()
    res=db.selectOne("SELECT * FROM project.work_status WHERE `work_id`='"+str(wid)+"'")
    print(res)
    return render_template('admin/work status view.html',data=res)

@app.route('/profile_view')
def profile_view():
    lid=session['lid']
    db=Db()
    res=db.selectOne("SELECT * FROM project.staff WHERE `login_id`='"+str(lid)+"'")
    return render_template('user/profile view.html',data=res)

@app.route('/work_get_view')
def work_get_view():
    lid=session['lid']
    db=Db()
    res=db.select("SELECT * FROM work_assigned WHERE `staff_id`='"+str(lid)+"'")
    return render_template('user/work get view.html',data=res)

@app.route('/update_work_status/<wid>')
def update_status(wid):
    session['wid']=wid
    db=Db()
    res=db.selectOne("SELECT * FROM work_assigned WHERE `work_id`='"+str(wid)+"'")
    return render_template('user/update status.html',data=res)

@app.route('/update_work_status_post',methods=['get','post' ])
def update_work_status_post():
    wid=session['wid']
    db=Db()
    Work_status = request.form['textfield']
    check="SELECT * FROM `work_status` WHERE `work_id`='"+wid+"'"
    data=db.selectOne(check)
    if data is None:
        res=db.insert("INSERT INTO `work_status`(`work_id`,`work_status`,`date`)VALUES('"+str(wid)+"','"+Work_status+"',curDate())");
        return '<script>alert("status updated");window.location="/work_get_view"</script>'
        print(res)
    else:
        qq=db.update("UPDATE `project`.`work_status`SET`work_status` = '"+Work_status+"',`date` = curDate() WHERE `work_id` = '"+str(wid)+"'")
        return '<script>alert("status updated");window.location="/work_get_view"</script>'




@app.route('/staff_view')
def staff_view():
    db=Db()
    res=db.select("SELECT * from staff")
    return render_template('user/staff view.html',data=res)

@app.route('/des/<rid>')
def des(rid):
    session['rid']=rid
    return render_template('user/des.html')

@app.route('/des_post',methods=['post'])
def des_post():
    lid=session['lid']
    rid=session['rid']
    photo=request.files['fileField1']
    photo.save("/Users/mohammedirfan/PycharmProjects/flaskProject3.6/static/images/"+photo.filename)

    from datetime import datetime

    fn = str(datetime.now().year) + str(datetime.now().month) + str(datetime.now().day) + str(
        datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second)

    process_image("/Users/mohammedirfan/PycharmProjects/flaskProject3.6/static/images/" + photo.filename,
                  "/Users/mohammedirfan/PycharmProjects/flaskProject3.6/static/images/" + fn + ".bmp")

    db=Db()
    qq=db.insert("INSERT INTO `project`.`image`(`sender_id`,`receiver_id`,`date`,`filename1`,`algoritgm`)VALUES('"+str(lid)+"','"+(rid)+"',curdate(),'static/images/" + fn + ".bmp','des3');")
    return '<script>alert("send successfully");window.location="/staff_view"</script>'













@app.route('/received_image')
def received_image():
    lid=session['lid']
    db=Db()
    res=db.select("SELECT `staff`.`name`,`image`.* FROM `staff`,`image` WHERE `image`.`receiver_id`='"+str(lid)+"' AND `image`.`sender_id`=`staff`.`login_id` ORDER BY `image_id` DESC")


    return render_template('user/received image.html',data=res)


@app.route('/decrypt/<imid>')
def decrypt(imid):
    db=Db()
    res=db.selectOne("SELECT * FROM image WHERE `image_id`='"+imid+"'")
    dec_process_image("/Users/mohammedirfan/PycharmProjects/flaskProject3.6/" + res['filename1'],
                      "/Users/mohammedirfan/PycharmProjects/flaskProject3.6/static/images/hhhhhhhhhhhhhhhhhhh.jpg")
    return send_file( "/Users/mohammedirfan/PycharmProjects/flaskProject3.6/static/images/hhhhhhhhhhhhhhhhhhh.jpg",as_attachment=True)

@app.route("/change_password")
def change_password():
    return render_template('user/change password.html')

@app.route('/change_password_post',methods=["post"])
def change_password_post():
    lid=session['lid']
    Old_password=request.form["textfield"]
    New_password=request.form["textfield2"]
    db=Db()
    res=db.selectOne("SELECT * from login WHERE `login_id`='"+str(lid)+"' AND `password`='"+Old_password+"'")
    if res is not None:
        db.update("UPDATE `login` SET `password` = '"+New_password+"' WHERE`login_id` = '" + str(lid) + "';")
        return '<script>alert("success");window.location="/"</script>'
    else:
        return '<script>alert("incorrect password");window.location="/change_password"</script>'








if __name__ == '__main__':
    app.run(debug=True)
