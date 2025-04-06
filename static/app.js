let waitingForCredentials = false;
let storedMessage = "";

function createClickableLink(message) {
    return message.replace(
        /(https?:\/\/[^\s]+)/g,
        '<a href="$1" target="_blank" style="color: blue; text-decoration: underline;">$1</a>'
    );
}

document.getElementById('chat-input').addEventListener('keypress', function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById('send-button').click();
    }
});

function startSpeechToText() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        console.log("Speech recognition is not supported in this browser.");
        return;
    }

    let recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';

    recognition.onresult = function (event) {
        let result = event.results[0][0].transcript;
        document.getElementById('chat-input').value = result;
        document.getElementById('send-button').click();
    };

    recognition.start();
}

function sendMessage(message) {
    let requestBody = { message: message };

    if (waitingForCredentials) {
        const credentials = message.split(" ");
        if (credentials.length < 2) {
            appendBotMessage("Please provide both username and password in this format: `username password`");
            return;
        }

        requestBody.username = credentials[0];
        requestBody.password = credentials[1];
        requestBody.message = storedMessage;
        waitingForCredentials = false;
    }

    fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody)
    })
    .then(response => response.json())
    .then(data => {
        appendUserMessage(message);

        if (data.ask_credentials) {
            waitingForCredentials = true;
            storedMessage = message;
            appendBotMessage(data.answer);
            return;
        }

        let formattedText = data.answer ? `<strong>${data.answer}</strong><br>` : "";

        if (data.student_info) {
            formattedText += `<strong>👤 Student Details:</strong><br>`;
            formattedText += `Name: ${data.student_info.Name}<br>`;
            formattedText += `Roll No: ${data.student_info["Roll No"]}<br>`;
            formattedText += `Reg No: ${data.student_info["UNi Reg No"]}<br>`;
            formattedText += `Total Attendance: ${data.student_info.Total}<br>`;
            formattedText += `Overall Percentage: ${data.student_info.Percentage}<br><br>`;
        }

        if (data.subjects) {
            formattedText += "<strong>📊 Subject-wise Attendance:</strong><br>";
            data.subjects.forEach(subj => {
                formattedText += `${subj.Subject}: ${subj.Attendance}<br>`;
            });
        }

        if (data.assignments) {
            formattedText += "<strong>📌 Assignments:</strong><br>";
            data.assignments.forEach(assign => {
                formattedText += `Subject: ${assign.Subject}<br>`;
                formattedText += `Semester: ${assign.Semester}<br>`;
                formattedText += `Title: ${assign.Title}<br>`;
                formattedText += `Issued On: ${assign["Issued On"]}<br>`;
                formattedText += `Last Date: ${assign["Last Date"]}<br>`;
                formattedText += `Status: ${assign.Status}<br><br>`;
            });
        }

        if (data.sessional_exams) {
            formattedText += "<strong>📝 Session Exam Details:</strong><br>";
            data.sessional_exams.forEach(session => {
                formattedText += `Subject: ${session.Subject}<br>`;
                formattedText += `Exam: ${session.Exam}<br>`;
                formattedText += `Maximum Marks: ${session["Maximum Marks"]}<br>`;
                formattedText += `Marks Obtained: ${session["Marks Obtained"]}<br><br>`;
            });
        }

        if (data.module_tests) {
            formattedText += "<strong>📖 Module Test Details:</strong><br>";
            data.module_tests.forEach(test => {
                formattedText += `Subject: ${test.Subject}<br>`;
                formattedText += `Exam: ${test.Exam}<br>`;
                formattedText += `Max Marks: ${test["Maximum Marks"]}<br>`;
                formattedText += `Obtained: ${test["Marks Obtained"]}<br><br>`;
            });
        }

        if (data.internal_marks) {
            formattedText += "<strong>📊 Internal Marks:</strong><br>";
            data.internal_marks.forEach(mark => {
                formattedText += `Subject: ${mark.Subject}<br>`;
                formattedText += `Maximum Marks: ${mark["Maximum Marks"]}<br>`;
                formattedText += `Marks Obtained: ${mark["Marks Obtained"]}<br><br>`;
            });
        }

        if (!data.answer) {
            formattedText = "I'm sorry, I couldn't generate a response.";
        }

        appendBotMessage(formattedText);
    })
    .catch(error => console.error('Error:', error));
}

function appendUserMessage(message) {
    let chatMessages = document.getElementById('chatbox-messages');
    let userMessage = document.createElement('div');
    userMessage.className = 'message user-message';
    userMessage.innerHTML = 'You: ' + message;
    chatMessages.appendChild(userMessage);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function appendBotMessage(message) {
    let chatMessages = document.getElementById('chatbox-messages');
    let botMessage = document.createElement('div');
    botMessage.className = 'message bot-message';
    botMessage.innerHTML = createClickableLink(message);
    chatMessages.appendChild(botMessage);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

document.getElementById('send-button').addEventListener('click', function () {
    let message = document.getElementById('chat-input').value.trim();
    if (message !== '') {
        sendMessage(message);
        document.getElementById('chat-input').value = '';
    }
});

document.getElementById('speech-button').addEventListener('click', startSpeechToText);

document.addEventListener("DOMContentLoaded", function () {
    const chatbox = document.getElementById("chatbox");
    const chatboxToggle = document.getElementById("chatbox-toggle");
    const minimizeButton = document.getElementById("minimize-button");
    const maximizeButton = document.getElementById("maximize-button");
    const closeButton = document.getElementById("close-button");

    minimizeButton.addEventListener("click", () => {
        chatbox.classList.toggle("fullscreen", false);
        chatbox.classList.toggle("minimized");
    });

    maximizeButton.addEventListener("click", () => {
        chatbox.classList.add("fullscreen");
        chatbox.classList.remove("minimized");
    });

    closeButton.addEventListener("click", () => {
        chatbox.classList.remove("show", "fullscreen", "minimized");
        chatboxToggle.style.display = "block";
    });

    chatboxToggle.addEventListener("click", () => {
        chatbox.classList.add("show");
        chatboxToggle.style.display = "none";
    });
});
