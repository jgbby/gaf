var backend_url = "http://localhost:8000"

export const getOverview = async (sessionId, query) => {
  try {
    const response = await fetch(backend_url + "/overview", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ session_id: sessionId, message: query }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    let assistant_response = data.response;
    console.log("assistant_response", assistant_response);
    return {
      role: "assistant",
      content: data.response
    }
  } catch (error) {
    console.error("Error posting chat message:", error);
    return "Sorry, there was an error processing your request.";
  }
}

export const postChatMessage = async (sessionId, query) => {
  try {
    const response = await fetch(backend_url + "/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ session_id: sessionId, message: query }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    let assistant_response = data.response;
    console.log("assistant_response", assistant_response);
    return {
      role: "assistant",
      content: data.response
    }
  } catch (error) {
    console.error("Error posting chat message:", error);
    return "Sorry, there was an error processing your request.";
  }
};
