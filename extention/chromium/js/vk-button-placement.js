function updateUi() {
    console.log("Run script under vk page feed...");

    function check_for_button() {
        // Returns a list of places where there is no butn...

        let all_view_btns = document.querySelectorAll(".like_cont.PostBottomActionLikeBtns");
        let empty_view_btns = [];

        for (let box of all_view_btns) {
            if (box.querySelector(".guard-icon") == null) {
                empty_view_btns.push(box);
            }
        }
           
        return empty_view_btns;
    }

    function send_text(evt) {
        // Grab the post field
        // Verify if it is filled
        // Send text if there is something in there.
        console.log("Trying to send some text...");
        let targeted_el = evt.target;
        let data_location = targeted_el.getAttribute("data-location");
        let post_box = document.createElement("p");
        console.log(evt.target)

        if (data_location == "post_field") {
            post_box = document.querySelector("#" + data_location);

        } else if (data_location == "regular_post") {
            let post_id = targeted_el.getAttribute("data-reaction-target-object");
            let triggered_post = document.querySelector("._like_" + post_id);
            post_box = triggered_post.parentElement.querySelector(".wall_post_text");

        }
        
        console.log(post_box)

        if (post_box) {
            if (post_box.innerHTML){
                console.log("There is some text!\n");
                let text = "Uploading text: " + post_box.innerHTML + " to the server..."
                alert(text);
                let body_data = {
                    'text': post_box.innerHTML
                }
                fetch('https://195.22.153.237:9000/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: body_data
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Success: ', data)
                })
                console.log("Request sent...")
            } else {
                alert("There is no text to send!")
            }
            
        } else {
            alert("There is no text to send!")
        }

    }

    function place_guard_button() {
        let post_actions_wrap = document.getElementById("page_add_media");
        let view_btns = check_for_button();
        
        // box with actions at the profile page
        // Inject guard button
        // Add click event to it to send user text
        if (post_actions_wrap && (post_actions_wrap.querySelector(".guard-icon") == null)) {
            let actual_location = post_actions_wrap.children[0];
            let action_copy = actual_location.children[0].cloneNode(true);

            action_copy.children[0].innerHTML = `
            <svg aria-hidden="true" focusable="false" data-prefix="fas" data-icon="shield-alt" 
            role="img" xmlns="http://www.w3.org/2000/svg" 
            viewBox="0 0 512 512" class="guard-icon">
                <path fill="currentColor"
                d="M466.5 83.7l-192-80a48.15 48.15 0 0 0-36.9 0l-192 80C27.7 91.1 16 108.6 16 128c0 198.5 114.5 335.7 221.5 380.3 11.8 4.9 25.1 4.9 36.9 0C360.1 472.6 496 349.3 496 128c0-19.4-11.7-36.9-29.5-44.3zM256.1 446.3l-.1-381 175.9 73.3c-3.3 151.4-82.1 261.1-175.8 307.7z">
                </path>
            </svg>
            `
            actual_location.insertBefore(action_copy, actual_location.children[0]);
    
            // proper names to the attributes.
            action_copy.setAttribute("data-title", "guard");
            action_copy.setAttribute("aria-lable", "guard");
    
            // set event on <span> because outer tag has no width.
            // data-location will be dependent on the page the user is at.
            action_copy.children[0].addEventListener("click", send_text);
            action_copy.children[0].setAttribute("data-location", "post_field")
            action_copy.children[0].id = "guard-action";
            // Disable events on path
            action_copy.children[0].children[0].style.pointerEvents = "none"
        }
        if (view_btns) {
            for (let views of view_btns) {
                // Выбрать бокс с активностью
                // уровнем ниже сделать див, без кучи данных/событий (поменять событие клика, убрать событие для лайка)
                let like_btns_wrap = views.children[0];
                let action_copy = like_btns_wrap.children[0].cloneNode(true);
                let svg_container = action_copy.querySelector(".PostButtonReactions__icon");

                svg_container.innerHTML = `
                <svg aria-hidden="true" focusable="false" data-prefix="fas" data-icon="shield-alt" 
                role="img" xmlns="http://www.w3.org/2000/svg" 
                viewBox="0 0 512 512" class="guard-icon">
                    <path fill="currentColor"
                    d="M466.5 83.7l-192-80a48.15 48.15 0 0 0-36.9 0l-192 80C27.7 91.1 16 108.6 16 128c0 198.5 114.5 335.7 221.5 380.3 11.8 4.9 25.1 4.9 36.9 0C360.1 472.6 496 349.3 496 128c0-19.4-11.7-36.9-29.5-44.3zM256.1 446.3l-.1-381 175.9 73.3c-3.3 151.4-82.1 261.1-175.8 307.7z">
                    </path>
                </svg>
                `
                svg_container.style.pointerEvents = "none";
                // меняем onClick, onkeydown, onmouseenter элемента под action_copy
                action_copy.children[0].removeAttribute("onclick");
                action_copy.children[0].removeAttribute("onkeydown");
                action_copy.children[0].removeAttribute("onmouseenter");
                // double copy, to remove reactions event.
                let copy2 = action_copy.cloneNode(true);

                // remove counter 
                console.log(copy2)
                copy2.querySelector(".PostBottomAction__count--withBg").innerHTML = ""
                copy2.children[0].setAttribute("data-location", "regular_post");
                copy2.addEventListener("click", send_text);

                
                
                like_btns_wrap.insertBefore(copy2, like_btns_wrap.children[0]);

            }
        }
        
    }

    

    place_guard_button();  
}

updateUi();
setInterval(updateUi, 500);


