from flask import Flask, request, jsonify, render_template
import uuid

app = Flask(__name__)

# Dictionary to store URL mappings and metadata
url_mapping = {}
url_metadata = {}


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# API to create a short URL
@app.route('/shorten', methods=['POST'])
def create_short_url():
    long_url = request.json.get('long_url')
    short_url = str(uuid.uuid4())[:6]  # Generate a short URL
    url_mapping[short_url] = long_url
    url_metadata[short_url] = {'hits': 0}  # Initialize hits to 0 for new short URL
    return jsonify({'short_url': short_url})


# API endpoint for search
@app.route('/search', methods=['GET'])
def search_urls():
    term = request.args.get('term')
    results = []
    for short_url, long_url in url_mapping.items():
        if term.lower() in long_url.lower():
            results.append({'title': term, 'url': long_url})
    return jsonify(results)


# API to get metadata of a short URL
@app.route('/metadata/<short_url>', methods=['GET'])
def get_metadata(short_url):
    if short_url in url_metadata:
        return jsonify(url_metadata[short_url])
    else:
        return jsonify({'error': 'Short URL not found'}), 404


# API to redirect short URL to original URL
@app.route('/<short_url>', methods=['GET'])
def redirect_to_original_url(short_url):
    if short_url in url_mapping:
        url_metadata[short_url]['hits'] += 1  # Increment hits for the short URL
        return jsonify({'redirecting to': url_mapping[short_url]})
    else:
        return jsonify({'error': 'Short URL not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)


