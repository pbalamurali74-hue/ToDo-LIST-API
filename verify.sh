#!/bin/bash

# Port
PORT=8000
URL="http://localhost:$PORT"

echo "=== STARTING Python REST API MANUAL VERIFICATION ==="
echo "Make sure the server is running on $URL (e.g. via 'python3 -m uvicorn app.main:app --reload')"
echo ""

# Generate a unique email suffix to allow running multiple times
EMAIL_SUFFIX=$RANDOM
EMAIL="manual_${EMAIL_SUFFIX}@test.com"

# 1. Register User
echo "1. Registering user with email: $EMAIL..."
REG_RESP=$(curl -s -X POST "$URL/register" \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"Manual User\", \"email\": \"$EMAIL\", \"password\": \"password123\"}")

echo "Registration Response: $REG_RESP"
TOKEN=$(echo "$REG_RESP" | grep -o '"token":"[^"]*' | grep -o '[^"]*$')
REFRESH_TOKEN=$(echo "$REG_RESP" | grep -o '"refreshToken":"[^"]*' | grep -o '[^"]*$')

if [ -z "$TOKEN" ]; then
  echo "❌ Registration failed. Token not found."
  exit 1
fi
echo "✅ Registration successful."
echo ""

# 2. Login User
echo "2. Logging in..."
LOGIN_RESP=$(curl -s -X POST "$URL/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\", \"password\": \"password123\"}")

echo "Login Response: $LOGIN_RESP"
TOKEN=$(echo "$LOGIN_RESP" | grep -o '"token":"[^"]*' | grep -o '[^"]*' | grep -o '[^"]*$')
if [ -z "$TOKEN" ]; then
  echo "❌ Login failed."
  exit 1
fi
echo "✅ Login successful."
echo ""

# 3. Create Todo
echo "3. Creating a new to-do item..."
TODO_RESP=$(curl -s -X POST "$URL/todos/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Verify Python API manually", "description": "Ensure endpoints function properly using curl"}')

echo "Create Todo Response: $TODO_RESP"
TODO_ID=$(echo "$TODO_RESP" | grep -o '"id":"[^"]*' | grep -o '[^"]*$')
if [ -z "$TODO_ID" ]; then
  echo "❌ Todo creation failed."
  exit 1
fi
echo "✅ Todo created with ID: $TODO_ID"
echo ""

# 4. Update Todo
echo "4. Updating the created to-do item..."
UPDATE_RESP=$(curl -s -X PUT "$URL/todos/$TODO_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Verify Python API manually (Updated)", "completed": true}')

echo "Update Todo Response: $UPDATE_RESP"
echo "✅ Todo updated successfully."
echo ""

# 5. List Todos (with pagination, filtering, search)
echo "5. Fetching to-do items..."
LIST_RESP=$(curl -s "$URL/todos/?page=1&limit=5&completed=true&search=Verify" \
  -H "Authorization: Bearer $TOKEN")

echo "List Response: $LIST_RESP"
echo "✅ List retrieved successfully."
echo ""

# 6. Delete Todo
echo "6. Deleting to-do item..."
DELETE_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE "$URL/todos/$TODO_ID" \
  -H "Authorization: Bearer $TOKEN")

if [ "$DELETE_STATUS" -ne 204 ]; then
  echo "❌ Todo deletion failed (Status: $DELETE_STATUS)."
  exit 1
fi
echo "✅ Todo deleted successfully (Status: 204)."
echo ""

# 7. Logout
echo "7. Logging out..."
curl -s -X POST "$URL/logout" \
  -H "Content-Type: application/json" \
  -d "{\"refreshToken\": \"$REFRESH_TOKEN\"}"

echo "✅ Logged out successfully."
echo ""
echo "=== VERIFICATION COMPLETED SUCCESSFULLY ==="
