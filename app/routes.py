"""
routes.py
------------
Webpage navigation.
"""
import imp
import os
import sys

from authorizenet import apicontractsv1
from authorizenet.apicontrollers import createTransactionController

from flask import render_template, flash, redirect, url_for, request
from app import app, mongo
from app.forms import LoginForm, RegisterForm, AccountForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user
from app.user import User

CONSTANTS = imp.load_source('modulename', 'constants.py')

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title='Homepage')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print("User is already authenticated!")
        return redirect('/union')
    else:
        print("User is not authenticated.")

    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.email.data, form.remember_me.data))

        results = mongo.db.Users.find_one({'email': form.email.data})

        print(results)

        if not results is None:
            user = User(results.get('first_name'), results.get('last_name'), form.email.data, results.get('_id'))
            # Validate password
            valid_user = User.check_password(results.get('password_hash'), form.password.data)

            if valid_user:
                login_user(user, remember=form.remember_me.data)
                print("User logged in!")
                return redirect('/union')

        
    return render_template('login.html', title='Login', form=form)

@app.route('/union')
def union():
    restaurants = mongo.db.UnionFood.find()
    return render_template('locations/union.html', title='Union', restaurants=restaurants)

@app.route('/lassonde')
def lassonde():
    return render_template('locations/lassonde.html', title='Lassonde')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Only display the webpage if the user is logged in. """
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))

    flash('Issue with registration')
    return render_template('register.html', title='Register', form=RegisterForm())

<<<<<<< HEAD
@app.route('/payment')
def payments():
    return render_template('payments.html')

@app.route('/payment', methods=['POST'])
def payments_post():
    cardnum = request.form['cardnumber']
    cardname = request.form['cardname']
    cc = request.form['cardcode']
    month = request.form['month']
    year = request.form['year']
    fn = request.form['fn']
    ln = request.form['ln']
    country = request.form['country']
    state = request.form['state']
    address1 = request.form['address_one']
    address2 = request.form['address_two']
    zip = request.form['zip']
    comp = request.form['company']
    amount = request.form['amt']
    ct = request.form['city']

    some_var = charge_card(cardnum, cardname, cc, month, year, fn, ln, country, state, address1, address2, zip, comp, amount, ct)

    return 'Nice ' + some_var.messages.resultCode

def charge_card(cardnum, cardname, cc, month, year, fn, ln, country, state, address1, address2, zip, comp, amount, ct):
    # Create a merchantAuthenticationType object with authentication details
    # retrieved from the constants file
    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name = CONSTANTS.apiLoginId
    merchantAuth.transactionKey = CONSTANTS.transactionKey

    # Create the payment data for a credit card
    creditCard = apicontractsv1.creditCardType()
    creditCard.cardNumber = cardnum
    creditCard.expirationDate = year + "-" + month
    creditCard.cardCode = cc

    # Add the payment data to a paymentType object
    payment = apicontractsv1.paymentType()
    payment.creditCard = creditCard

    # Create order information
    order = apicontractsv1.orderType()
    order.invoiceNumber = "10101"
    order.description = "Golf Shirts"

    # Set the customer's Bill To address
    customerAddress = apicontractsv1.customerAddressType()
    customerAddress.firstName = fn
    customerAddress.lastName = ln
    customerAddress.company = comp
    customerAddress.address = address1 + " " + address2
    customerAddress.city = ct
    customerAddress.state = state
    customerAddress.zip = zip
    customerAddress.country = country

    # Set the customer's identifying information
    customerData = apicontractsv1.customerDataType()
    customerData.type = "individual"
    customerData.id = "99999456654"
    customerData.email = "EllenJohnson@example.com"

    # Add values for transaction settings
    duplicateWindowSetting = apicontractsv1.settingType()
    duplicateWindowSetting.settingName = "duplicateWindow"
    duplicateWindowSetting.settingValue = "600"
    settings = apicontractsv1.ArrayOfSetting()
    settings.setting.append(duplicateWindowSetting)

    # setup individual line items
    line_item_1 = apicontractsv1.lineItemType()
    line_item_1.itemId = "12345"
    line_item_1.name = "first"
    line_item_1.description = "Here's the first line item"
    line_item_1.quantity = "2"
    line_item_1.unitPrice = "12.95"
    line_item_2 = apicontractsv1.lineItemType()
    line_item_2.itemId = "67890"
    line_item_2.name = "second"
    line_item_2.description = "Here's the second line item"
    line_item_2.quantity = "3"
    line_item_2.unitPrice = "7.95"

    # build the array of line items
    line_items = apicontractsv1.ArrayOfLineItem()
    line_items.lineItem.append(line_item_1)
    line_items.lineItem.append(line_item_2)

    # Create a transactionRequestType object and add the previous objects to it.
    transactionrequest = apicontractsv1.transactionRequestType()
    transactionrequest.transactionType = "authCaptureTransaction"
    transactionrequest.amount = amount
    transactionrequest.payment = payment
    transactionrequest.order = order
    transactionrequest.billTo = customerAddress
    transactionrequest.customer = customerData
    transactionrequest.transactionSettings = settings
    transactionrequest.lineItems = line_items

    # Assemble the complete transaction request
    createtransactionrequest = apicontractsv1.createTransactionRequest()
    createtransactionrequest.merchantAuthentication = merchantAuth
    createtransactionrequest.refId = "MerchantID-0001"
    createtransactionrequest.transactionRequest = transactionrequest
    # Create the controller
    createtransactioncontroller = createTransactionController(
    createtransactionrequest)
    createtransactioncontroller.execute()

    response = createtransactioncontroller.getresponse()

    if response is not None:
        # Check to see if the API request was successfully received and acted upon
        if response.messages.resultCode == "Ok":
            # Since the API request was successful, look for a transaction response
            # and parse it to display the results of authorizing the card
            if hasattr(response.transactionResponse, 'messages') is True:
                print(
                    'Successfully created transaction with Transaction ID: %s'
                    % response.transactionResponse.transId)
                print('Transaction Response Code: %s' %
                      response.transactionResponse.responseCode)
                print('Message Code: %s' %
                      response.transactionResponse.messages.message[0].code)
                print('Description: %s' % response.transactionResponse.
                      messages.message[0].description)
            else:
                print('Failed Transaction.')
                if hasattr(response.transactionResponse, 'errors') is True:
                    print('Error Code:  %s' % str(response.transactionResponse.
                                                  errors.error[0].errorCode))
                    print(
                        'Error message: %s' %
                        response.transactionResponse.errors.error[0].errorText)
        # Or, print errors if the API request wasn't successful
        else:
            print('Failed Transaction.')
            if hasattr(response, 'transactionResponse') is True and hasattr(
                    response.transactionResponse, 'errors') is True:
                print('Error Code: %s' % str(
                    response.transactionResponse.errors.error[0].errorCode))
                print('Error message: %s' %
                      response.transactionResponse.errors.error[0].errorText)
            else:
                print('Error Code: %s' %
                      response.messages.message[0]['code'].text)
                print('Error message: %s' %
                      response.messages.message[0]['text'].text)
    else:
        print('Null Response.')

    return response

=======
>>>>>>> 317a1d4faf67c1bc0afc757a3baad2c4ae521c2a
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/account')
def account():
    """ Only display the webpage if the user is logged in. """
    if current_user.is_authenticated:
        return render_template('account.html', title='Account', form=AccountForm())
    return redirect(url_for('login'))

@app.route('/payment')
def payments():
    return render_template('payments.html', title='Payment')

@app.route('/panda-express')
def panda():
    food_items = mongo.db.PandaExpressFood.find()
    return render_template('restaurants/panda-express.html', title='Panda Express', items=food_items)