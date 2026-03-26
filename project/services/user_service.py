import json


with open('data/users.json', 'r') as f:
    users_data = json.load(f)



class UserService:
    def __init__(self):
        self.users = users_data

    
    def get_all_users(self):
        return self.users
    
    
    def get_user_by_id(self, user_id):
        return next((u for u in self.users if u['id'] == user_id), None)
    

    def get_next_id(self):
        if not self.users:
            return 1
        return max( u['id'] for u in self.users) + 1
    
    
    def create_new_record(self, users):
        with open('data/users.json', 'w') as f:
            json.dump(users, f, indent=4)


    def add_user(self, user_data):
        new_id = self.get_next_id()
        user_data['id'] = new_id
        self.users.append(user_data)
        self.create_new_record(self.users)
        return user_data
    

    def delete_user(self, user_id):
        user = self.get_user_by_id(user_id)
        if user:
            self.users.remove(user)
            self.create_new_record(self.users)
            return True
        return False
    

    def update_user(self, user_id, user_data):
        user = self.get_user_by_id(user_id)
        if user:
            user.update(user_data)
            self.create_new_record(self.users)
            return user
        return None

