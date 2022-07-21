from flask import jsonify, redirect, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import db
import uuid

class User:
    def start_session(self, user):
        session["logged_in"] = True
        if "password" in user:
            del user["password"]
        session["user"] = user
        return jsonify({"success":user}), 200

    def signup(self):
        # Create a new user
        user = {"_id":uuid.uuid4().hex,
        "username":request.form.get('name'),
        "password":request.form.get('password'),
        "Confirm Password":request.form.get('confirm_password'),
        "data":{}
        }

        #Encrypt the password
        if user['password'] == user['Confirm Password']:
            del user["Confirm Password"]
            user['password'] = pbkdf2_sha256.encrypt(user['password'])
        else:
            return jsonify({"error":"Passwords do not match"}), 400

        #Check Username
        user["username"] = user["username"].lower()
        if db.users.find_one({"username":user['username']}):
            return jsonify({"error":"Username already exists"}), 400

        if db.users.insert_one(user):
            self.start_session(user)

        return jsonify({"error":"Signup failed"}), 200

    def login(self):
        username = {"username": request.form.get('name')}
        username = {"username":username["username"].lower()}
        user = db.users.find_one(username)
        
        if user and pbkdf2_sha256.verify(request.form.get('password'), user["password"]):
            return self.start_session(user)

        return jsonify({"error":"Login failed"}), 401

    def signout(self):
        session.clear()
        return redirect("/")

    def create_budget(self):
        user = session["user"]
        title = request.form.get("title").lower()
        budget = int(request.form.get("budget"))

        if title in user["data"]:
            return jsonify({"error":"Budget already exists"}), 400
        else:
            user["data"][title] = {"budget":budget, "total_spent":0, "remaining_budget":budget, "transactions":{}, "Entertainment":0, "Food":0, "Loans":0, "Other":0}
            db.users.update_one({"_id":user["_id"]}, {"$set":{"data":user["data"]}})
            self.start_session(user)

        return jsonify({"success":user}), 200

    def add_transaction(self):
        user = session["user"]
        budget = request.form.get("budget_id").lower()
        transaction = request.form.get("transaction").lower()
        date = request.form.get("date")
        amount = request.form.get("amount")
        transaction_type = request.form.get("type")

        if budget == "":
            return jsonify({"error":"Budget not specified"}), 400

        if budget in user['data']:
            user["data"][budget]["transactions"][transaction] = {"date":date, "amount":amount, "transaction_type":transaction_type}
            user["data"][budget]["total_spent"] += int(amount)
            user["data"][budget]["remaining_budget"] -= int(amount)

            if transaction_type == "Entertainment":
                user["data"][budget]["Entertainment"] += int(amount)
            if transaction_type == "Food":
                user["data"][budget]["Food"] += int(amount)
            if transaction_type == "Loans":
                user["data"][budget]["Loans"] += int(amount)
            if transaction_type == "Other":
                user["data"][budget]["Other"] += int(amount)

            if user["data"][budget]["remaining_budget"] < 0:
                user["data"][budget]["remaining_budget"] = 0
            db.users.update_one({"_id":user["_id"]}, {"$set":{"data":user["data"]}})
            self.start_session(user)

        return jsonify({"success": user}), 200
