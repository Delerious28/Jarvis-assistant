import os
import uuid
import requests
from datetime import datetime, timedelta

def process_news_request(text, json_key_file, text_to_speech):
    if any(keyword in text for keyword in ["news about", "latest news", "news on"]):
        query = text.replace("news about", "").replace("latest news", "").replace("news on", "").strip()
        news_response = get_news(query, json_key_file, text_to_speech)

        if news_response.get("filenames"):
            response_text = "Here are the latest news articles."
            output_filenames = news_response["filenames"]
            for idx, filename in enumerate(output_filenames):
                news_text = f"News article {idx + 1}."
                print(f"Converting article {idx + 1} to speech: {filename}")
                text_to_speech(news_text, json_key_file, filename)
            return {"text": response_text, "filenames": output_filenames}
        else:
            return {"text": "Sorry, I couldn't find any news on that topic."}
    return {"text": "No relevant keywords found in the input."}

def get_news(query, json_key_file, text_to_speech):
    try:
        api_key = '#newsdata_api_key#'
        url = f'https://newsdata.io/api/1/news?apikey={api_key}&q={query}&language=en'

        response = requests.get(url)
        if response.status_code == 200:
            news_data = response.json()
            
            if 'choices' in news_data:
                return {"text": "Received OpenAI response instead of news articles. Please refine your query."}

            articles = news_data.get('results', [])
            if not articles:
                return {"text": f"No news articles found for '{query}'."}

            articles.sort(key=lambda x: x.get('published_at', ''), reverse=True)

            directory = "speech_files"
            os.makedirs(directory, exist_ok=True)

            output_filenames = []

            current_year = datetime.now().year
            articles_processed = 0

            current_date = datetime.now()
            time_range = timedelta(days=3) 

            for idx, article in enumerate(articles):
                article_date = article.get('published_at', '').split('T')[0] if article.get('published_at') else None
                if article_date:
                    published_date = datetime.fromisoformat(article_date)
                    if current_date - published_date <= time_range:
                        title = article.get('title', 'No title')
                        description = article.get('description', 'No description')
                        news_text = f"Title: {title}\nDescription: {description}"

                        if news_text.strip():
                            output_filename = os.path.join(directory, f"news_output_{uuid.uuid4().hex}_{articles_processed}.mp3")
                            result = text_to_speech(news_text, json_key_file, output_filename)

                            if result:
                                output_filenames.append(output_filename)
                                articles_processed += 1
                                if articles_processed >= 3:  
                                    break
                            else:
                                print(f"Failed to generate speech for article {idx}")

            if output_filenames:
                return {"text": "News retrieved successfully.", "filenames": output_filenames}
            else:
                return {"text": f"No valid news articles found for '{query}' in the recent period."}

        else:
            return {"text": f"Failed to fetch news with status code: {response.status_code}"}

    except Exception as e:
        return {"text": f"Error fetching news: {str(e)}"}
