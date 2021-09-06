#Libraries and Packages used for implementation
Pillow(PIL) - load and create new image
Pycryptodome - for DES3
mysql.connector - connecting database to project

#framework used
Flask

#python version
3.62

#Database connection - Dbconnection.py
at the time of setting database connection you should change localhost user and password in Dbconnection.py

#Structure of database - db.sql
you can import it

#code Triple DES - des.py
key length-24 byte(192 bit)-Three seperate key with 8 byte
initialization vector(IV) - 8 byte

#admin
admin username and password is already set in database
username:admin
password:admin
admin can add staff,when admin add a staff the email saved as username and phone number saved as password

#user
user can login to user account via registered email address(username) and phone number(password)
user can change password after login to user account
a user can send image to another user
when a user send an image it is encrypted and store in the path static/images with corresponding date and time,and extension bmp
received user can decrypt image after login to receiver account by clicking decode (received image is downloaded)
Aaa




