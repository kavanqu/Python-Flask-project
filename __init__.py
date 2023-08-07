import User
import shelve
from setup import set_up_db

from flask import Flask, render_template, request, redirect, url_for

from Forms import (
    LoginForm, RegisterForm, PasswordResetForm,
    UpdateUserForm, CheckoutForm
)


def get_all_categories():
    db = shelve.open('storage.db', 'r')
    categories_dict = db['Categories']
    db.close()

    cat_list = []
    for key in categories_dict:
        category = categories_dict.get(key)
        cat_list.append(category)

    return cat_list


app = Flask(__name__)
current_user = None



set_up_db()
category_list = get_all_categories()

@app.route('/', methods=['GET', 'POST'])
def home():
    global current_user, category_list
    show_modal = request.args.get('showModal', None)

    return render_template('main.html', category_list=category_list, user=current_user, showModal=show_modal)


@app.route('/myCourses', methods=['GET'])
def my_courses():
    global current_user, category_list

    return render_template('myCourses.html', category_list=category_list, user=current_user)


@app.route('/feedback', methods=['GET'])
def feedback():
    global current_user, category_list

    return render_template('feedback.html', category_list=category_list, user=current_user)


@app.route('/contactUs', methods=['GET'])
def contact_us():
    global current_user, category_list

    return render_template('contactUs.html', category_list=category_list, user=current_user)


@app.route('/userFeedback', methods=['GET'])
def user_feedback():
    global current_user, category_list

    return render_template('userFeedback.html', category_list=category_list, user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global current_user, category_list
    show_modal = request.args.get('showModal', None)

    login_form = LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()

        user = [v for k, v in users_dict.items() if v.get_email() == login_form.email.data]
        if len(user) == 0 or user[0].get_password() != login_form.password.data:
            return render_template('login.html', form=login_form, category_list=category_list, user=current_user,
                                   showModal=show_modal, failed=True)
        else:
            current_user = user[0]

            return redirect(url_for('home'))
    return render_template('login.html', form=login_form, category_list=category_list,
                           user=current_user, showModal=show_modal)


@app.route('/register', methods=['GET', 'POST'])
def register():
    global current_user, category_list

    register_form = RegisterForm(request.form)
    if request.method == 'POST' and register_form.validate():
        users_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            users_dict = db['Users']
        except KeyError:
            print("Error in retrieving Users from storage.db.")
        user = User.User(
            register_form.first_name.data,
            register_form.last_name.data,
            register_form.password.data,
            register_form.email.data,
            register_form.birth_date.data
        )

        users_dict[user.get_user_id()] = user
        db['Users'] = users_dict
        db.close()

        return redirect(url_for('login', showModal='create'))
    return render_template('register.html', form=register_form, category_list=category_list, user=current_user)


@app.route('/forgetPassword', methods=['GET', 'POST'])
def forget_password():
    global current_user, category_list

    password_reset_form = PasswordResetForm(request.form)
    if request.method == 'POST' and password_reset_form.validate():
        return redirect(url_for('login', showModal='reset'))
    return render_template('forgetPassword.html', form=password_reset_form,
                           category_list=category_list, user=current_user)


@app.route('/errors')
def errors():
    global current_user, category_list

    return render_template('errors.html', category_list=category_list, user=current_user)


@app.route('/transaction')
def transaction():
    global current_user, category_list

    return render_template('transactions.html', category_list=category_list, user=current_user)


@app.route('/booking')
def booking():
    global current_user, category_list

    return render_template('bookings.html', category_list=category_list, user=current_user)


@app.route('/account/', methods=['GET'])
@app.route('/account/<int:user_id>', methods=['POST'])
def account(user_id=None):
    global current_user, category_list
    show_modal = request.args.get('showModal', None)

    if current_user.get_admin():
        user_list = User.User.get_all_users()
    else:
        user_list = [current_user]

    if request.method == 'POST':
        db = shelve.open('storage.db', 'w')
        users_dict = db['Users']
        users_dict.pop(user_id)
        db['Users'] = users_dict
        db.close()

        if current_user.get_admin():
            return redirect(url_for('account', users_list=user_list, showModal='delete'))
        else:
            current_user = None
            return redirect(url_for('home', showModal='delete'))

    return render_template('account.html', user=current_user, category_list=category_list,
                           users_list=user_list, showModal=show_modal)


@app.route('/updateUser/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    global current_user, category_list

    update_user_form = UpdateUserForm(request.form)
    if request.method == 'GET':
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()
        user = users_dict.get(user_id)

        return render_template('updateUser.html', form=update_user_form, category_list=category_list,
                               user=current_user, editUser=user)

    print(update_user_form.validate())
    print(update_user_form.errors)
    if request.method == 'POST' and update_user_form.validate():
        print("POST")
        db = shelve.open('storage.db', 'w')
        users_dict = db['Users']

        user = users_dict.get(user_id)
        user.set_password(update_user_form.password.data)
        user.set_email(update_user_form.email.data)
        if current_user.get_user_id() == user.get_user_id():
            user.set_birth_date(update_user_form.birth_date.data)
            current_user = user

        db['Users'] = users_dict
        db.close()

        return redirect(url_for('account', showModal='update'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    global current_user, category_list

    checkout_form = CheckoutForm(request.form)
    if request.method == 'POST' and checkout_form.validate():
        return redirect(url_for('home', showModal='payment'))

    return render_template('checkout.html', form=checkout_form, category_list=category_list,
                           user=current_user, total_price=224.00, discount=0.5)


@app.route('/logout', methods=['GET'])
def logout():
    global current_user

    current_user = None
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
