import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import ChatWindow from './components/ChatWindow'
import NavBar from './components/NavBar'
import './App.css'
import { Chat } from 'openai/resources/index.mjs'

function App() {
  return (
    <>
      <NavBar></NavBar>
      <ChatWindow></ChatWindow>
    </>
  )
}

export default App
