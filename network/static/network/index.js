document.addEventListener('DOMContentLoaded', function() {

    window.addEventListener('resize', checkMobile);

    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))

    const followed = document.querySelector('#followed-button');

    const follow = document.querySelectorAll('#follow.dropdown-menu');
    const edit = document.querySelectorAll('#edit');
    const back = document.querySelector('#back-button');

    const blocks = document.querySelectorAll('#post');
    likeResponse(blocks);
    checkMobile();

    const modal = document.querySelector("#myModal");
    const settings = document.querySelector(".settings");
    const close = document.querySelector(".close");
    const closeArrow = document.querySelector(".close-arrow");
    const save = document.querySelector(".save");
    const pfp = document.querySelector(".old-pfp");

    if (settings) {
        const name = document.querySelector("#name");
        const profileName = document.querySelectorAll("#profile-name");
        const bio = document.querySelector("#bio");
        const profileBio = document.querySelector("#profile-bio");
        const location = document.querySelector("#location");
        const profileLocation = document.querySelector("#profile-location");
        const website = document.querySelector("#website");
        const profileWebsite = document.querySelector("#profile-website");
        const profileWebsiteText = document.querySelector(".lightblue");
        const file = document.querySelector("#file");

        fetch(`/profiles/${save.dataset.userName}`)
          .then(response => response.json())
          .then(profileData => {
            name.value = profileData[0].name;
            bio.value = profileData[0].bio;
            location.value = profileData[0].location;
            website.value = profileData[0].website;
        })

        settings.onclick = () => {
            modal.style.display = "block";
        }
        close.onclick = () => {
            modal.style.display = "none";
        }
        closeArrow.onclick = () => {
            modal.style.display = "none";
        }
        window.onclick = (event) => {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }

        file.addEventListener('change', function() {
            const refreshIcons = document.querySelectorAll('.reicn');
            loadFile(file, refreshIcons);
        })

        save.onclick = () => {
            updateUserInfo(save.dataset.userName);
            modal.style.display = "none";
            fetch(`/profiles/${save.dataset.userName}`)
              .then(response => response.json())
              .then(profileData => {
                profileName.forEach(element => {
                    element.innerHTML = profileData[0].name;
                });
                profileBio.innerHTML = profileData[0].bio;
                profileLocation.innerHTML = profileData[0].location;
                profileWebsite.href = "//".concat(profileData[0].website);
                let website = profileData[0].website;
                if (website.includes("https://")) {
                    website = website.slice(8);
                } else if (website.includes("http://")) {
                    website = website.slice(7);
                }
                profileWebsiteText.innerHTML = website;
            })
            const file = document.querySelector('#file');
            const icons = document.querySelectorAll('.icn');
            loadFile(file, icons);
        }
    }


    if (followed) {
        followed.addEventListener('mouseover', showUnfollow);
        followed.addEventListener('mouseout', hideUnfollow);
    };

    if (back) {
        let ref = document.referrer

        back.addEventListener('click', function() {
            if (ref && ref != window.location) {
                window.location = document.referrer;
            } else {
                history.back();
            }

        })
    }

    if (follow) {
        follow.forEach(item => {
            fetch(`/follow/${item.dataset.profile}`)
             .then(response => response.json())
             .then(follow => {
                let followItem = item.querySelector("#follow-item");
                let unfollowItem = item.querySelector("#unfollow-item");
                let followButton = document.querySelector("#follow-button");
                let followedButton = document.querySelector("#followed-button");
                if (follow.follows) {
                    if (followButton && followedButton) {
                        followButton.style.display = "none";
                        followedButton.style.display = "block";
                    }
                    followItem.style.display = "none";
                    unfollowItem.style.display = "flex";
                } else {
                    if (followButton && followedButton) {
                        followButton.style.display = "block";
                        followedButton.style.display = "none";
                    }
                    unfollowItem.style.display = "none";
                    followItem.style.display = "flex";
                }
             })
            item.addEventListener('click', function() {
                fetch(`/follow/${item.dataset.profile}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        user: item.dataset.user,
                        followed: item.dataset.profile
                    })
                })
                window.location.href = window.location.href;
            })
        })
    };

    if (edit) {
        edit.forEach(item => {
            item.addEventListener('click', function() {
                let itemDiv = this.parentElement.parentElement.parentElement.parentElement;
                let bodyDiv = itemDiv.querySelector("#text");
                let currentText = bodyDiv.innerHTML;
                let modal = document.querySelector("#myEditModal");
                let close = modal.querySelector(".close");
                let arrow = modal.querySelector(".close-arrow");
                let editor = document.querySelector("#post-editor");
                let update = document.querySelector("#update-post");
                modal.style.display = "block";
                editor.innerHTML = currentText;

                close.onclick = () => {
                    modal.style.display = "none";
                }
                arrow.onclick = () => {
                    modal.style.display = "none";
                }
                window.onclick = (event) => {
                    if (event.target == modal) {
                        modal.style.display = "none";
                    }
                }

                update.onclick = () => {
                    console.log(itemDiv.dataset.number);
                    fetch(`/edit/${itemDiv.dataset.number}`, {
                        method: 'PUT',
                        body: JSON.stringify({
                            new_body: editor.innerHTML
                        })
                    })
                    modal.style.display = "none";
                    bodyDiv.innerHTML = editor.innerHTML;
                }


            })
        })
    };

});

function loadFile(file, elements) {
    const pfp = file.files[0];
    if (pfp) {
        const reader = new FileReader();
        reader.addEventListener('load', function() {
            changeSrc(elements, reader.result);
        })
        reader.readAsDataURL(pfp);
    }
}
function changeSrc(elements, newImage) {
    elements.forEach(element => {
        element.setAttribute('src', newImage);
    })
}

function updateUserInfo(username) {
    let name = document.querySelector("#name");
    let bio = document.querySelector("#bio");
    let location = document.querySelector("#location");
    let website = document.querySelector("#website").value;
    if (website.includes("https://")) {
        website = website.slice(8);
    } else if (website.includes("http://")) {
        website = website.slice(7);
    }
    console.log(website);

    fetch(`/profiles/${username}`, {
        method: 'PUT',
        body: JSON.stringify({
            name: name.value,
            bio: bio.value,
            location: location.value,
            website: website
        })
    })
}

function checkMobile() {
    let links = document.querySelectorAll('.link');
    let blocks = document.querySelectorAll("#block");

    if (screen.width <= 900) {
        if (links) {
            links.forEach(link => {
                link.style.display = 'none';
            })
        }
        if (blocks) {
            blocks.forEach(block => {
                block.classList.remove("hover");
            })
        }
        if (screen.width <= 650) {
            document.querySelector('.close').style.display = "none";
            document.querySelector('.close-arrow').style.display = "block";
        }
        else {
            document.querySelector('.close').style.display = "block";
            document.querySelector('.close-arrow').style.display = "none";
        }
    } else {
        if (links) {
            links.forEach(link => {
                link.style.display = 'inline';
            })
        }
        if (blocks) {
            blocks.forEach(block => {
                block.classList.add("hover");
            })
        }
    }
}

function showUnfollow() {
    const followed = document.querySelector('#followed-button');

    followed.innerHTML = 'Unfollow';
    followed.style.color = 'red';
    followed.style.background = '#F4212E1A';
    followed.style.borderColor = '#FDC9CE';
}

function hideUnfollow() {
    const followed = document.querySelector('#followed-button');

    followed.innerHTML = 'Following';
    followed.style.color = 'black';
    followed.style.background = 'white';
    followed.style.borderColor = '#BEBEBE ';
}

function likeResponse(blocks) {
    blocks.forEach(block => {
        let postIdNum = block.dataset.number;
        let currentUser = block.dataset.user;
        let currentUserEmail = block.dataset.userEmail;

        let likeButton = block.querySelector('#like-button');
        let likedButton = block.querySelector('#liked-button');
        let likeCount = block.querySelector('#like-count');

        fetch(`/posts/${postIdNum}`)
        .then(response => response.json())
        .then(posts => {
            posts.forEach(post => {

                let likedByUser;
                let currentLikeCount = post.likes_count;
                let currentLikeUsers = post.like_users;

                if (post.like_users.includes(currentUserEmail)) {
                    likeButton.style.display = 'none';
                    likedButton.style.display = 'block';
                    likedByUser = true;
                } else {
                    likeButton.style.display = 'block';
                    likedButton.style.display = 'none';
                    likedByUser = false;
                }

                likeButton.addEventListener('click', function() {

                    fetch(`/posts/${postIdNum}`, {
                        method: 'PUT',
                        body: JSON.stringify({
                            user_liked: false
                        })
                      })
                    likeButton.style.display = 'none';
                    likedButton.style.display = 'block';

                    currentLikeCount = currentLikeCount + 1;
                    likeCount.innerHTML = currentLikeCount;

                })

                likedButton.addEventListener('click', function() {

                    fetch(`/posts/${postIdNum}`, {
                        method: 'PUT',
                        body: JSON.stringify({
                            user_liked: true
                        })
                      })

                    likeButton.style.display = 'block';
                    likedButton.style.display = 'none';

                    currentLikeCount = currentLikeCount - 1;
                    likeCount.innerHTML = currentLikeCount;

                })

            })

        });

    })
}

