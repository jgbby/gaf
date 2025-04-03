import React, { useState, useEffect, useRef } from "react";
import "./NavBar.css";

function NavBar() {
    const [isDarkMode, setIsDarkMode] = useState(false);
    
    const toggleDarkMode = () => {
        setIsDarkMode(!isDarkMode);
    };
    
    useEffect(() => {
        document.body.classList.toggle("dark-mode", isDarkMode);
    }, [isDarkMode]);
    
    return (
        <nav className={`navbar ${isDarkMode ? "dark" : ""}`}>
            <div className="navbar-content">
                <h1>GAF Chatbot</h1>
                <button onClick={toggleDarkMode}>
                {isDarkMode ? "Light Mode" : "Dark Mode"}
                </button>
            </div>
            <img id="instalily-logo" src="./assets/instalily_logo.png"></img>
        </nav>
    );
}
export default NavBar;