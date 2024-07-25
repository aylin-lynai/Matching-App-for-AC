# Matching-App-for-AC :tada:

Matching-App measures users' real-time reactions of happiness to funny memes and identifies potential matches based on shared humor. The web application detects users' emotions, specifically happiness, from their facial expressions using a webcam feed. It then assigns happiness scores for each meme per user. Based on these scores, it matches users with similar humor profiles. The app also offers user registration, login, emotion analysis, and user matching functionalities.

## Features :star2:

- User Registration and Login :closed_lock_with_key:
- Emotion Detection (Happiness) using Webcam :blush:
- Happiness Score Calculation :smile:
- User Matching based on Happiness Scores :heart:

## Setup and Installation :hammer_and_wrench:

### Prerequisites :clipboard:

- Python 3.x :snake:
- Virtual Environment (`venv`) :hammer_and_wrench:

### Installation Steps :rocket:

1. **Clone the repository:**

    ```sh
    git clone <repository_url>
    cd Matching-App-for-AC
    ```

2. **Create a virtual environment:**

    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    - **On Windows:**

        ```sh
        venv\Scripts\activate
        ```

    - **On macOS/Linux:**

        ```sh
        source venv/bin/activate
        ```

4. **Install the required dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

5. **Setup the database:**

    ```sh
    python models.py
    ```

6. **Clear the database tables (if needed):**

    ```sh
    python clear_tables.py
    ```

7. **Run the application:**

    ```sh
    flask run
    ```

8. **Usage:**

    Navigate to [http://localhost:5000/](http://localhost:5000/) in your browser :globe_with_meridians:

## Project Structure :open_file_folder:

- **app.py**: Main application file that initializes the Flask app and defines routes. :file_folder:
- **clear_tables.py**: Script to clear and recreate database tables. :wastebasket:
- **happiness_detector.py**: Contains the logic for analyzing images to detect emotions. :blush:
- **models.py**: Database models and configuration. :card_file_box:
- **haarcascade_frontalface_default.xml**: Haar cascade file for face detection. :eye:
- **requirements.txt**: List of dependencies required for the project. :scroll:

## Important Notes :memo:

- The application uses the webcam to capture images for emotion analysis. Ensure your webcam is properly configured and accessible by the browser. :camera:
- The database used is SQLite, configured in `models.py`. :card_file_box:

## Dependencies :package:

Refer to the `requirements.txt` file for a complete list of dependencies. Key libraries include:

- Flask :leaves:
- Flask-SQLAlchemy :card_file_box:
- DeepFace :blush:
- OpenCV :eye:
- NumPy :1234:
