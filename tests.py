import unittest
from flask import Flask, jsonify, current_app
from bson import ObjectId
from pymongo import MongoClient
from app.routes import routes

class TodoAppTestCase(unittest.TestCase):

    def setUp(self):
        """Set up the Flask test client."""
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True

        # MongoDB URI and client setup
        username = "kyadavalli04"
        password = "Kousthubh%40mongodb"
        mongo_uri = f"mongodb+srv://{username}:{password}@cluster0.2o0bzi6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

        # Initialize MongoDB client and database
        client = MongoClient(mongo_uri)
        self.app.db = client['testdb']  # Store db in app context

        # Register routes blueprint
        self.app.register_blueprint(routes)

        # Set up the Flask test client
        self.client = self.app.test_client()

        # Ensure we have an app context for the test cases
        self.app.app_context().push()

        self.todo_id = None  # Placeholder for todo ID after adding a todo

    def test_todo_operations(self):
        """Test the full sequence of add, display, update, and delete todo."""
        
        # Step 1: Add Todo
        data = {'title': 'Test Todo 1', 'description': 'Test Description 1'}
        response = self.client.post('/add', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('title', response.json)
        self.assertEqual(response.json['title'], 'Test Todo 1')
        
        self.todo_id = response.json['_id']  # Save the ID for further testing
        print(f"Added Todo: {response.json['title']}")

        # Step 2: Display All Todos
        response = self.client.get('/display')
        self.assertEqual(response.status_code, 200)
        
        if len(response.json) == 0:
            print("No tasks remaining. All tasks are completed.")
        else:
            print("Remaining tasks:")
            for todo in response.json:
                print(f"Title: {todo['title']}, Description: {todo['description']}")

        # Step 3: Update Todo
        update_data = {'title': 'Updated Todo Title'}
        response = self.client.put(f'/edit/{self.todo_id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)
        self.assertEqual(response.json['message'], 'Todo updated successfully')

        print(f"Updated Todo Title: {update_data['title']}")

        # Step 4: Delete Todo
        response = self.client.delete(f'/delete/{self.todo_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)
        self.assertEqual(response.json['message'], 'Todo deleted successfully')

        print("Deleted Todo successfully.")

        print("All tests passed successfully.")

if __name__ == '__main__':
    unittest.main()
