from flask import Flask, render_template, request, redirect, url_for, session
from form import Feedbackform, Reply
import shelve
import feedback as f
# from feedback import msg

app = Flask(__name__)
app.secret_key = 'any_random_string'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/Feedbackform', methods=['GET', 'POST'])
def create_user():
    feedback_form = Feedbackform(request.form)
    if request.method == 'POST' and feedback_form.validate():
        feedback_dict = {}
        db = shelve.open('storage.db', 'c')
        try:
            feedback_dict = db['feedback']
        except:
            print("Error in retrieving Users from storage.db.")

        feedback = f.feedback(feedback_form.rating.data, feedback_form.name.data, feedback_form.email.data, feedback_form.subject.data, feedback_form.details.data)
        feedback_dict[feedback.get_user_id()] = feedback
        db['feedback'] = feedback_dict

        # Test codes
        feedback_dict = db['feedback']
        feedback = feedback_dict[feedback.get_user_id()]
        print(feedback.get_name(), "was stored in storage.db successfully with user_id == ", feedback.get_user_id())
        db.close()

        session['feedback_form_created'] = feedback.get_name()
        return redirect(url_for('home'))

    return render_template('Feedbackform.html', user_list=feedback_form)



@app.route('/update_feedback/<int:id>/', methods=['GET', 'POST'])
def update_feedback(id):
    update_user_form = Feedbackform(request.form)
    feedback_dict = {}
    db = shelve.open('storage.db', 'r')
    feedback_dict = db['feedback']
    db.close()
    feedback_list = []
    for key in feedback_dict:
        feedback_item = feedback_dict.get(key)
        feedback_list.append(feedback_item)
    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        users_dict = db['feedback']
        user = users_dict.get(id)
        user.set_rating(update_user_form.rating.data)
        user.set_name(update_user_form.name.data)
        user.set_email(update_user_form.email.data)
        user.set_subject(update_user_form.subject.data)
        user.set_detail(update_user_form.details.data)
        db['feedback'] = users_dict
        db.close()

        return redirect(url_for('retrieveUsers'))
    else:
        users_dict = {}
        db = shelve.open('storage.db', 'r')
        users_dict = db['feedback']
        db.close()
        user = users_dict.get(id)
        update_user_form.rating.data = user.get_rating()
        update_user_form.name.data = user.get_name()
        update_user_form.email.data = user.get_email()
        update_user_form.subject.data = user.get_subject()
        update_user_form.details.data = user.get_details()

    return render_template('update_feedback.html',user_list = feedback_list,form=update_user_form)



@app.route('/retrieveUsers')
def retrieveUsers():
    feedback_dict = {}
    db = shelve.open('storage.db', 'r')
    feedback_dict = db['feedback']
    db.close()
    feedback_list = []
    for key in feedback_dict:
        feedback_item = feedback_dict.get(key)
        feedback_list.append(feedback_item)

    return render_template('retrieveUsers.html', count=len(feedback_list), users_list=feedback_list)


@app.route('/replyUser/<int:id>/', methods=['GET', 'POST'])
def replyUser(id):
    feedback_dict = {}
    db = shelve.open('storage.db', 'c')
    feedback_dict = db['feedback']

    feedback = feedback_dict.get(id)
    replies = Reply(request.form)

    if request.method == 'POST':
        action = request.form["txtAction"]

        if action == "dosave":
            # Process the reply and update the feedback's reply field
            feedback.reply = replies.reply.data  # Assuming you have a field named 'reply' in your Feedback class
            db['feedback'] = feedback_dict
            db.close()
            return redirect(url_for('retrieveUsers'))

        elif action == "dodelete":
            if id in feedback_dict:
                del feedback_dict[id]
                db['feedback'] = feedback_dict
                db.close()
                return redirect(url_for('retrieveUsers'))

    db.close()
    return render_template('replyUser.html', user_list=[feedback], id=id, reply=replies)


@app.route('/deleteUser/<int:id>', methods=['POST'])
def delete_user(id):
    feedback_dict = {}
    db = shelve.open('storage.db', 'c')
    feedback_dict = db['feedback']

    if id in feedback_dict:
        del feedback_dict[id]
        db['feedback'] = feedback_dict
        db.close()

    return redirect(url_for('retrieveUsers'))

def delete_user(id):
    feedback_dict = {}
    db = shelve.open('storage.db', 'w')
    try:
        feedback_dict = db['feedback']
    except KeyError:
        pass  # Handle the case where 'feedback' key doesn't exist

    if id in feedback_dict:
        feedback_dict.pop(id)
        db['feedback'] = feedback_dict
    db.close()

    return redirect(url_for('retrieveUsers'))


@app.route('/contactpage')
def contactpage():
    return render_template('contactpage.html')

if __name__ == '__main__':
    app.run()
