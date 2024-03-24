from datetime import timezone, datetime
from flask import Blueprint, jsonify, request
import src.utils.config as config
from src.utils.database.update_data import update_links_data
from src.utils.token_required import token_required

update_links = Blueprint('update_links', __name__)

@update_links.route('/update_links', methods=['POST'])
@token_required
def update_links_view():
    json_data = request.get_json()
    for review_links in json_data:
        created = int(datetime.now(timezone.utc).timestamp() * 1000)
        review_links['created'] = created
        if 'mail' not in review_links:
            return jsonify({"code": "error", "message": "Missing 'mail' in data"})
        update_links_data(config.conn,review_links)
    return jsonify({"code": "200", "message": "Data has been modified successfully"})