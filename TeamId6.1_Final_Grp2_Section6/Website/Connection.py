from flask import Flask, render_template, request,session,redirect  ,jsonify
import psycopg2
from flask_session import Session
from json import dumps
from datetime import date
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.static_folder='static'
Session(app)
conn = psycopg2.connect(host='localhost', database='bams',
                        user='postgres', password='ronit123')
cursor = conn.cursor()
user_id = 0


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/Team')
def team():
    return render_template('Team.html')

@app.route('/Documentation')
def document():
    return render_template('Documentation.html')

@app.route('/Database')
def database():
    return render_template('Database.html')

@app.route('/Booking',methods=['get','post'])
def booking():
    return render_template('Booking.html')

@app.route('/Canceldone', methods=['get','post'])
def canceldone():
    return render_template('Cancel_done.html')

@app.route('/Bookingdone', methods=['get','post'])
def bookingdone():
    return render_template('Booking_done.html')

@app.route('/CustomerId', methods=['get','post'])
def customerid():
    return render_template('Customer_id.html')

@app.route('/DoBooking',methods=['get','post'])
def dobooking():
    return render_template('Do Booking.html')

@app.route('/Cancelbooking', methods=['get','post'])
def cancelbooking():
    return render_template('Cancel Booking.html')

@app.route('/Customerbooking')
def customerdetails():
    return render_template('Customer Details.html')

@app.route('/CustomerBooking', methods=['post','get'])
def CustomerBooking():
    print("Hello")
    if request.method == 'POST':
        Customer_name = request.form.get('name')
        DOB = request.form.get('dob')
        Height = request.form.get('height')
        Weight = request.form.get('weight')
        Gender = request.form.get('Gender')
        Activity_id = request.form.get('activity_id')
        cursor.execute('select count(*) from ba_ms.\"Customer\"')
        result = cursor.fetchone()
        count = result[0]+1
        print(result)
        insert_query = """ INSERT INTO ba_ms.\"Customer\" VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        try:
            record = (int(count), Customer_name, Gender, Activity_id, DOB, int(Height), int(Weight))
            print(insert_query,record)
            cursor.execute(insert_query, record)
            conn.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into Customer table")
            
        except:
            return "Invalid details"
    return render_template('Booking.html')


@app.route('/DoBooking', methods=['post','get'])
def doBooking():
    print("Hello")
    if request.method == 'POST':
        Booking_date = request.form.get('Booking_date')
        Booking_time = request.form.get('Booking_time')
        Customer_id = request.form.get('Customer_id')
        Payment_id = request.form.get('Payment_id')
        Payment_method = request.form.get('Payment Method')
        Payment_amount = request.form.get('Payment_amount')
        Activity_id = request.form.get('activity_id')
        cursor.execute('select count(*) from ba_ms.\"Booking\"')
        result = cursor.fetchone()
        count = result[0]+1
        print(result)
        insert_query = """ INSERT INTO ba_ms.\"Booking\" VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
        try:
            record = (int(count), Booking_date, Booking_time, int(Payment_id), Payment_method, int(Payment_amount), Activity_id, int(Customer_id))
            cursor.execute(insert_query, record)
            conn.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into Booking table")
        except:
            return "Invalid details"
    return render_template('Do Booking.html')


@app.route('/Cancel', methods=['post','get'])
def CancelBooking():
    print("Hello")
    if request.method == 'POST':
        Customer_id = request.form.get('Customer_id')
        delete_query = """ DELETE FROM ba_ms.\"Booking\" where ba_ms.\"Booking\".
        "Customer_id\" = %s"""
        try:
            record = (Customer_id)
            cursor.execute(delete_query, record)
            conn.commit()
            count = cursor.rowcount
            print(count, "Record deleted successfully from Booking table")
        except:
            return "Invalid details"
    return redirect('/Canceldone')

@app.route('/CustomerId')
def get_customer_id():
    if request.method == 'POST':
        query="select Customer_id from ba_ms.\"Customer\"".format(session['mobile'])
        cursor.execute(query)
        if cursor.pgresult_ptr is not None:
            uid=cursor.fetchone()
            query="select Customer_id from ba_ms.\"Customer\"".format(uid[0])
            cursor.execute(query)
            result=cursor.fetchall()
            print(result)
            return dumps(result,default=str)
    return jsonify("")


if __name__ == '__main__':
    app.run(debug=True)
