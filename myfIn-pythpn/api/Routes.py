import uuid,json
from flask import Blueprint,jsonify,request
from firebase_admin import firestore,auth,credentials,initialize_app

db=firestore.client()
user_ref=db.collection('expdetails')

Routes=Blueprint('Routes',__name__)

@Routes.route('/add',methods=['POST'])

def create():
  
  try:
  
    uid = str(uuid.uuid4())
    user_data = json.loads(request.data)
    user_ref.document(uid).set(user_data)
    return jsonify({"success":True}),200
  
  except Exception as e:
    return f"An error occured :{e}"


@Routes.route('/getall', methods=['GET'])
def get_all():
    try:
        all_users = [doc.to_dict() for doc in user_ref.stream()]
        return jsonify({"success": True, "data": all_users}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500
  
@Routes.route('/getUserExp', methods=['GET'])
def get_user_exp():
    try:
       
        user_email = request.args.get('user_email')
        print(user_email)
        # Get user details from Firebase Authentication
        user = auth.get_user_by_email(user_email)
        print(user)

        # Get the UID of the user
        user_id = user.uid

        # Filter documents based on the user_id
        query = user_ref.where('userId', '==', user_id).stream()


        # Convert documents to a list of dictionaries
        filtered_users = [doc.to_dict() for doc in query]

        return jsonify({"success": True, "data": filtered_users}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500
