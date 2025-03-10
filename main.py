from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# Store cooldown timestamps (could use a database for persistence)
cooldowns = {}

# Define the default cooldown period (in seconds)
DEFAULT_COOLDOWN_PERIOD = 60  # 1 minute

# Supersecretkey for verification
SUPER_SECRET_KEY = "yourSuperSecretKey123"  # Change this to your desired secret key

@app.route('/use-item', methods=['GET'])
def use_item():
    # Get the supersecretkey from query parameters
    supersecretkey = request.args.get('supersecretkey')

    # Check if the supersecretkey is correct
    if supersecretkey != SUPER_SECRET_KEY:
        return jsonify({'error': 'Invalid supersecretkey'}), 403  # Forbidden if key is incorrect

    user_id = request.args.get('userId')
    cooldown_period = request.args.get('cooldown', DEFAULT_COOLDOWN_PERIOD, type=int)

    if not user_id:
        return jsonify({'error': 'userId is required'}), 400

    # Ensure the cooldown period is a positive integer
    if cooldown_period <= 0:
        return jsonify({'error': 'Cooldown period must be a positive integer'}), 400

    current_time = int(time.time())  # Get current time in Unix format (seconds)

    # Check if the user is on cooldown
    if user_id in cooldowns and current_time < cooldowns[user_id]:
        remaining_time = cooldowns[user_id] - current_time
        return jsonify({'error': f'Cooldown active. Try again in {remaining_time} seconds.'}), 429

    # Set new cooldown timestamp
    cooldowns[user_id] = current_time + cooldown_period

    return jsonify({'message': f'Action successful! Cooldown set for {cooldown_period} seconds.'})

if __name__ == '__main__':
    app.run(debug=True)
  
