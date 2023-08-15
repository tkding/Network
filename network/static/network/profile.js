document.addEventListener('DOMContentLoaded', function() {
    const profileTitle = document.getElementById("profileTitle");
    const followersCount = document.getElementById("followersCount");
    const followingCount = document.getElementById("followingCount");
    const followButton = document.getElementById("followButton");
    const unfollowButton = document.getElementById("unfollowButton");
    const postsList = document.getElementById("postsList");

    const profileUserIdInput = document.getElementById("profileUserId");
    const user_id = profileUserIdInput.value;
    console.log('DOMContentLoaded event fired');

    
    // check if user is following this profile
    // only check is current user is not the user of this profile

    // Check if the profile is not the current user's profile
    const isCurrentUserProfile = profileTitle.getAttribute("data-is-current-user") === "True";
    console.log(`isCurrentUserProfile: ${isCurrentUserProfile}`);

    // check if user is logged in
    const isLoggedIn = profileTitle.getAttribute("data-is-logged-in") === "True";

    if(isLoggedIn){
        if(!isCurrentUserProfile){
            console.log('Current user is not the profile user');
            console.log('Before fetch profile');
            fetch(`/check_follow/${user_id}`)
                .then((response) => response.json())
                .then((data) => {
                    console.log('Fetch check_follow successful', data.is_following);
                    if(data.is_following){
                        displayFollowButton(true);
                    } else {
                        displayFollowButton(false);
                    }
                })
                .catch((error) => {
                    console.error("Error:", error);
                });

            console.log('After fetch check_follow');
        }
        else{
            console.log('Current user is the profile user');    
        }
    }
    else{
        console.log('User is not logged in');
    }
    
    if (followButton) {
        console.log('Follow button found');
        followButton.addEventListener("click", () => {
            console.log('Follow button clicked');
            toggleFollow(true);
        });
    }

    if (unfollowButton) {
        console.log('Unfollow button found');
        unfollowButton.addEventListener("click", () => {
            console.log('Unfollow button clicked');
            toggleFollow(false);
        });
    }
    

    // function to display only either follow or unfollow button
    function displayFollowButton(following) {
        if (following) {
            followButton.style.display = "none";
            unfollowButton.style.display = "block";
        } else {
            followButton.style.display = "block";
            unfollowButton.style.display = "none";
        }
    }

    // Function to toggle follow/unfollow
    function toggleFollow(follow) {
        console.log(`toggleFollow ${follow} user: ${user_id}`);

        fetch(`/toggle_follow/${user_id}`, {
            method: "PUT",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ follow }), // update the follow status
        })
        .then((response) => response.json()) // convert to json
        .then((data) => {
            displayFollowButton(follow);
            // update the followers count
            followersCount.innerHTML = `Followers: ${data.followers_count}`;
        })
        .catch((error) => {
            console.error("Error:", error);
        });
    }

    // function to get CSRF token from cookie
    function getCookie(name){
        let cookieValue = null;
        if(document.cookie && document.cookie !== ''){
            const cookies = document.cookie.split(';');
            for(let i = 0; i < cookies.length; i++){
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if(cookie.substring(0, name.length + 1) === (name + '=')){
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});





