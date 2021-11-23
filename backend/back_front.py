from flask import Flask, request, jsonify

app = Flask(__name__)

# USEFUL LINKS:
# https://codesnnippets.com/consuming-a-flask-rest-api-with-vue-js-front-end-web-development-with-python-and-flask-part-7/
# https://medium.com/@onejohi/building-a-simple-rest-api-with-python-and-flask-b404371dc699
# https://auth0.com/blog/developing-restful-apis-with-python-and-flask/


# Test function from the lectures
"""
@app.route('/get_sum', methods=['GET'])
def get_sum():
    x = request.args.get('x')
    y = request.args.get('y')
    result = int(x) + int(y)

    return '{}'.format(result)
"""


# Test dictionaries as database proxies - those are the ones the @app.route are referencing
users = [{'user_id' = 1234,
        'name' = 'Max',
        'surname' = 'Muster',
        'email' = 'Max.Muster@test.com',
        'exercise_duration' = 10,
        'objective' = 'A1'}]

exercise = [{'info1' = 'test1',
            'info2' = 'test2',
            'info3' = 'test3'}]

student_progress = [{'user_id' = 1234,
                    'item_id' = 3456,
                    'created_at' = '01.01.2001'}]
# ----------------------------------------------------------------------------------------------------------------------
###############
## GET CALLS ##
###############

##############
# Teacher UI #
##############
# GET ALL STUDENTS
@app.route('/users', methods=['GET'])
def get_all_students():
    response_object = {'status': 'success'}

    response_object['users'] = users
    return jsonify(response_object)

##############
# Student UI #
##############
# GET EXERCISE FOR SPECIFIC STUDENT - probably won't work what's the correct /? /exercise or /student or neither?
@app.route('/exercise', methods=['GET'])
def get_exercise():
    response_object = {'status': 'success'}

    response_object['exercise'] = exercise

    for user in users:
        if user['user_id'] == users:
            response_object['exercise'] = exercise

            return jsonify(response_object)
    return False

##############
# Backend ML #
##############


# ----------------------------------------------------------------------------------------------------------------------
################
## POST CALLS ##
################

##############
# Teacher UI #
##############
# ADD A STUDENT
@app.route('/users', methods=['POST'])
def add_student():
    response_object = {'status': 'success'}

    post_data = request.get_json()

    users.append({'user_id' : post_data.get('user_id'),
                  'name' : post_data.get('name'),
                  'surname' : post_data.get('surname'),
                  'email' : post_data.get('email'),
                  'exercise_duration' : post_data.get('exercise_duration'),
                  'objective' : post_data.get('objective')
                  })

    # short hand notation for exactly the same without having to write out the dictionary?
    #users.append(request.get_json())

    response_object['message'] = 'student added!'

    return jsonify(response_object)


# DELETE A STUDENT
@app.route('/users', methods=['POST'])
def delete_student(user_id):
    users = request.get_json()

    for user in users:
        if user['user_id'] == user_id:
            users.remove(user)
            return True
    return False


# UPLOAD EXERCISE
@app.route('/exercise', methods=['POST'])
def upload_exercise():
    response_object = {'status': 'success'}

    post_data = request.get_json()

    exercise.append({'info1': post_data.get('info1'),
                  'info2': post_data.get('info2'),
                  'info3': post_data.get('info3')
                  })

    response_object['message'] = 'exercise uploaded!'

    return jsonify(response_object)


##############
# Student UI #
##############
# RETURN RESULT
@app.route('/student_progress', methods=['POST'])
def return_result():
    response_object = {'status': 'success'}

    post_data = request.get_json()

    student_progress.append({'user_id': post_data.get('user_id'),
                            'item_id': post_data.get('item_id'),
                            'created_at': post_data.get('created_at')
                             })

    response_object['message'] = 'exercise uploaded!'

    return jsonify(response_object)


##############
# Backend ML #
##############






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
