from flask import Flask, render_template, request, session
import requests
import time
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your actual secret key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
# def analyze():
#     url = request.form['url']
#     metrics = measure_performance(url)
#     metrics['url'] = url
    
#     session['metrics'] = metrics  # Store metrics in session

#     return render_template('results.html', metrics=metrics)
def analyze():
    url = request.form['url']
    metrics = measure_performance(url)
    metrics['url'] = url

    # Check if load_time is valid before accessing it
    if metrics.get('load_time') is not None:
        session['metrics'] = metrics  # Store metrics in session
    else:
        metrics['speed_message'] = 'Could not retrieve loading time.'

    return render_template('results.html', metrics=metrics)



# def measure_performance(url):
#     start_time = time.time()
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # Check for HTTP errors
#         load_time = time.time() - start_time  # Measure load time after the request
#         page_size = len(response.content) / 1024  # Size in KB
#         num_requests = len(response.history) + 1  # +1 for the final request
        
#         # Analyze resources for optimization suggestions
#         optimization_suggestions = analyze_resources(response.content)

#         # SEO analysis
#         seo_metrics = analyze_seo(response.content)
        
#         speed_message = "The website is loading fine." if load_time <= 3 else "The website is a bit slow."
        
#         return {
#             'load_time': load_time,
#             'page_size': page_size,
#             'num_requests': num_requests,
#             'speed_message': speed_message,
#             'optimization_suggestions': optimization_suggestions,
#             'seo_metrics': seo_metrics  # Include SEO metrics
#         }
#     except requests.RequestException as e:
#         return {
#             'error': str(e),
#             'load_time': None,
#             'page_size': None,
#             'num_requests': None,
#             'speed_message': 'Could not retrieve metrics.',
#             'optimization_suggestions': [],
#             'seo_metrics': None
#         }

def measure_performance(url):
    start_time = time.time()
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        load_time = time.time() - start_time
        page_size = len(response.content) / 1024
        num_requests = len(response.history) + 1
        
        optimization_suggestions = analyze_resources(response.content)
        seo_metrics = analyze_seo(response.content)

        speed_message = "The website is loading fine." if load_time <= 3 else "The website is a bit slow."

        return {
            'load_time': load_time,
            'page_size': page_size,
            'num_requests': num_requests,
            'speed_message': speed_message,
            'optimization_suggestions': optimization_suggestions,
            'seo_metrics': seo_metrics
        }
    except requests.RequestException as e:
        return {
            'error': str(e),
            'load_time': None,
            'page_size': None,
            'num_requests': None,
            'speed_message': 'Could not retrieve metrics.',
            'optimization_suggestions': [],
            'seo_metrics': None
        }




def analyze_resources(content):
    soup = BeautifulSoup(content, 'html.parser')
    images = [img['src'] for img in soup.find_all('img', src=True)]
    
    suggestions = []
    
    # Check for optimization suggestions
    for img in images:
        # Placeholder for actual optimization check
        if 'large_image' in img:  # You can add conditions to check image size or format
            suggestions.append(f"Consider compressing the image: {img}")
    
    if len(images) > 10:
        suggestions.append("Consider reducing the number of images to optimize loading time.")
    
    return suggestions

def analyze_seo(content):
    soup = BeautifulSoup(content, 'html.parser')

    title = soup.title.string if soup.title else "No title found"
    title_length = len(title) if title != "No title found" else 0

    meta_description = ''
    for meta in soup.find_all('meta'):
        if 'name' in meta.attrs and meta['name'].lower() == 'description':
            meta_description = meta['content']
            break
    meta_description_length = len(meta_description)

    keywords = []
    for meta in soup.find_all('meta'):
        if 'name' in meta.attrs and meta['name'].lower() == 'keywords':
            keywords = meta['content'].split(',')
            break  # Exit after finding the first keywords meta tag

    return {
        'title': title,
        'meta_description': meta_description,
        'keywords': keywords,
        'title_length': title_length,
        'meta_description_length': meta_description_length
    }

if __name__ == '__main__':
    app.run(debug=True)
