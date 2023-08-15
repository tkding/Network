# Social Network Project

## Project Overview

[![Watch the video demonstration](https://img.youtube.com/vi/2Dq8OK5moZU/maxresdefault.jpg)](https://youtu.be/2Dq8OK5moZU)

This project involves building a social network web application using Django, Python, JavaScript, HTML, and CSS. The application allows users to create accounts, make posts, follow other users, and interact with posts by liking them. The project aims to implement the core functionality of a social media platform.

## Features

1. **User Authentication and Profiles:** Users can register, log in, and update their profiles. The user model contains fields for username, email, password, and additional user-specific information.

2. **New Post:** Authenticated users can create new text-based posts by entering content in a text area and clicking a "Post" button.

3. **All Posts:** The "All Posts" page displays posts from all users, sorted by most recent. Each post shows the username of the poster, content, timestamp, and the number of likes.

4. **Profile Pages:** Users can click on a username to view their profile page. The profile displays follower and following counts, along with the user's posts in reverse chronological order. Other users can follow/unfollow the profile user.

5. **Following Page:** The "Following" page displays posts from users that the current user follows. Pagination allows users to navigate through posts.

6. **Pagination:** Posts are paginated, displaying 10 posts per page. "Next" and "Previous" buttons facilitate navigation between pages.

7. **Edit Post:** Users can edit their own posts using an "Edit" button. The content is replaced with a textarea for editing, and changes can be saved without reloading the entire page.

8. **Like and Unlike:** Users can like and unlike posts by clicking a button. JavaScript asynchronously updates the like count and post appearance without a full page refresh.

## Getting Started

1. Clone the repository:
   ```
   git clone https://github.com/your-username/social-network.git
   cd social-network
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up the database:
   ```
   python manage.py migrate
   ```

4. Create a superuser account:
   ```
   python manage.py createsuperuser
   ```

5. Run the development server:
   ```
   python manage.py runserver
   ```

6. Access the application in your browser at `http://localhost:8000`.

