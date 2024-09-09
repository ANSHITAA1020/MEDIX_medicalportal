function togglePopup() {
    const popupSection = document.getElementById('popup-section');
    popupSection.classList.toggle('active'); // Toggle the active class

    // Optionally, you can also blur the main content when the popup is active
    const mainContent = document.getElementById('main-content');
    if (popupSection.classList.contains('active')) {
        mainContent.style.filter = 'blur(5px)'; // Apply blur effect
    } else {
        mainContent.style.filter = 'none'; // Remove blur effect
    }
}
           // ABOUT ME SECTION POPUP 
           document.addEventListener('DOMContentLoaded', function() {
            const aboutBtn = document.getElementById('aboutUsBtn');
            const aboutPopup = document.getElementById('aboutPopup');
            const closeBtn = document.querySelector('.close');
    
            // Function to open the popup
            function openPopup() {
                aboutPopup.style.display = 'block';
            }
    
            // Function to close the popup
            function closePopup() {
                aboutPopup.style.display = 'none';
            }
    
            // Open the popup when "About Us" is clicked
            aboutBtn.addEventListener('click', function(event) {
                event.preventDefault(); // Prevent default link behavior
                openPopup();
            });
    
            // Close the popup when the close button is clicked
            closeBtn.addEventListener('click', function() {
                closePopup();
            });
    
            // Close the popup if the user clicks outside the popup content
            window.addEventListener('click', function(event) {
                if (event.target == aboutPopup) {
                    closePopup();
                }
            });
        });
       //dropdown menu for DEPARTMENTS
        document.addEventListener('DOMContentLoaded', function () {
            var dropdownToggle = document.querySelector('.dropdown-toggle');
            var dropdownMenu = document.querySelector('.dropdown-menu');
        
            dropdownToggle.addEventListener('click', function (event) {
                event.preventDefault(); // Prevent the default action of the anchor
                dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
            });
        
            // Optional: Close the dropdown when clicking outside of it
            window.addEventListener('click', function (event) {
                if (!dropdownToggle.contains(event.target) && !dropdownMenu.contains(event.target)) {
                    dropdownMenu.style.display = 'none';
                }
            });
        });
// user profile dropdown
function toggleDropdown() {
    document.getElementById("dropdownMenu").classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
    if (!event.target.matches('.user-button')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

// Add CSS for the show class
const style = document.createElement('style');
style.innerHTML = `
    .dropdown-content.show {
        display: block;
    }
`;
document.head.appendChild(style);
  

//meds video in popup
function goToChatbot() {
    // Get the video element
    var video = document.getElementById('popupVideo');
    
    // Pause the video when the button is pressed
    video.pause();

    // Optionally, navigate to a different page or perform other actions here
    // window.location.href = "your-chatbot-url.html";
}

function goToChatbot() {
    document.getElementById('popup').style.display = 'none'; // Hide the popup
    document.getElementById('main-content').style.filter = 'none'; // Remove blur effect
    }

    function updateTime() {
    const now = new Date();
    let hours = now.getHours();
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const ampm = hours >= 12 ? 'PM' : 'AM';
    
    // Convert to 12-hour format
    hours = hours % 12;
    hours = hours ? hours : 12; // Convert hour '0' to '12'
    
    const timeString = `${hours}:${minutes} ${ampm}`;
    document.getElementById('current-time').textContent = timeString;
}

// Update time immediately and then every second
updateTime();
setInterval(updateTime, 1000);

// section which is scrollinng in loop
const container = document.querySelector('.scrollable-container');
let isMouseDown = false;

let startX, scrollLeft;
/* Review Section Styling */

