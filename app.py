from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/convert', methods=['GET'])
def convert_gregorian_to_hebrew():
    date = request.args.get('date')
    if not date:
        return jsonify({'error': 'Date not provided.'}), 400
    
    try:
        if len(date.split('-')) != 3 or not all(part.isdigit() for part in date.split('-')):
            raise ValueError('Invalid date format. Expected format: YYYY-MM-DD.')

        hebcal_url = f'https://www.hebcal.com/converter?cfg=json&date={date}&g2h=1&strict=1'
        response = requests.get(hebcal_url)
        response.raise_for_status()
        return jsonify(response.json())

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

if __name__ == '__main__':
    app.run(debug=True)
