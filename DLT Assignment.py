from flask import Flask, jsonify
import requests
import re

app = Flask(__name__)
    
def latest_stories_div(content):
    # Find the index of the opening tag of the div with data-module-name="latest stories"
    start_tag_index = content.find('<div class="partial latest-stories" data-module_name="Latest Stories">')

    if start_tag_index != -1:
        # Initialize a counter to keep track of nested divs
        div_counter = 1

        # Iterate through the content starting from the opening tag
        for i in range(start_tag_index + len('<div class="partial latest-stories" data-module_name="Latest Stories">'), len(content)):
            if content[i:i + len('<div')] == '<div':
                div_counter += 1
            elif content[i:i + len('</div>')] == '</div>':
                div_counter -= 1

            # Check if we've found the closing tag corresponding to the "latest stories" div
            if div_counter == 0:
                end_tag_index = i + len('</div>')
                content_inside_div = content[start_tag_index:end_tag_index]
                return content_inside_div

def get_time_stories():
    url = "https://time.com"
    response = requests.get(url)
    content = response.text
    
    latest_stories_div_content = latest_stories_div(content)
    print(latest_stories_div_content)

    # Use regex to extract titles and links from the extracted content
    if latest_stories_div_content:
        stories = []
        
        # Find all occurrences of the pattern for 'a' tags and corresponding 'h3' tags
        matches = re.finditer(r'<a href="([^"]+)">\s*<h3 class="latest-stories__item-headline">([^<]+)<\/h3>\s*<\/a>', content)
        
        for match in matches:
            link = match.group(1)
            title = match.group(2).strip()
            stories.append({"title": title, "link": url + link})

        return stories
    else:
        return []

@app.route('/getTimeStories', methods=['GET'])
def get_time_stories_api():
    latest_stories_info = get_time_stories()
    
    if latest_stories_info:
        return jsonify(latest_stories_info)
    else:
        return jsonify({"error": "Latest stories info not found"}), 404

if __name__ == '__main__':
    app.run(host='localhost', port=5000)



