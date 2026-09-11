const API_URL = "/ask";


async function askQuestion() {

    const input = document.getElementById("questionInput");
    const chatBox = document.getElementById("chatBox");

    const question = input.value.trim();

    if (!question) {
        return;
    }

    // Show user question
    chatBox.innerHTML += `
        <div class="message user">
            <div class="message-content">
                <strong>You</strong>
                <p>${question}</p>
            </div>
        </div>
    `;

    input.value = "";

    // Loading message
    const loadingId = "loading-" + Date.now();

    chatBox.innerHTML += `
        <div class="message bot" id="${loadingId}">
            <div class="message-content">
                <strong>Rulebook Assistant</strong>
                <p>Searching the rulebook...</p>
            </div>
        </div>
    `;

    chatBox.scrollTop = chatBox.scrollHeight;

    try {

        const response = await fetch(API_URL, {

            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },

            body: JSON.stringify({
                question: question
            })
        });

        if (!response.ok) {
            throw new Error("API request failed");
        }

        const data = await response.json();

        document.getElementById(loadingId).remove();

        displayAnswer(data);

    } catch (error) {

        document.getElementById(loadingId).remove();

        chatBox.innerHTML += `
            <div class="message bot">
                <div class="message-content">
                    <strong>Error</strong>
                    <p>
                        Could not connect to the Rulebook API.
                        Please make sure the FastAPI server is running.
                    </p>
                </div>
            </div>
        `;
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}


function displayAnswer(data) {

    const chatBox = document.getElementById("chatBox");

    let citationsHTML = "";

    if (data.citations && data.citations.length > 0) {

        data.citations.forEach((citation, index) => {

            citationsHTML += `
                <div class="citation">

                    <strong>Citation ${index + 1}</strong>

                    <p>
                        <b>Source:</b>
                        ${citation.source}
                    </p>

                    <p>
                        <b>Section:</b>
                        ${citation.section}
                    </p>

                    <p>
                        <b>Similarity Score:</b>
                        ${citation.similarity_score}
                    </p>

                    <div class="passage">
                        <b>Passage:</b>
                        <br>
                        ${citation.passage}
                    </div>

                </div>
            `;
        });
    }

    chatBox.innerHTML += `
        <div class="message bot">

            <div class="message-content">

                <strong>Rulebook Assistant</strong>

                <div>
                    <span class="status ${data.status}">
                        ${data.status.toUpperCase()}
                    </span>
                </div>

                <p>
                    ${data.answer}
                </p>

                ${citationsHTML}

            </div>

        </div>
    `;
}


// Press Enter to ask question
document
    .getElementById("questionInput")
    .addEventListener("keydown", function(event) {

        if (event.key === "Enter") {
            askQuestion();
        }

    });